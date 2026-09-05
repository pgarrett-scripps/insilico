"""Fetch a preprint, run the referee panel over it, and write a review bundle.

    python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
    python scripts/run_review.py --issue-body "$ISSUE_BODY" --submission-id 12

Output lands in ``docs/reviews/<year>/<slug>/v<N>/r<M>/`` and is what the bot
commits.
``--dry-run`` resolves and downloads without calling a model, so you can check a
URL is reviewable before spending anything.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fetch_preprint import (  # noqa: E402
    download,
    extract_authorship,
    extract_url,
    resolve,
)
from manuscript_source import (  # noqa: E402
    ManuscriptSourceUnreadable,
    OfficialFullTextUnavailable,
    select_manuscript_source,
)
from review_bundle import BUNDLE_FILES, panel_scores, write_bundle  # noqa: E402,F401
from review_commands import CommandError, parse_command  # noqa: E402
from review_paths import REPO, REVIEWS, ROUND_RECORD, RUNS  # noqa: E402,F401
from review_plan import (  # noqa: E402,F401
    Plan,
    _rerun_provenance,
    _same_draft,
    baseline_eligible,
    draft_matches,
    draft_number,
    existing_bundles,
    find_paper_dir,
    latest_baseline,
    paper_slug,
    plan_review,
    slugify,
)
from review_provenance import (  # noqa: E402,F401
    configuration_record,
    insilico_version,
    journal_profile_record,
    pipeline_version,
)
from review_telemetry import RunTelemetry, _telemetry_recorder  # noqa: E402,F401


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

VERDICT_LABEL = {
    "accept": "Accept",
    "minor": "Minor revision",
    "major": "Major revision",
    "reject": "Reject",
}


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
        help="re-review a draft that already has a review as a new immutable attempt. "
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

    if args.dry_run:
        pdf = download(preprint, workdir)
        print(f"pdf       {pdf} ({pdf.stat().st_size // 1024} KiB)", file=sys.stderr)
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
        print(
            f"plan      {plan.kind}: manuscript v{plan.draft}, review r{plan.attempt}",
            file=sys.stderr,
        )
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
        f"plan      {plan.kind}: manuscript v{plan.draft}, review r{plan.attempt}"
        + (
            f", ruling against {plan.prior.relative_to(paper_dir)}"
            if plan.prior else ""
        ),
        file=sys.stderr,
    )

    from peerreviewagents.agents.editor.desk_screen import screen_mode
    from peerreviewagents.default_config import get_config
    from peerreviewagents.graph.review_graph import PeerReviewGraph
    from peerreviewagents.ingest.loader import ManuscriptUnreadable
    from peerreviewagents.reports import write_reports

    # Only pass what was explicitly asked for. Anything omitted falls through
    # to ./peerreview.toml, which is where the [models.*] tables live.
    overrides = {
        "output_dir": str(workdir / "reports"),
        # Every reviewer gets the complete selected text. Section maps remain
        # navigation metadata and never decide which prose reaches the model.
        "manuscript_char_budget": None,
        # Survives ordinary local reruns and records each successful agent
        # atomically. The key includes manuscript content + semantic config,
        # so unrelated papers or model settings never share outputs.
        "checkpoint_dir": str(RUNS / ".checkpoints"),
        # `replace` is the legacy command for a fresh review of the same draft.
        # Resuming would replay the recorded panel byte-for-byte, so a new
        # immutable attempt always samples fresh.
        "resume": not bool(plan.previous_attempt),
    }
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

    pdf: Path | None = None
    try:
        manuscript_source = select_manuscript_source(preprint, None, workdir, config)
    except OfficialFullTextUnavailable as structured_failure:
        try:
            pdf = download(preprint, workdir)
        except ValueError as exc:
            message = f"official full text and PDF fetch failed: {exc}"
            print(f"unreadable: {message}", file=sys.stderr)
            if out := os.environ.get("GITHUB_OUTPUT"):
                reason = " ".join(message.split())
                with open(out, "a", encoding="utf-8") as fh:
                    fh.write("unreadable=true\n")
                    fh.write(f"unreadable_reason={reason}\n")
            return 3
        print(f"pdf       {pdf} ({pdf.stat().st_size // 1024} KiB)", file=sys.stderr)
        try:
            manuscript_source = select_manuscript_source(
                preprint,
                pdf,
                workdir,
                config,
                try_structured=False,
                previous_attempts=structured_failure.attempts,
            )
        except ManuscriptSourceUnreadable as exc:
            print(f"unreadable: {exc}", file=sys.stderr)
            if out := os.environ.get("GITHUB_OUTPUT"):
                reason = " ".join(str(exc).split())
                with open(out, "a", encoding="utf-8") as fh:
                    fh.write("unreadable=true\n")
                    fh.write(f"unreadable_reason={reason}\n")
            return 3
    except ManuscriptSourceUnreadable as exc:
        print(f"unreadable: {exc}", file=sys.stderr)
        if out := os.environ.get("GITHUB_OUTPUT"):
            reason = " ".join(str(exc).split())
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("unreadable=true\n")
                fh.write(f"unreadable_reason={reason}\n")
        return 3
    manuscript = manuscript_source.path
    print(
        f"text      {manuscript_source.kind}: {manuscript_source.tool}",
        file=sys.stderr,
    )

    if plan.previous_attempt is not None:
        # Round 1, and no `revision_of` in the config. Both are the point.
        # `revision_of` hands the editor the earlier round's decision, score
        # and required-revisions list as its reference point, and a re-review
        # that inherits the verdict it exists to test tests nothing.
        old = _rerun_provenance(str(plan.previous_attempt)) or {}
        revision = {
            "round": 1,
            "kind": "rerun",
            "previous_attempt": str(plan.previous_attempt.relative_to(paper_dir)),
            "prior_decision": str(old.get("decision") or ""),
            "prior_mean_score": old.get("mean_score"),
            "prior_pipeline_sha": (old.get("pipeline") or {}).get("sha") or "",
            "prior_reviewed_at": str(old.get("generated_at") or "")[:10],
        }
        print(
            f"re-reviewing {plan.previous_attempt.relative_to(paper_dir)} "
            f"({revision['prior_decision'] or 'no decision'}, "
            f"mean {revision['prior_mean_score']})",
            file=sys.stderr,
        )
        # The draft number matched, so the archive says this is the same
        # version. Confirm the text as well: a server that quietly reposted
        # different content under one version number would otherwise let a
        # re-review claim to be a like-for-like comparison when it is not.
        if old:
            prior_source = ((old.get("ingest") or {}).get("source") or {}).get("kind")
            if not prior_source and pdf is None:
                pdf = download(preprint, workdir)
            check_path = manuscript if prior_source else pdf
            assert check_path is not None
            if not _same_draft(check_path, old, config):
                return 1

    if prior_bundle is not None:
        prior = json.loads((prior_bundle / ROUND_RECORD).read_text(encoding="utf-8"))
        prior_round = int(prior.get("round", 1))
        revision = {
            "round": prior_round + 1,
            "prior_bundle": str(prior_bundle.relative_to(paper_dir)),
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
            f"revision  round {revision['round']} of "
            f"{prior_bundle.relative_to(paper_dir)}"
            f", {revision['prior_required_revisions']} required revision(s)"
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
    state: dict = {}
    try:
        with _telemetry_recorder(graph.run_id) as telemetry:
            # The selected representation has already passed an identity and
            # completeness check against archive metadata.
            # Keep the latest accumulated snapshot. If a later graph node
            # fails, the completed reviewer/auditor results and their exact
            # errors remain available instead of disappearing with invoke().
            for _node, snapshot in graph.stream(str(manuscript)):
                state = snapshot
    except ManuscriptUnreadable as exc:
        # No bundle, no verdict, nothing published. This final guard catches a
        # selected representation that the pipeline itself still cannot read.
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

    source_record = manuscript_source.record()
    ingest = dict(state.get("ingest") or {})
    state["ingest"] = ingest
    ingest["source"] = source_record
    ingest["tool"] = manuscript_source.tool
    ingest["source_format"] = manuscript_source.kind
    if manuscript_source.kind in {"jats", "html"}:
        ingest["section_source"] = f"official_{manuscript_source.kind}"
    else:
        ingest["section_source"] = "none"

    # A valid-looking editor verdict is not enough. Older PRA versions could
    # continue after a reviewer failed and issue a decision from seven of the
    # requested eight specialists. The graph now stops before synthesis, and
    # this independent boundary check prevents a degraded or older graph from
    # ever becoming a publishable bundle.
    if not state.get("desk_rejected") and not state.get("panel_complete"):
        errors = "; ".join(state.get("errors") or []) or "required panel did not complete"
        print(f"review failed: {errors}", file=sys.stderr)
        return 1

    if not state.get("desk_rejected") and not state.get("publication_ready"):
        errors = "; ".join(state.get("errors") or []) or str(
            state.get("run_status") or "review never became publishable"
        )
        print(f"review failed: {errors}", file=sys.stderr)
        return 1

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
    else:
        dest = RUNS / f"{slug}-v{version}-{dt.datetime.now():%Y%m%d-%H%M%S}"

    graded = bool(config.get("models"))
    if plan.previous_attempt:
        review_kind = "editorial_rereview" if graded else "experiment"
    elif plan.prior:
        review_kind = "revision"
    else:
        review_kind = "initial" if graded else "experiment"
    review_record = {
        "id": str(dest.relative_to(REPO)),
        "manuscript_version": plan.draft,
        "attempt": plan.attempt,
        "kind": review_kind,
        "baseline_eligible": graded,
        "lifecycle": "active",
        "previous_review_id": (
            str(plan.previous_attempt.relative_to(REPO))
            if plan.previous_attempt else ""
        ),
        "revision_of": str(plan.prior.relative_to(REPO)) if plan.prior else "",
    }

    write_bundle(
        preprint, state, run_dir, dest,
        args.submission_id, args.submitter, telemetry.costs, revision,
        submitter_is_author=args.submitter_is_author,
        ingest=state.get("ingest"),
        research=telemetry.research,
        config=config,
        review=review_record,
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
