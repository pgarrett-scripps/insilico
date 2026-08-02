"""Resolve a preprint URL to a local PDF plus whatever metadata the source offers.

Supported sources:

    arXiv       — full metadata via the arXiv Atom API
    bioRxiv     — full metadata via api.biorxiv.org
    medRxiv     — full metadata via api.biorxiv.org

Direct PDF links are rejected — see :func:`resolve` for why. Stdlib only, no
API keys.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path

USER_AGENT = "InSilico-overlay-journal/0.1 (+https://github.com/pgarrett-scripps)"
TIMEOUT = 60

# A URL sitting on its own in an issue-form field.
URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")

ARXIV_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf|html)/(?P<id>\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)",
    re.I,
)
# Both the content path and a bare DOI form.
#
# Two DOI prefixes are in play: bioRxiv/medRxiv used 10.1101 historically and
# switched to 10.64898 — every preprint posted recently carries the new one, so
# matching only 10.1101 rejects current submissions outright. Kept as an
# explicit alternation rather than a loose `10\.\d+` so a random DOI from some
# other registrar isn't silently treated as a preprint.
RXIV_PREFIXES = ("10.1101", "10.64898")

# The suffix is matched by its actual shape rather than as "everything up to
# the end of the string". Both servers mint one of exactly two forms:
#
#     2020.03.24.20042937    dated, used since 2019
#     001834                 legacy, a bare serial
#
# Spelling that out is what lets the pattern stop at the DOI and ignore
# whatever the browser appended. The previous version instead used a lazy
# `[^\s/?#]+?` anchored to the end of the string, which had to reach the end
# to match at all — so a trailing slash from a copy-pasted address bar was
# rejected as an unrecognised URL, and a real bioRxiv link ending `.full-text`
# was *accepted* with the junk swallowed into the DOI. That second failure is
# the dangerous one: it silently produced the identifier
# `10.1101/2020.03.24.20042937v1.full-text`, which then became the API query,
# the PDF URL (`…v1.full-textv1.full.pdf`) and the published directory name.
RXIV_SUFFIX = r"(?:\d{4}\.\d{2}\.\d{2}\.\d+|\d{6,})"
RXIV_RE = re.compile(
    r"(?:(?P<server>biorxiv|medrxiv)\.org/content/)?"
    r"(?P<doi>(?:" + "|".join(re.escape(p) for p in RXIV_PREFIXES) + r")/"
    + RXIV_SUFFIX + r")"
    r"(?:v(?P<version>\d+))?",
    re.I,
)


@dataclass
class Preprint:
    """What we managed to learn about a submission before reviewing it."""

    url: str
    source: str  # arxiv | biorxiv | medrxiv
    pdf_url: str
    identifier: str = ""
    doi: str = ""
    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    published: str = ""
    version: str = ""
    # Fingerprint of the exact bytes reviewed, filled in by download(). A
    # review is only meaningful against a specific revision of a manuscript,
    # and "we reviewed arxiv.org/abs/1706.03762" does not name one — authors
    # replace preprints in place. Recording both lets a later check say which
    # published reviews are now stale. See scripts/check_updates.py.
    pdf_sha256: str = ""
    pdf_bytes: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


# Nothing we legitimately fetch comes close to this. An unbounded read is a
# memory bomb: a runner has a couple of GB, and `resp.read()` will happily
# take whatever the far end sends, whether or not it is the PDF it claims.
MAX_DOWNLOAD_BYTES = 60 * 1024 * 1024


def _get(
    url: str,
    max_bytes: int = MAX_DOWNLOAD_BYTES,
    opener: urllib.request.OpenerDirector | None = None,
) -> bytes:
    """Fetch a URL, refusing anything implausibly large.

    Read in chunks with a running total rather than trusting Content-Length,
    which the server chooses and can simply lie about or omit.

    ``opener`` lets a caller impose extra policy on the fetch. It exists for
    one case: an author-supplied URL, where every redirect hop has to be
    re-checked rather than trusted. Preprint fetches leave it unset, since
    those URLs are rebuilt by :func:`resolve` for three known hosts.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    open_url = opener.open if opener is not None else urllib.request.urlopen
    with open_url(req, timeout=TIMEOUT) as resp:  # noqa: S310
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(
                    f"{url} is larger than {max_bytes // (1024 * 1024)} MB and "
                    "was not downloaded. Preprints are not this big; if this is "
                    "a real manuscript, submit it as a normal preprint posting."
                )
            chunks.append(chunk)
        return b"".join(chunks)


