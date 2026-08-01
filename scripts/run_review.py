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
from pathlib import Path
from queue import Empty, Queue

sys.path.insert(0, str(Path(__file__).parent))

from fetch_preprint import Preprint, download, extract_url, resolve  # noqa: E402

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
) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    cost_by_node = cost_by_node or {}

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
        )
    )


def render_landing(
    preprint: Preprint,
    provenance: dict,
    title: str,
    copied: list[tuple[str, str]],
    reviewer_files: list[Path],
    audit_files: list[Path],
    submission_id: str,
    submitter: str,
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
    if provenance.get("desk_rejected"):
        # Surfaced in frontmatter so the index can mark these distinctly
        # rather than filing them next to reasoned panel rejections.
        fm.append("desk_rejected: true")
    fm.append("---")

    rows = [
        f"| Preprint | [{preprint.url}]({preprint.url}) |",
        f"| Source | {preprint.source} |",
    ]
    if preprint.doi:
        rows.append(f"| DOI | `{preprint.doi}` |")
    if preprint.authors:
        rows.append(f"| Authors | {', '.join(preprint.authors)} |")
    if preprint.published:
        rows.append(f"| Posted | {preprint.published} |")
    rows.append(f"| Reviewed | {provenance['generated_at'][:10]} |")
    if provenance.get("mean_score") is not None:
        rows.append(f"| Mean panel score | {provenance['mean_score']} / 5 |")
    if submission_id:
        rows.append(f"| Submission | [#{submission_id}]({REPO_URL}/issues/{submission_id}) |")
    if submitter:
        rows.append(f"| Submitted by | [@{submitter}](https://github.com/{submitter}) |")

    desk_rejected = provenance.get("desk_rejected")
    # "Panel recommendation" would be a false claim on a desk reject: no panel
    # convened. Say what actually happened, and why the page is short.
    headline = (
        f"**Desk rejected — {VERDICT_LABEL.get(decision, decision)}**"
        if desk_rejected
        else f"**Panel recommendation: {VERDICT_LABEL.get(decision, decision)}**"
    )

    body = [
        "\n".join(fm),
        "",
        f"# {title}",
        "",
        headline,
        "",
    ]
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
        body += ["## Abstract", "", f"> {preprint.abstract}", ""]

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
    return "\n".join(body)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="preprint URL")
    src.add_argument("--issue-body", help="free text to scrape a URL out of")
    ap.add_argument("--submission-id", default="", help="submission issue number")
    ap.add_argument("--submitter", default="", help="GitHub login of the submitter")
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
    ap.add_argument("--dry-run", action="store_true", help="resolve + download only")
    args = ap.parse_args()

    url = args.url or extract_url(args.issue_body)
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

    config = get_config(**overrides)

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
    slug = slugify(title) or slugify(preprint.identifier) or "submission"
    dest = REVIEWS / year / slug

    write_bundle(
        preprint, state, run_dir, dest,
        args.submission_id, args.submitter, cost_by_node,
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
            fh.write(f"title={title}\n")
            fh.write(f"cost={state.get('total_cost') or 0}\n")

    shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
