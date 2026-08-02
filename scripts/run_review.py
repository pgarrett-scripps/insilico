"""Fetch a preprint, run the referee panel over it, and write a review bundle.

    python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
    python scripts/run_review.py --issue-body "$ISSUE_BODY" --submission-id 12

Output lands in ``docs/reviews/<year>/<slug>/`` and is what the bot commits.
``--dry-run`` resolves and downloads without calling a model, so you can check a
URL is reviewable before spending anything.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.parse
from pathlib import Path
from queue import Empty, Queue

sys.path.insert(0, str(Path(__file__).parent))

from fetch_preprint import (  # noqa: E402
    _get,
    Preprint,
    download,
    extract_authorship,
    extract_url,
    resolve,
)

# Written by the pipeline next to the markdown. It is what makes a review
# revisable — the machine-readable record of what this round asked for, with
# stable ids a later round rules on. Published, not internal: without it in
# the bundle there is nothing to point `--revision-of` at.
ROUND_RECORD = "round.json"

# The authors' response, copied into the bundle verbatim. Published rather
# than merely linked: a GitHub comment can be edited after the review answers
# it, and a record that cites mutable text is not a record.
AUTHOR_RESPONSE = "author_response.md"

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"


def _load_dotenv() -> None:
    """Read ./.env so local runs don't need keys exported into the shell.

    Deliberately does not overwrite anything already set, so CI secrets and an
    explicit `ANTHROPIC_API_KEY=... python scripts/run_review.py` both win over
    the file. Hand-rolled rather than pulled from python-dotenv: this script
    runs before the pipeline is necessarily installed, and the format we need
    is a dozen lines of KEY=value.
    """
    env_file = REPO / ".env"
    if not env_file.is_file():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# Links out to GitHub must be absolute — the review pages are rendered by
# MkDocs under docs/, where a relative path can't reach the issue tracker.
REPO_URL = (
    f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/"
    f"{os.environ.get('GITHUB_REPOSITORY', 'pgarrett-scripps/insilico')}"
)

# The published address, which is what a citation has to point at — a repo
# path is not a citable location. Kept in step with `site_url` in mkdocs.yml;
# override with SITE_URL when building a copy that lives somewhere else.
SITE_URL = os.environ.get(
    "SITE_URL", "https://pgarrett-scripps.github.io/insilico"
).rstrip("/")

# Files the pipeline emits, in the order a reader should meet them.
BUNDLE_ORDER = [
    ("summary.md", "Summary"),
    ("decision_letter.md", "Decision letter"),
    # Both are written only when the desk found something. integrity.md is the
    # submission-integrity scan (concealed text / prompt injection); on a
    # desk reject it is the whole story, so it is listed above the panel
    # material rather than buried at the end.
    ("integrity.md", "Submission integrity scan"),
    ("desk_screen.md", "Desk screen"),
    # Revision rounds only. The verification is what the panel was actually
    # allowed to see of the authors' response letter — corroborated pointers,
    # never the letter's own prose — so publishing it is what makes the claim
    # "the letter could not move a score" checkable rather than asserted.
    ("author_response_verification.md", "Author response verification"),
    ("meta_review.md", "Area chair synthesis"),
    ("author_rebuttal.md", "Simulated author rebuttal"),
    ("debate_transcript.md", "Advocate / skeptic debate"),
    ("journal_recommendations.md", "Venue suggestions"),
]

# Model tags map to groups of agents; spell them out for readers who haven't
# read the pipeline's config docs. There is deliberately no "screen" entry:
# the desk screen resolves through the `reviewer` tag so it warms the cache
# the panel reads, so that tag never appears in a resolved config.
_TAG_LABEL = {
    "reviewer": "specialist reviewers (×8) + desk screen",
    "audit": "editorial audits (×2)",
    "debate": "advocate / skeptic",
    "synthesis": "area chair, rebuttal, editor, journal scout",
}

VERDICT_LABEL = {
    "accept": "Accept",
    "minor": "Minor revision",
    "major": "Major revision",
    "reject": "Reject",
}


def slugify(text: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if len(s) <= limit:
        return s
    return s[:limit].rsplit("-", 1)[0] or s[:limit]


def paper_slug(preprint: Preprint, title: str) -> str:
    """A directory name that is readable *and* unique to one preprint.

    Titles alone are neither. slugify truncates at 60 characters, so two
    genuinely different papers can collide:

        "Deep learning approaches for the prediction of protein structure..."
        "Deep learning approaches for the prediction of protein folding..."

    both reduce to `deep-learning-approaches-for-the-prediction-of-protein`,
    and the second review would land on top of the first. Appending the
    preprint's own identifier makes the name unique by construction — and
    since submissions are restricted to arXiv/bioRxiv/medRxiv, there is
    always one.
    """
    title_part = slugify(title, limit=50)
    id_part = slugify(preprint.identifier or preprint.doi or preprint.url, limit=40)
    slug = "-".join(p for p in (title_part, id_part) if p)
    return slug or "submission"


def find_prior_bundle(preprint: Preprint, title: str) -> Path | None:
    """The most recent revisable round already published for this preprint.

    Searched across all year directories, not just this preprint's own year:
    a revised preprint can carry a later posting date than the version we
    reviewed, which would put v2 in a different year folder from v1 and make
    the paper's own history invisible to it.

    Only bundles with a round record count. A review published before round
    records existed cannot be the basis of a revision round, and silently
    treating it as round 1 would produce a round 2 that had nothing to rule on.

    Matched on the preprint's identifier, never on the directory name. The
    slug embeds the title, and authors retitle between versions routinely — so
    a slug lookup would miss its own round 1 for exactly the papers most
    likely to be revised, report "no revisable round", and quietly restart at
    round 1 with the referees' prior points lost.
    """
    del title  # kept for call-site symmetry; the identifier is what matches
    wanted = (preprint.identifier or preprint.doi or "").strip().lower()
    if not wanted:
        return None

    best: tuple[int, Path] | None = None
    for record_path in sorted(REVIEWS.glob(f"*/*/v*/{ROUND_RECORD}")):
        bundle = record_path.parent
        try:
            prov = json.loads(
                (bundle / "provenance.json").read_text(encoding="utf-8")
            )
            record = json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pre = prov.get("preprint") or {}
        found = str(pre.get("identifier") or pre.get("doi") or "").strip().lower()
        if found != wanted:
            continue
        rnd = int(record.get("round", 1))
        if best is None or rnd > best[0]:
            best = (rnd, bundle)
    return best[1] if best else None


def next_version(paper_dir: Path) -> int:
    """The version number this review should be written as.

    Never returns an existing one: re-reviewing a revised manuscript adds
    `v2` beside `v1` rather than replacing it. Overwriting would both lose
    the earlier review and leave its orphaned specialist reports sitting in
    the new bundle, so a reader would see v1 reports presented as part of v2.
    """
    existing = [
        int(p.name[1:])
        for p in paper_dir.glob("v*")
        if p.is_dir() and p.name[1:].isdigit()
    ]
    return max(existing, default=0) + 1


def md_text(value: str) -> str:
    """Neutralise author-supplied text before it enters a markdown page.

    Titles, abstracts and author names arrive from the preprint server, which
    means the *authors* wrote them — and markdown renders inline HTML, so a
    manuscript posted with `<script>` in its abstract becomes stored XSS on
    every reader's browser. That needs no model to be fooled and no editor to
    be careless: it is simply published.

    Escaping the three HTML-significant characters is enough, because the
    output is markdown rather than HTML — `&lt;` renders as a literal `<`, so
    a title that legitimately contains one still reads correctly.
    """
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def md_cell(value: str) -> str:
    """As :func:`md_text`, for a table cell, where a pipe also breaks layout."""
    return md_text(value).replace("|", "\\|")


def yaml_scalar(value: str) -> str:
    """Quote a scalar so a colon or quote in a title can't break the frontmatter."""
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_scalar(v) for v in values) + "]"


