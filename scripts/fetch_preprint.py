"""Resolve a preprint URL to a local PDF plus whatever metadata the source offers.

Supported sources, in order of how much metadata we get back:

    arXiv       — full metadata via the arXiv Atom API
    bioRxiv     — full metadata via api.biorxiv.org
    medRxiv     — full metadata via api.biorxiv.org
    direct PDF  — no metadata; title is inferred downstream from the manuscript

Stdlib only. No API keys.
"""

from __future__ import annotations

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
RXIV_RE = re.compile(
    r"(?:(?P<server>biorxiv|medrxiv)\.org/content/)?(?P<doi>10\.1101/[^\s/?#]+?)(?:v(?P<version>\d+))?(?:\.full)?(?:\.pdf)?$",
    re.I,
)


@dataclass
class Preprint:
    """What we managed to learn about a submission before reviewing it."""

    url: str
    source: str  # arxiv | biorxiv | medrxiv | direct
    pdf_url: str
    identifier: str = ""
    doi: str = ""
    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    published: str = ""
    version: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:  # noqa: S310
        return resp.read()


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
    bare = arxiv_id.split("v")[0] if re.match(r"^\d{4}\.", arxiv_id) else arxiv_id
    pp = Preprint(
        url=url,
        source="arxiv",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
        identifier=arxiv_id,
    )
    try:
        api = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(bare)}"
        entry = ET.fromstring(_get(api)).find("a:entry", _ATOM)
        if entry is None:
            return pp
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


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# --- bioRxiv / medRxiv ------------------------------------------------------


def _resolve_rxiv(url: str, doi: str, server: str, version: str) -> Preprint:
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
        payload = json.loads(_get(f"https://api.biorxiv.org/details/{server}/{doi}"))
        records = payload.get("collection") or []
        if not records:
            return pp
        rec = records[-1]  # newest version
        pp.title = _clean(rec.get("title", ""))
        pp.abstract = _clean(rec.get("abstract", ""))
        pp.published = rec.get("date", "")
        pp.version = rec.get("version", version)
        authors = rec.get("authors", "")
        pp.authors = [a.strip() for a in authors.split(";") if a.strip()]
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

    m = ARXIV_RE.search(url)
    if m:
        return _resolve_arxiv(url, m.group("id"))

    m = RXIV_RE.search(url)
    if m and m.group("doi"):
        server = (m.group("server") or "biorxiv").lower()
        return _resolve_rxiv(url, m.group("doi"), server, m.group("version") or "")

    if url.lower().endswith(".pdf"):
        return Preprint(url=url, source="direct", pdf_url=url)

    raise ValueError(
        f"unrecognized preprint URL: {url!r}\n"
        "Supported: arxiv.org/abs/..., biorxiv.org/content/10.1101/..., "
        "medrxiv.org/content/10.1101/..., or a direct link to a .pdf"
    )


def download(preprint: Preprint, dest_dir: Path) -> Path:
    """Fetch the PDF. Raises if the response clearly is not one."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", preprint.identifier or "preprint").strip("-")
    dest = dest_dir / f"{stem or 'preprint'}.pdf"

    data = _get(preprint.pdf_url)
    if not data.startswith(b"%PDF"):
        raise ValueError(
            f"{preprint.pdf_url} did not return a PDF "
            f"(got {len(data)} bytes starting {data[:16]!r}). "
            "Scanned or paywalled sources are not supported."
        )
    dest.write_bytes(data)
    return dest


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
