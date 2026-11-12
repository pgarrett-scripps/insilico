"""Turn a local PeerReviewAgents run into a publishable review bundle.

The hosted panel is gone. A review is now produced on the editor's own machine,
inside one Claude Code session, and arrives here as a pull request. No paid API
key exists anywhere in that path, and nothing in this file can create one.

The work splits in two, deliberately:

``prepare`` resolves the paper to a permanent identity, fetches the exact bytes
of that revision, hashes them, and decides where a review of it would belong. It
spends nothing and talks to no model.

``publish`` reads a finished engine run and writes the bundle: the documents, the
provenance record, and the manifest. It spends nothing either.

Between the two, the skill runs ``peerreview review``, which starts a Claude Code
session on the plugin that ships inside the engine. That is the only step that
costs anything, and keeping it outside this file means no command here can start
a review by accident.

One thing this module will not do is adopt a verdict. The engine's editor agent
records an advisory judgement, a reading of significance and of how strong the
evidence is, and it recommends no accept or reject. So ``--decision`` is the
editor's, typed after reading the run, and the provenance record says so in as
many words.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib
import importlib.metadata
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_preprint import Preprint, download, resolve  # noqa: E402
from review_paths import REPO, REVIEWS, ROUND_RECORD, RUNS  # noqa: E402
from review_plan import (  # noqa: E402
    CommandError,
    draft_number,
    find_paper_dir,
    paper_slug,
    plan_review,
)
from review_provenance import insilico_version, pipeline_version  # noqa: E402

ENGINE_PACKAGE = "peerreviewagents"
STARTER_MODULE = "peerreviewagents.plugin.starter"
PROVENANCE_SCHEMA = 4
GENERATOR_KIND = "local-claude-code-plugin"
TRANSPORT_PROVIDER = "claude-code"
DECISIONS = ("accept", "minor", "major", "reject")

# Where the engine puts things under the folder passed to `peerreview review`.
# The run lands in `review/` and the imported manuscript in `manuscript/`, so
# `--run` may name either the output folder or the review folder inside it, and
# `--workspace` has a sibling to default to.
REVIEW_DIRECTORY = "review"
MANUSCRIPT_DIRECTORY = "manuscript"

# The six specialist tracks the plugin ships, each writing one `audit_<track>.md`
# report into the run. Named here so a bundle can say which reports are missing
# rather than quietly publishing fewer.
SPECIALIST_TRACKS = (
    "stats",
    "figures-tables",
    "methods-reporting",
    "citations",
    "consistency",
    "field",
)

# Carried in every version 4 record. It is the one claim in the file that no
# hash can back, so it is stated plainly rather than implied by a flag.
ATTESTATION = (
    "This review was generated locally in a Claude Code session on a "
    "subscription, with no paid API key in the path. The named editor read the "
    "run and chose the decision before the review was merged, and merging is "
    "what publishes it."
)

# Written instead when the operator says nobody has read the run yet. Such a
# record cannot be published: the guard is in cmd_publish, and the statement
# exists so that a rehearsal bundle on disk cannot be mistaken for a reviewed
# one if somebody copies it by hand.
UNREAD_STATEMENT = (
    "This review was generated locally in a Claude Code session on a "
    "subscription. No editor has attested to reading the run, so it is a "
    "rehearsal and must not be published."
)

SEVERITY_ORDER = {"major": 0, "moderate": 1, "minor": 2}
REQUIRED_SEVERITIES = ("major", "moderate")

# The one state a review may be published from. The engine carries a second
# finished state, `complete-without-findings`, and that is not a review here.
# The server writes it in exactly one case: every finding the reviewers raised
# failed the evidence guards and was quarantined.
#
# A run that read the manuscript end to end and genuinely raised nothing is
# `complete` with the guard status `clean`, and that publishes with an empty
# findings list, which is the honest record of a manuscript found sound. The
# quarantined case is the opposite claim, a review endorsing none of its own
# work, and publishing it under the same words would tell authors their paper
# drew no findings when every finding was thrown away.
FINISHED_STATUSES = ("complete",)
ALL_FINDINGS_QUARANTINED = "all-findings-quarantined"
WITHOUT_FINDINGS_STATUS = "complete-without-findings"

# insilico publishes Claude Code runs only. Every claim a bundle makes about how
# the review was paid for is a claim about a Claude subscription, and the only
# transport this path can describe is the one the plugin runs on.
PUBLISHABLE_PROVIDERS = ("claude-code",)

# The route this pipeline bills on, named in every published record. The engine
# has no billing policy of its own: it runs inside whatever subscription the
# Claude CLI is signed in to, and spends nothing else.
BILLING_POLICY = "claude-subscription-v1"

# How a published record says the transport claim was checked. There is no
# publish-time probe any more, because the engine exposes no authentication
# reading in 0.9. What backs the claim is the run's own start-up probe: the
# engine refuses to spend a run until a Claude Code session has started, loaded
# the plugin and connected the `peerreview` MCP server, and it records what that
# probe saw. A session that started had a login, and the starter removes
# ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN from the environment it hands the
# session, so no key in the operator's shell can have paid for it.
VERIFIED_BY = "run_startup_probe"
MCP_SERVER_NAME = "peerreview"

# The manifest key holding the workflow the plugin ran. Hashed on its own as
# well as inside the plugin fingerprint, because it is the one file that decides
# which agents ran in what order.
WORKFLOW_FILE = "plugin/workflows/review.js"
PLUGIN_PREFIX = "plugin/"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def maybe_json(path: Path) -> dict:
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        value = read_json(path)
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _list(value: object) -> list:
    return value if isinstance(value, list) else []


def engine_record() -> dict:
    """Which release of the engine is installed here.

    The version comes from the installed distribution. The engine exposes no
    `__version__` and no API version of its own in 0.9, so there is one source
    and a missing one is a refusal rather than an empty string.
    """
    try:
        version = importlib.metadata.version(ENGINE_PACKAGE)
    except importlib.metadata.PackageNotFoundError as exc:
        raise CommandError(
            "PeerReviewAgents is not installed here, so the record cannot name "
            "the engine that produced the review. Install it, or run this with "
            "the virtual environment the review ran in."
        ) from exc
    return {"name": ENGINE_PACKAGE, "version": str(version)}


def installed_code_manifest() -> dict:
    """Hash the installed plugin and engine the way a run records them.

    The plugin server writes `{relative path: sha256}` over three trees when a
    run starts: the plugin it loaded, the engine's Python modules, and the
    plugin server's own modules. This reproduces that mapping from the installed
    package, so a run's recorded bytes and the installed bytes can be compared.
    A mismatch is not an error: a run made from a checkout of the plugin is a
    real run, and the record says which it was.
    """
    try:
        starter = importlib.import_module(STARTER_MODULE)
    except ImportError as exc:
        raise CommandError(
            f"{STARTER_MODULE} is not importable, so the installed plugin "
            "cannot be fingerprinted. Install PeerReviewAgents 0.9.0 or newer."
        ) from exc
    here = Path(starter.__file__).resolve().parent
    plugin_root = Path(starter.plugin_dir()).resolve()
    files: dict[str, str] = {}
    for path in sorted(plugin_root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            files[PLUGIN_PREFIX + path.relative_to(plugin_root).as_posix()] = digest(
                path.read_bytes()
            )
    for path in sorted((here.parent / "engine").glob("*.py")):
        files["engine/" + path.name] = digest(path.read_bytes())
    for path in sorted(here.glob("*.py")):
        files["plugin-python/" + path.name] = digest(path.read_bytes())
    if not files:
        raise CommandError(f"The engine at {here} has no source files to fingerprint")
    return files


def code_fingerprint(code: dict, source: str, *, prefix: str = "") -> dict:
    """Hash a recorded source manifest, or one prefixed subset of it.

    Hashing the canonical form of the mapping gives one comparable number, so a
    run's recorded bytes and the installed bytes can be checked against each
    other without publishing a file list per review.
    """
    subset = {
        key: value
        for key, value in sorted(_dict(code).items())
        if not prefix or str(key).startswith(prefix)
    }
    if not subset:
        raise CommandError(
            "A source manifest was recorded with no files in it"
            + (f" under {prefix}" if prefix else "")
        )
    return {
        "algorithm": "sha256",
        "file_count": len(subset),
        "sha256": digest(canonical(subset)),
        "source": source,
    }


def plugin_record(code: dict, run: dict) -> dict:
    """The plugin that ran, identified by its own bytes rather than its name.

    Two runs can both say `plugin-two-track-v1` and have run different agent
    files. The plugin fingerprint settles which, and the workflow hash settles
    which agents ran in what order, since `workflows/review.js` is the file that
    decides that.
    """
    fingerprint = code_fingerprint(code, "run_manifest", prefix=PLUGIN_PREFIX)
    workflow = str(_dict(code).get(WORKFLOW_FILE) or "")
    if not workflow:
        raise CommandError(
            f"The run manifest records no {WORKFLOW_FILE}, so the record cannot "
            "say which workflow produced the review. The plugin server writes "
            "the hash of every plugin file it loaded into manifest.json."
        )
    workflow_version = str(run.get("workflow_version") or "")
    if not workflow_version:
        raise CommandError(
            "The run records no workflow version, so the record cannot say "
            "which workflow produced the review."
        )
    return {
        "fingerprint": fingerprint,
        "workflow_sha256": workflow,
        "workflow_version": workflow_version,
        "finding_schema_version": str(run.get("finding_schema_version") or ""),
    }


def transport_record(*, provider: str, runtime: dict, startup: dict) -> dict:
    """Which harness ran the agents, taken from the run rather than probed.

    `provider` is the transport the run itself recorded, so the record cannot
    name one transport while the run used another. Anything outside
    `PUBLISHABLE_PROVIDERS` is refused here, before any record is written.

    The claim this makes is narrow on purpose. It is not that an account of a
    particular kind paid for the run: the engine reads no authentication status
    in 0.9 and this file will not guess one. It is that a real Claude Code
    session started, loaded the engine's plugin and connected its MCP server,
    which the engine proves before it spends anything and records in
    `startup.json`, and that the session ran with no API key in its environment,
    which the starter guarantees by removing ANTHROPIC_API_KEY and
    ANTHROPIC_AUTH_TOKEN from the environment it hands the session.

    Pure, so the refusals can be tested without a CLI and without a model.
    """
    provider = str(provider or "")
    if provider not in PUBLISHABLE_PROVIDERS:
        raise CommandError(
            f"This run used the {provider or 'unrecorded'} transport, and this "
            f"path records {', '.join(PUBLISHABLE_PROVIDERS)} runs only. Review "
            "the paper again on Claude Code, or publish it by another route."
        )
    startup = _dict(startup)
    if not startup:
        raise CommandError(
            "This run recorded no startup.json, so there is no evidence a Claude "
            "Code session ever started. The engine writes it before it spends "
            "anything. Point --run at the folder `peerreview review` wrote."
        )
    problems = [str(p) for p in _list(startup.get("problems")) if str(p).strip()]
    if problems:
        raise CommandError(
            "The run's start-up probe reported "
            f"{'; '.join(problems)}. A run that could not load the plugin "
            "cannot be published as a review the plugin produced."
        )
    probe = _dict(startup.get("probe"))
    connected = [
        server
        for server in _list(probe.get("mcp_servers"))
        if MCP_SERVER_NAME in str(_dict(server).get("name") or "")
        and str(_dict(server).get("status") or "") == "connected"
    ]
    if not connected:
        raise CommandError(
            f"The run's start-up probe saw no connected {MCP_SERVER_NAME} MCP "
            "server, so nothing proves the agents had the engine's tools. Re-run "
            "the review and publish that run."
        )
    return {
        "provider": provider,
        "executable": "claude",
        "version": str(_dict(runtime).get("claude_code_version") or "") or None,
        "billing_policy": BILLING_POLICY,
        "login_verified": True,
        "verified_by": VERIFIED_BY,
        "verified_at": str(startup.get("at") or "") or None,
        # A constant here and a constant in the schema. This path cannot reach a
        # paid key, so the field is a statement about the design rather than a
        # measurement, and a record needing it to be true is not a local review
        # and has no business in this shape.
        "paid_api_key_used": False,
    }


def resolve_review_dir(run: Path) -> Path:
    """The folder holding protocol.json, whichever of the two was passed.

    `peerreview review <pdf> <out>` writes the review into `<out>/review` and
    the imported manuscript into `<out>/manuscript`. Both paths are useful to
    type, so both are accepted and resolved here rather than at four call sites.
    """
    run = Path(run).resolve()
    if (run / REVIEW_DIRECTORY / "protocol.json").is_file():
        return run / REVIEW_DIRECTORY
    return run


def resolve_workspace(review_dir: Path, flag: str) -> Path:
    """The imported manuscript workspace, named or found beside the run.

    The engine writes it as a sibling of the review folder, so the default is
    the one the run actually used. It stays overridable because the guard it
    feeds, `bind_run_to_input`, is the only thing tying a run to the paper that
    was prepared.
    """
    if flag:
        return Path(flag).resolve()
    sibling = Path(review_dir).resolve().parent / MANUSCRIPT_DIRECTORY
    if (sibling / "paper.json").is_file():
        return sibling
    raise CommandError(
        f"No manuscript workspace at {sibling}, so this run cannot be tied to "
        "the paper that was prepared. Pass --workspace with the folder holding "
        "paper.json."
    )


def agent_rows(protocol: dict, package: dict, runtime: dict) -> list[dict]:
    """One row per agent that ran, from the three files that each know part of it.

    `protocol.json` holds the role, the track and the tool allowance each slot
    was given. `editor-package.json` holds what each reviewer delivered.
    `runtime.json` holds what the harness observed, including the model the slot
    actually ran on.

    The harness emits a placeholder row for an agent it has not named yet, with
    a label and nothing else. Those are skipped: an `agent-3` with no model, no
    state and no usage is not an agent that ran, and publishing five of them
    would overstate the panel.
    """
    rows: dict[str, dict] = {}
    for slot, agent in sorted(_dict(protocol.get("agents")).items()):
        agent = _dict(agent)
        rows[str(slot)] = {
            "slot": str(slot),
            "role": str(agent.get("role") or "") or None,
            "track": str(agent.get("track") or "") or None,
            "attempt": agent.get("attempt"),
            "tool_calls": agent.get("tool_calls"),
            "model": str(agent.get("model") or "") or None,
        }
    for entry in _list(package.get("reviewer_provenance")):
        entry = _dict(entry)
        slot = str(entry.get("slot") or "")
        if not slot:
            continue
        row = rows.setdefault(slot, {"slot": slot})
        for key in ("role", "track", "attempt", "tool_calls", "model"):
            if not row.get(key) and entry.get(key) not in (None, ""):
                row[key] = entry[key]
        row["findings"] = entry.get("findings")
        row["none_found"] = bool(entry.get("none_found"))
    for observed in _list(runtime.get("agents")):
        observed = _dict(observed)
        label = str(observed.get("label") or "")
        if not label:
            continue
        # A row with nothing but a label is a slot the harness reserved and
        # never filled. Treating it as an agent that ran would put five empty
        # reviewers on the published panel.
        if not any(observed.get(key) for key in ("state", "model", "agentType")):
            continue
        row = rows.setdefault(label, {"slot": label})
        if observed.get("model") and not row.get("model"):
            row["model"] = str(observed["model"])
        if observed.get("agentType"):
            row["agent_type"] = str(observed["agentType"])
        if observed.get("state"):
            row["state"] = str(observed["state"])
        if observed.get("tokens") is not None:
            row["tokens"] = observed["tokens"]
        if observed.get("toolCalls") is not None and not row.get("tool_calls"):
            row["tool_calls"] = observed["toolCalls"]
    return [
        {key: value for key, value in row.items() if value not in (None, "")}
        for _, row in sorted(rows.items())
    ]


def model_map(agents: list[dict]) -> dict[str, str]:
    """Which model wrote which report, keyed by the slot that wrote it.

    This is the site's model table. A run on this path has a real per-agent
    split, because the plugin pins a model in each agent file, so the table says
    something rather than repeating one id down a column.
    """
    return {
        str(row["slot"]): str(row["model"])
        for row in agents
        if row.get("slot") and row.get("model")
    }


def model_phrase(models: dict[str, str]) -> str:
    """The models that wrote this review, counted by how many agents ran on each."""
    counts: dict[str, int] = {}
    for model in models.values():
        counts[model] = counts.get(model, 0) + 1
    if not counts:
        return "models the run did not record"
    return ", ".join(
        f"{model} ({count} agent{'' if count == 1 else 's'})"
        for model, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    )


def completeness(progress: dict, package: dict) -> dict:
    """The stage ledger, which is what says whether the review is whole.

    The server keeps a ledger of the stages a run requires and the ones that
    reported. A run can reach `complete` with a stage that never reported only
    when the editor accepted the pool without it, so the counts and the
    acceptance travel together in the record.
    """
    stages = _dict(progress.get("stages")) or _dict(package.get("stages"))
    if not stages:
        return {}
    record = {
        "required": [str(s) for s in _list(stages.get("required"))],
        "reported": [str(s) for s in _list(stages.get("reported"))],
        "missing": [str(s) for s in _list(stages.get("missing"))],
        "none_found": [str(s) for s in _list(stages.get("none_found"))],
        "editor_accepted": bool(stages.get("editor_accepted")),
    }
    attempts = {
        str(slot): int(count)
        for slot, count in _dict(stages.get("attempts")).items()
        if isinstance(count, int)
    }
    if attempts:
        record["attempts"] = attempts
        record["retried"] = sorted(slot for slot, count in attempts.items() if count > 1)
    return record


def read_run(run_dir: Path) -> dict:
    """Everything about the run that the run itself recorded.

    The plugin server and the starter write five files into the review folder.
    `protocol.json` says what was asked of the engine: the arm, the reviewer
    count, the tool allowances and one entry per agent slot. `manifest.json`
    captures the paper id and the hash of every plugin and engine file loaded,
    at the moment the run started. `progress.json` holds the final status, the
    guard status and the stage ledger. `runtime.json` holds what the harness
    observed: the models, the wall time, the tokens and the Claude Code version.
    `editor-package.json` holds the review.

    Every key in the result was read from one of those files. A value the run
    did not record is left out, so a caller that needs it has to say so rather
    than silently inherit a default from the prepare step or a publish flag.
    """
    run_dir = resolve_review_dir(run_dir)
    protocol = maybe_json(run_dir / "protocol.json")
    manifest = maybe_json(run_dir / "manifest.json")
    progress = maybe_json(run_dir / "progress.json")
    runtime = maybe_json(run_dir / "runtime.json")
    # Reading provenance is not the same job as reading the review. A run with
    # no editor package is refused by cmd_publish, which asks for it directly,
    # and this function stays able to describe a run that failed.
    try:
        package = editor_package(run_dir)
    except CommandError:
        package = {}

    record: dict = {}
    # A published record is read by strangers, and an absolute path in it
    # describes the machine that wrote it rather than the review. The path is
    # recorded when it is inside this repository and left out otherwise.
    if run_dir.is_relative_to(REPO):
        record["directory"] = run_dir.relative_to(REPO).as_posix()

    def put(key: str, value: object) -> None:
        if value not in (None, "", [], {}):
            record[key] = value

    plan = _dict(manifest.get("plan")) or _dict(protocol.get("plan"))

    put("arm", protocol.get("arm") or package.get("arm") or plan.get("arm") or progress.get("arm"))
    put(
        "workflow_version",
        package.get("workflow_version")
        or manifest.get("workflow_version")
        or protocol.get("version"),
    )
    put(
        "finding_schema_version",
        package.get("finding_schema_version")
        or manifest.get("finding_schema_version")
        or protocol.get("finding_schema_version"),
    )
    put("provider", protocol.get("provider"))
    reviewers = package.get("reviewer_count")
    if not isinstance(reviewers, int):
        reviewers = protocol.get("reviewers")
    if not isinstance(reviewers, int):
        reviewers = progress.get("reviewers")
    if isinstance(reviewers, int):
        record["reviewers"] = reviewers
    put("specialist_tracks", [str(t) for t in _list(plan.get("specialists"))])
    put("synthesis_policy", package.get("synthesis_policy"))
    put("paper_id", manifest.get("paper_id") or protocol.get("paper_id"))
    put("literature_cutoff", protocol.get("literature_cutoff"))
    put("body_finding_limit", protocol.get("body_finding_limit"))
    put("engine_source", manifest.get("code"))
    put("status", progress.get("status") or runtime.get("status"))
    # Kept because the status alone no longer distinguishes the two outcomes a
    # reader cares about: a manuscript nobody found fault with is `clean` with
    # no findings, and a review whose every finding was thrown away is
    # `all-findings-quarantined`.
    put(
        "review_guard_status",
        progress.get("review_guard_status") or package.get("review_guard_status"),
    )
    for key in (
        "findings_delivered",
        "findings_submitted",
        "quarantined_findings_count",
        "tool_calls_total",
    ):
        value = progress.get(key)
        if isinstance(value, int):
            record[key] = value
    if isinstance(package.get("escalated_count"), int):
        record["escalated_count"] = package["escalated_count"]
    put(
        "findings_by_track",
        {
            str(track): count
            for track, count in _dict(package.get("findings_by_track")).items()
            if isinstance(count, int)
        },
    )
    for key in ("wall_seconds", "tokens_total"):
        value = runtime.get(key)
        if isinstance(value, (int, float)):
            record[key] = value
    put("completeness", completeness(progress, package))

    record["errors"] = run_errors(progress, runtime, package)
    return record


def run_errors(progress: dict, runtime: dict, package: dict) -> list[str]:
    """What the run recorded going wrong, rather than an empty list by default.

    A blocked run says so in progress.json, and the starter repeats the cause in
    runtime.json. A finding the server refused to accept is quarantined with a
    reason instead of ending the run, so those are counted here: a reader
    deciding how much to trust a review should see that three of its findings
    were thrown away.

    Finishing with no findings is not one of these. A run that read the
    manuscript and raised nothing is `complete` with the guard status `clean`,
    and listing that as an error told a reader a review of a sound manuscript
    had gone wrong. A reviewer that reported no findings on its track is the
    same, which is why `none_found` is recorded and not listed here.
    """
    errors: list[str] = []
    if progress.get("error"):
        errors.append(str(progress["error"]))
    reason = str(runtime.get("blocked_reason") or "")
    if reason and reason not in errors:
        errors.append(reason)
    status = str(progress.get("status") or runtime.get("status") or "")
    if status and status not in FINISHED_STATUSES:
        errors.append(f"The run finished in state {status}.")
    # Said plainly, because the two readings are far apart: the reviewers
    # endorsed nothing because every finding they wrote failed the engine's
    # evidence guards, which is not a manuscript they found sound.
    guard = str(progress.get("review_guard_status") or package.get("review_guard_status") or "")
    if guard == ALL_FINDINGS_QUARANTINED:
        errors.append(
            "Every finding this run produced was quarantined by the engine's "
            "evidence guards, so the review endorses none of them."
        )
    quarantined = progress.get("quarantined_findings_count")
    if isinstance(quarantined, int) and quarantined > 0:
        errors.append(
            f"{quarantined} finding(s) failed the evidence guards and were "
            "quarantined out of this review."
        )
    stages = _dict(progress.get("stages")) or _dict(package.get("stages"))
    missing = [str(s) for s in _list(stages.get("missing"))]
    if missing:
        errors.append(
            f"{len(missing)} required stage(s) never reported: {', '.join(sorted(missing))}."
        )
    if stages and not stages.get("editor_accepted"):
        errors.append("The editor stage did not accept the pooled findings.")
    return errors


def editor_package(run_dir: Path) -> dict:
    """The engine's final review, read from the run folder it was written in."""
    run_dir = resolve_review_dir(run_dir)
    candidate = run_dir / "editor-package.json"
    if candidate.is_file():
        return read_json(candidate)
    raise CommandError(
        f"No editor-package.json under {run_dir}. Point --run at the folder "
        "`peerreview review` wrote."
    )