def pipeline_version() -> dict[str, str]:
    """Identify exactly which referee panel produced a review."""
    info = {"sha": os.environ.get("PEERREVIEW_PIPELINE_SHA", "")}
    try:
        from importlib.metadata import version

        info["version"] = version("peerreviewagents")
    except Exception:  # noqa: BLE001 - metadata is best-effort
        info["version"] = "unknown"
    return info


def panel_scores(state: dict) -> list[dict]:
    out = []
    for report in state.get("reports", []) or []:
        if not isinstance(report, dict):
            continue
        out.append(
            {
                "reviewer": report.get("reviewer", "unknown"),
                "score": report.get("score"),
                "confidence": report.get("confidence"),
            }
        )
    return out


@contextlib.contextmanager
def _cost_recorder(run_id: str):
    """Aggregate per-agent spend off the pipeline's observability bus.

    The pipeline emits a ``usage`` event per model call carrying the node name
    and a cost, but only ever persists the run total. Registering a queue for
    this run collects the breakdown without touching the pipeline.

    Drained after the graph finishes rather than concurrently: ``Queue`` is
    unbounded, the run is synchronous, and a drain thread would be one more
    thing to get wrong for data that is only read at the end. Never fails the
    review — an accounting problem must not lose a completed panel.
    """
    from peerreviewagents.observability import clear_observer, register_observer

    costs: dict[str, float] = {}
    queue: Queue = Queue()
    register_observer(queue, run_id)
    try:
        yield costs
    finally:
        clear_observer(run_id)
        try:
            while True:
                try:
                    event = queue.get_nowait()
                except Empty:
                    break
                if event.kind != "usage" or not event.cost_usd:
                    continue
                node = event.node or "unattributed"
                costs[node] = round(costs.get(node, 0.0) + event.cost_usd, 6)
        except Exception as exc:  # noqa: BLE001
            print(f"warning: cost breakdown unavailable ({exc})", file=sys.stderr)


