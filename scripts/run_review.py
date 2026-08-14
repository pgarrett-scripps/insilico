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
import json
import os
import re
import shutil
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from queue import Empty, Queue

sys.path.insert(0, str(Path(__file__).parent))

from fetch_preprint import (  # noqa: E402
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
# Where an unpublished run lands. Outside docs/, so the site's content globs
# never see it: a run made to test a pipeline change is a question about the
# pipeline, not a review of anybody's paper. Git-ignored.
RUNS = REPO / "runs"


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
# ran, pass or reject.
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
    "desk_screen.md",
    "panel_gaps.md",
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


def find_paper_dir(preprint: Preprint) -> Path | None:
    """The directory already holding this paper's reviews, if any.

    Matched on the preprint's identifier rather than the slug, for the reason
    :func:`find_prior_bundle` gives: the slug embeds the title and authors
    retitle between drafts, so a slug lookup misses its own earlier rounds for
    exactly the papers most likely to have them.
    """
    wanted = (preprint.identifier or preprint.doi or "").strip().lower()
    if not wanted:
        return None
    for prov_path in sorted(REVIEWS.glob("*/*/v*/provenance.json")):
        try:
            prov = json.loads(prov_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pp = prov.get("preprint") or {}
        got = str(pp.get("identifier") or pp.get("doi") or "").strip().lower()
        if got and got == wanted:
            return prov_path.parent.parent
    return None


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
    round 1. The panel would not notice — it reads every draft cold — but the
    editor's numbered required revisions are the whole lineage of a
    manuscript, and a round that cannot find them severs it.
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


def draft_number(preprint: Preprint) -> int:
    """Which draft of the paper this is, per the archive.

    The bundle directory is named after this, not after how many times we have
    run. `v3` means "our review of the authors' third draft" — a fact about
    the paper rather than a count of our activity.

    It is a fact we are given, not one we choose: `resolve()` always reports
    whatever the archive serves now, and refuses to go backwards. So the
    number only ever increases, and folder order can never disagree with the
    order the drafts were written in.
    """
    try:
        return max(1, int(str(preprint.version or "1").strip()))
    except (TypeError, ValueError):
        return 1


def existing_bundles(paper_dir: Path) -> dict[int, Path]:
    """Draft number -> bundle, for every review already published of a paper."""
    out: dict[int, Path] = {}
    for p in sorted(paper_dir.glob("v*")):
        if p.is_dir() and p.name[1:].isdigit():
            out[int(p.name[1:])] = p
    return out


@dataclass
class Plan:
    """Where this review goes, and what kind of run it therefore is."""

    dest: Path
    draft: int
    # The bundle this round rules against, or None for a first look. Set only
    # when an earlier draft was reviewed AND left a round record.
    prior: Path | None = None
    # True when we are overwriting our own earlier review of this same draft.
    replacing: bool = False

    @property
    def kind(self) -> str:
        if self.replacing:
            return "replacement"
        return "revision round" if self.prior else "first review"


def plan_review(
    paper_dir: Path, draft: int, replace: bool, *, publishing: bool = True
) -> Plan:
    """Decide where a review of ``draft`` belongs, or refuse.

    Three cases, and the caller declares none of them:

    - no review of this draft, none of any earlier draft  -> first look
    - no review of this draft, an earlier one exists      -> revision round
    - a review of this draft already exists              -> needs ``replace``

    The last case is the only one that can destroy anything, and it is
    deliberately narrow: it can only ever overwrite a review of the *same*
    draft. If the authors have posted a new version since, the draft number
    differs, so ``--replace`` silently becomes a new round rather than
    clobbering the record of a draft nobody can read any more.

    ``publishing`` is false for a run that lands in ``runs/``, and then that
    refusal does not apply: there is no bundle at stake, because the run
    cannot reach ``docs/reviews/`` at all. Enforcing it anyway made the
    already-reviewed papers the ones a pipeline change could never be tested
    against — which is backwards, since they are the ones with a published
    result to compare against.
    """
    published = existing_bundles(paper_dir)
    dest = paper_dir / f"v{draft}"

    if draft in published and publishing:
        if not replace:
            raise CommandError(
                f"Draft v{draft} of this paper has already been reviewed "
                f"({dest.relative_to(REPO) if dest.is_relative_to(REPO) else dest}). "
                "The archive still serves that draft, so there is nothing new "
                "to read. Pass --replace (or `/review replace`) to review it "
                "again and overwrite, or wait for the authors to post a new "
                "version."
            )
        return Plan(dest=dest, draft=draft, replacing=True)

    # A revision round rules against the newest earlier draft that left a
    # round record. Reviews published before round records existed cannot be
    # ruled against — there is nothing in them for a referee to check off — so
    # those fall through to a fresh look rather than a broken second round.
    prior = None
    for n in sorted((v for v in published if v < draft), reverse=True):
        if (published[n] / ROUND_RECORD).is_file():
            prior = published[n]
            break
    return Plan(dest=dest, draft=draft, prior=prior)


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
    """Read `/review` and its options out of a comment.

    Grammar, deliberately tiny:

        /review                          the configured panel (peerreview.toml)
        /review anthropic                the same, said out loud
        /review openrouter <model>       one model for every agent
        /review replace ...              redo a draft already reviewed

    There is one verb. Whether a run is a first look or a new round is not
    something an editor should have to declare: the archive says which draft
    exists, and a draft we have not reviewed is a new round. `/revise` is
    still accepted because editors have muscle memory for it, and does exactly
    what `/review` does.

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
    out: dict = {"replace": False, "provider": None, "model": None}
    if not parts or not parts[0].startswith("/"):
        return out

    command = parts[0].lower()
    if command not in ("/review", "/revise"):
        return out

    rest = parts[1:]
    if rest and rest[0].lower() == "replace":
        out["replace"] = True
        rest = rest[1:]
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


@dataclass
class RunTelemetry:
    """What the bus said about a run, beyond the documents it produced."""

    # node -> USD spent
    costs: dict[str, float] = field(default_factory=dict)
    # node -> [{tool, query, hits, error?}], in the order the lookups happened
    research: dict[str, list[dict]] = field(default_factory=dict)


@contextlib.contextmanager
def _telemetry_recorder(run_id: str):
    """Collect per-agent spend and research lookups off the observability bus.

    The pipeline emits a ``usage`` event per model call and a ``tool`` event
    per research lookup, each carrying its node name, but only ever persists
    the run's cost total. Registering a queue for this run collects both
    breakdowns without touching the pipeline.

    The research half is the one a reader needs. A referee that cites prior
    work is making a different claim depending on whether it searched for that
    work or recalled it, and no other published field separates those: the
    tool-using agents cost more whether or not a tool was ever called.

    Drained on a thread as events arrive, and echoed to stderr, because the
    alternative was unusable. Draining only in the ``finally`` block meant a
    run that hung produced no record of how far it got: the events existed,
    in memory, unreachable until the thing that was not finishing finished.
    A stalled review printed `plan` and then nothing for as long as you left
    it, and the only way to find the responsible node was to SIGINT the
    process and read the traceback. Now the last line of the log names the
    last node that completed.

    Never fails the review — an accounting problem must not lose a completed
    panel — so the thread swallows its own errors and is a daemon: if it dies,
    the run still writes its bundle, one line poorer.
    """
    from peerreviewagents.observability import clear_observer, register_observer

    telemetry = RunTelemetry()
    queue: Queue = Queue()
    register_observer(queue, run_id)
    done = threading.Event()
    started = time.monotonic()

    def record(event) -> None:
        node = event.node or "unattributed"
        # `node_start` without a matching `node_end` is the whole point: on a
        # stalled run the last unpaired arrow names the agent that hung, which
        # previously took a SIGINT and a traceback to learn.
        if event.kind == "node_start":
            print(f"  {time.monotonic() - started:6.0f}s  -> {node}", file=sys.stderr)
        elif event.kind == "node_end":
            spent = telemetry.costs.get(node)
            print(
                f"  {time.monotonic() - started:6.0f}s  ok {node:<28} "
                f"{event.text:>7}"
                + (f"  ${spent:.4f}" if spent else ""),
                file=sys.stderr,
            )
        elif event.kind == "usage" and event.cost_usd:
            telemetry.costs[node] = round(
                telemetry.costs.get(node, 0.0) + event.cost_usd, 6
            )
        elif event.kind == "tool":
            call = {
                "tool": event.tool_name,
                "query": event.tool_query,
                "hits": event.tool_hits,
            }
            if event.tool_error:
                call["error"] = event.tool_error
            telemetry.research.setdefault(node, []).append(call)

    def drain() -> None:
        while not done.is_set():
            try:
                record(queue.get(timeout=0.5))
            except Empty:
                continue
            except Exception as exc:  # noqa: BLE001
                print(f"warning: run telemetry unavailable ({exc})", file=sys.stderr)
                return

    pump = threading.Thread(target=drain, name="telemetry", daemon=True)
    pump.start()
    try:
        yield telemetry
    finally:
        clear_observer(run_id)
        done.set()
        pump.join(timeout=2)
        # Anything the pump had not reached yet. The queue is unbounded and
        # the producer has stopped, so this terminates.
        try:
            while True:
                try:
                    record(queue.get_nowait())
                except Empty:
                    break
        except Exception as exc:  # noqa: BLE001
            print(f"warning: run telemetry unavailable ({exc})", file=sys.stderr)


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
    research: dict[str, list[dict]] | None = None,
) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    cost_by_node = cost_by_node or {}
    revision = revision or {}
    research = research or {}

    # Every document is copied, including the ones a desk reject makes
    # byte-identical (it sets decision_letter and desk_screen to the same
    # body). A reader following a direct link should find the file; the site
    # is what decides not to show one text under two headings.
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
        # What the referees looked up, and what came back. The site claims
        # novelty and literature search live rather than working from recall;
        # this is the only thing published that can substantiate that. An
        # entry carrying `error` and no tool name is a referee that fell back
        # to reviewing without research tools.
        "research_by_node": dict(sorted(research.items())) if research else {},
        "errors": state.get("errors", []),
        "preprint": preprint.to_dict(),
    }
    # provenance.json is the whole published record of the run. The site
    # renders every page from it, so this script writes data and no markup —
    # which is why a change to how a review *looks* no longer means editing
    # the program that produces reviews.
    (dest / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    # Where the manuscript comes from. Exactly one, and --rerun-of belongs
    # here rather than beside --revision-of: it names the preprint as much as
    # it names a prior round, because the whole point is to review the
    # identical draft rather than whatever the URL resolves to today.
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
    # What kind of run this is used to be three flags. It is now a consequence
    # of which draft the archive serves: a draft we have not reviewed is a new
    # round, and one we have is a re-review that has to say so.
    ap.add_argument(
        "--replace",
        action="store_true",
        help="re-review a draft that already has a review, overwriting it. "
             "Use after changing prompts, models or config. Cannot touch a "
             "review of a different draft: if the authors have posted a new "
             "version since, this writes a new round instead.",
    )
    ap.add_argument(
        "--publish",
        action="store_true",
        help="write into docs/reviews/, where the site publishes it. Off by "
             "default so a run made to test a pipeline change does not become "
             "a published review; those land in runs/ and are printed for "
             "comparison. The workflow passes this; local runs usually should "
             "not.",
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
        args.provider = args.provider or selected["provider"]
        args.model = args.model or selected["model"]
        args.replace = args.replace or selected["replace"]

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
        # Reports the plan too. --dry-run exists to check a URL is worth
        # spending on, and "we reviewed this draft already" is exactly that
        # kind of answer — worth getting before the panel, not after.
        print(json.dumps(preprint.to_dict(), indent=2))
        try:
            plan = plan_review(
                find_paper_dir(preprint)
                or REVIEWS
                / (preprint.published or dt.date.today().isoformat())[:4]
                / paper_slug(preprint, preprint.title or preprint.identifier),
                draft_number(preprint),
                args.replace,
                # Predict what the real run with these same flags will do. A
                # dry run that refuses where the run itself would proceed is
                # worse than no dry run.
                publishing=args.publish,
            )
        except CommandError as exc:
            print(f"{exc}", file=sys.stderr)
            return 4
        print(f"plan      {plan.kind}: draft v{plan.draft}", file=sys.stderr)
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

    # Decided here, before a single model call. Refusing a draft we have
    # already reviewed is worth nothing after the panel has run and the bill
    # has been paid — and the destination is knowable the moment the archive
    # tells us which draft it serves.
    #
    # The paper's directory is found by identifier where possible, never by
    # slug alone: the slug embeds the title, authors retitle between versions
    # routinely, and a slug lookup would open a second directory for the same
    # paper and split its history in two.
    year = (preprint.published or dt.date.today().isoformat())[:4]
    slug = paper_slug(preprint, preprint.title or preprint.identifier)
    known = find_paper_dir(preprint)
    paper_dir = known or (REVIEWS / year / slug)
    try:
        plan = plan_review(
            paper_dir, draft_number(preprint), args.replace, publishing=args.publish
        )
    except CommandError as exc:
        print(f"{exc}", file=sys.stderr)
        if out := os.environ.get("GITHUB_OUTPUT"):
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("already_reviewed=true\n")
                fh.write(f"already_reviewed_reason={' '.join(str(exc).split())}\n")
        return 4
    print(
        f"plan      {plan.kind}: draft v{plan.draft}"
        + (f", ruling against {plan.prior.name}" if plan.prior else ""),
        file=sys.stderr,
    )

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
    prior_bundle = plan.prior
    if prior_bundle is not None:
        overrides["revision_of"] = str(prior_bundle)

    config = get_config(**overrides)

    if plan.replacing:
        # Round 1, and no `revision_of` in the config. Both are the point.
        # `revision_of` hands the editor the earlier round's decision, score
        # and required-revisions list as its reference point, and a re-review
        # that inherits the verdict it exists to test tests nothing.
        old = _rerun_provenance(str(plan.dest)) or {}
        revision = {
            "round": 1,
            "kind": "rerun",
            "replaced": plan.dest.name,
            "prior_decision": str(old.get("decision") or ""),
            "prior_mean_score": old.get("mean_score"),
            "prior_pipeline_sha": (old.get("pipeline") or {}).get("sha") or "",
            "prior_reviewed_at": str(old.get("generated_at") or "")[:10],
        }
        print(
            f"replacing {plan.dest.name} "
            f"({revision['prior_decision'] or 'no decision'}, "
            f"mean {revision['prior_mean_score']})",
            file=sys.stderr,
        )
        # The draft number matched, so the archive says this is the same
        # version. Confirm the text as well: a server that quietly reposted
        # different content under one version number would otherwise let a
        # replacement claim to be a like-for-like comparison when it is not.
        if old and not _same_draft(pdf, old, config):
            return 1

    if prior_bundle is not None:
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
        print(
            f"revision  round {revision['round']} of {prior_bundle.name}"
            f" — {revision['prior_required_revisions']} required revision(s)"
            " carried in",
            file=sys.stderr,
        )

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
        with _telemetry_recorder(graph.run_id) as telemetry:
            # The PDF, not a conversion of it. The pipeline converts it to
            # markdown internally; handing it a .md instead would record a
            # converter that did not read this file, and would change the
            # manuscript cache key that the next round re-derives to recover
            # this draft.
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
    version = plan.draft

    # Where it lands is decided by --publish, not by what kind of run it was.
    # A run made to see what a prompt change did is a question about the
    # pipeline, and answering it should not add a review to a stranger's paper
    # — which is exactly how this corpus acquired four reviews of one draft.
    if args.publish:
        dest = plan.dest
        if plan.replacing and dest.exists():
            # Removed rather than written over: the old bundle's specialist
            # reports would otherwise survive alongside the new ones and be
            # read as part of this review.
            shutil.rmtree(dest)
    else:
        dest = RUNS / f"{slug}-v{version}-{dt.datetime.now():%Y%m%d-%H%M%S}"

    write_bundle(
        preprint, state, run_dir, dest,
        args.submission_id, args.submitter, telemetry.costs, revision,
        submitter_is_author=args.submitter_is_author,
        ingest=state.get("ingest"),
        research=telemetry.research,
    )
    rel = dest.relative_to(REPO)
    desk_rejected = bool(state.get("desk_rejected"))
    print(f"bundle    {rel}", file=sys.stderr)
    print(f"decision  {decision}{' (desk reject)' if desk_rejected else ''}", file=sys.stderr)
    for node, spend in sorted(telemetry.costs.items(), key=lambda kv: -kv[1]):
        print(f"  cost    {node:<28} ${spend:.4f}", file=sys.stderr)
    for node, calls in sorted(telemetry.research.items()):
        lost = sum(1 for c in calls if c.get("error"))
        hits = sum(c.get("hits", 0) for c in calls)
        note = f" ({lost} failed)" if lost else ""
        print(f"  search  {node:<28} {len(calls)} call(s), {hits} hit(s){note}", file=sys.stderr)

    # Flattened for the same reason as unreadable_reason above: a newline in a
    # `key=value` output line silently truncates the value and leaves the
    # remainder parsed as another key.
    title = " ".join((preprint.title or preprint.identifier or url).split())

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
            fh.write(f"title={title}\n")
            fh.write(f"cost={state.get('total_cost') or 0}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