def bind_run_to_input(prepared: dict, workspace: Path, run: dict) -> dict:
    """Refuse to publish a run of one paper under another paper's identity.

    Nothing else in this pipeline ties the three pieces together. `prepare`
    hashes a PDF, the engine imports some PDF into a workspace, and the run
    reviews some workspace. Each step records enough to check the next, and
    until this function existed none of it was checked, so a run of paper B
    could be published as a review of paper A and exit zero.

    The chain is: the hash prepare took of the fetched bytes, the hash the
    importer took of the bytes it was given, and the paper id the run recorded.
    """
    paper = maybe_json(Path(workspace) / "paper.json")
    if not paper:
        raise CommandError(
            f"No paper.json in {workspace}. Point --workspace at the manuscript "
            "folder the run imported."
        )
    imported = str(paper.get("source_sha256") or "")
    expected = str(prepared["input"]["sha256"])
    if not imported:
        raise CommandError(
            "The workspace records no source hash, so this run cannot be tied "
            "to the paper that was prepared."
        )
    if imported != expected:
        raise CommandError(
            "This run reviewed different bytes than were prepared. The prepared "
            f"PDF hashes to {expected} and the imported manuscript hashes to "
            f"{imported}. Review the PDF that prepare fetched, or prepare the "
            "paper this workspace holds."
        )
    workspace_paper_id = str(paper.get("id") or "")
    run_paper_id = str(run.get("paper_id") or "")
    if not workspace_paper_id:
        raise CommandError(
            f"The paper.json in {workspace} records no paper id, so this run "
            "cannot be tied to the manuscript that was imported. Import the "
            "paper again."
        )
    if not run_paper_id:
        raise CommandError(
            "The run records no paper id, so there is nothing to compare "
            "against the workspace and no way to tell which paper it reviewed. "
            "The plugin server writes it into protocol.json and manifest.json "
            "when the run starts."
        )
    if run_paper_id != workspace_paper_id:
        raise CommandError(
            f"The run reviewed paper {run_paper_id} but --workspace holds paper "
            f"{workspace_paper_id}. Point --run and --workspace at the same review."
        )
    manifest = Path(workspace) / "manifest.json"
    return {
        "workspace_manifest_sha256": digest(manifest.read_bytes()) if manifest.is_file() else None,
        "paper_id": workspace_paper_id,
    }