def extract_authorship(text: str) -> str:
    """Whether the submitter said they are an author: 'yes' | 'no' | ''.

    Issue forms render as ``### Heading\n\nvalue``, so the answer is the first
    non-empty line under its heading. Returns '' when the field is absent —
    submissions predating it, or a `/review` run from a plain issue — and the
    published page then says the relationship is unrecorded rather than
    guessing at one.
    """
    lines = (text or "").splitlines()
    for i, line in enumerate(lines):
        if "are you an author" not in line.lower():
            continue
        for value in lines[i + 1:]:
            value = value.strip()
            if not value or value.startswith("#"):
                continue
            low = value.lower()
            if low.startswith("yes"):
                return "yes"
            if low.startswith("no"):
                return "no"
            break
    return ""


def extract_url(text: str) -> str:
    """Pull the first plausible preprint URL out of free text (e.g. an issue body).

    Issue forms render as ``### Heading\n\nvalue``, so a bare scan for the first
    URL is both sufficient and robust to field reordering. Markdown link syntax
    and trailing punctuation are stripped.
    """
    for raw in URL_RE.findall(text or ""):
        candidate = raw.rstrip(".,;:)")
        if candidate.lower().startswith(("http://", "https://")):
            return candidate
    raise ValueError("no URL found in the submission text")


# --- arXiv ------------------------------------------------------------------

_ATOM = {"a": "http://www.w3.org/2005/Atom"}


def _resolve_arxiv(url: str, arxiv_id: str) -> Preprint:
    """Resolve to the *latest* version, whatever the submitted URL pinned.

    A review has to name the version it read, and a submitter linking
    `abs/1706.03762v1` from an old email should not silently get v1 reviewed
    when v3 is what exists. Both preprint sources therefore behave the same
    way: resolve to current, and record which version that was.

    That also makes revisions work. Without a version on the record, nothing
    can tell that a manuscript has moved on — the update check has nothing to
    compare and a revision round would re-review the draft it already read.
    """
    bare = arxiv_id.split("v")[0] if re.match(r"^\d{4}\.", arxiv_id) else arxiv_id
    pp = Preprint(
        url=url,
        source="arxiv",
        pdf_url=f"https://arxiv.org/pdf/{bare}",
        identifier=bare,
    )
    try:
        api = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(bare)}"
        entry = ET.fromstring(_get(api)).find("a:entry", _ATOM)
        if entry is None:
            return pp
        # The entry id carries the current version: .../abs/1706.03762v5
        entry_id = _text(entry, "a:id")
        m = re.search(r"/abs/(?P<id>[^/\s]+?)v(?P<version>\d+)\s*$", entry_id)
        if m:
            pp.version = m.group("version")
            pp.pdf_url = f"https://arxiv.org/pdf/{m.group('id')}v{pp.version}"
        pp.title = _clean(_text(entry, "a:title"))
        pp.abstract = _clean(_text(entry, "a:summary"))
        pp.published = _text(entry, "a:published")[:10]
        pp.authors = [
            _clean(n.text or "")
            for n in entry.findall("a:author/a:name", _ATOM)
            if (n.text or "").strip()
        ]
        doi = entry.find("a:doi", _ATOM)
        pp.doi = (doi.text or "").strip() if doi is not None else f"10.48550/arXiv.{bare}"
    except (urllib.error.URLError, ET.ParseError, TimeoutError):
        pass  # metadata is a nicety; the PDF is what matters
    return pp


