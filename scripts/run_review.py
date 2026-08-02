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

REPO_URL = (
    f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/"
    f"{os.environ.get('GITHUB_REPOSITORY', 'pgarrett-scripps/insilico')}"
)

# Bundle documents the pipeline emits. This script only decides which files
# travel with a review; how they are labelled, ordered and presented is the
# site's business, and lives in src/lib/corpus.js.
#
# integrity.md and desk_screen.md are written only when the desk found
# something. author_response_verification.md appears on revision rounds: it is
# what the panel was actually allowed to see of the authors' letter —
# corroborated pointers, never the letter's own prose — so publishing it is
# what makes "the letter could not move a score" checkable rather than
# asserted.
BUNDLE_FILES = [
    "summary.md",
    "decision_letter.md",
    "integrity.md",
    "desk_screen.md",
    "author_response_verification.md",
    "meta_review.md",
    "author_rebuttal.md",
    "debate_transcript.md",
    "journal_recommendations.md",
]

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

    # Every document is copied, including the ones a desk reject makes
    # byte-identical (it sets decision_letter, desk_screen and integrity to the
    # same body). A reader following a direct link should find the file; the
    # site is what decides not to show one text under three headings.
    for name in BUNDLE_FILES:
        src = run_dir / name
        if src.exists():
            shutil.copy2(src, dest / name)

    for src in sorted(run_dir.glob("review_*.md")) + sorted(run_dir.glob("audit_*.md")):
        shutil.copy2(src, dest / src.name)

    # Data rather than a document, but it has to travel with the bundle: it is
    # the thing a later round is pointed at.
    if (run_dir / ROUND_RECORD).exists():
        shutil.copy2(run_dir / ROUND_RECORD, dest / ROUND_RECORD)

    # Snapshot of the authors' response exactly as submitted. GitHub comments
    # can be edited after the fact, so a published review that merely links to
    # one would end up citing text that no longer says what we answered. The
    # copy is what makes the record hold still.
    #
    # Whether one arrived is recorded rather than left to be inferred later:
    # an `/appeal` with no author comment is explicitly allowed, and without
    # this flag the correction notice would claim a response was verified and
    # link to a file that was never written — on exactly the rounds where
    # neither happened.
    statement = revision.get("statement_path")
    revision["response_published"] = bool(statement and Path(statement).is_file())
    if revision["response_published"]:
        shutil.copy2(statement, dest / AUTHOR_RESPONSE)

    decision = state.get("decision", "unknown")
    scores = panel_scores(state)
    numeric = [s["score"] for s in scores if isinstance(s.get("score"), (int, float))]

    provenance = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "provider": os.environ.get("REVIEW_PROVIDER", "anthropic"),
        "model": os.environ.get("REVIEW_MODEL", ""),
        # Which model each stage actually ran on. Without these a reader sees
        # only the fallback and cannot tell which agent wrote which report:
        # `models` is keyed by tag (reviewer, audit, debate, synthesis),
        # `agent_models` by the individual agents that override their tag.
        "models": json.loads(os.environ.get("REVIEW_MODELS") or "{}"),
        "agent_models": json.loads(os.environ.get("REVIEW_AGENT_MODELS") or "{}"),
        # Always set from the resolved config before this runs; the literal is
        # only reached by a direct call in a test, and matches peerreview.toml.
        "debate_rounds": int(os.environ.get("REVIEW_DEBATE_ROUNDS", "1")),
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
    # provenance.json is the whole published record of the run. The site
    # renders every page from it, so this script writes data and no markup —
    # which is why a change to how a review *looks* no longer means editing
    # the program that produces reviews.
    (dest / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


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

    Checking the URL is necessary but not sufficient — see
    :class:`_GuardedRedirectHandler` for the other half.
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


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-check every redirect hop against the same rule as the first URL.

    Vetting only the URL the submitter typed is not a control, because the
    submitter also chooses what that URL redirects *to*. urllib follows
    redirects automatically, so a perfectly public https host answering 302
    with ``http://169.254.169.254/latest/meta-data/iam/security-credentials/``
    lands the runner's cloud credentials in the fetched file — which this
    pipeline then publishes verbatim into the review bundle as the authors'
    response. The check that ran before the request is exactly the check that
    has to run again at each hop.

    Refusals are raised rather than returned so a blocked hop stops the run
    with the reason, instead of degrading to a fetch of something else.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _reject_internal_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _public_opener() -> urllib.request.OpenerDirector:
    """An opener that enforces :func:`_reject_internal_url` on every hop."""
    return urllib.request.build_opener(_GuardedRedirectHandler)


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
    data = _get(source, max_bytes=8 * 1024 * 1024, opener=_public_opener())
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
    # explicit value here would beat the TOML and silently defeat the [models]
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

    workdir = Path(tempfile.mkdtemp(prefix="insilico-"))
    try:
        return _run(args, workdir)
    except ValueError as exc:
        # resolve() and extract_url() reject an unusable submission with a
        # message written to be read by the person who submitted it — which
        # host to use, why a bare PDF is not enough. A traceback buries that
        # under a stack nobody needs, in an Actions log an editor is skimming.
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        # The published policy says manuscript PDFs live in a temporary
        # directory and are deleted afterwards. Cleaning up only where the run
        # succeeded made that untrue for every early exit — an unresolvable
        # URL, a refused revision, a failed panel, a dry run — which between
        # them are most of the ways a run ends.
        shutil.rmtree(workdir, ignore_errors=True)


def _run(args, workdir: Path) -> int:
    """The review itself. Split out so the temp directory is always cleaned."""
    url = args.url or extract_url(args.issue_body)
    # The form asks directly; a `/review` on a plain issue has no field to
    # read, and the page then says so rather than assuming either way.
    if not args.submitter_is_author and args.issue_body:
        args.submitter_is_author = extract_authorship(args.issue_body)
    preprint = resolve(url)
    print(f"resolved  {preprint.source}: {preprint.identifier or preprint.url}", file=sys.stderr)
    if preprint.title:
        print(f"title     {preprint.title}", file=sys.stderr)

    pdf = download(preprint, workdir)
    print(f"pdf       {pdf} ({pdf.stat().st_size // 1024} KiB)", file=sys.stderr)

    if args.dry_run:
        print(json.dumps(preprint.to_dict(), indent=2))
        return 0

    # Stop before the panel if the metadata lookup came back empty. The
    # resolvers treat that as survivable — the PDF is what gets reviewed — but
    # a published review with no title, no authors and no DOI cannot be cited,
    # cannot be found, and does not name the work it judges. It is not worth
    # the cost of a panel, and the failure is nearly always transient
    # throttling that a later re-run will not hit.
    if not preprint.title:
        print(
            f"no metadata for {preprint.identifier or url}: the source returned "
            "no title, authors or DOI, so a review of it could not be cited or "
            "found. This is usually the API throttling us — wait a minute and "
            "run it again.",
            file=sys.stderr,
        )
        return 1

    from peerreviewagents.agents.editor.desk_screen import screen_mode
    from peerreviewagents.default_config import get_config
    from peerreviewagents.graph.review_graph import PeerReviewGraph
    from peerreviewagents.reports import write_reports

    # Only pass what was explicitly asked for. Anything omitted falls through
    # to ./peerreview.toml, which is where the [models.*] tables live.
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
