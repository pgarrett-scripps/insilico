"""Fetch a preprint, run the referee panel over it, and write a review bundle.

    python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
    python scripts/run_review.py --issue-body "$ISSUE_BODY" --submission-id 12

Output lands in ``docs/reviews/<year>/<slug>/`` and is what the bot commits.
``--dry-run`` resolves and downloads without calling a model, so you can check a
URL is reviewable before spending anything.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

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
    ("meta_review.md", "Area chair synthesis"),
    ("author_rebuttal.md", "Simulated author rebuttal"),
    ("debate_transcript.md", "Advocate / skeptic debate"),
    ("journal_recommendations.md", "Venue suggestions"),
]

# Model tags map to groups of agents; spell them out for readers who haven't
# read the pipeline's config docs.
_TAG_LABEL = {
    "reviewer": "specialist reviewers (×8)",
    "audit": "editorial audits (×2)",
    "debate": "advocate / skeptic",
    "screen": "desk screen",
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


def write_bundle(
    preprint: Preprint,
    state: dict,
    run_dir: Path,
    dest: Path,
    submission_id: str,
    submitter: str,
) -> None:
    dest.mkdir(parents=True, exist_ok=True)

    copied: list[tuple[str, str]] = []
    for name, label in BUNDLE_ORDER:
        src = run_dir / name
        if src.exists():
            shutil.copy2(src, dest / name)
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
        "panel": scores,
        "mean_score": round(sum(numeric) / len(numeric), 2) if numeric else None,
        "total_cost_usd": state.get("total_cost"),
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

    body = [
        "\n".join(fm),
        "",
        f"# {title}",
        "",
        f"**Panel recommendation: {VERDICT_LABEL.get(decision, decision)}**",
        "",
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

    state = PeerReviewGraph(config).review(str(pdf))

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

    write_bundle(preprint, state, run_dir, dest, args.submission_id, args.submitter)
    rel = dest.relative_to(REPO)
    print(f"bundle    {rel}", file=sys.stderr)
    print(f"decision  {decision}", file=sys.stderr)

    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as fh:
            fh.write(f"decision={decision}\n")
            fh.write(f"slug={slug}\n")
            fh.write(f"year={year}\n")
            fh.write(f"path={rel}\n")
            fh.write(f"title={title}\n")
            fh.write(f"cost={state.get('total_cost') or 0}\n")

    shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