def _text(node: ET.Element, path: str) -> str:
    found = node.find(path, _ATOM)
    return (found.text or "") if found is not None else ""


# Anything that looks like an HTML tag. Preprint metadata is written by the
# authors, and it reaches many places — <title>, meta tags, headings, cards.
# A manuscript posted as `Cool paper <script>…</script>` would otherwise be
# one forgotten escape away from stored XSS on every reader's browser.
#
# Stripped at ingestion rather than escaped at each render: there are many
# render sites and only one ingestion point, and an escape that has to be
# remembered in ten places is one that will be forgotten in the eleventh.
# Renderers still escape as well — this is the belt, not the braces.
_TAGLIKE = re.compile(r"<[^>]*>")


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", _TAGLIKE.sub("", s)).strip()


# --- bioRxiv / medRxiv ------------------------------------------------------


def _rxiv_records(server: str, doi: str) -> list[dict]:
    """Metadata records for a DOI on one server, newest last. [] if unknown."""
    payload = json.loads(_get(f"https://api.biorxiv.org/details/{server}/{doi}"))
    records = payload.get("collection") or []
    return records if isinstance(records, list) else []


def _resolve_rxiv(
    url: str, doi: str, server: str, version: str, certain: bool = True
) -> Preprint:
    """Resolve a bioRxiv/medRxiv DOI, confirming which server actually has it.

    ``certain`` is False when the submitted link was a bare DOI, which names
    no server — the two share both DOI prefixes, so there is nothing in the
    string to tell them apart. Guessing bioRxiv and moving on would publish a
    medRxiv preprint labelled ``source: biorxiv`` and point every link and the
    PDF fetch at a bioRxiv URL that does not exist. Asking each server which
    one holds it is one request and removes the guess.
    """
    suffix = f"v{version}" if version else ""
    pp = Preprint(
        url=url,
        source=server,
        pdf_url=f"https://www.{server}.org/content/{doi}{suffix or 'v1'}.full.pdf",
        identifier=doi,
        doi=doi,
        version=version,
    )
    try:
        records = _rxiv_records(server, doi)
        if not records and not certain:
            # The prefix is shared, so an empty answer here means "not this
            # one", not "not a preprint". Try the other before giving up.
            other = "medrxiv" if server == "biorxiv" else "biorxiv"
            records = _rxiv_records(other, doi)
            if records:
                server = other
                pp.source = other
                pp.url = f"https://www.{other}.org/content/{doi}{suffix}"
        if not records:
            return pp
        rec = records[-1]  # newest version
        pp.title = _clean(rec.get("title", ""))
        pp.abstract = _clean(rec.get("abstract", ""))
        pp.published = rec.get("date", "")
        pp.version = rec.get("version", version)
        authors = rec.get("authors", "")
        pp.authors = [_clean(a) for a in authors.split(";") if a.strip()]
        pp.pdf_url = (
            f"https://www.{server}.org/content/{doi}v{pp.version or 1}.full.pdf"
        )
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        pass
    return pp


# --- entry points -----------------------------------------------------------