def sorted_findings(package: dict) -> list[dict]:
    """The findings the editor put in the body of the letter, worst first."""
    findings = [f for f in _list(package.get("findings")) if isinstance(f, dict)]
    return sorted(findings, key=lambda f: SEVERITY_ORDER.get(str(f.get("severity")), 9))


def appendix_findings(package: dict) -> list[dict]:
    """The findings the editor kept but did not place in the letter's body.

    The plugin caps the body at eight. Everything else a reviewer raised and the
    editor accepted goes to the appendix rather than being dropped, so the
    bundle publishes both and says which is which.
    """
    findings = [f for f in _list(package.get("appendix")) if isinstance(f, dict)]
    return sorted(findings, key=lambda f: SEVERITY_ORDER.get(str(f.get("severity")), 9))


def severity_counts(findings: list[dict]) -> dict[str, int]:
    counts = {"major": 0, "moderate": 0, "minor": 0}
    for finding in findings:
        severity = str(finding.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def escalated(findings: list[dict]) -> list[dict]:
    return [f for f in findings if f.get("escalate")]


def _location(finding: dict) -> str:
    placement = finding.get("placement")
    if placement not in (None, "anchored"):
        return f"unplaced ({placement})"
    block = finding.get("block_id")
    return f"block {block}" if block else "not located"


def _tags(finding: dict) -> str:
    """How a reader should weigh one finding, in the engine's own vocabulary.

    The track says which reader raised it, and the basis says what it rests on:
    `computed` is arithmetic the reviewer did and recorded, `two-quotes` is two
    anchored passages that disagree, and `judgement` is neither. A reader
    deciding whether to act on a finding needs that before the wording.
    """
    parts = [str(finding.get("severity") or "unstated")]
    track = str(finding.get("track") or "")
    if track:
        parts.append(f"track {track}")
    basis = str(finding.get("basis") or "")
    if basis:
        parts.append(f"basis {basis}")
    parts.append(_location(finding))
    if finding.get("escalate"):
        parts.append("escalated")
    return ", ".join(parts)


def basis_note(finding: dict) -> list[str]:
    basis = str(finding.get("basis") or "")
    if not basis:
        return []
    reason = str(finding.get("basis_reason") or "").strip()
    return [f"**What it rests on:** {basis}" + (f". {reason}" if reason else ""), ""]


def method_paragraph(run: dict, models: dict[str, str]) -> str:
    """Describe the run that happened, from what the run recorded.

    Every clause is conditional on a recorded value, and an unrecorded one is
    admitted rather than assumed. There is no debate stage to describe in 0.9
    and no single model: the plugin pins a model per agent file, and the record
    carries the map.
    """
    reviewers = run.get("reviewers")
    tracks = [str(t) for t in _list(run.get("specialist_tracks"))]
    arm = str(run.get("arm") or "")

    if not isinstance(reviewers, int):
        shape = (
            "The run did not record how many reviewer passes it made, so this "
            "review cannot be described more precisely than as the output of "
            f"the engine's {arm or 'review'} arm."
        )
    elif reviewers <= 1:
        shape = (
            "One core reviewer read the whole manuscript, so nothing checked "
            "that reviewer that was any better than it. Read it as one careful "
            "reading."
        )
    else:
        shape = (
            f"{reviewers} core reviewers read the manuscript independently, "
            "each writing up what it found on its own."
        )
    if tracks:
        shape += (
            f" {len(tracks)} specialist readers then checked it on one dimension "
            f"each ({', '.join(tracks)}), and an editor agent pooled every "
            "finding, ruled on the ones a reviewer escalated, and chose which "
            "belong in the body of the letter."
        )
    elif arm:
        shape += f" The run used the {arm} arm, which convened no specialist readers."

    return (
        f"{shape} Every agent ran inside one Claude Code session on the editor's "
        "own machine, on a subscription, each on the model its plugin agent file "
        f"pins: {model_phrase(models)}. There was no desk screen and no debate "
        "stage, and agents sharing a model are not independent corroboration of "
        "one another."
    )


def attestation_paragraph(attestation: dict) -> str:
    """Who stands behind the decision, which depends on whether anyone read it."""
    editor = str(attestation.get("editor") or "the editor")
    if attestation.get("human_reviewed_before_merge"):
        return (
            f"The decision above was chosen by {editor}, a human editor, after "
            "reading the run. The engine's editor agent records an advisory "
            "judgement and recommends no verdict."
        )
    return (
        f"{editor} typed the decision above without attesting to having read "
        "the run, so it stands on nothing and this bundle is a rehearsal that "
        "must not be published. The engine's editor agent records an advisory "
        "judgement and recommends no verdict."
    )


def verdict_section(verdict: dict) -> list[str]:
    """The editor agent's judgement, labelled as advisory everywhere it appears.

    It is published because it is the most useful thing in the run for a reader
    deciding whether to read the paper, and it is labelled because it is one
    model's reading. It is not the decision, it recommends no verdict, and the
    record says the decision came from a person.
    """
    verdict = _dict(verdict)
    rows = [
        ("Significance", verdict.get("significance")),
        ("Strength of evidence", verdict.get("strength_of_evidence")),
        ("Reasoning", verdict.get("reasoning")),
        ("What it rests on", verdict.get("basis")),
        ("Stated limitation", verdict.get("limitation")),
    ]
    rows = [(label, str(value).strip()) for label, value in rows if str(value or "").strip()]
    if not rows:
        return []
    lines = [
        "## Advisory judgement from the engine",
        "",
        "This is the editor agent's reading, not the decision. It recommends no "
        "accept or reject, it is one model's judgement of the manuscript, and "
        "the decision above is the editor's. Whether anyone read the run before "
        "taking it is stated with the decision, not here.",
        "",
    ]
    for label, value in rows:
        lines += [f"**{label}.** {value}", ""]
    return lines


def render_summary(
    preprint: Preprint, package: dict, provenance: dict, findings: list[dict]
) -> str:
    counts = severity_counts(findings)
    generator = provenance["generator"]
    run = generator["run"]
    appendix = appendix_findings(package)
    escalations = escalated(findings) + escalated(appendix)
    lines = [
        f"# Review Summary: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "**Target venue:** In Silico",
        f"**Generated by:** {generator['engine']['name']} {generator['engine']['version']}, "
        f"{generator['plugin']['workflow_version']}, run locally on the "
        f"{run.get('arm') or 'unrecorded'} arm",
        f"**Findings in this letter:** {len(findings)} "
        f"({counts['major']} major, {counts['moderate']} moderate, {counts['minor']} minor)"
        + (f", with {len(appendix)} more in the appendix" if appendix else ""),
        f"**Escalated by a reviewer:** {len(escalations)}",
        "",
        "## How this review was produced",
        "",
        method_paragraph(run, provenance.get("models") or {}),
        "",
        attestation_paragraph(generator["attestation"]),
        "",
    ]
    tracks = _dict(run.get("findings_by_track"))
    if tracks:
        lines += [
            "Findings raised per track, before the editor pooled them: "
            + ", ".join(f"{track} {count}" for track, count in sorted(tracks.items()))
            + ".",
            "",
        ]
    summary = str(package.get("summary") or "").strip()
    if summary:
        lines += ["## The editor agent's summary of the review", "", summary, ""]
    lines += verdict_section(package.get("verdict"))
    if findings:
        lines += ["## Findings in the letter", ""]
        for number, finding in enumerate(findings, 1):
            title = str(finding.get("title") or "Untitled finding").strip()
            lines.append(f"{number}. **{title}** ({_tags(finding)})")
        lines.append("")
    if appendix:
        limit = run.get("body_finding_limit")
        lines += [
            "## Findings in the appendix",
            "",
            "Accepted by the editor agent and kept out of the letter's body, "
            f"which the workflow caps at {limit or 'a fixed number of'} findings.",
            "",
        ]
        for number, finding in enumerate(appendix, 1):
            title = str(finding.get("title") or "Untitled finding").strip()
            lines.append(f"{number}. **{title}** ({_tags(finding)})")
        lines.append("")
    limitations = [str(v).strip() for v in _list(package.get("limitations")) if str(v).strip()]
    if limitations:
        lines += ["## Stated limitations of this review", ""]
        lines += [f"- {item}" for item in limitations]
        lines.append("")
    return "\n".join(lines)


def render_decision_letter(
    preprint: Preprint, package: dict, provenance: dict, findings: list[dict]
) -> str:
    required = [f for f in findings if str(f.get("severity")) in REQUIRED_SEVERITIES]
    optional = [f for f in findings if str(f.get("severity")) == "minor"]
    appendix = appendix_findings(package)
    attestation = provenance["generator"]["attestation"]
    if attestation.get("human_reviewed_before_merge"):
        standing = (
            "This letter reports one locally generated review. The decision is "
            "the editor's, taken after reading the run in full."
        )
    else:
        standing = (
            "This letter reports one locally generated review as a rehearsal. "
            "Nobody has attested to reading the run, so the decision above "
            "stands on nothing and this letter must not be published."
        )
    lines = [
        f"# Decision Letter: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "",
        f"{standing} Everything below it is the reviewers' and the editor "
        "agent's, quoted or paraphrased from the saved run rather than "
        "rewritten.",
        "",
    ]
    summary = str(package.get("summary") or "").strip()
    if summary:
        lines += ["## Assessment", "", summary, ""]
    if required:
        lines += ["## Required changes", ""]
        for number, finding in enumerate(required, 1):
            lines += _letter_entry(f"R{number}", finding)
    if optional:
        lines += ["## Suggestions", ""]
        for number, finding in enumerate(optional, 1):
            lines += _letter_entry(f"S{number}", finding)
    if not findings:
        lines += [
            "## Findings",
            "",
            "The reviewers recorded no findings against this manuscript.",
            "",
        ]
    if appendix:
        lines += [
            "## Appendix",
            "",
            "Findings the editor agent accepted and left out of the body above. "
            "They are not withdrawn, and they are listed in full here.",
            "",
        ]
        for number, finding in enumerate(appendix, 1):
            lines += _letter_entry(f"A{number}", finding)
    rulings = [r for r in _list(package.get("escalation_rulings")) if isinstance(r, dict)]
    if rulings:
        by_uid = {str(f.get("finding_uid") or ""): f for f in [*findings, *appendix]}
        lines += [
            "## Rulings on escalated findings",
            "",
            "A reviewer may escalate a finding it believes bears on whether the "
            "paper stands. The editor agent ruled on each one, and the rulings "
            "are published whichever way they went.",
            "",
        ]
        for ruling in rulings:
            uid = str(ruling.get("finding_uid") or "")
            title = str(_dict(by_uid.get(uid)).get("title") or "").strip()
            lines += [f"### {title or uid or 'Unidentified finding'}", ""]
            if uid:
                lines += [f"`{uid}`", ""]
            text = str(ruling.get("ruling") or "").strip()
            if text:
                lines += [text, ""]
    return "\n".join(lines)


def _letter_entry(label: str, finding: dict) -> list[str]:
    title = str(finding.get("title") or "Untitled finding").strip()
    lines = [
        f"### {label}. {title}",
        "",
        f"**Severity:** {str(finding.get('severity') or 'unstated')}  ",
        f"**Raised by:** {str(finding.get('slot') or 'an unrecorded slot')} "
        f"on track {str(finding.get('track') or 'unrecorded')}  ",
        f"**Location:** {_location(finding)}",
        "",
    ]
    if finding.get("escalate"):
        lines += [
            "**The reviewer escalated this finding as bearing on the paper's "
            "central claim.**",
            "",
        ]
    lines += basis_note(finding)
    quote = str(finding.get("quote") or "").strip()
    if quote:
        lines += ["Manuscript passage:", "", f"> {quote}", ""]
    comment = str(finding.get("comment") or "").strip()
    if comment:
        lines += [comment, ""]
    replacement = str(finding.get("replacement") or "").strip()
    if replacement:
        lines += ["Suggested replacement:", "", f"> {replacement}", ""]
    counter = str(finding.get("counterevidence") or "").strip()
    if counter:
        lines += [f"**Strongest counterpoint:** {counter}", ""]
    reason = str(finding.get("editor_reason") or "").strip()
    if reason:
        lines += [f"**The editor agent's reason for placing it here:** {reason}", ""]
    raising = finding.get("reviewers_raising")
    if isinstance(raising, int) and raising > 1:
        lines += [f"**Raised independently by {raising} reviewers.**", ""]
    uid = str(finding.get("finding_uid") or "").strip()
    if uid:
        lines += [f"`{uid}`", ""]
    return lines


def render_stats(preprint: Preprint, ingest: dict, generator: dict) -> str:
    lines = [
        "# Manuscript Statistics",
        "",
        f"**Title:** {preprint.title or 'Untitled submission'}",
        f"**Source:** {preprint.source} {preprint.identifier}",
        f"**Revision reviewed:** v{preprint.version or 'unrecorded'}",
        "",
        "## Bytes reviewed",
        "",
        f"- PDF size: {generator['input']['bytes']} bytes",
        f"- PDF sha256: `{generator['input']['sha256']}`",
    ]
    manifest = generator["input"].get("workspace_manifest_sha256")
    if manifest:
        lines.append(f"- Workspace manifest sha256: `{manifest}`")
    chars = ingest.get("chars")
    if chars:
        lines.append(f"- Manuscript text: {chars} characters")
    if ingest.get("text_sha256"):
        lines.append(f"- Manuscript text sha256: `{ingest['text_sha256']}`")
    blocks = ingest.get("blocks")
    if blocks:
        lines.append(f"- Source blocks: {blocks}")
    lines += [
        "",
        "## How the text was read",
        "",
        f"Imported by {ingest.get('tool') or 'the engine importer'} into "
        "evidence-linked source blocks. Quotations in this review were validated "
        "against those blocks before the review was saved.",
        "",
    ]
    return "\n".join(lines)


def ingest_record(workspace: Path | None) -> dict:
    """What the reviewers were handed, measured off the workspace with no model."""
    record = {"format": "markdown", "tool": "peerreviewagents import_paper"}
    if workspace is None:
        return record
    workspace = Path(workspace)
    manuscript = workspace / "manuscript.md"
    if manuscript.is_file():
        text = manuscript.read_text(encoding="utf-8")
        record["chars"] = len(text)
        record["text_sha256"] = digest(text.encode())
    paper = workspace / "paper.json"
    if paper.is_file():
        blocks = maybe_json(paper).get("blocks")
        if isinstance(blocks, list):
            record["blocks"] = len(blocks)
    return record


def track_reports(run_dir: Path) -> dict[str, Path]:
    """The specialist reports the run wrote, keyed by the file name they keep.

    `src/lib/corpus.js` already lists any `audit_<track>.md` in a bundle as a
    report of its own, so copying them in is all that is needed to publish what
    each specialist read the manuscript for.
    """
    run_dir = resolve_review_dir(run_dir)
    return {
        path.name: path
        for path in sorted(run_dir.glob("audit_*.md"))
        if path.is_file() and path.stat().st_size
    }


def review_kind(plan_kind: str, baseline_eligible: bool) -> str:
    """The published label for this attempt, in the vocabulary the site reads.

    `review.kind` is printed on the provenance panel and read by Notices.astro,
    so this reuses the hosted panel's words rather than inventing one. The rule
    there is that an ungraded run is an experiment whatever else it is, and a
    run on this path is ungraded unless the editor claims it. A revision round
    keeps its own name, because what it is measured against matters more than
    how it was produced.
    """
    if plan_kind == "revision round":
        return "revision"
    if not baseline_eligible:
        return "experiment"
    if plan_kind == "same-draft re-review":
        return "editorial_rereview"
    return "initial"


def build_provenance(
    *,
    preprint: Preprint,
    prepared: dict,
    package: dict,
    run: dict,
    fingerprint: dict,
    plugin: dict,
    agents: list[dict],
    decision: str,
    editor: str,
    human_reviewed: bool,
    route: str,
    draft: int,
    attempt: int,
    submitter: str,
    submitter_is_author: str,
    baseline_eligible: bool,
    ingest: dict,
    transport: dict,
    review_id: str,
    publishing: bool,
) -> dict:
    """The published record of what produced this review.

    Version 4. It carries the same identity fields as the hosted panel's version
    2 record, and in place of that panel's accounting it carries a generator
    block: the engine and the hash of every file it loaded, the plugin and the
    workflow that decided which agents ran, the transport and its billing
    policy, one row per agent with the model it ran on, the input hash, the
    stage ledger that says whether the review is whole, the editor agent's
    advisory judgement, and the attestation that a person read the run before it
    was merged.
    """
    findings = sorted_findings(package)
    appendix = appendix_findings(package)
    # Recorded only when somebody actually submitted the paper. A review an
    # editor started themselves was solicited by nobody, and writing an empty
    # claim for it would be read as a claim we failed to collect.
    attribution = (
        {"submitter": submitter, "submitter_is_author": submitter_is_author}
        if submitter
        else {}
    )
    kind = review_kind(str(prepared.get("plan_kind") or ""), baseline_eligible)
    if not editor:
        raise CommandError("An editor has to be named before a review can be attested")
    # The run's own record, with the counts this bundle actually wrote added.
    # Nothing from the prepare step or the publish flags is folded in: prepare
    # states an intention and the run states what happened, and when the two
    # disagree the run is the one that is true.
    run_record = {key: value for key, value in run.items() if key != "engine_source"}
    run_record["findings"] = len(findings)
    run_record["appendix_findings"] = len(appendix)
    run_record["escalated_in_bundle"] = len(escalated(findings) + escalated(appendix))
    # The provider is the run's too. It used to be a constant at the top level
    # and another constant inside the transport, so a record could say
    # claude-code twice over a run on another transport, and nothing in the file
    # compared the two.
    provider = str(run.get("provider") or "")
    if not provider:
        raise CommandError(
            "This run records no provider, so the record cannot say which "
            "transport produced the review."
        )
    if str(transport.get("provider") or "") != provider:
        raise CommandError(
            f"The run used the {provider} transport and the transport record "
            f"names {transport.get('provider')}. A record that names two "
            "transports describes neither run."
        )
    models = model_map(agents)
    if not models:
        raise CommandError(
            "This run records no model for any agent, so the record cannot say "
            "what wrote the review. The plugin server writes one per slot into "
            "protocol.json, and the starter records what the harness served "
            "into runtime.json."
        )
    generator = {
        "kind": GENERATOR_KIND,
        "engine": engine_record(),
        "engine_fingerprint": fingerprint,
        "plugin": plugin,
        "transport": transport,
        "agents": agents,
        "input": prepared["input"],
        "run": run_record,
        # Published, and labelled advisory in the schema, on the page and in the
        # documents. The engine recommends no verdict, and the decision below is
        # a person's.
        "advisory_verdict": _dict(package.get("verdict")),
        "decision_source": "human_editor",
        "attestation": {
            "locally_generated": True,
            "human_reviewed_before_merge": human_reviewed,
            # Said outright, because the only thing that used to distinguish a
            # rehearsal from a published review was which folder it sat in, and
            # a folder can be copied. The schema requires false here.
            "rehearsal": not publishing,
            "editor": editor,
            "statement": ATTESTATION if human_reviewed else UNREAD_STATEMENT,
        },
    }
    return {
        "schema_version": PROVENANCE_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "insilico": insilico_version(),
        "generator": generator,
        "review": {
            "id": review_id,
            "manuscript_version": draft,
            "attempt": attempt,
            "kind": kind,
            "lifecycle": "active",
            "baseline_eligible": baseline_eligible,
            "route": route,
        },
        "provider": provider,
        # Which model wrote which report, keyed by the slot that wrote it. The
        # plugin pins a model per agent file, so this is a real split rather
        # than one id repeated down a column, and the site reads exactly this
        # field when it says what checked the reviewers.
        "models": models,
        "decision": decision,
        "desk_rejected": False,
        "round": 1,
        "ingest": ingest,
        "panel": [],
        # A subscription has no per-review price. Null says there is no figure,
        # where a zero would read as a measured free run.
        "total_cost_usd": None,
        "errors": [str(e) for e in _list(run.get("errors"))],
        "preprint": preprint.to_dict(),
        **attribution,
    }


def write_manifest(dest: Path) -> None:
    """Hash every file in the bundle, so a later edit to one is visible."""
    dest = Path(dest)
    files = {
        path.relative_to(dest).as_posix(): digest(path.read_bytes())
        for path in sorted(dest.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    write_json(dest / "manifest.json", {"schema_version": 1, "files": files})


def write_round_record(
    dest: Path, preprint: Preprint, provenance: dict, findings: list[dict]
) -> None:
    """The machine-readable round record a later revision round is measured against.

    Each required revision carries the engine's own `finding_uid` now. A
    revision round has to say which of the previous round's findings it is
    answering, and an `R1-03` that means nothing outside this file could not be
    matched back to the finding the reviewer wrote.
    """
    required = [
        {
            "id": f"R1-{number:02d}",
            "finding_uid": str(finding.get("finding_uid") or ""),
            "track": str(finding.get("track") or ""),
            "basis": str(finding.get("basis") or ""),
            "escalated": bool(finding.get("escalate")),
            "text": str(finding.get("comment") or finding.get("title") or "").strip(),
            "source_reviewer": str(finding.get("slot") or ""),
            "blocking": False,
        }
        for number, finding in enumerate(
            [f for f in findings if str(f.get("severity")) in REQUIRED_SEVERITIES], 1
        )
    ]
    write_json(
        dest / ROUND_RECORD,
        {
            "schema_version": 1,
            "round": 1,
            "manuscript_title": preprint.title,
            "decision": provenance["decision"],
            "required_revisions": required,
            "minor_suggestions": [
                str(f.get("comment") or f.get("title") or "").strip()
                for f in findings
                if str(f.get("severity")) == "minor"
            ],
            "manuscript_text_sha256": provenance["ingest"].get("text_sha256", ""),
            "manuscript_file_sha256": provenance["generator"]["input"]["sha256"],
            "desk_rejected": False,
        },
    )


def claude_version() -> str | None:
    """What `claude --version` prints, through the engine's own resolver.

    Reported rather than required, and never a review: the preflight is allowed
    to say the harness is missing, which is more useful than refusing to print
    the fingerprint the operator asked for.
    """
    try:
        starter = importlib.import_module(STARTER_MODULE)
    except ImportError:
        return None
    try:
        return starter.claude_version()
    except Exception:  # noqa: BLE001 - a preflight must not fail on a missing CLI
        return None


def cmd_fingerprint(args: argparse.Namespace) -> int:
    """Preflight. Prints what is installed, and calls no model."""
    manifest = installed_code_manifest()
    record = {
        "engine": engine_record(),
        "engine_fingerprint": code_fingerprint(manifest, "installed_engine"),
        "plugin_fingerprint": code_fingerprint(
            manifest, "installed_engine", prefix=PLUGIN_PREFIX
        ),
        "workflow_sha256": manifest.get(WORKFLOW_FILE),
        "transport": {
            "provider": TRANSPORT_PROVIDER,
            "executable": "claude",
            "version": claude_version(),
            "billing_policy": BILLING_POLICY,
            "paid_api_key_used": False,
        },
    }
    print(json.dumps(record, indent=2))
    if not record["transport"]["version"]:
        print(
            "\nThe Claude CLI did not report a version. A review needs it on "
            "PATH and signed in to the subscription account.",
            file=sys.stderr,
        )
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    """Resolve the paper, fetch the exact bytes, and decide where a review goes."""
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise CommandError(f"{out} already holds a prepared paper. Use a new folder.")
    out.mkdir(parents=True, exist_ok=True)

    preprint = None
    publishable = False
    if args.paper:
        preprint = resolve(args.paper)
        publishable = True

    if args.pdf:
        source = Path(args.pdf).resolve()
        if not source.is_file():
            raise CommandError(f"No PDF at {source}")
        pdf = out / "manuscript.pdf"
        shutil.copyfile(source, pdf)
        local_file = True
    elif preprint is not None:
        pdf = download(preprint, out)
        local_file = False
    else:
        raise CommandError("Pass --paper, or --pdf, or both.")

    data = pdf.read_bytes()
    if preprint is not None and not preprint.pdf_sha256:
        preprint.pdf_sha256 = digest(data)
        preprint.pdf_bytes = len(data)

    kind = "pdf" if preprint is None else ("arxiv" if preprint.source == "arxiv" else "doi")
    identifier = (
        args.paper if preprint is None else (preprint.identifier or preprint.doi or preprint.url)
    )
    record = {
        "publishable": publishable,
        "pdf": str(pdf),
        "arm": args.arm,
        "reviewers": args.reviewers,
        "literature_cutoff": args.literature_cutoff or dt.date.today().isoformat(),
        "input": {
            "kind": kind,
            "identifier": identifier,
            "sha256": digest(data),
            "bytes": len(data),
            "local_file": local_file,
        },
        "preprint": preprint.to_dict() if preprint is not None else None,
    }

    if publishable:
        paper_dir = find_paper_dir(preprint) or (
            REVIEWS / str(dt.date.today().year) / paper_slug(preprint, preprint.title)
        )
        draft = draft_number(preprint)
        plan = plan_review(paper_dir, draft, args.replace, publishing=True)
        record["destination"] = str(plan.dest)
        record["draft"] = plan.draft
        record["attempt"] = plan.attempt
        record["plan_kind"] = plan.kind
    else:
        record["destination"] = str(RUNS / f"local-{digest(data)[:12]}")
        record["draft"] = 1
        record["attempt"] = 1
        record["plan_kind"] = "unpublishable local run"

    write_json(out / "prepared.json", record)
    print(json.dumps(record, indent=2))
    if not publishable:
        print(
            "\nThis run cannot be published. A review has to name the exact "
            "revision it judged, and a bare PDF does not. Re-run prepare with "
            "--paper to publish.",
            file=sys.stderr,
        )
    return 0


def absolute_path_fields(value: object, trail: str = "") -> list[str]:
    """Where a record carries a path that only exists on the machine that wrote it.

    A published provenance record is read by people with no access to this disk,
    so an absolute path in it identifies the operator's filesystem rather than
    the review.
    """
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found += absolute_path_fields(child, f"{trail}.{key}" if trail else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found += absolute_path_fields(child, f"{trail}[{index}]")
    elif isinstance(value, str) and (value.startswith("/") or value.startswith("file://")):
        found.append(trail or "(root)")
    return found


_DROPPED = object()

# The fields the engine fills with a path on the machine that ran the review.
# The plugin server writes the manuscript's absolute path as `pdf` and the
# loaded plugin's as `plugin_root`, both into the run manifest. The older names
# are kept because a run folder written by an earlier engine may still be
# published from.
#
# This is a list of field names rather than a test on the value because the
# first version tested the value: any string beginning with a slash was taken
# for a path. A reviewer writing "/ 2 is the wrong denominator" had the comment
# silently deleted from the published package, and a path written inside a
# sentence was missed regardless. Review content is never rewritten now. What
# catches a path the engine starts recording in a field nothing here knows about
# is the leak scan over the written bundle, below.
PATH_FIELDS = frozenset({
    "memo_path",
    "pdf",
    "plugin_dir",
    "plugin_root",
    "run_directory",
    "source_review_path",
    "workspace",
})


def readable_path(text: str) -> object:
    """A path value as a reader can use it, or _DROPPED if they cannot.

    A path inside this repository is rewritten relative to it, because it still
    points at something a reader has. A path outside it names a directory on one
    machine, so the field goes rather than being published as noise. The hash
    beside it is what tied the file to its bytes, and that is kept.
    """
    raw = text[len("file://") :] if text.startswith("file://") else text
    raw = raw.strip()
    if raw.startswith("~"):
        return _DROPPED
    try:
        path = Path(raw)
        if not path.is_absolute():
            return text
        path = path.resolve()
    except (OSError, ValueError, RuntimeError):
        return _DROPPED
    if path.is_relative_to(REPO.resolve()):
        return path.relative_to(REPO.resolve()).as_posix()
    return _DROPPED


def without_local_paths(value: object, *, field: str = "") -> object:
    """The same JSON with the engine's path fields made repo relative or dropped.

    `editor-package.json` is the engine's own output copied into the bundle, and
    a run folder records absolute paths in several places. Only the fields in
    `PATH_FIELDS` and dictionary keys that are themselves absolute paths are
    touched, so the review's own words reach the reader as the reviewer wrote
    them.
    """
    if isinstance(value, dict):
        scrubbed = {}
        for key, child in value.items():
            # A mapping keyed by an absolute path, such as a per-file hash map,
            # leaks through the key rather than the value. A key that is an
            # absolute path is never something a reviewer wrote.
            name = key
            if isinstance(key, str) and (key.startswith("/") or key.startswith("file://")):
                relative = readable_path(key)
                if relative is _DROPPED:
                    continue
                name = relative
            cleaned = without_local_paths(child, field=key if isinstance(key, str) else "")
            if cleaned is not _DROPPED:
                scrubbed[name] = cleaned
        return scrubbed
    if isinstance(value, list):
        return [
            cleaned
            for cleaned in (without_local_paths(child, field=field) for child in value)
            if cleaned is not _DROPPED
        ]
    if isinstance(value, str) and field in PATH_FIELDS:
        return readable_path(value)
    return value


def local_path_needles() -> list[str]:
    """The strings that reach a published file only by mistake.

    The first version of this scan looked for a leading slash in a JSON value,
    which both missed and over-matched: it read none of the Markdown, nothing
    keyed by a path, no `~/` or Windows form, and no path written inside a
    sentence, while flagging a reviewer's own arithmetic. These two strings are
    the operator's home directory and this checkout, in whatever shape they take
    on the machine doing the publishing. No review has a reason to contain
    either, and prose does not contain them by accident.
    """
    needles = {str(REPO.resolve())}
    try:
        needles.add(str(Path.home().resolve()))
    except (OSError, RuntimeError):
        pass
    return sorted(needle for needle in needles if needle not in ("", "/"))


def bundle_local_path_leaks(dest: Path) -> list[str]:
    """Every file in a written bundle that names the machine that wrote it.

    This reads what is on disk rather than what the code meant to write, which
    is the point: it is the guard that catches a path the engine started
    recording in a field nothing here knows about, in any file of the bundle,
    including the specialist reports copied in from the run.
    """
    needles = local_path_needles()
    found: list[str] = []
    for path in sorted(Path(dest).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".json", ".jsonl", ".md", ".txt"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for needle in needles:
            if needle in text:
                found.append(f"{path.relative_to(dest).as_posix()} names {needle}")
    return found


def publish_destination(prepared: dict, *, publishing: bool) -> Path:
    """Where this bundle is written, which depends on whether it is published.

    Without ``--publish`` the publishability and decision guards are relaxed, so
    the bundle is a rehearsal and must not land in the published tree. It used
    to: ``prepare`` records a destination under ``docs/reviews`` for any paper
    with a permanent identity, and ``publish`` wrote there whatever the flag
    said. A rehearsal therefore produced a complete, renderable bundle inside
    the directory the site builds from, and the only thing keeping it off the
    site was that nobody had committed it yet.

    Both destinations are resolved and then required to be inside the tree they
    belong to. Trusting the recorded destination on the publish path meant any
    string in prepared.json was written to, and building the rehearsal path out
    of unresolved parts let `..` segments through, which is why the refusal
    below it could never fire.
    """
    dest = Path(prepared["destination"]).expanduser().resolve()
    if publishing:
        if not dest.is_relative_to(REVIEWS.resolve()):
            raise CommandError(
                f"A published bundle has to be written inside {REVIEWS}, and "
                f"prepared.json points at {dest}. Prepare the paper again."
            )
        return dest
    rehearsal_root = (RUNS / "rehearsal").resolve()
    slug = dest.parent.parent.name or "unnamed"
    rehearsal = (rehearsal_root / slug / dest.parent.name / dest.name).resolve()
    if not rehearsal.is_relative_to(rehearsal_root):
        raise CommandError(
            f"A rehearsal bundle would be written outside {rehearsal_root}, at "
            f"{rehearsal}. Refusing. Pass --publish to publish deliberately."
        )
    return rehearsal


def bundle_identifier(dest: Path) -> str:
    """How a record names its own bundle, without naming the operator's disk.

    The repository relative path when there is one. A rehearsal written outside
    the repository keeps the last three segments, which is the slug and the
    route, because that identifies the bundle and nothing else about the machine
    it was written on.
    """
    dest = Path(dest).resolve()
    repo = REPO.resolve()
    if dest.is_relative_to(repo):
        return dest.relative_to(repo).as_posix()
    return "/".join(dest.parts[-3:])


def require_complete_run(run_dir: Path, run: dict) -> None:
    """A published review has to come from a run that finished.

    Publishing checked neither the state nor the transport. A directory holding
    only an editor package, with no protocol.json and no progress.json,
    published with an empty error list, and so did a run whose progress.json
    said `blocked`. Both produced a record that read like a clean review.

    Finished means `complete`, and nothing else. A run that read the manuscript
    and raised no finding is `complete` with the guard status `clean`, and it
    publishes as a review with the empty findings list the reader should see.
    The engine's other finished state, `complete-without-findings`, is written
    only when every finding was quarantined, so it is refused here by name
    before the status check: that bundle's letter would tell the authors their
    paper drew no findings, when the truth is that the review endorses none of
    the findings it wrote.

    A blocked run is refused too, and the refusal repeats the cause the run
    itself recorded rather than only the state name, because the state name
    alone sent the operator back to a log to find out there was no Claude login.

    The transport is checked here as well. This path records Claude Code runs
    only, so a run on anything else would otherwise be written up with a Claude
    subscription attestation it has no claim to.
    """
    run_dir = resolve_review_dir(run_dir)
    protocol_path = run_dir / "protocol.json"
    if not protocol_path.is_file():
        raise CommandError(
            f"{run_dir} has no protocol.json, so there is no record of what was "
            "asked of the engine. Point --run at the folder `peerreview review` "
            "wrote."
        )
    # Only the file's existence was checked, so a zero byte protocol.json
    # satisfied the guard while answering none of the questions it was added to
    # ask. The run has to say what was asked of the engine, not merely have a
    # file where that would be written.
    if not maybe_json(protocol_path):
        raise CommandError(
            f"{protocol_path} is empty or is not a JSON object, so the run "
            "records nothing about what was asked of the engine."
        )
    # The arm replaces 0.8's mode and policy, and there is no single model to
    # require: the plugin pins one per agent file, and protocol.json says so in
    # a sentence rather than an id. What has to be recorded is which arm ran,
    # on which transport, under which workflow.
    missing = [field for field in ("arm", "provider", "workflow_version") if not run.get(field)]
    if missing:
        raise CommandError(
            f"{protocol_path} records no {', '.join(missing)}, so the published "
            "record could not say how the review was produced. Point --run at "
            "the folder `peerreview review` wrote."
        )
    provider = str(run.get("provider") or "")
    if provider not in PUBLISHABLE_PROVIDERS:
        raise CommandError(
            f"This run recorded the {provider} transport, and this path "
            f"publishes {', '.join(PUBLISHABLE_PROVIDERS)} runs only. Every "
            "claim a published bundle makes about how the review was paid for "
            "is a claim about a Claude subscription, so a run on another "
            "transport cannot be published through it."
        )
    # progress.json is the server's ledger: the final status, the guard status
    # and the stage counts are all written there. read_run falls back to
    # runtime.json's status and the editor package's stage counts so that a
    # damaged run can still be described, and those fallbacks are the reason
    # the file's absence has to be refused here by name. A folder holding an
    # editor package and a runtime record, with no ledger, reads as a finished
    # clean review on the strength of two files that say nothing about the
    # guards.
    progress_path = run_dir / "progress.json"
    if not maybe_json(progress_path):
        raise CommandError(
            f"{run_dir} has no readable progress.json, so the run recorded no "
            "ledger of its stages or its evidence guards. Point --run at the "
            "folder `peerreview review` wrote."
        )
    status = str(run.get("status") or "")
    if not status:
        raise CommandError(
            f"{progress_path} records no status, so the run never recorded "
            "whether it finished. A review cannot be published from it."
        )
    # Named before the status, because this is the case the status describes and
    # the operator needs to be told which of the two it is.
    if (
        run.get("review_guard_status") == ALL_FINDINGS_QUARANTINED
        or status == WITHOUT_FINDINGS_STATUS
    ):
        raise CommandError(
            f"This run ended as {status} with guard status "
            f"{run.get('review_guard_status') or 'unrecorded'}, which the engine "
            "writes when every finding it produced was quarantined by the "
            "evidence guards. A review that endorses none of its own findings is "
            "not a manuscript found sound, and publishing it would say so to the "
            "authors. Read the quarantine reasons in the run, and re-run the "
            "engine or publish nothing."
        )
    if status not in FINISHED_STATUSES:
        cause = next((str(problem) for problem in _list(run.get("errors")) if problem), "")
        raise CommandError(
            f"This run ended in state {status} rather than "
            f"{' or '.join(FINISHED_STATUSES)}, so it is not a review."
            + (f" The run recorded: {cause}" if cause else "")
            + " Re-run the engine, or drop --publish to keep the bundle as a "
            "rehearsal."
        )
    # The stage ledger is the only thing that says whether every reader the arm
    # asked for actually reported. A run can reach `complete` with a stage
    # missing when the editor accepted the pool without it, and a bundle that
    # says three core reviewers and six specialists over a run where two of them
    # never answered is a claim about a panel that did not sit.
    ledger = _dict(run.get("completeness"))
    missing_stages = [str(s) for s in _list(ledger.get("missing"))]
    if missing_stages:
        raise CommandError(
            f"{len(missing_stages)} stage(s) the {run.get('arm')} arm requires "
            f"never reported: {', '.join(sorted(missing_stages))}. The bundle "
            "would describe readers that did not report. Re-run the review, or "
            "drop --publish to keep it as a rehearsal."
        )


def cmd_publish(args: argparse.Namespace) -> int:
    """Write the bundle from a finished engine run."""
    prepared_dir = Path(args.prepared).resolve()
    prepared = read_json(prepared_dir / "prepared.json")
    if args.publish and not prepared.get("publishable"):
        raise CommandError(
            "This paper was prepared from a local PDF with no permanent "
            "identifier, so it cannot be published. Prepare it again with "
            "--paper."
        )
    if args.decision not in DECISIONS:
        raise CommandError(f"--decision must be one of: {', '.join(DECISIONS)}")
    human_reviewed = args.human_reviewed == "yes"
    if args.publish and not human_reviewed:
        raise CommandError(
            "A review cannot be published unless the editor has read the run. "
            "Read it, then pass --human-reviewed yes."
        )
    # A rehearsal that carried a true attestation was a published record in
    # every respect except where it sat, so copying its folder into docs/reviews
    # by hand produced a review that passed every check. An attestation is a
    # claim attached to a publication, and a rehearsal makes no publication, so
    # the two cannot be asked for together.
    if human_reviewed and not args.publish:
        raise CommandError(
            "--human-reviewed yes is an attestation, which only a published "
            "review can carry. Add --publish to publish this run, or pass "
            "--human-reviewed no to rehearse the bundle."
        )

    run_dir = resolve_review_dir(Path(args.run))
    package = editor_package(run_dir)
    run = read_run(run_dir)
    if args.publish:
        require_complete_run(run_dir, run)
    workspace = resolve_workspace(run_dir, args.workspace)
    preprint_data = prepared.get("preprint")
    if preprint_data is None:
        raise CommandError("A bundle needs preprint metadata. Prepare with --paper.")
    preprint = Preprint(**preprint_data)

    # Before anything is written: is this a run of the paper that was prepared?
    binding = bind_run_to_input(prepared, workspace, run)
    if binding["workspace_manifest_sha256"]:
        prepared["input"]["workspace_manifest_sha256"] = binding["workspace_manifest_sha256"]
    ingest = ingest_record(workspace)

    # The fingerprint is the engine's own record of every file it loaded, taken
    # at the moment the run started, not a re-hash of whatever is installed now.
    # Taking it at publish time recorded the bytes of the machine writing the
    # bundle, which is not the claim the record makes.
    engine_source = run.get("engine_source")
    if not isinstance(engine_source, dict) or not engine_source:
        raise CommandError(
            f"{run_dir} records no source manifest, so the code that produced "
            "this review cannot be identified. The plugin server writes it to "
            "manifest.json at the start of a run."
        )
    fingerprint = code_fingerprint(engine_source, "run_manifest")
    plugin = plugin_record(engine_source, run)
    try:
        installed = installed_code_manifest()
    except CommandError:
        installed = None
    if installed is not None:
        fingerprint["matches_installed_engine"] = (
            code_fingerprint(installed, "installed_engine")["sha256"] == fingerprint["sha256"]
        )
        plugin["matches_installed_plugin"] = (
            installed.get(WORKFLOW_FILE) == plugin["workflow_sha256"]
        )

    runtime = maybe_json(run_dir / "runtime.json")
    agents = agent_rows(maybe_json(run_dir / "protocol.json"), package, runtime)
    # The transport is the run's own, read from the start-up probe the engine ran
    # before it spent anything. A run on a transport this path cannot publish is
    # refused here even when the bundle is only a rehearsal.
    transport = transport_record(
        provider=str(run.get("provider") or ""),
        runtime=runtime,
        startup=maybe_json(run_dir / "startup.json"),
    )

    dest = publish_destination(prepared, publishing=args.publish)
    route = f"v{prepared['draft']}/r{prepared['attempt']}"
    review_id = bundle_identifier(dest)
    provenance = build_provenance(
        preprint=preprint,
        prepared=prepared,
        package=package,
        run=run,
        fingerprint=fingerprint,
        plugin=plugin,
        agents=agents,
        decision=args.decision,
        editor=args.editor,
        human_reviewed=human_reviewed,
        route=route,
        draft=int(prepared["draft"]),
        attempt=int(prepared["attempt"]),
        submitter=args.submitter,
        submitter_is_author=args.submitter_is_author,
        baseline_eligible=args.baseline_eligible,
        ingest=ingest,
        transport=transport,
        review_id=review_id,
        publishing=args.publish,
    )

    # The engine's own output is copied into the bundle, and a run folder
    # records absolute paths in several places. Scrubbing happens before
    # anything is written, so the manifest hashes the file a reader will get.
    published_package = without_local_paths(package) if args.publish else package

    if args.publish:
        leaked = absolute_path_fields(provenance)
        if leaked:
            raise CommandError(
                "This record would publish absolute local paths at "
                f"{', '.join(leaked)}. A published record may not name the "
                "operator's filesystem."
            )

    # Every document is rendered from the scrubbed package. Rendering from the
    # unscrubbed one put the paths back: a reviewer's `source_review_path` was
    # dropped from the JSON and then printed in decision_letter.md, where no
    # scan was looking for it.
    findings = sorted_findings(published_package)
    reports = track_reports(run_dir)
    if dest.exists() and any(dest.iterdir()):
        raise CommandError(f"Refusing to overwrite an existing review bundle: {dest}")

    # The bundle is built outside the published tree and moved in once every
    # guard has passed. The guards used to run after six files had already been
    # written into docs/reviews, so a refusal left most of a bundle behind, with
    # no manifest and nothing saying it was rejected.
    with tempfile.TemporaryDirectory(prefix="local-review-bundle-") as staging:
        stage = Path(staging)

        (stage / "summary.md").write_text(
            render_summary(preprint, published_package, provenance, findings), encoding="utf-8"
        )
        (stage / "decision_letter.md").write_text(
            render_decision_letter(preprint, published_package, provenance, findings),
            encoding="utf-8",
        )
        (stage / "manuscript_stats.md").write_text(
            render_stats(preprint, ingest, provenance["generator"]), encoding="utf-8"
        )
        # The specialist reports, as each track wrote them. The site lists an
        # `audit_<track>.md` as a report of its own, so a reader can see what
        # the statistics reader looked for rather than only what the editor
        # agent kept from it.
        for name, path in reports.items():
            shutil.copyfile(path, stage / name)
        write_json(stage / "provenance.json", provenance)
        write_round_record(stage, preprint, provenance, findings)
        # Kept beside the documents so a reader can check a quotation against
        # the structured record the reviewers actually produced.
        write_json(stage / "editor-package.json", published_package)

        # Read back what is actually on disk before the manifest fixes it. This
        # is the check that cannot be fooled by a file nobody thought to scrub,
        # or by a field no version of this script knows the engine writes.
        if args.publish:
            leaked = bundle_local_path_leaks(stage)
            if leaked:
                raise CommandError(
                    "This bundle names the machine that produced it: "
                    f"{', '.join(leaked)}. Nothing was written to {dest}."
                )
        write_manifest(stage)

        dest.mkdir(parents=True, exist_ok=True)
        for path in sorted(stage.iterdir()):
            shutil.move(str(path), str(dest / path.name))

    print(f"bundle   {dest}")
    print(f"decision {provenance['decision']} (chosen by {args.editor})")
    print(
        f"findings {len(findings)} in the letter, "
        f"{provenance['generator']['run']['appendix_findings']} in the appendix"
    )
    print(f"reports  {len(reports)} specialist track report(s) copied in")
    print(
        f"baseline {'eligible' if provenance['review']['baseline_eligible'] else 'experimental only'}"
    )
    print(f"models   {model_phrase(provenance['models'])}")
    if run.get("specialist_tracks"):
        absent = [track for track in SPECIALIST_TRACKS if f"audit_{track}.md" not in reports]
        if absent:
            print(f"warning  no specialist report written for: {', '.join(absent)}")
    if not args.publish:
        print("rehearsal, written outside docs/reviews. Re-run with --publish to publish.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "fingerprint", help="Print the installed engine and plugin, calling no model"
    )
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("prepare", help="Resolve a paper, fetch its bytes, and plan the bundle path")
    p.add_argument("--paper", help="arXiv id, bioRxiv or medRxiv DOI, or an archive URL")
    p.add_argument("--pdf", help="Local PDF supplying the exact bytes for that identity")
    p.add_argument("--out", required=True, help="Empty folder for the fetched paper and the plan")
    p.add_argument(
        "--arm",
        default="full-two-track",
        help="The engine arm the review will run. Recorded here so the plan and "
        "the run can be compared, and taken from the run when the bundle is written",
    )
    p.add_argument("--reviewers", type=int, default=3, help="Core reviewers the review will run")
    p.add_argument("--literature-cutoff", default="")
    p.add_argument(
        "--replace", action="store_true", help="Allow a new attempt on an already reviewed draft"
    )
    p.set_defaults(func=cmd_prepare)

    p = sub.add_parser("publish", help="Write a review bundle from a finished engine run")
    p.add_argument("--prepared", required=True, help="The folder prepare wrote")
    p.add_argument(
        "--run",
        required=True,
        help="The folder `peerreview review` wrote, or the review folder inside it",
    )
    p.add_argument(
        "--workspace",
        default="",
        help="The imported manuscript workspace. Defaults to the manuscript "
        "folder beside the run, whose paper.json is what ties this run to the "
        "paper that was prepared",
    )
    p.add_argument(
        "--decision",
        required=True,
        choices=DECISIONS,
        help="The editor's decision, not the engine's",
    )
    p.add_argument(
        "--editor",
        required=True,
        help="Who read the run and chose the decision. Published in the record, "
        "because an attestation with nobody behind it attests to nothing",
    )
    p.add_argument(
        "--human-reviewed",
        required=True,
        choices=("yes", "no"),
        help="Has the named editor read this run in full. There is no default. "
        "Answering no writes a rehearsal bundle that cannot be published",
    )
    p.add_argument(
        "--submitter", default="", help="GitHub login of the submitter, when there is one"
    )
    p.add_argument(
        "--submitter-is-author",
        default="",
        choices=("", "yes", "no"),
        help="What the submitter claimed about their connection to the paper. "
        "Unverified either way, and recorded only with --submitter",
    )
    p.add_argument(
        "--baseline-eligible",
        action="store_true",
        help="Let this review set the paper's editorial status. Off by default, "
        "because no human read the manuscript",
    )
    p.add_argument(
        "--publish", action="store_true", help="Write into docs/reviews rather than runs"
    )
    p.set_defaults(func=cmd_publish)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except CommandError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
