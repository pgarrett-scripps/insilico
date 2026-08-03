"""Fetch a preprint, run the referee panel over it, and write a review bundle.

    python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
    python scripts/run_review.py --issue-body "$ISSUE_BODY" --submission-id 12

Output lands in ``docs/reviews/<year>/<slug>/v<N>/`` and is what the bot commits.
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
# desk_screen.md carries the triage verdict and is written whenever that screen
# ran, pass or reject. integrity.md is written only when the concealed-text scan
# found something, so most bundles do not have one.
#
# The pipeline also supports an author response letter, and In Silico
# deliberately never sends one. Given a letter asserting that revisions were
# made, the compliance auditor confirmed four of them and invented supporting
# detail — a permutation test "reported in the Fig. 6 legend" that appears
# nowhere in the manuscript — and the editor moved the verdict a full grade on
# the strength of it. Re-running the identical round with no letter attached,
# the same auditor read the manuscript and got all ten items right. Authors
# still get a reply published beside the review; it simply never reaches an
# agent, because an interested party's prose is not evidence and this system
# demonstrably cannot treat it as anything else.
#
# manuscript_stats.md is counts, not opinion: how the PDF converted, how long
# the paper is, how its prose is shaped. It travels because this is an overlay
# journal — the reader has the PDF and the panel had a conversion of it, and
# without these numbers there is no way to check that those were the same
# document. Nothing in it reaches an agent; see the pipeline's ingest/prose.py.
BUNDLE_FILES = [
    "summary.md",
    "decision_letter.md",
    "integrity.md",
    "desk_screen.md",
    "meta_review.md",
    "author_rebuttal.md",
    "debate_transcript.md",
    "journal_recommendations.md",
    "manuscript_stats.md",
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


def _rerun_provenance(bundle: str) -> dict | None:
    """The provenance of the bundle being re-reviewed, or None with a message.

    Only provenance is needed, not a round record: a rerun is a fresh round 1
    that rules on nothing from before, so reviews published before round
    records existed can still be rerun. That is deliberate — the oldest
    reviews are the ones most likely to predate a pipeline worth re-running.
    """
    path = Path(bundle).resolve()
    prov_path = path / "provenance.json"
    if not prov_path.is_file():
        print(
            f"--rerun-of {bundle}: no provenance.json there. Point this at a "
            "published bundle directory, e.g. docs/reviews/2026/<slug>/v1.",
            file=sys.stderr,
        )
        return None
    try:
        prov = json.loads(prov_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"--rerun-of {bundle}: unreadable provenance.json ({exc}).", file=sys.stderr)
        return None
    if not (prov.get("preprint") or {}).get("url"):
        print(
            f"--rerun-of {bundle}: provenance records no preprint URL, so the "
            "draft it reviewed cannot be fetched again.",
            file=sys.stderr,
        )
        return None
    prov["_bundle"] = path
    return prov


def _same_draft(pdf: Path, prior: dict, config: dict) -> bool:
    """Whether the manuscript just fetched is the one the prior round read.

    A rerun exists to hold the manuscript fixed and vary the pipeline, so this
    guard is the whole feature: without it a comparison silently measures a
    manuscript change and a pipeline change at once, and produces a bundle
    that looks exactly like evidence about the pipeline.

    It compares the *converted text*, not the PDF. Those are different
    questions and the file hash answers the wrong one. Measured on this very
    paper: three downloads of the same pinned bioRxiv URL over ten hours gave
    three different file checksums at an identical 1,689,095 bytes — the
    server stamps something fixed-width into the container — while the
    converted text came back byte-identical all three times. Checking the file
    hash refuses every bioRxiv rerun, including the correct ones.

    Older bundles predate the text fingerprint. Those fall back to the
    character count, which is weak but real, and say so — refusing to rerun
    the oldest reviews would defeat the purpose, since they are the ones most
    likely to predate a pipeline worth re-running.
    """
    from peerreviewagents.ingest.loader import load_manuscript_record

    ok, message = draft_matches(
        prior.get("ingest") or {}, load_manuscript_record(str(pdf), config).ingest
    )
    print(message if ok else f"{message}\n{_REVISE_HINT}", file=sys.stderr)
    return ok


_REVISE_HINT = (
    "A rerun holds the manuscript fixed and varies the pipeline, so a "
    "comparison here would measure both at once. If the authors posted a new "
    "version, that is a revision — use --revise."
)


def draft_matches(prior: dict, current: dict) -> tuple[bool, str]:
    """Compare two ingest records. Pure, so it can be tested without a PDF.

    Three tiers, strongest first. The text fingerprint is proof. The character
    count is evidence, and is all that older bundles carry. A bundle recording
    neither cannot be checked, and says so rather than claiming a match.
    """
    want = str(prior.get("text_sha256") or "")
    if want:
        got = str(current.get("text_sha256") or "")
        if want == got:
            return True, f"rerun     same draft confirmed (text {got[:16]}…)"
        return False, (
            "This is not the manuscript that bundle reviewed.\n"
            f"  recorded text {want}\n"
            f"  converted     {got}"
        )

    want_chars, got_chars = prior.get("chars"), current.get("chars")
    if isinstance(want_chars, int) and isinstance(got_chars, int):
        if want_chars == got_chars:
            return True, (
                f"rerun     same draft, probably: {got_chars:,} characters, "
                "matching the prior round. That bundle predates the text "
                "fingerprint, so this is a length match, not proof."
            )
        return False, (
            "This is not the manuscript that bundle reviewed.\n"
            f"  recorded  {want_chars:,} characters\n"
            f"  converted {got_chars:,}"
        )

    return True, (
        "warning: the prior bundle recorded nothing about the text it read, so "
        "this rerun cannot show it read the same draft."
    )


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


# A model slug an editor may name in a comment. Deliberately strict: the
# comment body is untrusted text that ends up in a config value and in a
# published record, so anything outside this alphabet is refused rather than
# sanitised. Covers every real OpenRouter slug — `vendor/model`, optionally
# `:free`, `:nitro`, `@preset` — and nothing that looks like a shell or a path.
_MODEL_SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9._-]*)?/[a-z0-9][a-z0-9._-]*(:[a-z0-9-]+)?$", re.I)

# Providers an editor may select by name. Not the full set the pipeline
# supports — `openai` is omitted because there is no key for it here, and a
# command that silently does nothing is worse than one that is refused.
_SELECTABLE_PROVIDERS = ("anthropic", "openrouter")


class CommandError(ValueError):
    """An editor's command could not be understood. The message is shown to
    them on the issue, so it says what to type instead."""


def parse_command(body: str) -> dict:
    """Read `/review`, `/revise` and their provider options out of a comment.

    Grammar, deliberately tiny:

        /review                          the configured panel (peerreview.toml)
        /review anthropic                the same, said out loud
        /review openrouter <model>       one model for every agent
        /revise ...                      any of the above, as a revision round

    Parsed here rather than in the workflow because the comment is untrusted
    input. Bash sees it only as an environment variable; this is the one place
    it is interpreted, and everything it can produce is either a known constant
    or a string that matched :data:`_MODEL_SLUG_RE`.

    OpenRouter requires an explicit model and always will. Its free tier is a
    rotating set of specific slugs, not a stable "free" alias, so guessing one
    would silently review a paper on whatever happened to be cheapest that
    week and publish the result without anyone having chosen it.
    """
    first = (body or "").strip().splitlines()[0] if (body or "").strip() else ""
    parts = first.split()
    out: dict = {"revise": False, "provider": None, "model": None}
    if not parts or not parts[0].startswith("/"):
        return out

    command = parts[0].lower()
    if command not in ("/review", "/revise"):
        return out
    out["revise"] = command == "/revise"

    rest = parts[1:]
    if not rest:
        return out

    provider = rest[0].lower()
    if provider not in _SELECTABLE_PROVIDERS:
        raise CommandError(
            f"`{rest[0]}` is not a provider I know. Use "
            f"`{command}`, `{command} anthropic`, or "
            f"`{command} openrouter <model>`."
        )
    out["provider"] = provider

    if provider == "anthropic":
        if len(rest) > 1:
            raise CommandError(
                f"`{command} anthropic` takes no model: the Anthropic runs use "
                "the per-stage split in `peerreview.toml`, which is the whole "
                "point of that file. To force one model, use "
                f"`{command} openrouter <model>`."
            )
        return out

    if len(rest) < 2:
        raise CommandError(
            "OpenRouter needs an explicit model, e.g. "
            f"`{command} openrouter nvidia/nemotron-3-ultra:free`. There is no "
            "stable alias for the free tier — the free models are a rotating "
            "set of specific slugs, so naming one is the only way to know what "
            "reviewed the paper."
        )
    model = rest[1]
    if not _MODEL_SLUG_RE.match(model):
        raise CommandError(
            f"`{model}` does not look like an OpenRouter model. They are "
            "`vendor/model`, optionally with a `:tag` — for example "
            "`nvidia/nemotron-3-ultra:free`."
        )
    out["model"] = model
    return out


def pipeline_version() -> dict[str, str]:
    """Identify exactly which referee panel produced a review.

    The workflow sets ``PEERREVIEW_PIPELINE_SHA`` from the commit it pinned.
    A local run has no such pin, and used to record an empty sha — which is
    the wrong answer for the one thing reruns exist to do. Comparing two
    reviews of the same draft is only informative if the record says which
    two pipelines were compared, and "unrecorded" makes the comparison
    unciteable.

    So fall back to asking the installed package where it came from. That
    works for an editable install off a checkout, which is how local runs are
    set up, and returns nothing when the package came from a wheel — in which
    case the empty string is the honest answer it always was.
    """
    info = {"sha": os.environ.get("PEERREVIEW_PIPELINE_SHA", "")}
    if not info["sha"]:
        info["sha"] = _installed_pipeline_sha()
    try:
        from importlib.metadata import version

        info["version"] = version("peerreviewagents")
    except Exception:  # noqa: BLE001 - metadata is best-effort
        info["version"] = "unknown"
    return info


def _installed_pipeline_sha() -> str:
    """HEAD of the checkout the installed pipeline is imported from, or ''.

    Marked ``+dirty`` when that checkout has uncommitted changes, because a
    rerun against a working tree is exactly when the sha alone would lie: two
    reviews would name the same commit while running different code.
    """
    try:
        import subprocess  # noqa: PLC0415 - only needed on this path

        import peerreviewagents

        repo = Path(peerreviewagents.__file__).resolve().parent.parent
        if not (repo / ".git").exists():
            return ""
        run = lambda *a: subprocess.run(  # noqa: E731
            a, cwd=repo, capture_output=True, text=True, timeout=5, check=True
        ).stdout.strip()
        sha = run("git", "rev-parse", "HEAD")
        dirty = run("git", "status", "--porcelain")
        return f"{sha}+dirty" if dirty else sha
    except Exception:  # noqa: BLE001 - identification is best-effort
        return ""


def panel_scores(state: dict) -> list[dict]:
    """Each referee's score, keeping a null one null.

    A null score means the dimension had nothing to judge in this manuscript —
    a data-analysis review of a paper with no quantitative analysis. It is
    carried through as null and left out of the mean, never filled in: the
    reviewer that had to invent a number reliably invented a generous one, and
    the resulting inflation is invisible once it has become a float.
    """
    out = []
    for report in state.get("reports", []) or []:
        if not isinstance(report, dict):
            continue
        entry = {
            "reviewer": report.get("reviewer", "unknown"),
            "score": report.get("score"),
            "confidence": report.get("confidence"),
        }
        reason = str(report.get("not_applicable_reason") or "").strip()
        if entry["score"] is None and reason:
            entry["not_applicable_reason"] = reason
        out.append(entry)
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
    ingest: dict | None = None,
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
        # How the manuscript was read, as the pipeline recorded it. The panel
        # is given a markdown rendering of the PDF rather than the PDF itself,
        # and under compression a quoted sentence will be missing its articles
        # and copulas — so a reader checking a quotation against the paper
        # needs to know this before concluding the referee misquoted it.
        "ingest": ingest or {},
        "screens": json.loads(os.environ.get("REVIEW_SCREENS") or "{}"),
        "panel": scores,
        "mean_score": round(sum(numeric) / len(numeric), 2) if numeric else None,
        # How many referees the mean is actually over. A 4.1 across eight
        # referees and a 4.1 across three are different claims, and without
        # both numbers a page showing only the mean cannot tell them apart.
        "scored_count": len(numeric),
        "panel_size": len(scores),
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


def _prior_cache_key(prior_bundle: Path) -> str:
    """The manuscript cache key the previous round wrote into round.json."""
    try:
        record = json.loads((prior_bundle / ROUND_RECORD).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(record.get("manuscript_cache_key") or "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    # Where the manuscript comes from. Exactly one, and --rerun-of belongs
    # here rather than beside --revision-of: it names the preprint as much as
    # it names a prior round, because the whole point is to review the
    # identical draft rather than whatever the URL resolves to today.
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="preprint URL")
    src.add_argument("--issue-body", help="free text to scrape a URL out of")
    src.add_argument(
        "--rerun-of",
        metavar="BUNDLE",
        help="path to a bundle to re-review under the current pipeline. The "
             "SAME draft is reviewed again from scratch, with no knowledge of "
             "the earlier round, and the new bundle sits beside it. Use this "
             "after changing prompts, models or config, to see what the change "
             "did. Not a revision: the manuscript has not moved.",
    )
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
        "--command",
        default="",
        help="the editor's comment body, e.g. '/review openrouter "
             "vendor/model'. Parsed here rather than in the workflow because "
             "it is untrusted text; see parse_command.",
    )
    ap.add_argument("--dry-run", action="store_true", help="resolve + download only")
    args = ap.parse_args()

    if args.command:
        try:
            selected = parse_command(args.command)
        except CommandError as exc:
            # Written to be read by the editor who typed it, on the issue.
            print(f"{exc}", file=sys.stderr)
            if out := os.environ.get("GITHUB_OUTPUT"):
                with open(out, "a", encoding="utf-8") as fh:
                    fh.write("bad_command=true\n")
                    fh.write(f"bad_command_reason={' '.join(str(exc).split())}\n")
            return 2
        args.revise = args.revise or selected["revise"]
        args.provider = args.provider or selected["provider"]
        args.model = args.model or selected["model"]

    if args.revise and args.revision_of:
        ap.error("--revise and --revision-of do the same job; pass one.")
    if args.rerun_of and (args.revise or args.revision_of):
        ap.error(
            "--rerun-of re-reviews the SAME draft under a new pipeline; "
            "--revise/--revision-of review a NEW draft against the old round. "
            "They answer different questions; pass one."
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
    rerun_prov: dict | None = None
    if args.rerun_of:
        rerun_prov = _rerun_provenance(args.rerun_of)
        if rerun_prov is None:
            return 1
        url = str((rerun_prov.get("preprint") or {}).get("url") or "")
        # Carried forward, because they describe the submission and the
        # submission has not changed. Only the pipeline has.
        args.submitter = args.submitter or str(rerun_prov.get("submitter") or "")
        args.submitter_is_author = (
            args.submitter_is_author or str(rerun_prov.get("submitter_is_author") or "")
        )
    else:
        url = args.url or extract_url(args.issue_body)
    # The form asks directly; a `/review` on a plain issue has no field to
    # read, and the page then says so rather than assuming either way.
    if not args.submitter_is_author and args.issue_body:
        args.submitter_is_author = extract_authorship(args.issue_body)
    preprint = resolve(url)
    print(f"resolved  {preprint.source}: {preprint.identifier or preprint.url}", file=sys.stderr)
    if preprint.title:
        print(f"title     {preprint.title}", file=sys.stderr)

    if rerun_prov is not None:
        # resolve() follows the URL to whatever the server serves now, which
        # for a bare bioRxiv link is the LATEST version. A rerun that silently
        # picked up v2 would report a pipeline change while actually measuring
        # a manuscript change, which is the one thing this flag exists to
        # prevent. Pin the recorded PDF URL and check the bytes below.
        pinned = str((rerun_prov.get("preprint") or {}).get("pdf_url") or "")
        if pinned:
            preprint.pdf_url = pinned

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
    from peerreviewagents.ingest.loader import ManuscriptUnreadable
    from peerreviewagents.reports import write_reports

    # Only pass what was explicitly asked for. Anything omitted falls through
    # to ./peerreview.toml, which is where the [models.*] tables live.
    overrides = {"output_dir": str(workdir / "reports")}
    if args.provider:
        overrides["provider"] = args.provider
    if args.model:
        overrides["reasoning_model"] = args.model
        # Clearing these is what makes "one model for everything" true, and
        # leaving them set is a trap rather than a partial success. The tag
        # tables win over `reasoning_model` — resolve_model reads
        # `raw.get("model") or config.get("reasoning_model")` — so with
        # peerreview.toml's split intact, `--provider openrouter --model X`
        # sends every agent to OpenRouter asking for `claude-haiku-4-5` and
        # `claude-opus-5`. X reviews nothing, the slugs are not valid there,
        # and the run either fails oddly or bills someone for Claude.
        #
        # So a named model means exactly one model. That is also the honest
        # reading of the request: an editor naming a free model wants the free
        # model, not a panel that quietly kept four paid ones.
        overrides["models"] = {}
        overrides["agent_models"] = {}
    if args.debate_rounds is not None:
        overrides["max_debate_rounds"] = args.debate_rounds

    revision: dict = {"round": 1}
    if rerun_prov is not None:
        # Round 1, and no `revision_of` in the config. Both are the point: the
        # panel must not be shown the earlier round's findings, or it would
        # rule on them instead of reading the paper, and a rerun that inherits
        # the verdict it is supposed to be testing tests nothing.
        prior_pipeline = (rerun_prov.get("pipeline") or {}).get("sha") or ""
        revision = {
            "round": 1,
            "kind": "rerun",
            "rerun_of": rerun_prov["_bundle"].name,
            "prior_decision": str(rerun_prov.get("decision") or ""),
            "prior_mean_score": rerun_prov.get("mean_score"),
            "prior_pipeline_sha": prior_pipeline,
            "prior_reviewed_at": str(rerun_prov.get("generated_at") or "")[:10],
        }
        print(
            f"rerun     of {revision['rerun_of']} "
            f"({revision['prior_decision'] or 'no decision'}, "
            f"mean {revision['prior_mean_score']}, "
            f"pipeline {prior_pipeline[:8] or 'unrecorded'})",
            file=sys.stderr,
        )
    if args.revise:
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

    config = get_config(**overrides)

    # After config, because answering "same draft?" means converting the PDF
    # the way this run will convert it, and the conversion depends on config
    # (compression above all). The parse is cached, so the graph reuses it
    # rather than paying for it twice.
    if rerun_prov is not None and not _same_draft(pdf, rerun_prov, config):
        return 1

    if args.revision_of:
        prior = json.loads((prior_bundle / ROUND_RECORD).read_text(encoding="utf-8"))
        prior_round = int(prior.get("round", 1))
        revision = {
            "round": prior_round + 1,
            "prior_bundle": prior_bundle.name,
            "prior_decision": str(prior.get("decision", "")),
            "prior_round": int(prior.get("round", 1)),
            # The count the PREVIOUS round asked for. This round's own count
            # lives in its round.json; keeping them apart stops the paper
            # page attributing one round's asks to another.
            "prior_required_revisions": len(prior.get("required_revisions") or []),
            "kind": "revision",
            "baseline": restore_prior_draft(prior_bundle, workdir, config),
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
    try:
        with _cost_recorder(graph.run_id) as cost_by_node:
            # The PDF, not a conversion of it. The pipeline converts it to
            # markdown internally; handing it a .md instead would route the
            # integrity screen to its markup scanner, which cannot see text
            # concealed in a content stream, and would change the manuscript
            # cache key that the next round re-derives to recover this draft.
            state = graph.review(str(pdf))
    except ManuscriptUnreadable as exc:
        # No bundle, no verdict, nothing published. A scanned or image-only
        # PDF is the usual cause, and docs/submit.md already tells authors we
        # cannot read one — this is that promise being kept at the point it
        # can be checked, instead of a panel reviewing the converter's output
        # and a reader discovering it by comparing a quotation to the PDF.
        print(f"unreadable: {exc}", file=sys.stderr)
        if out := os.environ.get("GITHUB_OUTPUT"):
            # Flattened: a newline in a `key=value` output line silently
            # truncates the value and leaves the remainder parsed as another
            # key. The message is one line today; this keeps it one.
            reason = " ".join(str(exc).split())
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("unreadable=true\n")
                fh.write(f"unreadable_reason={reason}\n")
        return 3

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
    if args.revision_of or rerun_prov is not None:
        # Stay in the paper's existing directory. The slug embeds the title,
        # so a revision that renamed the manuscript would otherwise open a
        # second directory for the same paper and split its review history in
        # two — with each half claiming to be the whole record.
        #
        # A rerun needs it for a plainer reason: the two reviews are of the
        # same draft, and the whole value of the exercise is being able to
        # read them side by side on one page.
        anchor = args.revision_of or str(rerun_prov["_bundle"])
        paper_dir = Path(anchor).resolve().parent
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
        ingest=state.get("ingest"),
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