def write_bundle(
    preprint: Preprint,
    state: dict,
    run_dir: Path,
    dest: Path,
    submission_id: str,
    submitter: str,
    cost_by_node: dict[str, float] | None = None,
    revision: dict | None = None,
    # Appended rather than inserted: write_bundle is called positionally in
    # several places, and a new parameter in the middle silently rebinds them.
    submitter_is_author: str = "",
) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    cost_by_node = cost_by_node or {}
    revision = revision or {}

    # On a desk reject the pipeline sets decision_letter, desk_screen and
    # integrity to the *same* body, so all three land here byte-identical.
    # Copy them all (a reader following a direct link should find the file)
    # but list each distinct document once, or the landing page shows the
    # same text under three headings.
    copied: list[tuple[str, str]] = []
    seen: dict[str, str] = {}
    for name, label in BUNDLE_ORDER:
        src = run_dir / name
        if not src.exists():
            continue
        shutil.copy2(src, dest / name)
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest in seen:
            continue
        seen[digest] = name
        copied.append((name, label))

    reviewer_files = sorted(run_dir.glob("review_*.md"))
    audit_files = sorted(run_dir.glob("audit_*.md"))
    for src in reviewer_files + audit_files:
        shutil.copy2(src, dest / src.name)

    # Not in BUNDLE_ORDER because it is data, not a document to link from the
    # landing page — but it has to travel with the bundle, since it is the
    # thing a later round is pointed at.
    if (run_dir / ROUND_RECORD).exists():
        shutil.copy2(run_dir / ROUND_RECORD, dest / ROUND_RECORD)

    # Snapshot of the authors' response exactly as submitted. GitHub comments
    # can be edited after the fact, so a published review that merely links to
    # one would end up citing text that no longer says what we answered. The
    # copy is what makes the record hold still.
    statement = revision.get("statement_path")
    if statement and Path(statement).is_file():
        shutil.copy2(statement, dest / AUTHOR_RESPONSE)

    decision = state.get("decision", "unknown")
    title = preprint.title or state.get("manuscript_title") or "Untitled submission"
    scores = panel_scores(state)
    numeric = [s["score"] for s in scores if isinstance(s.get("score"), (int, float))]

    provenance = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "provider": os.environ.get("REVIEW_PROVIDER", "anthropic"),
        "model": os.environ.get("REVIEW_MODEL", ""),
        # Per-role overrides, if any. Without these a reader can't tell which
        # model actually produced which report — "model" is only the fallback.
        # Per-agent model config. Without this a reader sees only the
        # fallback model and can't tell which agent wrote which report.
        "models": json.loads(os.environ.get("REVIEW_MODELS") or "{}"),
        "agent_models": json.loads(os.environ.get("REVIEW_AGENT_MODELS") or "{}"),
        "debate_rounds": int(os.environ.get("REVIEW_DEBATE_ROUNDS", "2")),
        "decision": decision,
        # A desk reject and a panel reject are both `decision: reject` but are
        # not the same editorial act — one is a verdict after ten reports and a
        # debate, the other stops before any of that. Readers and the index
        # both need to tell them apart, and `decision` alone cannot.
        "desk_rejected": bool(state.get("desk_rejected")),
        # The review round, which is NOT the bundle's vN. Re-running a review
        # of the same manuscript under new criteria makes a new bundle at
        # round 1; only a review of a revised draft advances the round. Left
        # separate so the two can never be read off each other.
        "round": int(revision.get("round") or 1),
        "revision": revision,
        # Anyone may submit any public preprint, so a review the authors asked
        # for and one they did not are different things and the page has to
        # say which. Recorded as a claim, because nothing here verifies it.
        "submitter": submitter,
        "submitter_is_author": submitter_is_author,
        "screens": json.loads(os.environ.get("REVIEW_SCREENS") or "{}"),
        "panel": scores,
        "mean_score": round(sum(numeric) / len(numeric), 2) if numeric else None,
        "total_cost_usd": state.get("total_cost"),
        # Per-agent spend, so cost decisions are measured rather than guessed.
        "cost_by_node": dict(sorted(cost_by_node.items())) if cost_by_node else {},
        "errors": state.get("errors", []),
        "preprint": preprint.to_dict(),
    }
    (dest / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")

    (dest / "index.md").write_text(
        render_landing(
            preprint, provenance, title, copied,
            reviewer_files, audit_files, submission_id, submitter,
            site_path(dest),
        )
    )


def restore_prior_draft(prior_bundle: Path, workdir: Path, config: dict) -> dict:
    """Put the previously reviewed PDF back in the ingest cache.

    A revision round diffs the new draft against the old one, but the round
    record deliberately stores no copy of the manuscript — only its ingest
    cache key. That cache lives on whichever machine ran the review, and a
    CI runner is destroyed when the job ends, so on GitHub the previous draft
    is always gone and the round would quietly degrade to a no-diff review.

    We can rebuild it because we recorded exactly which bytes were reviewed:
    the preprint's versioned PDF URL and a SHA-256 of the file. Re-fetch,
    check it still hashes to what we reviewed, and re-parse it — the ingest
    cache is keyed by file content, so parsing the identical file repopulates
    the identical key.

    Returns a status dict recorded in provenance. Never raises: a failed
    restoration costs the diff, not the round, and the caller says so on the
    published page rather than presenting a no-diff round as a real one.
    """
    status = {"restored": False, "reason": "", "verified": False}
    try:
        prov = json.loads((prior_bundle / "provenance.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        status["reason"] = f"could not read the previous round's provenance ({exc})"
        return status

    pre = prov.get("preprint") or {}
    url, want_sha = pre.get("pdf_url", ""), pre.get("pdf_sha256", "")
    if not url:
        status["reason"] = "the previous round recorded no PDF URL"
        return status

    try:
        data = _get(url)
    except Exception as exc:  # noqa: BLE001 - any fetch failure is the same outcome
        status["reason"] = f"could not re-fetch the previous draft ({exc})"
        return status

    got_sha = hashlib.sha256(data).hexdigest()
    if want_sha and got_sha != want_sha:
        # The file at that URL is no longer the file we reviewed. Diffing
        # against it would produce a confident delta over the wrong baseline,
        # which is worse than having no diff at all.
        status["reason"] = (
            f"the PDF at {url} no longer matches what round "
            f"{prov.get('round', 1)} reviewed (recorded {want_sha[:12]}…, "
            f"fetched {got_sha[:12]}…), so it is not a safe baseline"
        )
        return status
    status["verified"] = bool(want_sha)

    prior_pdf = workdir / "prior-draft.pdf"
    prior_pdf.write_bytes(data)

    try:
        from peerreviewagents.ingest.cache import cache_key
        from peerreviewagents.ingest.loader import load_manuscript

        key = cache_key(prior_pdf, config)
        recorded = _prior_cache_key(prior_bundle)
        if recorded and key != recorded:
            # Same bytes should give the same key; a mismatch means the key
            # derivation changed upstream, and the graph will look up the old
            # one and miss. Better to say so than to leave it looking fine.
            status["reason"] = (
                "the re-parsed draft does not land on the cache key the "
                "previous round recorded, so the pipeline will not find it"
            )
            return status
        load_manuscript(str(prior_pdf), config)
    except Exception as exc:  # noqa: BLE001
        status["reason"] = f"could not re-parse the previous draft ({exc})"
        return status

    status["restored"] = True
    return status


def _reject_internal_url(source: str) -> None:
    """Refuse a URL that points inside the runner's own network.

    Unlike the preprint path, which only ever builds URLs for three known
    hosts, this fetches whatever an editor pasted. On a CI runner that reaches
    the cloud metadata endpoint and anything else on the local network, so a
    mistyped or malicious link turns the reviewer into a request forwarder.

    Address-based rather than an allowlist: a response letter can legitimately
    live on any number of hosts, and the property that actually matters is
    that it is not somewhere only the runner can see. Every resolved address
    is checked, since a name can return several.
    """
    import ipaddress
    import socket

    parsed = urllib.parse.urlparse(source)
    if parsed.scheme != "https":
        raise SystemExit(
            f"author statement must be an https URL, got {parsed.scheme or 'none'}."
        )
    host = parsed.hostname or ""
    if not host:
        raise SystemExit(f"could not read a hostname from {source}")
    try:
        infos = socket.getaddrinfo(host, parsed.port or 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise SystemExit(f"could not resolve {host}: {exc}") from exc
    for info in infos:
        addr = ipaddress.ip_address(info[4][0])
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
            or addr.is_unspecified
        ):
            raise SystemExit(
                f"{host} resolves to {addr}, which is inside the runner's own "
                "network. Response letters have to be fetchable from the "
                "public internet."
            )


def fetch_statement(source: str, workdir: Path) -> Path:
    """Materialise the authors' response letter as a local file.

    A URL or a path, because a submitter has an issue comment to work with and
    not a filesystem. Nothing is inspected here on purpose: the letter is
    untrusted, interested-party input, and the pipeline screens it at the desk
    on the same gate as the manuscript. Sniffing it first would just be a
    second, worse screen.
    """
    if not source.lower().startswith(("http://", "https://")):
        path = Path(source)
        if not path.is_file():
            raise SystemExit(f"author statement not found: {source}")
        return path
    _reject_internal_url(source)
    # A response letter is prose. The default cap is sized for PDFs of whole
    # manuscripts, which this is not.
    data = _get(source, max_bytes=8 * 1024 * 1024)
    # Extension decides the parser upstream, so keep the one the URL implies
    # and fall back to markdown, which the loader treats as plain text.
    suffix = Path(urllib.parse.urlparse(source).path).suffix.lower()
    if suffix not in (".pdf", ".md", ".txt", ".tex", ".docx"):
        suffix = ".md"
    dest = workdir / f"author-statement{suffix}"
    dest.write_bytes(data)
    return dest


def _prior_cache_key(prior_bundle: Path) -> str:
    """The manuscript cache key the previous round wrote into round.json."""
    try:
        record = json.loads((prior_bundle / ROUND_RECORD).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(record.get("manuscript_cache_key") or "")


def site_path(path: Path) -> str:
    """Where a bundle directory will live on the published site.

    Resolved first so a relative path works: `docs/reviews/2026/x/v1` is not
    relative_to the absolute REVIEWS, and the fallback below would quietly
    drop the year — producing a citation URL that looks right and 404s.
    """
    try:
        return "reviews/" + path.resolve().relative_to(REVIEWS.resolve()).as_posix()
    except ValueError:
        # Rendered off-tree (tests, ad-hoc runs), where there is no year to
        # recover. Keep the trailing components so the shape is still right.
        return "reviews/" + "/".join(path.parts[-2:])


# LaTeX chokes on these unescaped, and generated titles are not sanitised
# anywhere else — a paper with an ampersand or a percent in its title would
# otherwise emit BibTeX that fails to compile.
_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def bibtex_escape(text: str) -> str:
    return "".join(_LATEX_ESCAPES.get(c, c) for c in str(text))


def bibtex_key(slug: str, suffix: str = "") -> str:
    """A citation key that is stable, unique, and legal BibTeX."""
    key = "insilico-" + re.sub(r"[^A-Za-z0-9-]+", "-", slug).strip("-").lower()
    return f"{key}-{suffix}" if suffix else key


def citation_block(
    *,
    title: str,
    url: str,
    year: str,
    key: str,
    reviewed_doi: str = "",
    reviewed_version: str = "",
    note_extra: str = "",
    evergreen: bool = False,
) -> list[str]:
    """A 'Cite this review' section: plain text plus BibTeX.

    Two addresses, mirroring how Zenodo separates a concept DOI from a version
    DOI, so that adding real DOIs later slots into a format already in use:

    - the paper page is *evergreen* — it always shows the latest review
    - each ``vN`` page is *immutable* — it is one review of one revision

    Which to cite depends on the claim being made, so each page says plainly
    which kind it is rather than leaving the reader to guess.

    Authorship is the honest part. The panel is a program, so the author is
    the journal, and the note says machine-generated. Citing an LLM panel as
    though it were a named referee would misrepresent what this is.
    """
    scope = (
        "always resolves to the most recent review of this paper"
        if evergreen
        else "is a permanent link to this specific review, and will not change"
    )
    # One sentence naming what was reviewed, then any extras. Built as a whole
    # rather than joined from fragments — "peer review. of doi:..." is what
    # joining gets you.
    head = "Machine-generated peer review"
    if reviewed_doi:
        head += f" of doi:{reviewed_doi}"
        if reviewed_version:
            head += f" v{reviewed_version}"
    sentences = [head] + ([note_extra] if note_extra else [])
    note = ". ".join(sentences) + "."

    plain = f'In Silico ({year}). Review of "{title}". In Silico. {url}'

    lines = [
        "## Cite this review",
        "",
        f"This URL {scope}.",
        "",
        "```",
        plain,
        "```",
        "",
        '<details class="quote"><summary>BibTeX</summary>',
        "",
        "```bibtex",
        f"@misc{{{key},",
        f"  title        = {{Review of {{{bibtex_escape(title)}}}}},",
        # Braced so BibTeX styles don't lowercase or reorder it as a personal
        # name — "In Silico" is a corporate author, not a person called Silico.
        "  author       = {{In Silico}},",
        f"  year         = {{{year}}},",
        "  howpublished = {In Silico, an AI-refereed overlay journal},",
        # Escaped like any other field. Our slugs are [a-z0-9-] so this is a
        # no-op in practice, but an unescaped underscore in a url field is a
        # LaTeX error outside \url{}, and a citation that won't compile is
        # worse than no citation at all.
        f"  url          = {{{bibtex_escape(url)}}},",
        f"  note         = {{{bibtex_escape(note)}}}",
        "}",
        "```",
        "",
        "</details>",
        "",
        "Please cite the preprint itself as well — this reviews that work, it",
        "does not replace it. The review is machine-generated and advisory; if",
        "you are citing it as evidence about the paper, say so explicitly.",
        "",
    ]
    return lines


def card_description(provenance: dict, review_count: int = 1) -> str:
    """One line for the social card and og:description.

    Written to be read out of context — on a timeline, next to a link, with
    no surrounding page. So it leads with the verdict and always says the
    review is machine-generated: a shared card is exactly where that could
    otherwise be mistaken for a journal acceptance.
    """
    if provenance.get("desk_rejected"):
        head = "Desk rejected before review"
    else:
        head = VERDICT_LABEL.get(
            provenance.get("decision", ""), provenance.get("decision", "reviewed")
        )
        score = provenance.get("mean_score")
        if score is not None:
            head += f" · mean panel score {score}/5"
    tail = "AI referee panel — advisory, not a certification."
    if review_count > 1:
        tail = f"{review_count} reviews on record. {tail}"
    return f"{head}. {tail}"


def write_paper_page(paper_dir: Path) -> None:
    """Rewrite the paper's landing page from whatever review versions exist.

    Regenerated from the directory rather than appended to, so it stays
    correct if a version is added or removed by hand. This page is what the
    index links to and what a citation should point at: it is the stable
    address for "In Silico's review record for this paper", while each
    ``vN/`` is the immutable address for one review.
    """
    versions = sorted(
        (p for p in paper_dir.glob("v*") if p.is_dir() and p.name[1:].isdigit()),
        key=lambda p: int(p.name[1:]),
        reverse=True,
    )
    if not versions:
        return

    records = []
    for vdir in versions:
        try:
            prov = json.loads((vdir / "provenance.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        records.append((vdir.name, prov))
    if not records:
        return

    _, latest = records[0]
    pre = latest.get("preprint", {})
    title = pre.get("title") or "Untitled submission"
    decision = latest.get("decision", "unknown")
    desk = latest.get("desk_rejected")

    fm = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"decision: {yaml_scalar(decision)}",
        f"source: {yaml_scalar(pre.get('source', ''))}",
        f"preprint_url: {yaml_scalar(pre.get('url', ''))}",
        f"doi: {yaml_scalar(pre.get('doi', ''))}",
        f"reviewed: {yaml_scalar(str(latest.get('generated_at', ''))[:10])}",
        f"authors: {yaml_list(pre.get('authors') or [])}",
        f"review_count: {len(records)}",
        # Drives the social-card subtitle and the og:description. Without it
        # every shared review link carries the site's generic tagline, which
        # tells a reader nothing about the paper they were sent.
        f"description: {yaml_scalar(card_description(latest, len(records)))}",
    ]
    if latest.get("mean_score") is not None:
        fm.append(f"mean_score: {latest['mean_score']}")
    if desk:
        fm.append("desk_rejected: true")
    fm.append("---")

    chip = (
        '<span class="ins-verdict ins-verdict--desk">Desk reject</span>'
        if desk
        else f'<span class="ins-verdict ins-verdict--{decision}">'
        f"{VERDICT_LABEL.get(decision, decision)}</span>"
    )

    body = [
        "\n".join(fm),
        "",
        f"# {md_text(title)}",
        "",
        '<div class="ins-decision">',
        f"  {chip}",
        f'  <span class="ins-decision__label">Most recent: {VERDICT_LABEL.get(decision, decision)}</span>',
        f'  <span class="ins-decision__note">{len(records)} review'
        f"{'' if len(records) == 1 else 's'} on record</span>",
        "</div>",
        "",
    ]

    url = pre.get("url", "")
    rows = [f"| Preprint | [{md_cell(url)}]({url}) |"] if url else []
    if pre.get("doi"):
        rows.append(f"| DOI | `{pre['doi']}` |")
    if pre.get("authors"):
        rows.append(f"| Authors | {md_cell(', '.join(pre['authors']))} |")
    if rows:
        body += ["| | |", "|---|---|", "\n".join(rows), ""]

    body += [
        "## Review history",
        "",
        "Each review below describes the revision of the manuscript named in its",
        "row. Earlier reviews are never edited or removed when a new one is added —",
        "they remain the record of what the panel said about that revision.",
        "",
        "| Review | Round | Manuscript version | Recommendation | Reviewed |",
        "|---|---|---|---|---|",
    ]
    for name, prov in records:
        p = prov.get("preprint", {})
        verdict = (
            "Desk reject"
            if prov.get("desk_rejected")
            else VERDICT_LABEL.get(prov.get("decision", ""), prov.get("decision", "—"))
        )
        mver = f"v{p.get('version')}" if p.get("version") else "—"
        rnd = int(prov.get("round") or 1)
        if (prov.get("revision") or {}).get("kind") == "correction":
            # Same round, corrected. Numbering it as a new round would make the
            # count of manuscript revisions unreadable.
            body.append(
                f"| [{name}]({name}/index.md) | {rnd} (corrected) | {mver} "
                f"| {verdict} | {str(prov.get('generated_at', ''))[:10]} |"
            )
            continue
        # A round with no verified baseline is not the same evidence as one
        # that diffed the drafts, and the history is where that comparison
        # gets made — so it is flagged in the row, not only on the page.
        if rnd > 1 and not ((prov.get("revision") or {}).get("baseline") or {}).get(
            "restored"
        ):
            rnd_cell = f"{rnd} ⚠"
        else:
            rnd_cell = str(rnd)
        # `{name}/index.md`, not `{name}/`: MkDocs resolves .md targets and
        # warns on a bare directory in a markdown link.
        body.append(
            f"| [{name}]({name}/index.md) | {rnd_cell} | {mver} | {verdict} "
            f"| {str(prov.get('generated_at', ''))[:10]} |"
        )
    body.append("")

    if any(int(p.get("round") or 1) > 1 for _, p in records):
        body += [
            "A round above 1 means the authors revised the manuscript and the panel",
            "ruled on what changed rather than re-reading it cold. ⚠ marks a round",
            "that ran without a verified comparison of the old and new drafts — the",
            "referees still held their earlier points, but the delta was not checked",
            "against the previous file.",
            "",
        ]
        body += revision_arc(paper_dir, records)

    # The fingerprint is what makes "which revision was this?" answerable
    # rather than a matter of trust. Only shown when one was recorded.
    shas = [
        (name, prov.get("preprint", {}).get("pdf_sha256", ""))
        for name, prov in records
    ]
    if any(sha for _, sha in shas):
        body += [
            "??? note \"PDF fingerprints\"",
            "",
            "    SHA-256 of the exact file each panel was given.",
            "",
        ]
        for name, sha in shas:
            body.append(f"    - `{name}` — `{sha or 'not recorded'}`")
        body.append("")

    latest_name = records[0][0]
    body += citation_block(
        title=title,
        url=f"{SITE_URL}/{site_path(paper_dir)}/",
        year=str(latest.get("generated_at", ""))[:4] or str(dt.date.today().year),
        key=bibtex_key(paper_dir.name),
        reviewed_doi=pre.get("doi", ""),
        reviewed_version=str(pre.get("version") or ""),
        note_extra=(
            f"{len(records)} reviews on record; this URL shows {latest_name}"
            if len(records) > 1
            else ""
        ),
        evergreen=True,
    )

    (paper_dir / "index.md").write_text("\n".join(body), encoding="utf-8")


def revision_arc(paper_dir: Path, records: list[tuple[str, dict]]) -> list[str]:
    """How the recommendation moved across rounds, and what was asked each time.

    This is the thing In Silico can publish that a conventional journal does
    not: not just the final verdict but the whole trajectory — what was
    required, whether the next round found it done, and how the panel moved.
    Built from ``round.json`` in each bundle rather than from the prose, so it
    reports the same numbered items the pipeline itself reasoned about.
    """
    # Oldest first: an arc reads forwards.
    chron = sorted(records, key=lambda r: int(r[1].get("round") or 1))
    steps = []
    for name, prov in chron:
        verdict = (
            "desk reject"
            if prov.get("desk_rejected")
            else VERDICT_LABEL.get(prov.get("decision", ""), "—").lower()
        )
        steps.append(f"**{verdict}**")
    if len(steps) < 2:
        return []

    lines = ["### How it moved", "", " → ".join(steps), ""]

    for name, prov in chron:
        rnd = int(prov.get("round") or 1)
        asked = _required_count(paper_dir / name)
        if asked is None:
            continue
        if asked:
            lines.append(
                f"- Round {rnd} required {asked} "
                f"revision{'' if asked == 1 else 's'} "
                f"([`round.json`]({name}/round.json))."
            )
        else:
            lines.append(f"- Round {rnd} required no revisions.")
    lines.append("")
    return lines


def _required_count(bundle: Path) -> int | None:
    """How many numbered revisions a round required, from its own record.

    Read from the bundle's round.json rather than from provenance: the
    `revision` block in provenance describes the round this one *followed*,
    so its revision count belongs to the previous round, not this one.
    """
    try:
        record = json.loads((bundle / ROUND_RECORD).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    items = record.get("required_revisions")
    return len(items) if isinstance(items, list) else None


def solicitation_note(provenance: dict) -> list[str]:
    """Say whether the authors asked for this review.

    Anyone may submit any public preprint here, which makes In Silico usable
    for scrutinising work nobody has looked at — and equally usable for
    attaching a permanent public criticism to a rival's paper. Publishing both
    kinds identically would let the second hide inside the first.

    So the page states which it is. The claim is the submitter's and nothing
    verifies it; saying so is the point, since an unverifiable claim presented
    as fact is worse than one presented as a claim.
    """
    claim = provenance.get("submitter_is_author") or ""
    if claim == "yes":
        return [
            '!!! note "Requested by an author"',
            "    Submitted by someone who states they are an author of this paper.",
            "    We do not verify that claim.",
            "",
        ]
    if claim == "no":
        return [
            '!!! warning "The authors did not request this review"',
            "    It was submitted by someone who states they are **not** an author.",
            "    The authors were not consulted, have not seen it, and have not",
            "    replied to it. Weigh it accordingly.",
            "",
            "    Authors: if this misreads your paper, open an issue and we will",
            "    correct or withdraw it. See [contesting a review](../../../../policy.md#contesting-a-review).",
            "",
        ]
    return [
        '!!! note "Solicitation unrecorded"',
        "    This review predates our recording of whether the submitter was an",
        "    author, so we cannot say whether the authors asked for it.",
        "",
    ]


def revision_note(provenance: dict) -> list[str]:
    """State what this round was compared against, including when it wasn't.

    A revision round whose baseline could not be recovered still produces a
    full review — the reviewers still hold their prior points, the compliance
    auditor still checks the required revisions — but nothing in it is
    grounded in an actual v1→v2 comparison. On the page those two rounds look
    identical unless we say otherwise, so we say otherwise.
    """
    rev = provenance.get("revision") or {}
    prior = rev.get("prior_decision", "")

    if rev.get("kind") == "correction":
        who = rev.get("only_reviewers") or []
        scope = (
            f"Only {', '.join(who)} re-ran; every other referee's assessment is "
            "carried forward unchanged, so the panel score still reflects all of "
            "them."
            if who
            else "The whole panel re-ran."
        )
        lines = [
            '!!! info "Correction to the review, not a new manuscript"',
            "    The authors challenged the review itself. **The manuscript is",
            "    unchanged** — this is not a revision round and does not advance the",
            "    round number.",
            "",
            f"    {scope}",
            "",
            "    Their response was checked against the manuscript before the panel",
            "    saw it. Referees received corroborated pointers to passages to",
            "    re-read, never the response as prose, so it could direct attention",
            f"    but not move a score by assertion. See [the response]({AUTHOR_RESPONSE})",
            "    exactly as submitted.",
            "",
        ]
        if prior:
            lines.insert(
                4,
                f"    The review being corrected recommended "
                f"**{VERDICT_LABEL.get(prior, prior)}**.",
            )
            lines.insert(5, "")
        return lines

    if int(provenance.get("round") or 1) <= 1:
        return []

    lines = [
        f'!!! info "Revision round {provenance["round"]}"',
        "    The authors revised the manuscript after a previous review, and this",
        "    round rules on what changed: each referee revisits the points it",
        "    raised, and an auditor checks the previous decision letter's required",
        "    revisions against the new draft.",
        "",
    ]
    if prior:
        lines.insert(
            4,
            f"    The previous round recommended "
            f"**{VERDICT_LABEL.get(prior, prior)}**.",
        )
        lines.insert(5, "")

    baseline = rev.get("baseline") or {}
    if not baseline.get("restored"):
        lines += [
            '!!! warning "No draft comparison in this round"',
            "    The previously reviewed PDF could not be recovered, so this round",
            "    has no section-by-section comparison of the old and new drafts.",
            "    The referees still hold their earlier points and rule on them, but",
            "    nothing here rests on a verified diff of what actually changed.",
            "",
            f"    Reason: {baseline.get('reason') or 'unknown'}.",
            "",
        ]
    return lines


def render_landing(
    preprint: Preprint,
    provenance: dict,
    title: str,
    copied: list[tuple[str, str]],
    reviewer_files: list[Path],
    audit_files: list[Path],
    submission_id: str,
    submitter: str,
    bundle_path: str = "",
) -> str:
    decision = provenance["decision"]
    fm = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"decision: {yaml_scalar(decision)}",
        f"source: {yaml_scalar(preprint.source)}",
        f"preprint_url: {yaml_scalar(preprint.url)}",
        f"doi: {yaml_scalar(preprint.doi)}",
        f"reviewed: {yaml_scalar(provenance['generated_at'][:10])}",
        f"authors: {yaml_list(preprint.authors)}",
    ]
    if submission_id:
        fm.append(f"submission_issue: {yaml_scalar(submission_id)}")
    # Read by the index to put a score on each card without opening every
    # provenance.json. Absent on a desk reject, where no panel scored anything.
    if provenance.get("mean_score") is not None:
        fm.append(f"mean_score: {provenance['mean_score']}")
    fm.append(f"description: {yaml_scalar(card_description(provenance))}")
    if provenance.get("desk_rejected"):
        # Surfaced in frontmatter so the index can mark these distinctly
        # rather than filing them next to reasoned panel rejections.
        fm.append("desk_rejected: true")
    if int(provenance.get("round") or 1) > 1:
        fm.append(f"round: {int(provenance['round'])}")
    fm.append("---")

    rows = [
        f"| Preprint | [{md_cell(preprint.url)}]({preprint.url}) |",
        f"| Source | {preprint.source} |",
    ]
    if preprint.doi:
        rows.append(f"| DOI | `{md_cell(preprint.doi)}` |")
    if preprint.authors:
        rows.append(f"| Authors | {md_cell(', '.join(preprint.authors))} |")
    if preprint.published:
        rows.append(f"| Posted | {preprint.published} |")
    rows.append(f"| Reviewed | {provenance['generated_at'][:10]} |")
    if provenance.get("mean_score") is not None:
        rows.append(f"| Mean panel score | {provenance['mean_score']} / 5 |")
    if submission_id:
        rows.append(f"| Submission | [#{submission_id}]({REPO_URL}/issues/{submission_id}) |")
    if submitter:
        claim = {
            "yes": " — states they are an author",
            "no": " — **states they are not an author**",
        }.get(provenance.get("submitter_is_author") or "", "")
        rows.append(
            f"| Submitted by | [@{submitter}](https://github.com/{submitter})"
            f"{claim} |"
        )

    desk_rejected = provenance.get("desk_rejected")
    # "Panel recommendation" would be a false claim on a desk reject: no panel
    # convened. Say what actually happened, and why the page is short.
    if desk_rejected:
        chip = '<span class="ins-verdict ins-verdict--desk">Desk reject</span>'
        label = "Rejected at the desk"
        note = "no referee panel convened"
    else:
        chip = (
            f'<span class="ins-verdict ins-verdict--{decision}">'
            f"{VERDICT_LABEL.get(decision, decision)}</span>"
        )
        label = f"Panel recommendation: {VERDICT_LABEL.get(decision, decision)}"
        note = "advisory — a human editor decides"

    round_no = int(provenance.get("round") or 1)
    if round_no > 1:
        note = f"round {round_no} · {note}"

    body = [
        "\n".join(fm),
        "",
        f"# {md_text(title)}",
        "",
        '<div class="ins-decision">',
        f"  {chip}",
        f'  <span class="ins-decision__label">{label}</span>',
        f'  <span class="ins-decision__note">{note}</span>',
        "</div>",
        "",
    ]
    body += revision_note(provenance)
    body += solicitation_note(provenance)
    if desk_rejected:
        body += [
            "!!! danger \"Rejected at the desk — no referee panel was convened\"",
            "    This submission was stopped before review. There are no specialist",
            "    reports, no debate and no area-chair synthesis below, because none",
            "    were produced. See the documents listed under *The review* for the",
            "    reason.",
            "",
            "    A desk rejection on submission integrity means the file was found to",
            "    conceal instructions aimed at an automated reviewer. That scan is",
            "    deterministic and runs before any model reads the manuscript, so no",
            "    reviewer was exposed to the concealed text.",
            "",
        ]

    body += [
        "| | |",
        "|---|---|",
        "\n".join(rows),
        "",
    ]

    if preprint.abstract:
        body += ["## Abstract", "", f"> {md_text(preprint.abstract)}", ""]

    body += ["## The review", ""]
    for name, label in copied:
        body.append(f"- [{label}]({name})")
    if reviewer_files:
        body += ["", "### Specialist reports", ""]
        for src in reviewer_files:
            reviewer = src.stem.replace("review_", "").replace("_", " ").title()
            body.append(f"- [{reviewer}]({src.name})")

    if audit_files:
        body += [
            "",
            "### Editorial audits",
            "",
            "Factual checklists rather than opinions — these bypass the debate",
            "and go straight to the editor.",
            "",
        ]
        for src in audit_files:
            auditor = src.stem.replace("audit_", "").replace("_", " ").title()
            body.append(f"- [{auditor}]({src.name})")

    panel = provenance.get("panel") or []
    if panel:
        body += ["", "### Panel scores", "", "| Reviewer | Score | Confidence |", "|---|---|---|"]
        for entry in panel:
            reviewer = str(entry.get("reviewer", "")).replace("_", " ").title()
            body.append(
                f"| {reviewer} | {entry.get('score', '—')} | {entry.get('confidence', '—')} |"
            )

    pipe = provenance["pipeline"]
    sha = f" @ `{pipe['sha'][:8]}`" if pipe.get("sha") else ""
    body += [
        "",
        "## Provenance",
        "",
        f"Produced by [PeerReviewAgents](https://github.com/pgarrett-scripps/PeerReviewAgents) "
        f"`{pipe.get('version', 'unknown')}`{sha} on `{provenance.get('model') or 'unspecified'}` "
        f"with {provenance['debate_rounds']} debate round(s). "
        "Machine-readable: [`provenance.json`](provenance.json).",
        "",
    ]

    # With model tags configured the panel and the chair ran on different
    # models, and a reader deserves to know which wrote which.
    tags = provenance.get("models") or {}
    per_agent = provenance.get("agent_models") or {}
    if tags or per_agent:
        fallback = provenance.get("model") or "—"
        body += [
            "Not every stage ran on the same model:",
            "",
            "| Stage | Model |",
            "|---|---|",
        ]
        for tag in sorted(tags):
            entry = tags[tag] if isinstance(tags[tag], dict) else {"model": tags[tag]}
            body.append(
                f"| {_TAG_LABEL.get(tag, tag)} | `{entry.get('model') or fallback}` |"
            )
        for agent in sorted(per_agent):
            entry = (
                per_agent[agent]
                if isinstance(per_agent[agent], dict)
                else {"model": per_agent[agent]}
            )
            body.append(
                f"| {agent.replace('_', ' ')} (override) "
                f"| `{entry.get('model') or fallback}` |"
            )
        body.append("")

    if desk_rejected:
        # The generic advisory below describes an LLM panel. On a desk reject
        # there wasn't one, and an integrity reject isn't a judgment at all —
        # it's a deterministic finding about the file. Saying "advisory"
        # about it would understate it; saying "panel" would be untrue.
        body += [
            "!!! warning \"How this decision was reached\"",
            "    This submission was stopped at the desk, not judged by a referee",
            "    panel. A submission-integrity rejection is a deterministic finding",
            "    about the submitted file rather than an opinion about the work, and",
            "    says nothing about the quality of the research itself. Authors who",
            "    believe the finding is mistaken should open an issue.",
            "",
        ]
    else:
        body += [
            "!!! warning \"Advisory only\"",
            "    This review was generated by an LLM panel. The recommendation above is",
            "    advisory; the editorial decision on this submission was made by a human",
            "    editor. Nothing here has been verified by a human referee.",
            "",
        ]

    pipe = provenance["pipeline"]
    body += citation_block(
        title=title,
        url=f"{SITE_URL}/{bundle_path}/",
        year=provenance["generated_at"][:4],
        key=bibtex_key(Path(bundle_path).parent.name, Path(bundle_path).name),
        reviewed_doi=preprint.doi,
        reviewed_version=preprint.version,
        note_extra=(
            f"Produced by PeerReviewAgents {pipe.get('version', 'unknown')}"
            + (f" @ {pipe['sha'][:8]}" if pipe.get("sha") else "")
        ),
    )
    return "\n".join(body)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="preprint URL")
    src.add_argument("--issue-body", help="free text to scrape a URL out of")
    ap.add_argument("--submission-id", default="", help="submission issue number")
    ap.add_argument("--submitter", default="", help="GitHub login of the submitter")
    ap.add_argument(
        "--submitter-is-author",
        choices=("yes", "no", ""),
        default="",
        help="whether the submitter stated they are an author. Read from the "
             "submission form when --issue-body is given; recorded and shown "
             "on the published review.",
    )
    ap.add_argument("--provider", default=os.environ.get("REVIEW_PROVIDER") or None)
    # Left unset by default so ./peerreview.toml owns model selection — an
    # explicit value here would beat the TOML and silently defeat the [roles]
    # table's fallback model.
    ap.add_argument("--model", default=os.environ.get("REVIEW_MODEL") or None)
    ap.add_argument(
        "--debate-rounds",
        type=int,
        default=int(os.environ["REVIEW_DEBATE_ROUNDS"])
        if os.environ.get("REVIEW_DEBATE_ROUNDS")
        else None,
    )
    ap.add_argument(
        "--revision-of",
        metavar="BUNDLE",
        help="path to the previous round's bundle directory (e.g. "
             "docs/reviews/2026/<slug>/v1). Turns this into a revision round: "
             "reviewers rule on the points they raised, a compliance auditor "
             "checks the previous letter's required revisions against the new "
             "draft, and the editor decides on the delta.",
    )
    ap.add_argument(
        "--revise",
        action="store_true",
        help="continue this preprint's most recent round automatically, "
             "instead of naming the previous bundle with --revision-of.",
    )
    ap.add_argument(
        "--appeal",
        action="store_true",
        help="the manuscript is unchanged and the REVIEW is being challenged. "
             "Runs a correction against the most recent round: no compliance "
             "audit, no draft diff, and normally only the disputed reviewers "
             "re-run. Does not advance the round number.",
    )
    ap.add_argument(
        "--only-reviewers",
        metavar="NAMES",
        help="comma-separated reviewers to re-run on an appeal, e.g. "
             "'methodology,rigor'. The rest keep their previous reports, so "
             "the panel is still scored over all of them. Default: all.",
    )
    ap.add_argument(
        "--statement-source",
        metavar="URL",
        help="where the response came from (e.g. the GitHub comment URL), "
             "recorded in provenance so the published snapshot is traceable.",
    )
    ap.add_argument(
        "--author-statement",
        metavar="URL_OR_PATH",
        help="the authors' response letter. Treated as untrusted, "
             "interested-party input: injection-screened at the desk and "
             "never shown to the panel as prose. Requires --revision-of.",
    )
    ap.add_argument("--dry-run", action="store_true", help="resolve + download only")
    args = ap.parse_args()

    if args.revise and args.revision_of:
        ap.error("--revise and --revision-of do the same job; pass one.")
    if args.appeal and args.revise:
        ap.error(
            "--appeal and --revise are different acts: an appeal says the "
            "review is wrong about an unchanged manuscript, a revision says "
            "the manuscript changed. Pass one."
        )
    if args.only_reviewers and not args.appeal:
        ap.error(
            "--only-reviewers only applies to --appeal. A revision has a new "
            "draft, which every reviewer needs to see."
        )
    if args.author_statement and not (args.revision_of or args.revise or args.appeal):
        ap.error(
            "--author-statement requires --revision-of, --revise or --appeal: "
            "a response answers a previous round's review, so there has to "
            "be one."
        )

    url = args.url or extract_url(args.issue_body)
    # The form asks directly; a `/review` on a plain issue has no field to
    # read, and the page then says so rather than assuming either way.
    if not args.submitter_is_author and args.issue_body:
        args.submitter_is_author = extract_authorship(args.issue_body)
    preprint = resolve(url)
    print(f"resolved  {preprint.source}: {preprint.identifier or preprint.url}", file=sys.stderr)
    if preprint.title:
        print(f"title     {preprint.title}", file=sys.stderr)

    workdir = Path(tempfile.mkdtemp(prefix="insilico-"))
    pdf = download(preprint, workdir)
    print(f"pdf       {pdf} ({pdf.stat().st_size // 1024} KiB)", file=sys.stderr)

    if args.dry_run:
        print(json.dumps(preprint.to_dict(), indent=2))
        return 0

    from peerreviewagents.agents.editor.desk_screen import screen_mode
    from peerreviewagents.default_config import get_config
    from peerreviewagents.graph.review_graph import PeerReviewGraph
    from peerreviewagents.reports import write_reports

    # Only pass what was explicitly asked for. Anything omitted falls through
    # to ./peerreview.toml, which is where the [roles] table lives.
    overrides = {"output_dir": str(workdir / "reports")}
    if args.provider:
        overrides["provider"] = args.provider
    if args.model:
        overrides["reasoning_model"] = args.model
    if args.debate_rounds is not None:
        overrides["max_debate_rounds"] = args.debate_rounds

    revision: dict = {"round": 1}
    if args.revise or args.appeal:
        found = find_prior_bundle(
            preprint, preprint.title or preprint.identifier
        )
        if found is None:
            print(
                "No revisable round found for this preprint. Either it has "
                "never been reviewed here, or its reviews predate round "
                "records — run /review for a fresh round instead.",
                file=sys.stderr,
            )
            return 1
        args.revision_of = str(found)

    if args.revision_of:
        prior_bundle = Path(args.revision_of).resolve()
        if not (prior_bundle / ROUND_RECORD).is_file():
            print(
                f"--revision-of {args.revision_of}: no {ROUND_RECORD} there.\n"
                "A revision round needs the previous round's machine-readable "
                "record. Reviews published before round records existed cannot "
                "be revised — re-review the current draft as a fresh round "
                "instead.",
                file=sys.stderr,
            )
            return 1
        overrides["revision_of"] = str(prior_bundle)
        if args.appeal:
            overrides["revision_mode"] = "correction"
            if args.only_reviewers:
                overrides["only_reviewers"] = [
                    n.strip() for n in args.only_reviewers.split(",") if n.strip()
                ]
        statement_file = None
        if args.author_statement:
            statement_file = fetch_statement(args.author_statement, workdir)
            overrides["author_statement_path"] = str(statement_file)

    config = get_config(**overrides)

    if args.revision_of:
        prior = json.loads((prior_bundle / ROUND_RECORD).read_text(encoding="utf-8"))
        prior_round = int(prior.get("round", 1))
        revision = {
            # An appeal does NOT advance the round. Rounds count manuscript
            # revisions; if a correction bumped it, "round 3" would stop
            # telling a reader how many times the paper was rewritten.
            "round": prior_round if args.appeal else prior_round + 1,
            "prior_bundle": prior_bundle.name,
            "prior_decision": str(prior.get("decision", "")),
            "prior_round": int(prior.get("round", 1)),
            # The count the PREVIOUS round asked for. This round's own count
            # lives in its round.json; keeping them apart stops the paper
            # page attributing one round's asks to another.
            "prior_required_revisions": len(prior.get("required_revisions") or []),
            "author_statement": bool(args.author_statement),
            "kind": "correction" if args.appeal else "revision",
            "statement_source": args.statement_source or "",
            "statement_path": str(statement_file) if statement_file else "",
            "only_reviewers": list(config.get("only_reviewers") or []),
            # A correction compares nothing: the manuscript is unchanged by
            # definition, so there is no baseline to restore and no diff to
            # make. Claiming an unavailable baseline would read as a defect.
            "baseline": (
                {"restored": False, "reason": "", "verified": False, "n/a": True}
                if args.appeal
                else restore_prior_draft(prior_bundle, workdir, config)
            ),
        }
        max_rounds = int(config.get("max_rounds") or 3)
        if revision["round"] > max_rounds:
            print(
                f"This would be round {revision['round']}, and max_rounds is "
                f"{max_rounds}. An endless revise-and-resubmit loop is a "
                "failure, not a process — decide the submission instead.",
                file=sys.stderr,
            )
            return 1
        b = revision["baseline"]
        if args.appeal:
            who = ", ".join(revision["only_reviewers"]) or "the full panel"
            print(
                f"appeal    correction to round {revision['round']} "
                f"({prior_bundle.name}); re-running {who}",
                file=sys.stderr,
            )
        else:
            print(
                f"revision  round {revision['round']} of {prior_bundle.name}"
                f" — baseline {'restored' if b['restored'] else 'UNAVAILABLE'}",
                file=sys.stderr,
            )
            if not b["restored"]:
                print(f"          {b['reason']}", file=sys.stderr)

    # Record what actually ran, not what was requested — with roles configured
    # these differ per agent, so the resolved config is the honest answer.
    os.environ["REVIEW_PROVIDER"] = config["provider"]
    os.environ["REVIEW_MODEL"] = config["reasoning_model"]
    os.environ["REVIEW_DEBATE_ROUNDS"] = str(config["max_debate_rounds"])
    os.environ["REVIEW_MODELS"] = json.dumps(config.get("models") or {}, sort_keys=True)
    os.environ["REVIEW_AGENT_MODELS"] = json.dumps(
        config.get("agent_models") or {}, sort_keys=True
    )
    # What the desk was configured to do. Recorded per review because these
    # are policy commitments, and a reader should be able to confirm the gate
    # was actually on for *this* submission rather than trust the current
    # contents of peerreview.toml.
    os.environ["REVIEW_SCREENS"] = json.dumps(
        {
            "injection_screen": bool(config.get("injection_screen", True)),
            "injection_screen_action": config.get("injection_screen_action") or "reject",
            # Ask the pipeline rather than reading the key: `desk_screen_mode`
            # and the legacy boolean `desk_screen` both feed this, and
            # screen_mode() is what actually decides.
            "desk_screen_mode": screen_mode(config),
        },
        sort_keys=True,
    )

    # The pipeline reports one total, which is enough to know a run was
    # expensive and useless for knowing *why*. Per-agent usage already flows
    # through the observability bus; drain it so cost decisions can be made
    # from a breakdown instead of an inference.
    graph = PeerReviewGraph(config)
    with _cost_recorder(graph.run_id) as cost_by_node:
        state = graph.review(str(pdf))

    decision = state.get("decision")
    if decision not in VERDICT_LABEL:
        errors = "; ".join(state.get("errors") or []) or "no decision produced"
        print(f"review failed: {errors}", file=sys.stderr)
        return 1

    run_dir = Path(write_reports(state))
    title = preprint.title or state.get("manuscript_title") or preprint.identifier
    year = (preprint.published or dt.date.today().isoformat())[:4]
    slug = paper_slug(preprint, title)
    paper_dir = REVIEWS / year / slug
    if args.revision_of:
        # Stay in the paper's existing directory. The slug embeds the title,
        # so a revision that renamed the manuscript would otherwise open a
        # second directory for the same paper and split its review history in
        # two — with each half claiming to be the whole record.
        paper_dir = Path(args.revision_of).resolve().parent
        slug = paper_dir.name
    # Always a fresh vN. A re-review of a revised manuscript sits beside the
    # earlier one instead of overwriting it, which the policy promises and
    # the previous flat layout quietly broke.
    version = next_version(paper_dir)
    dest = paper_dir / f"v{version}"

    write_bundle(
        preprint, state, run_dir, dest,
        args.submission_id, args.submitter, cost_by_node, revision,
        submitter_is_author=args.submitter_is_author,
    )
    write_paper_page(paper_dir)
    rel = dest.relative_to(REPO)
    desk_rejected = bool(state.get("desk_rejected"))
    print(f"bundle    {rel}", file=sys.stderr)
    print(f"decision  {decision}{' (desk reject)' if desk_rejected else ''}", file=sys.stderr)
    for node, spend in sorted(cost_by_node.items(), key=lambda kv: -kv[1]):
        print(f"  cost    {node:<28} ${spend:.4f}", file=sys.stderr)

    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as fh:
            fh.write(f"decision={decision}\n")
            fh.write(f"desk_rejected={'true' if desk_rejected else 'false'}\n")
            fh.write(f"slug={slug}\n")
            fh.write(f"year={year}\n")
            fh.write(f"path={rel}\n")
            # The re-review case needs to be visible in the PR: "v2" means an
            # earlier review of this paper already exists and is not replaced.
            fh.write(f"version={version}\n")
            fh.write(f"round={revision['round']}\n")
            # Surfaced so the PR can say a revision round ran without a
            # verified diff, which changes how much the delta is worth.
            fh.write(
                "baseline="
                + ("restored" if (revision.get("baseline") or {}).get("restored")
                   else "unavailable" if revision["round"] > 1 else "n/a")
                + "\n"
            )
            fh.write(f"title={title}\n")
            fh.write(f"cost={state.get('total_cost') or 0}\n")

    shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