def resolve(url: str) -> Preprint:
    """Classify a URL and gather metadata. Does not download the PDF."""
    url = url.strip()

    # The stored URL is rebuilt from what matched, never echoed back from the
    # input. These patterns are *searched* rather than anchored, so a string
    # like `javascript:alert(1)#arxiv.org/abs/1706.03762` matches on the tail
    # — and keeping the raw input would publish it as a clickable link on the
    # review page. Canonicalising also means one preprint has one URL however
    # it was linked.
    m = ARXIV_RE.search(url)
    if m:
        return _resolve_arxiv(f"https://arxiv.org/abs/{m.group('id')}", m.group("id"))

    m = RXIV_RE.search(url)
    if m and m.group("doi"):
        # A bare DOI names no server, and the two share both prefixes — so
        # this is a starting guess to be confirmed, not an answer.
        named = m.group("server")
        server = (named or "biorxiv").lower()
        doi = m.group("doi")
        version = m.group("version") or ""
        canonical = f"https://www.{server}.org/content/{doi}"
        if version:
            canonical += f"v{version}"
        return _resolve_rxiv(canonical, doi, server, version, certain=bool(named))

    # Direct PDF links are deliberately not accepted. An overlay journal's
    # whole claim is that it reviews something with a permanent home, and a
    # bare PDF URL has no stable identity: no DOI, no version, no landing
    # page, nothing to tell a reader whether the file they download is the
    # one the panel read. It also rots — a review pointing at a dead link is
    # a review of nothing — carries no metadata, so title and authors have to
    # be guessed out of the PDF text, and turns `/review <url>` into an
    # arbitrary fetch from CI.
    if url.lower().endswith(".pdf"):
        raise ValueError(
            f"{url} is a direct PDF link, which we don't accept.\n"
            "Reviews have to name a specific, permanent revision of a "
            "manuscript, and a bare PDF URL doesn't provide one. Post the "
            "preprint to arXiv, bioRxiv or medRxiv and submit that link — "
            "you'll get a DOI and a version number, and the review will say "
            "exactly which revision it read."
        )

    raise ValueError(
        f"unrecognized preprint URL: {url!r}\n"
        "Supported: arxiv.org/abs/..., biorxiv.org/content/<doi>, "
        "medrxiv.org/content/<doi>. bioRxiv and medRxiv DOIs carry either the "
        "10.1101 or the newer 10.64898 prefix; both work."
    )


def download(preprint: Preprint, dest_dir: Path) -> Path:
    """Fetch the PDF. Raises if the response clearly is not one."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", preprint.identifier or "preprint").strip("-")
    dest = dest_dir / f"{stem or 'preprint'}.pdf"

    try:
        data = _get(preprint.pdf_url)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 404) and preprint.source in ("biorxiv", "medrxiv"):
            # bioRxiv serves a PDF only once a posting is fully indexed; before
            # that it 302s to /node/.full-text.pdf with an empty node id, which
            # then 403s. Days-old preprints hit this. Say so, rather than
            # surfacing a bare HTTPError that reads like a permissions problem.
            raise ValueError(
                f"{preprint.pdf_url} returned HTTP {exc.code}. bioRxiv/medRxiv "
                "don't serve a PDF until a posting is fully indexed, which can "
                "take a few days after it first appears. Try again in a few "
                "days."
            ) from exc
        raise ValueError(
            f"{preprint.pdf_url} returned HTTP {exc.code} ({exc.reason})."
        ) from exc

    if not data.startswith(b"%PDF"):
        raise ValueError(
            f"{preprint.pdf_url} did not return a PDF "
            f"(got {len(data)} bytes starting {data[:16]!r}). "
            "Scanned or paywalled sources are not supported."
        )
    preprint.pdf_sha256 = hashlib.sha256(data).hexdigest()
    preprint.pdf_bytes = len(data)
    dest.write_bytes(data)
    return dest


def fingerprint(preprint: Preprint) -> tuple[str, int]:
    """Hash the current PDF without keeping it. Used to re-check a published review.

    Deliberately separate from :func:`download` so an update check costs one
    request and no disk, and never touches the reviewed copy.
    """
    data = _get(preprint.pdf_url)
    if not data.startswith(b"%PDF"):
        raise ValueError(f"{preprint.pdf_url} no longer returns a PDF")
    return hashlib.sha256(data).hexdigest(), len(data)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="preprint URL, or free text containing one")
    ap.add_argument("--download-to", type=Path, help="also fetch the PDF here")
    args = ap.parse_args()

    pp = resolve(extract_url(args.url) if " " in args.url else args.url)
    if args.download_to:
        print(f"pdf: {download(pp, args.download_to)}")
    print(json.dumps(pp.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
