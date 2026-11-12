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
import getpass
import hashlib
import html
import importlib
import importlib.metadata
import json
import os
import re
import shlex
import shutil
import socket
import sys
import tempfile
import unicodedata
import urllib.parse
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

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
from review_schema import InvalidProvenance, assert_valid_provenance  # noqa: E402

ENGINE_PACKAGE = "peerreviewagents"
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

# The two states a run can finish in, which are the engine's own
# `COMPLETE_STATUSES`. `complete` is a review with findings in it, and
# `complete-without-findings` is a review written with none. Neither is a
# failure, so neither is listed as an error on the page. Whether a finished run
# may be published is not read off the status here: the engine answers that in
# `publishable`, because the same status covers a manuscript the reviewers
# raised nothing about and a review the guards emptied, and only the engine
# knows which of the two it wrote.
FINISHED_STATUSES = ("complete", "complete-without-findings")
# The two guard verdicts the engine writes, and the only two a record may
# carry. `clean` is a run the guards took nothing from, and `quarantined` is one
# they took something from, however much: the guards throwing out a finding they
# could not anchor is the guards working, so such a run still publishes and the
# bundle says how many were held back.
CLEAN_GUARD = "clean"
QUARANTINED_GUARD = "quarantined"
GUARD_VERDICTS = (CLEAN_GUARD, QUARANTINED_GUARD)
# The finished state for a review written with no findings in it. Named so the
# documents can say plainly that the reviewers raised nothing make-or-break,
# which is a result rather than a failed run. It is not a gate: a run of this
# status whose guards quarantined findings is held back by the engine, and the
# reason it gives names the count.
WITHOUT_FINDINGS_STATUS = "complete-without-findings"

# insilico publishes Claude Code runs only. Every claim a bundle makes about how
# the review was paid for is a claim about a Claude subscription, and the only
# transport this path can describe is the one the plugin runs on.
PUBLISHABLE_PROVIDERS = ("claude-code",)

# The engine arms that are not a review of somebody else's manuscript, and so
# are not a thing this path can publish as one. `draft-check` is what the engine
# runs on a draft of your own: the engine's own arm table calls it "not a study
# arm", it convenes no core reviewers, and nothing in it was written by a reader
# of a submitted paper.
#
# It has to be named here because the engine does not hold such a run back. Its
# publishability rule reads the status, the findings source and the guards, none
# of which a finished draft check fails, so `not_publishable_reasons` comes back
# empty for one and there is no engine sentence to print. What refused it before
# was the panel rule further down, "a published review needs at least one
# reviewer", which is true but reads as a broken run rather than as the wrong
# kind of run, and it would stop refusing the moment an arm with no reviewers
# became publishable for some other reason.
UNPUBLISHABLE_ARMS = ("draft-check",)

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
    """What one run file holds, or nothing when it holds nothing readable.

    `JSONDecodeError` is a `ValueError`, and so is the `UnicodeDecodeError` a
    file of bytes that are not UTF-8 raises on the way in. Catching the base
    class covers both, so a manifest.json or startup.json written by something
    other than the engine is refused by the caller that needed it rather than
    ending the command in a traceback.
    """
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        value = read_json(path)
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _list(value: object) -> list:
    return value if isinstance(value, list) else []


def engine_module(why: str):
    """The engine package, imported late, or a refusal naming what is missing.

    Late because most of the checks in this repository never read a run and
    have to pass with no engine installed at all, and in one place so that
    every refusal for a missing engine says the same thing.
    """
    try:
        return importlib.import_module(ENGINE_PACKAGE)
    except ImportError as exc:
        raise CommandError(
            f"{ENGINE_PACKAGE} is not importable, so {why}. Install "
            "PeerReviewAgents 0.9.0 or newer, or run this with the virtual "
            "environment the review ran in."
        ) from exc


def engine_public(name: str, why: str):
    """One name from `peerreviewagents.__all__`, or a refusal naming the gap.

    Everything this file needs from the engine is in that list. Nothing here
    reaches into `peerreviewagents.plugin` or `peerreviewagents.cli`: those are
    the engine's own internals, free to move between releases, and a publish
    path that imported one broke on an upgrade rather than on a change to the
    surface the engine supports.
    """
    engine = engine_module(why)
    try:
        return getattr(engine, name)
    except AttributeError as exc:
        raise CommandError(
            f"{ENGINE_PACKAGE}.{name} is not importable, so {why}. Install "
            "PeerReviewAgents 0.9.0 or newer, or run this with the virtual "
            "environment the review ran in."
        ) from exc


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

    The plugin tree is where `peerreviewagents.plugin_directory()` says it is,
    which is the engine's own answer and the one the starter passes the
    session. The two Python trees are read beside the installed package, under
    the names the server writes them under, so the three keys here and the three
    keys in a run's manifest mean the same files.
    """
    why = "the installed plugin cannot be fingerprinted"
    root = Path(engine_module(why).__file__).resolve().parent
    plugin_root = Path(engine_public("plugin_directory", why)()).resolve()
    files: dict[str, str] = {}
    for path in sorted(plugin_root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            files[PLUGIN_PREFIX + path.relative_to(plugin_root).as_posix()] = digest(
                path.read_bytes()
            )
    for path in sorted((root / "engine").glob("*.py")):
        files["engine/" + path.name] = digest(path.read_bytes())
    for path in sorted((root / "plugin").glob("*.py")):
        files["plugin-python/" + path.name] = digest(path.read_bytes())
    if not files:
        raise CommandError(f"The engine at {root} has no source files to fingerprint")
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


def transport_record(
    *, provider: str, runtime: dict, startup: dict, verified_at: str | None = None
) -> dict:
    """Which harness ran the agents, taken from the run rather than probed.

    `provider` is the transport the run itself recorded, so the record cannot
    name one transport while the run used another. Anything outside
    `PUBLISHABLE_PROVIDERS` is refused here, before any record is written.

    `startup` is the engine's reading of the probe, which is `probe` and
    `problems`, and `verified_at` is when the probe ran. They are separate
    arguments because the reading carries the first two and not the third.

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
    problems = [str(p) for p in _list(startup.get("problems")) if str(p).strip()]
    if problems:
        raise CommandError(
            "The run's start-up probe reported "
            f"{len(problems)} problem(s): {'. '.join(p.rstrip('.') for p in problems)}. "
            "A run that could not load the plugin cannot be published as a "
            "review the plugin produced."
        )
    # A run with no startup.json, and a run whose startup.json holds something
    # other than a probe, both read back as a null probe. Either way there is no
    # evidence a Claude Code session ever started, and the engine writes that
    # evidence before it spends anything.
    if startup.get("probe") is None:
        raise CommandError(
            "This run recorded no start-up probe, so there is no evidence a "
            "Claude Code session ever started. The engine writes one to "
            "startup.json before it spends anything. Point --run at the folder "
            "`peerreview review` wrote."
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
        "verified_at": str(verified_at or "") or None,
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


def agent_rows(reading: dict) -> list[dict]:
    """One row per agent that ran, as the engine read them back.

    `read_run` merges the protocol's slots with what the harness observed and
    gives each one a `slot`, `role`, `track`, `model`, `assigned_model`,
    `attempt`, `tool_calls`, `session_calls`, `tokens`, `state` and `labels`.
    Two facts the published record wants are not in those rows and are counted
    here: how many findings a slot delivered, which the findings themselves say,
    and whether it reported nothing, which the stage ledger says.

    `model` and `assigned_model` are two facts and one is never written in the
    other's place. `assigned_model` is the model the run asked that slot to run,
    which the plugin server writes into protocol.json before anything runs.
    `model` is what was observed running, from the harness stream and the
    agent's own report, and a slot that reported none has no `model` at all.
    Filling that gap from the plan would hide the one thing the pair exists to
    show, which is a slot that ran something other than what it was asked for.

    One agent is one row in 0.9, and nothing is filtered out here. The engine
    merges the tasks one agent ran into that agent's own row, with `labels`
    saying which they were, and it leaves out the harness's placeholder rows for
    agents it never ran. An earlier version of this function dropped rows that
    carried nothing but a label, to keep five empty reviewers off a published
    panel. Doing that now would drop a real slot the arm asked for and the run
    never filled, which is the row most worth seeing.
    """
    delivered: dict[str, int] = {}
    for finding in _list(reading.get("findings")):
        slot = str(_dict(finding).get("slot") or "")
        if slot:
            delivered[slot] = delivered.get(slot, 0) + 1
    silent = {str(s) for s in _list(_dict(reading.get("stages")).get("none_found"))}
    rows = []
    for observed in _list(reading.get("agents")):
        observed = _dict(observed)
        slot = str(observed.get("slot") or "")
        if not slot:
            continue
        row = {
            "slot": slot,
            "role": observed.get("role"),
            "track": observed.get("track"),
            "attempt": observed.get("attempt"),
            # The server's own count of what it served the slot, and the
            # session's larger count only when the server recorded none.
            "tool_calls": observed.get("tool_calls") or observed.get("session_calls"),
            "model": observed.get("model"),
            "assigned_model": observed.get("assigned_model"),
            "state": observed.get("state"),
            "tokens": observed.get("tokens"),
            "findings": delivered.get(slot, 0),
            "none_found": slot in silent,
        }
        rows.append({key: value for key, value in row.items() if value not in (None, "")})
    return sorted(rows, key=lambda row: str(row["slot"]))


def model_map(agents: list[dict]) -> dict[str, str]:
    """Which model wrote which report, keyed by the slot that wrote it.

    This is the site's model table, and every entry in it was observed: it is
    what each slot reported running, never what the run asked it to run. A slot
    nobody observed is absent rather than filled in from the plan, because the
    plan is a different fact and lives in `assigned_map`.

    A run on this path has a real per-slot split, because 0.9 gives each slot
    its own model, so the table says something rather than repeating one id down
    a column.
    """
    return {
        str(row["slot"]): str(row["model"])
        for row in agents
        if row.get("slot") and row.get("model")
    }


def assigned_map(agents: list[dict]) -> dict[str, str]:
    """Which model each slot was asked to run, keyed by slot.

    The plan, written down before anything ran. It is published beside the
    observed map rather than merged into it, because the two disagreeing is the
    most important thing a reader of the panel can be told, and a record that
    carried one number for both could not say it. Empty for a run written before
    0.9, which recorded no plan at all.
    """
    return {
        str(row["slot"]): str(row["assigned_model"])
        for row in agents
        if row.get("slot") and row.get("assigned_model")
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


def completeness(stages: dict) -> dict:
    """The stage ledger, which is what says whether the review is whole.

    The server keeps a ledger of the stages a run requires and the ones that
    reported, and `read_run` hands it back as `stages`. A run can reach
    `complete` with a stage that never reported only when the editor accepted
    the pool without it, so the counts and the acceptance travel together in
    the record.
    """
    stages = _dict(stages)
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


def engine_reading(run_dir: Path) -> dict:
    """The engine's own reading of a run folder, which is the only way in.

    `peerreviewagents.read_run` is the engine's supported surface for a folder
    on disk. It returns the same keys for every run, finished or killed or
    never started, names each file it could not read in `problems` rather than
    raising, and answers `publishable` itself. Nothing here opens a run file
    that it covers: a second reader beside it is a second status rule, and the
    two would disagree the first time the engine changed one.

    It raises for the two things that are not a damaged run: a folder that is
    not a run at all, and a run file that is a symlink, which is some other
    file's contents offered as this run's result. Both become refusals here.
    """
    reader = engine_public("read_run", "a run folder cannot be read")
    try:
        reading = reader(str(Path(run_dir)))
    except ValueError as exc:
        raise CommandError(
            f"The engine refused to read {run_dir}: {exc} Point --run at the "
            "folder `peerreview review` wrote."
        ) from exc
    if not isinstance(reading, dict):
        raise CommandError(f"{ENGINE_PACKAGE}.read_run returned no reading for {run_dir}")
    return reading


def startup_stamp(reading: dict) -> str | None:
    """When the start-up probe ran, the one field `read_run` does not carry.

    0.9 exposes the probe itself and the problems it reported, as
    `startup['probe']` and `startup['problems']`, and the code map and the
    transport as `identity['code_hashes']` and `identity['provider']`. All four
    used to be read out of the run folder here and are now taken from the
    reading, which leaves this: the moment the starter wrote `startup.json`,
    which the published record carries as `verified_at` because it is when the
    evidence for the transport claim was gathered. It is read from the file
    rather than invented, and a run without it publishes with a null.

    The file is taken from `reading['files']`, which is the engine's own map of
    the run files it found, rather than by joining `startup.json` onto the run
    folder here. Joining the name was this script deciding where the engine
    keeps a file: the reading already says where it is, and a run folder with no
    `startup.json` is absent from that map instead of being opened and missed.
    """
    stamped = _dict(reading.get("files")).get("startup.json")
    if not stamped:
        return None
    return str(maybe_json(Path(str(stamped))).get("at") or "") or None


def review_package(reading: dict) -> dict:
    """The editor's review, in the shape the documents are rendered from.

    `read_run` returns the editor's placement and judgement as separate keys,
    de-duplicated per `finding_uid` and with a finding the editor put in both
    lists counted once. This gathers them back into one record, which is what
    the bundle publishes beside the documents so a reader can check a quotation
    against the structured finding it came from.
    """
    return {
        "findings": _list(reading.get("body")),
        "appendix": _list(reading.get("appendix")),
        "summary": reading.get("summary"),
        "verdict": _dict(reading.get("verdict")),
        "limitations": _list(reading.get("limitations")),
        "escalation_rulings": _list(reading.get("escalation_rulings")),
        "review_guard_status": reading.get("guard_status"),
        "findings_source": reading.get("findings_source"),
        "quarantined_findings": _list(reading.get("quarantined")),
    }


def read_run(run_dir: Path) -> dict:
    """The run record for one folder, read through the engine."""
    return run_record(engine_reading(run_dir))


def run_record(reading: dict) -> dict:
    """What the run recorded, kept for the published record.

    Every value here comes from the engine's reading, and a value the run did
    not record is left out rather than defaulted, so a caller that needs one has
    to say so rather than silently inherit it from the prepare step or a publish
    flag. The transport and the code map are part of that reading in 0.9, as
    `identity['provider']` and `identity['code_hashes']`, and a run file damaged
    enough that the engine could not read either of them is named in `problems`
    and carried into the record there.
    """
    identity = _dict(reading.get("identity"))
    counts = _dict(reading.get("counts"))
    runtime = _dict(reading.get("runtime"))
    review_dir = Path(str(reading.get("review") or ""))

    record: dict = {}
    # A published record is read by strangers, and an absolute path in it
    # describes the machine that wrote it rather than the review. The path is
    # recorded when it is inside this repository and left out otherwise.
    if review_dir.is_absolute() and review_dir.is_relative_to(REPO):
        record["directory"] = review_dir.relative_to(REPO).as_posix()

    def put(key: str, value: object) -> None:
        if value not in (None, "", [], {}):
            record[key] = value

    put("arm", identity.get("arm"))
    put("workflow_version", identity.get("workflow_version"))
    put("finding_schema_version", identity.get("finding_schema_version"))
    put("provider", str(identity.get("provider") or ""))
    if isinstance(identity.get("reviewers"), int):
        record["reviewers"] = identity["reviewers"]
    put("specialist_tracks", [str(t) for t in _list(identity.get("specialists"))])
    # The ordered list the core reviewers were drawn from, and the slots whose
    # assigned model nothing ever observed. Both are the engine's own answers
    # rather than a second copy of its rules here: `models_unverified` decides
    # which slots the page has to admit it cannot vouch for, and getting that
    # rule subtly different here would have the page and the engine's own
    # REVIEW.md say different things about the same folder.
    put("reviewer_models", [str(m) for m in _list(identity.get("reviewer_models"))])
    put("models_unverified", [str(s) for s in _list(identity.get("models_unverified"))])
    put("paper_id", identity.get("paper_id"))
    put("literature_cutoff", identity.get("literature_cutoff"))
    put("claude_code_version", identity.get("claude_code_version")
        or runtime.get("claude_code_version"))
    put("engine_source", _dict(identity.get("code_hashes")))
    put("status", reading.get("status"))
    # The engine's own answer to the only question the publish gate asks, kept
    # in the record so a reader of the bundle sees the same flag the gate did.
    record["publishable"] = bool(reading.get("publishable"))
    put("findings_source", reading.get("findings_source"))
    put("cause", reading.get("cause"))
    put("note", reading.get("note"))
    put("problems", [str(p) for p in _list(reading.get("problems"))])
    # Kept because the status alone does not say whether the guards took
    # anything. A manuscript nobody found fault with is `clean` with no
    # findings, and a review the guards pulled a row out of is `quarantined`,
    # with the count of what they held back beside it.
    put("review_guard_status", reading.get("guard_status"))
    for key in ("findings_delivered", "findings_submitted"):
        if isinstance(counts.get(key), int):
            record[key] = counts[key]
    if isinstance(counts.get("quarantined"), int):
        record["quarantined_findings_count"] = counts["quarantined"]
    record["escalated_count"] = len(_list(reading.get("escalations")))
    # Counted from the findings rather than taken from a summary field, so the
    # table on the page and the findings beside it cannot disagree.
    by_track: dict[str, int] = {}
    for finding in _list(reading.get("findings")):
        track = str(_dict(finding).get("track") or "")
        if track:
            by_track[track] = by_track.get(track, 0) + 1
    put("findings_by_track", by_track)
    for key in ("wall_seconds", "tokens_total"):
        if isinstance(runtime.get(key), (int, float)):
            record[key] = runtime[key]
    put("completeness", completeness(reading.get("stages")))
    record["errors"] = run_errors(reading)
    return record


def run_errors(reading: dict) -> list[str]:
    """What the run recorded going wrong, rather than an empty list by default.

    `read_run` already decides why a run that is not complete stopped, so the
    cause is taken from it rather than re-derived. What this adds is the harm a
    finished run can still carry: a reader that never reported, an editor that
    did not accept the pool, a file the engine could not read in full, and
    whatever the engine itself holds the run back for.

    Finishing with no findings is not one of these. A run whose reviewers read
    the manuscript and raised nothing make-or-break is a review, which the
    engine finishes as `complete-without-findings` with the guard status
    `clean`, and listing that as an error told a reader a review of a sound
    manuscript had gone wrong. A reviewer that reported no findings on its track
    is the same, which is why `none_found` is recorded and not listed here.

    Nor is a finding the guards quarantined. The guard exists to throw out a
    finding whose quote it could not match to the manuscript, and doing so is
    the guard working rather than the run failing, which is why the engine
    publishes such a run. The count is carried in the record and shown on the
    page as what was held back, so a reader sees it without it being filed
    under what went wrong.

    The one place a guard verdict becomes an error is a review the guards
    emptied, and that is not decided here either: the engine refuses such a run
    in `not_publishable_reasons`, naming how many it held, and those sentences
    are copied in whenever the engine holds a run back for any reason at all.
    """
    errors: list[str] = []
    for value in (reading.get("cause"), reading.get("note")):
        if str(value or "").strip():
            errors.append(str(value).strip())
    status = str(reading.get("status") or "")
    if status and status not in FINISHED_STATUSES:
        errors.append(f"The run finished in state {status}.")
    # The engine's own sentences for a run it will not call publishable, in its
    # words rather than a second copy of its rules here. This is how a review
    # the guards emptied gets named as the harm it is while a review that
    # raised nothing does not: the engine tells the two apart, and this file
    # does not have to.
    if not reading.get("publishable"):
        for reason in _list(reading.get("not_publishable_reasons")):
            text = str(reason).strip()
            if text and text not in errors:
                errors.append(text)
    stages = _dict(reading.get("stages"))
    missing = [str(s) for s in _list(stages.get("missing"))]
    if missing:
        errors.append(
            f"{len(missing)} required stage(s) never reported: {', '.join(sorted(missing))}."
        )
    if stages and not stages.get("editor_accepted"):
        errors.append("The editor stage did not accept the pooled findings.")
    # A file the engine read only in part is a number nobody should quote, so
    # the record carries the engine's own list of them.
    for problem in _list(reading.get("problems")):
        text = str(problem).strip()
        if text and text not in errors:
            errors.append(text)
    return errors


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
    and no single model: each slot is assigned its own, and the record carries
    both that plan and what was observed to run.

    `models` is the observed map, which is the only thing this paragraph is
    allowed to describe as having written the review. Where a slot's model was
    never observed, the paragraph says so rather than quoting the plan as though
    somebody had watched it hold.
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

    ran = (
        f"and the models observed running were {model_phrase(models)}"
        if models
        else "and no slot's model was observed, so the record cannot say what ran"
    )
    unverified = [str(slot) for slot in _list(run.get("models_unverified"))]
    gap = ""
    if unverified:
        one = len(unverified) == 1
        gap = (
            f" The model that ran was not recorded for {len(unverified)} "
            f"{'slot' if one else 'slots'} ({', '.join(unverified)}), so for "
            f"{'it' if one else 'those'} the plan is all this record has."
        )
    return (
        f"{shape} Every agent ran inside one Claude Code session on the editor's "
        "own machine, on a subscription. The run assigned each slot a model of "
        f"its own, {ran}.{gap} There was no desk screen and no debate stage, and "
        "agents sharing a model are not independent corroboration of one another."
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


def no_findings_note(run: dict) -> str:
    """What a review with no findings in it says for itself, in plain words.

    An empty findings list reads like a run that broke, and most of the time it
    is the opposite: every reader the arm asked for reported and none of them
    raised anything that has to be fixed before the paper stands. The engine
    finishes such a run as `complete-without-findings`, publishes it like any
    other review, and this is the sentence that says so on the page rather than
    leaving a reader to infer it from a zero.

    A review the evidence guards emptied is the other way to reach that status
    and means the opposite, so it gets its own sentence. Publish refuses one, so
    it is only ever read here in a rehearsal bundle.
    """
    held = run.get("quarantined_findings_count")
    held = held if isinstance(held, int) else 0
    if held:
        return (
            f"No finding reached this letter, and the evidence guards held {held} "
            "back, so what the reviewers raised is not in this review. That is "
            "not a manuscript the panel found sound, and it is why publishing "
            "refuses a run in this state."
        )
    return (
        "The reviewers raised no make-or-break findings against this "
        "manuscript. Every core reviewer and specialist reader the arm asked "
        "for reported, the editor agent wrote the package, and nothing came "
        "back that has to be fixed before the paper stands. An empty findings "
        "list here is that result, not a run that went wrong."
    )


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
    if not findings and not appendix:
        lines += ["## What the review found", "", no_findings_note(run), ""]
    if findings:
        lines += ["## Findings in the letter", ""]
        for number, finding in enumerate(findings, 1):
            title = str(finding.get("title") or "Untitled finding").strip()
            lines.append(f"{number}. **{title}** ({_tags(finding)})")
        lines.append("")
    if appendix:
        lines += [
            "## Findings in the appendix",
            "",
            "Accepted by the editor agent and kept out of the letter's body, "
            "which the workflow caps at a fixed number of findings.",
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
            no_findings_note(provenance["generator"]["run"]),
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

    One file per known track, asked for by name. This used to glob `audit_*.md`,
    which published whatever happened to sit in the run folder under that
    prefix: a note somebody dropped there, a file an operator wrote while
    debugging, or a report from a track this repository does not know and cannot
    label. The page shows a report with no track as an unnamed one, so a file
    this list does not name is left where it is.
    """
    run_dir = resolve_review_dir(run_dir)
    candidates = ((f"audit_{track}.md", run_dir / f"audit_{track}.md") for track in SPECIALIST_TRACKS)
    return {
        name: path for name, path in candidates if path.is_file() and path.stat().st_size
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
    allowed_text: Sequence[str] = (),
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
    assigned = assigned_map(agents)
    if not models:
        raise CommandError(
            "No agent in this run was observed running a model, so the record "
            "cannot say what wrote the review. The plan is not an answer to "
            "that: the models the run asked for are in protocol.json and what "
            "each slot reported running is in runtime.json, and only the second "
            "of those says anything about the review that exists."
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
    review = {
        "id": review_id,
        "manuscript_version": draft,
        "attempt": attempt,
        "kind": kind,
        "lifecycle": "active",
        "baseline_eligible": baseline_eligible,
        "route": route,
    }
    if allowed_text:
        # What the editor allowed past the tier 2 leak scan, recorded because an
        # allowance is an editorial decision and not a setting. Each string is
        # text the scan read as a local path or an address, which the editor
        # then read and judged to be the review's own words. Published here, a
        # reader of the page can see exactly what was waived and disagree. It
        # never covers a machine fact, so nothing in this list is a path on the
        # editor's disk that the scan would otherwise have stopped.
        review["allowed_text"] = [str(text) for text in allowed_text]
    return {
        "schema_version": PROVENANCE_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "insilico": insilico_version(),
        "generator": generator,
        "review": review,
        "provider": provider,
        # Which model wrote which report, keyed by the slot that wrote it, and
        # beside it the model each slot was asked to run. Two fields because
        # they are two facts: `models` was observed and `assigned_models` is the
        # plan, a slot can be missing from the first while the plan for it
        # stands in the second, and a slot that ran a different family is a run
        # the engine refuses rather than a record that quietly reconciles them.
        # The site reads exactly these fields when it says what wrote each
        # report and what was asked for.
        "models": models,
        "assigned_models": assigned,
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


# What a version actually looks like: a number, a dot, a number, at the start,
# with an optional `v`. Claude Code prints `2.0.14 (Claude Code)`, which matches,
# and every refusal a broken install prints instead does not.
VERSION_SHAPE = re.compile(r"^v?\d+\.\d+")


def claude_version() -> str | None:
    """What `claude --version` prints, through the engine's own resolver.

    `peerreviewagents.claude_code_version()` is that resolver, and in 0.9 it
    answers `None` rather than raising when Claude Code is not on PATH. The
    guards here are for the engine being absent altogether, because this is
    reported rather than required and never a review: the preflight is allowed
    to say the harness is missing, which is more useful than refusing to print
    the fingerprint the operator asked for.

    The resolver returns the first line of the command's output, standard error
    included, and does not look at its exit status. A CLI that is on PATH but
    will not run answers with its complaint, and the fingerprint recorded that
    complaint as the version of the harness: `transport.version` read
    `"claude: error while loading shared libraries"`. Only something shaped like
    a version is kept, so a broken harness reports no version, which is what the
    line beneath the record already knows how to say.
    """
    try:
        resolver = engine_public("claude_code_version", "the harness cannot be named")
    except CommandError:
        return None
    try:
        version = resolver()
    except Exception:  # noqa: BLE001 - a preflight must not fail on a missing CLI
        return None
    reported = str(version or "").strip()
    return reported if VERSION_SHAPE.match(reported) else None


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


# Everything that names the machine a review was produced on rather than the
# review itself. The scan has two tiers, and they are refused differently.
#
# Tier 1 is the specific machine facts: a detected path with two segments or
# more (the home directory, this checkout, the run folder, and the working or
# temporary directory when either is that deep) and a host name carrying a
# digit, a hyphen or a dot. Each is refused wherever it appears, as a plain
# case-insensitive substring: no lookbehind, no lookahead, no field it is not
# read in, in every string and every dictionary key at any depth, in rendered
# prose and in a sentence quoted from the manuscript. Nothing waives one, not
# the paper and not a flag, because a published page that repeats one names the
# operator whatever the reason it got there.
#
# A substring, not a bounded match, because every boundary turned out to be a
# hole. `/home/ty` with a boundary on the left published `file:/home/ty/x.pdf`,
# `box:/home/ty/x`, `//home/ty/x`, `a~/home/ty/x` and
# `http://localhost:8000/home/ty/x`; `ty-ms-7c80` with one published
# `node.ty-ms-7c80` and `run_ty-ms-7c80_1`; and the fields a fact was not read
# in published the host name as a JSON key and as an `id`. None of that needs
# protecting from a substring test, because `/home/ty` and `ty-ms-7c80` cannot
# occur in a review of a paper, in this repository's own vocabulary, or in
# anything but a reference to this machine.
#
# What made the boundaries seem necessary was treating the generic facts as
# tier 1 as well: a one-segment path (`/tmp`, `/data`, `/root`), a host that is
# one plain alphabetic word (`media`, `core`, `editor`, `localhost`) and the
# bare user name. Those are words. A word is not a leak, and an unwaivable rule
# built on one refused `temperature/tmp ratio`, `training/data/test`, `$2\pi$`
# from a user called `pi`, `train/test split` from one called `test`, and every
# publish at all from a machine called `editor`, whose name is in the record's
# own vocabulary. So they are not facts now. They are covered by tier 2, through
# the shapes below: a path under a known root, a host after `@`, `//` or `\\` or
# before `:/`, and a user name directly after a home root. Refused by default,
# waivable when the refusal is wrong.
#
# Tier 2 is the patterns, which describe the shape of a path rather than any
# known one. A pattern fires only on something hard to read as anything but a
# local path: an absolute path whose first segment is a directory a machine of
# this kind actually has, a home relative path, a `$HOME` path, a file URL, a
# Windows share, a Windows path with a drive letter and at least two segments
# after it, or a mail address. `/etc/hosts` and the link target in
# `[x](/reviews/2026/foo/v1)` name nothing about the operator, so neither is a
# leak, and `mAP@0.5`, `IoU@0.75`, `(events)/person/year`, `5 mg /kg/day`,
# `$f:\mathbb{R}$` and `E:/Z` are a specialist's notation rather than a
# filesystem. A mail address has to end in an alphabetic top level domain, or
# name a machine outright, which is what tells `someone@example.org` and
# `bob@localhost` from `mAP@0.5`.
#
# A tier 2 hit is refused by default and can be allowed. Text printed in the
# manuscript is allowed by itself, because publishing a review cannot be refused
# for repeating the paper's own words, and any other tier 2 hit can be allowed
# by the editor reading it and passing `--allow-text='<the exact text>'` to
# publish, repeatable. Every allowance is written into the provenance record and
# printed on the published page, so a reader can see what was waived and judge
# it. That valve is why tier 2 only has to be sensible rather than perfect: a
# pattern that fires on `R:/G/B channel order` costs an editor one flag, where a
# tier 1 fact that fires on an ordinary word costs them every publish.
#
# No allowance reaches tier 1. A hit that contains a specific fact is reported
# as tier 1 from the start, with no flag offered, and an `--allow-text` value
# that contains one is refused by the same substring test rather than quietly
# failing to waive anything: `--allow-text='file:///<checkout>/scripts/x.py'`
# was an editor asking to publish this checkout's path by naming more of it
# than the fact does.
#
# The roots are the directories a path on a machine of this kind starts with.
# `home` and `Users` are where people keep their files, `mnt`, `media`, `data`,
# `srv`, `Volumes`, `scratch`, `workspace` and `nfs` are where drives, shares
# and cluster space are attached, and `tmp`, `var`, `root`, `opt` and `private`
# are the rest of a filesystem a run folder gets written under. They are matched
# without regard to case, because the same directory is `/Users` on one machine
# and `/users` on another. `usr` and `run` are deliberately absent: `/usr/bin`
# names nothing about the operator, and both read as a word in a sentence often
# enough to refuse ordinary review text.
LOCAL_ROOTS = (
    "home",
    "Users",
    "mnt",
    "tmp",
    "var",
    "root",
    "opt",
    "srv",
    "media",
    "data",
    "private",
    "Volumes",
    "scratch",
    "workspace",
    "nfs",
)

# One segment of a path, as any of these systems spells it. A segment stops at
# whitespace, at a quote, and at the punctuation that ends a sentence around a
# path rather than belonging to it.
_SEGMENT = r"[\w.+~%-]+"
# The first segment after a `~`, which may not start with a digit. `~1/3 of the
# cohort` is a fraction written the way a reviewer writes one, not a path in
# somebody's home directory.
_FIRST_SEGMENT = r"[A-Za-z._][\w.+~%-]*"
# A share host, which starts with a letter.
_HOST_SEGMENT = r"[A-Za-z][\w.-]*"
_ROOTS = f"(?i:{'|'.join(LOCAL_ROOTS)})"

LOCAL_REFERENCE_PATTERNS = (
    (
        "an absolute path",
        # A leading slash or two, then one of the roots, then at least one more
        # segment. A slash after a word character or a dot is prose or
        # arithmetic, so neither opens a path. A colon does: `host:/home/bob/x`,
        # `file:/home/bob/x.pdf` and `PATH=/usr/bin:/home/bob/bin` are all
        # paths, and refusing to see a path after a colon left the commonest way
        # one gets quoted unscanned. What a colon must not do is open a URL, so
        # the two-slash form, and only that form, refuses a colon in front of
        # it: `https://home/x` is a URL and `//home/x` is a path.
        re.compile(rf"(?:(?<![\w~./:])//|(?<![\w~./])/){_ROOTS}(?:/{_SEGMENT})+/?"),
    ),
    ("a file URL", re.compile(r"file://[^\s\"'<>)\]]+")),
    (
        "a path in a home directory",
        re.compile(rf"(?<![\w/])~(?:{_SEGMENT})?/{_FIRST_SEGMENT}(?:/{_SEGMENT})*"),
    ),
    (
        "a path under $HOME",
        re.compile(rf"\$(?:HOME|\{{HOME\}})/{_SEGMENT}(?:/{_SEGMENT})*"),
    ),
    (
        "a Windows share",
        # `\\host\share\...`, where the host starts with a letter and the whole
        # match ends at a boundary. LaTeX is full of double backslashes:
        # `\begin{pmatrix}1\\0\end{pmatrix}` read as a share called `0` holding
        # a directory called `end`, so a review of a paper with a matrix in it
        # could not be published. The closing boundary is part of the fix rather
        # than decoration, because without it the engine backtracks to `en` and
        # matches anyway.
        re.compile(
            rf"(?<![\w}}\\])\\\\{_HOST_SEGMENT}\\{_SEGMENT}"
            rf"(?:\\{_SEGMENT})*(?![\w.+~%{{-])"
        ),
    ),
    (
        "a Windows path",
        # A drive letter in either case and at least two segments after it. The
        # letter used to have to be upper case, which published
        # `c:\Users\bob\x.pdf`, and the separator had to be a single character,
        # which published the `C:\\Users\\bob\\x.pdf` that JSON hands back. Two
        # segments is what keeps `$f:\mathbb{R}$` and the matrix entry `E:/Z`
        # publishable. It is also why `R:/G/B channel order` and `E:/I/G ratio`
        # are refused: three segments of an RGB ordering look exactly like a
        # path, and an editor who reads one can pass --allow-text for it.
        re.compile(rf"(?<![\w:])[A-Za-z]:[\\/]+{_SEGMENT}(?:[\\/]+{_SEGMENT})+"),
    ),
    (
        "an email address",
        re.compile(r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    ),
    (
        "an email address on this machine",
        # Neither of these ends in a dotted domain, so the pattern above never
        # saw them. `bob@localhost` and `bob@192.168.1.4` name an account on a
        # machine rather than a person at an institution, which is exactly the
        # thing a published page must not carry.
        re.compile(r"[\w.+-]+@localhost(?![\w.-])", re.IGNORECASE),
    ),
    (
        "an email address at an IP address",
        re.compile(r"[\w.+-]+@(?:\d{1,3}(?:\.\d{1,3}){3}(?![\w.])|\[[0-9A-Fa-f:.]+\])"),
    ),
)

class Fact(NamedTuple):
    """One string that names this machine, with the rule for finding it.

    `specific` is the tier. A specific fact is one that cannot be read as
    anything but this machine, so it is matched as a plain substring everywhere
    and nothing waives it. A generic fact is a word that happens to be this
    machine's: a one-segment path, a one-word host name, a bare account name.
    Those are matched only in the shapes where a word can only be a machine, and
    they are waivable, because being wrong about a word has to be survivable.

    There is no field a fact is skipped in any more. A list of vocabulary fields
    existed to stop a host called `editor` refusing its own provenance record,
    and it published `ty-MS-7C80` as a JSON key and as an `id`. Fixing which
    facts are unwaivable is what removed the need for it.
    """

    why: str
    pattern: "re.Pattern[str]"
    specific: bool = True


class Leak(NamedTuple):
    """One hit: what it is, what it says, its tier, and where it was found.

    `machine_fact` is the tier. True is tier 1, a specific fact about this
    machine, which nothing waives. False is tier 2, a shape, which the
    manuscript or `--allow-text` can allow.
    """

    why: str
    text: str
    machine_fact: bool
    where: str = ""

    @property
    def line(self) -> str:
        """The refusal line: where it is, what it is, and the text itself."""
        if self.where:
            return f"{self.where} names {self.why}, {self.text!r}"
        return f"names {self.why}, {self.text!r}"

    def under(self, prefix: str) -> "Leak":
        """The same leak, reported inside a file."""
        return self._replace(where=f"{prefix}: {self.where}" if self.where else prefix)


def is_specific(name: str) -> bool:
    """Is this detected name one that can only be this machine.

    A host name carrying a digit, a hyphen, a dot or an underscore is a machine
    name and nothing else. A name that is one plain alphabetic word is a word:
    machines here are called `claude`, `media`, `editor`, `core` and `stats`,
    and every one of those appears in an ordinary review of an ordinary paper.
    """
    return not re.fullmatch(r"[A-Za-z]+", name)


def host_pattern(name: str) -> "re.Pattern[str]":
    """How to find this machine's own name, which depends on what it is called.

    A specific name is matched as a plain substring, in either case and with no
    boundary on either side. `ty-ms-7c80` typed in a comment is this machine as
    surely as `ty-MS-7C80` is, and so are `node.ty-ms-7c80`, `run_ty-ms-7c80_1`
    and a JSON key spelled with it, every one of which the bounded version
    published. Nothing has to be protected from this test, because no review of
    any paper contains this string.

    A generic name is matched only where a bare word cannot be anything but a
    machine: after an `@`, after a `//` or a `\\\\`, or before a `:/`. It is a
    tier 2 shape rather than a fact, so an editor can waive it. Matching such a
    name as a fact is what refused every publish from a machine called `editor`,
    whose name is in `generator.kind` and in a slot name, and the word `media`
    in a sentence identifies nobody.
    """
    text = re.escape(name)
    if is_specific(name):
        return re.compile(text, re.IGNORECASE)
    return re.compile(
        rf"(?:(?:(?<=@)|(?<=//)|(?<=\\\\)){text}(?![\w-])"
        rf"|(?<![\w.-]){text}(?=:[\\/]))",
        re.IGNORECASE,
    )


def path_segments(text: str) -> int:
    """How many named segments a detected path has.

    `/home/ty` has two, `/tmp` has one, and that count is the whole of the
    specific-or-generic decision for a path. Two segments is a place on one
    disk. One segment is a word that happens to be a directory, and every
    system has it.
    """
    return len([part for part in re.split(r"[\\/]+", text.strip("\\/")) if part])


def machine_facts(
    *, run_dir: Path | str | None = None, typed_run: Path | str | None = None
) -> tuple[Fact, ...]:
    """The strings that name this machine, looked up rather than recognised.

    All of it is known at publish time, so none of it has to be guessed from the
    shape of a string: the home directory, this checkout, the temporary
    directory, the working directory and the run folder are paths, and the host
    name and the user name are names. What each one is worth is the split above.

    A path of two or more segments, and a host name carrying a digit, a hyphen
    or a dot, are specific. They are matched as a plain case-insensitive
    substring, with no boundary on either side, everywhere, and nothing waives
    one. There is nothing to protect from that test: `/home/ty` and `ty-ms-7c80`
    do not occur in a review of a paper or in this repository's own vocabulary,
    which is why the boundaries that were there to protect ordinary text are
    gone, and with them every hole they left. `file:/home/ty/x.pdf`,
    `//home/ty/x`, `a~/home/ty/x`, `http://localhost:8000/home/ty/x`,
    `node.ty-ms-7c80`, `run_ty-ms-7c80_1` and the host as a JSON key were all
    published by the bounded version.

    A one-segment path, a one-word host name and the bare account name are
    generic. A word is not a leak. They are tier 2 shapes, found only where such
    a word can only be a machine, and waivable, because being wrong about a word
    has to be survivable: `/tmp` as a fact refused `temperature/tmp ratio`, a
    working directory of `/data` refused `training/data/test`, a user called
    `pi` refused `$2\\pi$`, and a host called `editor` refused every publish it
    made with no flag to get past it.
    """
    paths: dict[str, str] = {}

    def path_fact(why: str, value: object) -> None:
        text = str(value or "").rstrip("/")
        if len(text) > 1 and text not in ("~", "/"):
            paths.setdefault(text, why)

    def both_spellings(why: str, value: object) -> None:
        """A path as it is written and as the filesystem resolves it.

        Only the resolved spelling was registered, so on a machine where the
        home directory, the temporary directory or the run folder is a symlink,
        the name every tool prints was not a fact at all. `/home/ty` resolving
        to `/export/people/ty` meant a run under `/home/ty` published `/home/ty`
        and refused only the target nobody ever types.
        """
        text = str(value or "")
        if not text.strip():
            return
        path_fact(why, text)
        try:
            path_fact(why, Path(text).resolve())
        except (OSError, RuntimeError, ValueError):
            pass

    for why, source in (
        ("the home directory", Path.home),
        ("the working directory", Path.cwd),
    ):
        try:
            both_spellings(why, source())
        except (OSError, RuntimeError):
            pass
    # The environment's own answer, which is what a shell, a log line and most
    # of the engine's own output are written from. `Path.home()` reads the
    # password database when HOME is unset and `Path.cwd()` resolves symlinks,
    # so neither is necessarily the spelling the operator sees.
    for why, name in (
        ("the home directory", "HOME"),
        ("the home directory", "USERPROFILE"),
        ("the working directory", "PWD"),
        ("the temporary directory", "TMPDIR"),
        ("the temporary directory", "TMP"),
        ("the temporary directory", "TEMP"),
    ):
        both_spellings(why, os.environ.get(name, ""))
    both_spellings("this checkout", REPO)
    both_spellings("the temporary directory", tempfile.gettempdir())
    # The run folder, in the spelling the engine reads back and in the one the
    # editor typed. The engine resolves the path it was given before it records
    # it, so on a machine where the runs sit under a link, `--run
    # ~/runs/latest` never became a fact at all and the path the editor typed
    # and every log line holds was tier 2, waivable with the flag the refusal
    # printed. `typed_run` is absolute but not resolved, which is the whole
    # point of it.
    for why, folder in (
        ("the run folder", run_dir),
        ("the run folder as it was given", typed_run),
    ):
        if folder is None:
            continue
        both_spellings(why, folder)
        # The folder the runs live in, which is the home directory or the
        # checkout on most machines and a scratch disk on some. It is in every
        # run path the engine writes, so a run folder named relative to it still
        # names the machine.
        try:
            both_spellings("the folder the runs live in", Path(str(folder)).parent)
        except (OSError, RuntimeError, ValueError):
            pass

    facts: list[Fact] = []
    for text, why in paths.items():
        if path_segments(text) > 1:
            # Both spellings of the fact itself. The scan reads the raw string
            # and the canonical one, so a fact that canonicalises to something
            # else has to be looked for in both: HOME written `/home//ty/.` is
            # the same machine as HOME written `/home/ty`.
            for spelling in dict.fromkeys((text, canonical_text(text))):
                facts.append(Fact(why, re.compile(re.escape(spelling), re.IGNORECASE)))
            continue
        # One segment. `/tmp` and `/data` are on every machine, so the fact is
        # the shape of something under them rather than the word itself, and it
        # is waivable. When the root is one `LOCAL_REFERENCE_PATTERNS` already
        # reads, which is true of every usual one, that pattern reports it and
        # this fact would only add a second line about the same string.
        root = text.strip("/").lower()
        if root in {known.lower() for known in LOCAL_ROOTS}:
            continue
        facts.append(
            Fact(
                f"{why}, which is one directory on this machine",
                re.compile(
                    rf"(?<![\w.:/~-]){re.escape(text)}(?:/{_SEGMENT})+",
                    re.IGNORECASE,
                ),
                specific=False,
            )
        )

    host = socket.gethostname()
    for name in dict.fromkeys((host, host.split(".")[0])):
        if len(str(name)) > 1:
            facts.append(
                Fact(
                    "the host name",
                    host_pattern(str(name)),
                    specific=is_specific(str(name)),
                )
            )

    try:
        user = getpass.getuser()
    except Exception:  # noqa: BLE001 - no account name is not a failure to scan
        try:
            user = Path.home().name
        except (OSError, RuntimeError):
            user = ""
    if len(user) > 1:
        # Generic, and only directly after a home root, which is the one place a
        # user name is this operator rather than a word. As any path segment it
        # refused `$2\pi$` from a user called `pi`, `train/test split` from one
        # called `test` and `and/or` from one called `or`, and a user name is
        # also a common surname, so as a bare word it would refuse a citation.
        facts.append(
            Fact(
                "the user name under a home directory",
                re.compile(
                    rf"(?i:/home/|/users/|\\users\\){re.escape(user)}(?![\w-])"
                ),
                specific=False,
            )
        )
    return tuple(facts)


_THIS_MACHINE: tuple[Fact, ...] | None = None


def this_machine() -> tuple[Fact, ...]:
    """The facts about this machine, worked out once."""
    global _THIS_MACHINE
    if _THIS_MACHINE is None:
        _THIS_MACHINE = machine_facts()
    return _THIS_MACHINE


def manuscript_text(workspace: Path | str | None) -> str:
    """The manuscript as the reviewers were handed it, for the allowance above.

    A hit that appears verbatim in here is the paper's own text: the author
    address printed on its first page, a repository path in its data
    availability statement, a tool path in its methods. Publishing a review
    cannot be refused because the paper under review says something, so those
    are allowed. The exact facts are not.
    """
    if workspace is None:
        return ""
    manuscript = Path(workspace) / "manuscript.md"
    try:
        return manuscript.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def printed_in(text: str, document: str) -> bool:
    """Is this hit the document's own text rather than a fragment of one.

    A substring test was wrong in both directions of the same bug: a manuscript
    printing `joann@lab.example.org` allowed `ann@lab.example.org`, and one
    printing `/home/alice/project` allowed `/home/al`. So the hit has to stand
    on its own in the document, between boundaries, rather than merely occur in
    it. A full stop on the right is not excluded: a manuscript writes `data at
    /srv/public/set.` at the end of a sentence, and the path is still the
    paper's own words.
    """
    if not document or not text:
        return False
    return re.search(rf"(?<![\w.+-]){re.escape(text)}(?![\w+/-])", document) is not None


# Everything a reader reads as a slash or as a hyphen and `re` does not. NFKC
# folds the full width pair and nothing else, so U+2215 DIVISION SLASH, U+2044
# FRACTION SLASH, U+29F8 BIG SOLIDUS, U+2216 SET MINUS, U+27CB MATHEMATICAL
# RISING DIAGONAL, U+2571 BOX DRAWINGS LIGHT DIAGONAL and U+3033 VERTICAL KANA
# REPEAT MARK all survive it. A backslash is a slash here too: `C:\Users\bob`
# and `\home\ty\x` are the paths they read as, and the shapes that need the
# backslash itself still see it, because the raw string is scanned as well. The
# hyphens matter for the host name, which is the one fact with a hyphen in it:
# `ty‑MS‑7C80` written with U+2011 is this machine.
_LOOKALIKES = str.maketrans(
    {
        "\\": "/",
        "\u2216": "/",
        "\uff3c": "/",
        "\u2215": "/",
        "\u2044": "/",
        "\u29f8": "/",
        "\uff0f": "/",
        "\u27cb": "/",
        "\u2571": "/",
        "\u3033": "/",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\ufe58": "-",
        "\ufe63": "-",
        "\uff0d": "-",
    }
)
# A backslash in front of ASCII punctuation is an escape, not a path separator:
# `\/home\/ty` out of a JSON string and `ty\-MS\-7C80` out of a regular
# expression are both this machine, written by something that quoted them.
# Dropped before the look-alikes are folded, so that `\home\ty\x` still becomes
# `/home/ty/x` while `\/home` does not become `//home`.
_ESCAPED_PUNCTUATION = re.compile(r"\\([!-\/:-@\[-`{-~])")
_DOT_SEGMENT = re.compile(r"/\.(?=/)")
# Repeated slashes are one slash, except the pair that follows a scheme.
# `https://home/x` is a URL and `//home/x` is a path, and the patterns tell them
# apart by the colon in front, so collapsing `://` to `:/` would turn every URL
# whose host is a word like `home` or `data` into an absolute path.
_REPEATED_SLASH = re.compile(r"(?<!:)/{2,}")


def canonical_text(text: str, *, escapes_first: bool = True) -> str:
    """One string reduced to the characters it reads as, to a fixed point.

    Every encoding this scan has been got past is undone here rather than in a
    list of special cases, and undone repeatedly, because each layer can reveal
    another: `%252Fhome%252Fty` is a percent sign that decodes to a percent
    sign, and `&#37;2Fhome` is an HTML entity hiding one. The steps are NFKC,
    HTML entities, percent-decoding, dropping the format characters that print
    as nothing (U+200B through U+200D, U+2060, U+FEFF and the soft hyphen are
    all Cf), dropping a backslash that is escaping punctuation, folding the
    slash and hyphen look-alikes, and reducing `//` and `/./` to `/`. The loop
    stops when the string stops changing, which it always does, because every
    step either shortens the string or replaces a character with an ASCII one.

    A backslash is two things at once and the order decides which one it is
    read as, so there is no order that is right. With `escapes_first`, which is
    the default, `\\/home\\/ty` is a quoted `/home/ty` and `ty\\-MS\\-7C80` is a
    quoted host name. Without it, a backslash is a separator before anything
    else, and `\\opt\\.cache\\insilico` is `/opt/.cache/insilico` rather than
    the `/opt.cache/insilico` the other reading produces, which is a path on no
    machine. Either reading can be the one that holds the fact, so the scan
    takes both and reads a hit from whichever found it.

    The case of the result is the case of the input. Every fact and every
    pattern matches case-insensitively already, so folding the case here would
    buy nothing and would cost the one thing a hit has to keep: the text as the
    author wrote it, which is what `--allow-text` is compared against and what
    the refusal prints back. Both the text being scanned and the facts being
    looked for go through this, so the comparison happens in one spelling, and
    the raw string is scanned too, so a shape that needs a real backslash or a
    real `%` still matches.
    """
    current = text
    for _ in range(12):
        step = unicodedata.normalize("NFKC", current)
        step = html.unescape(step)
        step = urllib.parse.unquote(step)
        step = "".join(ch for ch in step if unicodedata.category(ch) != "Cf")
        if escapes_first:
            step = _ESCAPED_PUNCTUATION.sub(r"\1", step)
            step = step.translate(_LOOKALIKES)
        else:
            step = step.translate(_LOOKALIKES)
            step = _ESCAPED_PUNCTUATION.sub(r"\1", step)
        step = _DOT_SEGMENT.sub("", step)
        step = _REPEATED_SLASH.sub("/", step)
        if step == current:
            break
        current = step
    return current


def _scan_forms(text: str) -> tuple[str, ...]:
    """The forms of one string the scan reads: as written, and canonical.

    A handful of forms rather than a list of encodings. The raw string is read
    because the Windows share and the percent-encoded path are shapes in their
    own right, and the canonical form is read because `%2Fhome%2Fbob`,
    `&#47;home&#47;ty`, `/home/./ty`, `\\/home\\/ty` and `∕home∕ty` are all the
    same path and none of them matches a pattern written in slashes. Both
    readings of a backslash are canonicalised, because a quoted separator and a
    quoted punctuation mark are written the same way and whichever reading holds
    the fact is the one that matters.
    """
    forms = (text, canonical_text(text), canonical_text(text, escapes_first=False))
    return tuple(dict.fromkeys(forms))


def names_a_specific_fact(text: str, facts: Sequence[Fact]) -> bool:
    """Does this string contain something that can only be this machine.

    The test an allowance has to pass before it allows anything. An editor
    reading `file:///<checkout>/scripts/local_review.py` in a refusal and
    passing it back waived a tier 1 fact, because the flag matched the hit and
    nothing looked at what the hit was made of.
    """
    return any(
        fact.pattern.search(form)
        for fact in facts
        if fact.specific
        for form in _scan_forms(text)
    )


def local_references(
    text: str,
    *,
    facts: tuple[Fact, ...] | None = None,
    manuscript: str = "",
    allowed: Sequence[str] = (),
) -> list[Leak]:
    """Every local path or address in one string, with the tier it belongs to.

    An allowance is a tier 2 decision only. `manuscript` allows what the paper
    prints, `allowed` is what the editor passed `--allow-text` for, and neither
    reaches a specific fact: a hit carrying one is tier 1 whatever it is wrapped
    in, and is reported as tier 1 from the start rather than offered a flag.

    The longest form of each hit only. A home directory sitting inside a longer
    path is one leak and not two, and reporting it twice would make a refusal
    read as though more had escaped than did. When the longer form is a pattern
    hit wrapped around a machine fact, the line names the longer text and keeps
    the fact's tier, so an editor sees the whole path and `--allow-text` cannot
    publish it by naming more of it than the fact does.
    """
    facts = this_machine() if facts is None else facts
    waived = set(allowed)
    forms = _scan_forms(text)
    # Which form each hit came out of is kept, because the raw form is scanned
    # first and a hit that only the canonical form found is a different kind of
    # hit: it is the same disk written in an encoding, not a second one.
    found: list[tuple[Leak, bool]] = []
    for fact in facts:
        if not fact.specific:
            continue
        for index, form in enumerate(forms):
            found += [
                (Leak(fact.why, match.group(0), True), index > 0)
                for match in fact.pattern.finditer(form)
            ]
    named = {leak.text for leak, _ in found}
    generic = [(fact.why, fact.pattern) for fact in facts if not fact.specific]
    for why, pattern in (*generic, *LOCAL_REFERENCE_PATTERNS):
        for index, form in enumerate(forms):
            for match in pattern.finditer(form):
                hit = match.group(0)
                if hit in named:
                    continue
                found.append((Leak(why, hit, False), index > 0))
                named.add(hit)

    unique: list[Leak] = []
    only_folded: dict[str, bool] = {}
    for leak, folded in found:
        if leak not in unique:
            unique.append(leak)
        only_folded[leak.text] = only_folded.get(leak.text, True) and folded
    carrying: list[Leak] = []
    for leak in unique:
        inside = [
            other
            for other in unique
            if other.machine_fact and other.text != leak.text and other.text in leak.text
        ]
        if inside and not leak.machine_fact:
            leak = leak._replace(why=inside[0].why, machine_fact=True)
        carrying.append(leak)
    # One string is one leak, whichever form it was found in. The scan reads the
    # text as written and its canonical form, so a path that survives the
    # folding is found twice over: `C:\\Users\\bob\\x.pdf` is reported beside
    # `C:/Users/bob/x.pdf` and `/Users/bob/x.pdf` out of the folded copy, which
    # reads as three paths escaping where one did. A hit the folded copy found
    # inside the folded form of a hit already reported as written is dropped,
    # and its tier is carried onto that one first, so folding can raise a tier
    # and never hide a path. The line then names the spelling the file holds,
    # which is the one an editor can search for and the one `--allow-text` has
    # to match. A folded hit that no written hit covers is the whole point of
    # folding, `%2Fhome%2Fty` being a path only once decoded, and it stays, in
    # the only spelling that shows what it is.
    written = [leak for leak in carrying if not only_folded.get(leak.text, False)]
    covers = [_scan_forms(leak.text) for leak in written]
    echoes = [leak for leak in carrying if only_folded.get(leak.text, False)]
    spellings: list[Leak] = []
    for leak, cover in zip(written, covers):
        hidden = [
            echo
            for echo in echoes
            if echo.machine_fact and any(echo.text in form for form in cover)
        ]
        if hidden and not leak.machine_fact:
            leak = leak._replace(why=hidden[0].why, machine_fact=True)
        spellings.append(leak)
    spellings += [
        echo
        for echo in echoes
        if not any(echo.text in form for cover in covers for form in cover)
    ]
    longest = [
        leak
        for leak in spellings
        if not any(
            leak.text != other.text and leak.text in other.text for other in spellings
        )
    ]
    # Allowances are read last, against the hits as they will be reported. Read
    # first, allowing `//media/share/x` left the `media` inside it refused on its
    # own, because the longer hit the editor had read was gone before the shorter
    # one was reduced into it and there was nothing left to allow.
    return [
        leak
        for leak in longest
        if leak.machine_fact
        or not (leak.text in waived or printed_in(leak.text, manuscript))
    ]


def leak_refusal(leaks: Sequence[Leak]) -> str:
    """What a refused publish prints: every hit, and how to allow the waivable.

    The flag is printed ready to copy, because an editor reading a refusal has
    to be able to act on it without working out the quoting themselves, and
    because the allowance has to name the matched text exactly. It is printed in
    the `--allow-text=<text>` form: a hit can begin with a hyphen, and as a
    separate argument that reads as another option rather than as this one's
    value.
    """
    said = ", ".join(leak.line for leak in leaks)
    waivable = list(dict.fromkeys(leak.text for leak in leaks if not leak.machine_fact))
    unwaivable = [leak for leak in leaks if leak.machine_fact]
    if waivable:
        flags = " ".join(f"--allow-text={shlex.quote(text)}" for text in waivable)
        said += (
            " A hit that is the review's own words rather than this machine can"
            " be published by reading it first and passing it back on the same"
            f" command: {flags}. Each allowance is recorded in the provenance"
            " record, where a reader of the page can see it."
        )
    if unwaivable:
        said += (
            f" {len(unwaivable)} of these name this machine itself, looked up"
            " rather than recognised, and no flag and no manuscript waives one."
        )
    return said


def local_reference_fields(
    value: object,
    *,
    facts: tuple[Fact, ...] | None = None,
    manuscript: str = "",
    allowed: Sequence[str] = (),
    trail: str = "",
) -> list[Leak]:
    """Where a record names the machine that wrote it rather than the review.

    A published provenance record is read by people with no access to this disk,
    so a path on it, the name of this machine or somebody's address in it
    identifies the operator rather than the review. Every string in the record
    is read, whatever field it sits in, because the scrubber works from a list
    of field names and this is the guard on the field the engine has not
    written yet. A dictionary key is read too: a map of figures keyed by their
    absolute paths leaks through the key rather than the value.

    Each hit names the field, what it is, and the text itself, so an editor
    reading a refusal can see which string in which field stopped it.

    Every string is read by the same rule, keys and values alike. The earlier
    version switched the host name fact off in field names and in a list of
    fields whose values come from a fixed vocabulary, because a host called
    `editor` refused its own provenance record. That is what published
    `ty-MS-7C80` as a JSON key and as an `id`, a `status` and a `basis`. The
    tier split above is what makes a word-shaped host harmless, so nothing has
    to be switched off anywhere.
    """
    facts = this_machine() if facts is None else facts
    scan = {"facts": facts, "manuscript": manuscript, "allowed": allowed}
    found: list[Leak] = []
    if isinstance(value, dict):
        for key, child in value.items():
            below = f"{trail}.{key}" if trail else str(key)
            if isinstance(key, str):
                found += [
                    leak._replace(where=f"{below} (the field name)")
                    for leak in local_references(key, **scan)
                ]
            found += local_reference_fields(child, **scan, trail=below)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found += local_reference_fields(child, **scan, trail=f"{trail}[{index}]")
    elif isinstance(value, str):
        found += [
            leak._replace(where=trail or "(root)")
            for leak in local_references(value, **scan)
        ]
    return found


_DROPPED = object()

# The fields the engine fills with a path on the machine that ran the review,
# and the only fields in a published artifact this script will alter. Read off
# engine 0.9 rather than guessed: `peerreviewagents/plugin/server.py` writes the
# manuscript's absolute path as `pdf` and the loaded plugin's as `plugin_root`
# into the run manifest, `plugin/starter.py` and `runs.py` write `pdf` as well,
# and no other engine field holds an absolute path. The remaining names are
# fields earlier releases wrote, kept because a run folder from one may still be
# published, and they are listed here so the list is one place rather than a
# habit: nothing else in a bundle is a path field, whatever it looks like.
#
# This is a list of field names rather than a test on the value because the
# first version tested the value: any string beginning with a slash was taken
# for a path. A reviewer writing "/ 2 is the wrong denominator" had the comment
# silently deleted from the published package, and a path written inside a
# sentence was missed regardless. The value is still tested, by
# `looks_like_a_path` below, but only to decide whether one of these fields is
# holding the path it is supposed to: a sentence in `memo_path` is left alone
# and reported by the leak scan rather than deleted. Review content is never
# rewritten. What catches a path the engine starts recording in a field nothing
# here knows about is the leak scan over the written bundle, below.
PATH_FIELDS = frozenset({
    "memo_path",
    "pdf",
    "plugin_dir",
    "plugin_root",
    "run_directory",
    "source_review_path",
    "workspace",
})


def looks_like_a_path(text: str) -> bool:
    """Is this value the path its field is supposed to hold.

    A path has no whitespace in it and starts at a root: a slash, a `~`, a
    `file://` URL or a drive letter. `"/ 2 is the wrong denominator"` starts
    with a slash and is a sentence, and dropping it deleted a reviewer's comment
    from a published package.
    """
    raw = text[len("file://") :] if text.startswith("file://") else text
    raw = raw.strip()
    if not raw or re.search(r"\s", raw):
        return False
    return re.fullmatch(r"(?:~|[\\/]|[A-Za-z]:[\\/])\S*", raw) is not None


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


def without_local_paths(
    value: object,
    *,
    field: str = "",
    allowed: Sequence[str] = (),
    projected: list[str] | None = None,
    trail: str = "",
    facts: Sequence[Fact] | None = None,
) -> object:
    """The same JSON with the engine's own path fields made relative or dropped.

    `editor-package.json` is the engine's own output copied into the bundle, and
    a run folder records absolute paths in several places. Only a value in one
    of `PATH_FIELDS` that is actually a path is touched, so the review's own
    words reach the reader as the reviewer wrote them. Every change is appended
    to `projected`, which the caller prints: a published artifact that differs
    from the engine's own output says so on the command that published it, and
    nothing is altered silently.

    A key is never rewritten. A mapping keyed by a path leaks through the key
    rather than the value, and the version that rewrote a key inside this
    repository to a relative one turned `<checkout>/docs/figs/a.png` into
    `docs/figs/a.png` with nothing said. Engine 0.9 writes no mapping keyed by
    an absolute path at all, so there is no engine behaviour behind the rewrite
    to preserve, and a path-shaped key is refused here instead.

    What the refusal offers depends on what the key is. A key that names this
    machine is tier 1 wherever it sits, and the version that offered the flag
    for one sent the editor to a flag that then refused the allowance for
    naming a specific fact, which reads as the script changing its mind. The
    flag is offered only for a key an allowance could actually publish, and a
    key that names this machine is refused whatever was allowed.
    """
    facts = this_machine() if facts is None else facts
    if isinstance(value, dict):
        scrubbed = {}
        for key, child in value.items():
            keyed_by_a_path = isinstance(key, str) and looks_like_a_path(key)
            own_name = keyed_by_a_path and names_a_specific_fact(str(key), facts)
            if keyed_by_a_path and (own_name or key not in set(allowed)):
                choice = (
                    "read it, then edit the run's own copy. A field name that"
                    " names this machine is refused whatever it is wrapped in,"
                    " and no flag publishes it."
                    if own_name
                    else "read it, then either edit the run's own copy or"
                    " publish it deliberately with"
                    f" --allow-text={shlex.quote(str(key))}."
                )
                raise CommandError(
                    f"{key!r} is a field name in the engine's own output and it"
                    " is shaped like a path. Dropping it would publish an"
                    " artifact missing an entry the engine wrote, rewriting it"
                    " would publish an artifact that differs from the engine's"
                    " own output with nothing saying so, and keeping it would"
                    " publish the path. None of the three is this script's"
                    f" decision: {choice}"
                )
            below = f"{trail}.{key}" if trail else str(key)
            cleaned = without_local_paths(
                child,
                field=key if isinstance(key, str) else "",
                allowed=allowed,
                projected=projected,
                trail=below,
                facts=facts,
            )
            if cleaned is not _DROPPED:
                scrubbed[key] = cleaned
        return scrubbed
    if isinstance(value, list):
        return [
            cleaned
            for cleaned in (
                without_local_paths(
                    child,
                    field=field,
                    allowed=allowed,
                    projected=projected,
                    trail=f"{trail}[{index}]",
                    facts=facts,
                )
                for index, child in enumerate(value)
            )
            if cleaned is not _DROPPED
        ]
    if isinstance(value, str) and field in PATH_FIELDS and looks_like_a_path(value):
        relative = readable_path(value)
        if projected is not None and relative != value:
            where = trail or field
            projected.append(
                f"{where} dropped"
                if relative is _DROPPED
                else f"{where} rewritten to {relative}"
            )
        return relative
    return value


def projection_report(
    *,
    engine_package: dict,
    published: dict,
    projected: Sequence[str] = (),
) -> str:
    """How the published editor-package.json differs from the engine's own.

    The bundle's copy is not the engine's file with a few strings scrubbed. It
    is rebuilt by `review_package` from the same reading, and the rebuild is the
    intended projection: the engine's package carries the whole run, and the
    bundle publishes the parts a reader of the review needs. Saying "projected
    nothing" because no path field was touched described a file that leaves out
    a dozen of the engine's top-level keys, so the line names them instead, and
    names them by comparing the two key sets rather than from a list in this
    file that the next engine release would make wrong.
    """
    engine_keys = list(engine_package)
    published_keys = list(published)
    left_out = [key for key in engine_keys if key not in published_keys]
    added = [key for key in published_keys if key not in engine_keys]
    parts: list[str] = []
    if not engine_keys:
        parts.append(
            "the engine's own editor-package.json could not be read, so the "
            "keys carried into the bundle were not compared with it"
        )
    if left_out:
        parts.append(f"not carried: {', '.join(left_out)}")
    if added:
        parts.append(f"added by this bundle: {', '.join(added)}")
    if projected:
        parts.append(f"path fields projected: {', '.join(projected)}")
    if engine_keys and not left_out and not added and not projected:
        parts.append("every key the engine wrote, published as written")
    return "editor-package.json, " + ". ".join(parts)


# Every file in a bundle is scanned. The two JSON forms are parsed first, the
# rest is read as the text it is.
SCANNED_SUFFIXES = (".json", ".jsonl", ".md", ".txt")
PARSED_SUFFIXES = (".json", ".jsonl")


def file_local_references(
    path: Path,
    *,
    facts: tuple[Fact, ...] | None = None,
    manuscript: str = "",
    allowed: Sequence[str] = (),
) -> list[Leak]:
    """What one file in a bundle says about the machine it was written on.

    A JSON file is parsed and every string in it read at any depth, key or
    value, rather than being scanned as text. JSON doubles a backslash, so
    `C:\\Users\\someone\\x.pdf` reaches the file as `C:\\\\Users\\\\...` and a
    text scan of it matched nothing: a Windows path nested inside a record the
    engine wrote went out in a published bundle. Parsing reads the value a
    reader of that file gets.

    Markdown and plain text are scanned as text, because the prose is the
    content there and there is no structure to walk.

    Each line names the field as well as the hit, so a refusal says where in the
    file to look. A JSON file that will not parse is scanned as text and said to
    be unparsed rather than skipped, because a half-written record is exactly
    when a scan matters.
    """
    facts = this_machine() if facts is None else facts
    scan = {"facts": facts, "manuscript": manuscript, "allowed": allowed}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    suffix = path.suffix.lower()

    def as_text(field: str) -> list[Leak]:
        return [leak._replace(where=field) for leak in local_references(text, **scan)]

    if suffix == ".json":
        try:
            value = json.loads(text)
        except ValueError:
            return as_text("(unparsed JSON, read as text)")
        return local_reference_fields(value, **scan)
    if suffix == ".jsonl":
        found: list[Leak] = []
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError:
                found += [
                    leak._replace(
                        where=f"line {number} (unparsed JSON, read as text)"
                    )
                    for leak in local_references(line, **scan)
                ]
                continue
            found += local_reference_fields(row, **scan, trail=f"line {number}")
        return found
    return as_text("text")


def bundle_local_path_leaks(
    dest: Path,
    *,
    facts: tuple[Fact, ...] | None = None,
    manuscript: str = "",
    allowed: Sequence[str] = (),
) -> list[Leak]:
    """Every file in a written bundle that names the machine that wrote it.

    This reads what is on disk rather than what the code meant to write, which
    is the point: it is the guard that catches a path the engine started
    recording in a field nothing here knows about, in any file of the bundle,
    including the specialist reports copied in from the run and the prose of a
    document rendered from them.
    """
    facts = this_machine() if facts is None else facts
    found: list[Leak] = []
    for path in sorted(Path(dest).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        found += [
            leak.under(path.relative_to(dest).as_posix())
            for leak in file_local_references(
                path, facts=facts, manuscript=manuscript, allowed=allowed
            )
        ]
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


def require_complete_run(run_dir: Path, run: dict, reading: dict | None = None) -> None:
    """A published review has to come from a run that finished.

    Publishing checked neither the state nor the transport. A directory holding
    only an editor package, with no protocol.json and no progress.json,
    published with an empty error list, and so did a run whose progress.json
    said `blocked`. Both produced a record that read like a clean review.

    The engine answers the question now. `read_run` sets `publishable` only
    when the run finished, the findings came from a readable
    `editor-package.json` rather than the ledger, a guard verdict was recorded,
    the guards did not empty the review, and every run file could be read in
    full. That is the whole gate, and it is the engine's own rule rather than a
    second copy of it here, down to the words the refusal prints, which are the
    engine's `not_publishable_reasons`.

    No status is special-cased beside the flag. `complete-without-findings` is
    the finished state for a review written with no findings in it, and the two
    runs that end there are told apart by the engine rather than here: reviewers
    who read the manuscript and raised nothing make-or-break wrote a review and
    it publishes, while a review the guards emptied is held back with a reason
    naming how many they took. Reading the status here instead would refuse the
    first of those, which is a real review of a manuscript found sound.

    What this adds to the flag is the three things it does not cover. The
    transport has to be one this path can publish, because every claim a bundle
    makes about how the review was paid for is a claim about a Claude
    subscription. Every stage the arm asked for has to have reported, because a
    run can reach `complete` with a reader missing when the editor accepted the
    pool without it. And the refusals are named: a run refused only as "not
    publishable" sent the operator back to a log to find out there was no
    Claude login.
    """
    reading = reading if reading is not None else engine_reading(run_dir)
    status = str(reading.get("status") or "")
    # The arm replaces 0.8's mode and policy, and there is no single model to
    # require: 0.9 assigns one per slot and records the plan beside what ran.
    # What has to be recorded is which arm ran, on which transport, under which
    # workflow. A slot that ran a different model family from the one it was
    # assigned is not checked here either, and deliberately so: the engine puts
    # that in `not_publishable_reasons`, and the refusal below prints its words.
    missing = [field for field in ("arm", "provider", "workflow_version") if not run.get(field)]
    if missing:
        raise CommandError(
            f"This run records no {', '.join(missing)}, so the published record "
            "could not say how the review was produced. Point --run at the "
            "folder `peerreview review` wrote."
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
    arm = str(run.get("arm") or "")
    if arm in UNPUBLISHABLE_ARMS:
        raise CommandError(
            f"This run used the {arm} arm, which is what the engine runs on a "
            "draft of your own rather than a review of a submitted manuscript. "
            "It convenes no core reviewers and nobody outside the authorship "
            "read the paper, so there is no review in it to publish. Run the "
            "review arm the study asks for, or drop --publish to keep this "
            "bundle as a rehearsal."
        )
    if not reading.get("publishable"):
        # The engine names its own reasons, one sentence each, and that list is
        # never empty while the flag is false. Printing its words rather than a
        # second copy of its rules is the only way the refusal here and the
        # rule there cannot drift apart. The fallback covers an engine old
        # enough to set the flag without carrying the list.
        reasons = [
            str(reason).strip()
            for reason in _list(reading.get("not_publishable_reasons"))
            if str(reason).strip()
        ]
        problems = [str(p).strip() for p in _list(reading.get("problems")) if str(p).strip()]
        cause = str(reading.get("cause") or "").strip()
        source = str(reading.get("findings_source") or "none")
        detail = [f"The engine read it as {status or 'unknown'}."]
        if cause:
            detail.append(f"It stopped because: {cause}")
        if reasons:
            detail.append("The engine holds it back because:")
            detail += [f"({n}) {reason}." for n, reason in enumerate(reasons, start=1)]
        else:
            if source != "editor-package":
                detail.append(
                    f"Its findings came from {source}, which is not the editor's "
                    "own placement of them."
                )
            if problems:
                detail.append(
                    f"{len(problems)} run file(s) could not be read in full: "
                    + ", ".join(problems)
                )
        raise CommandError(
            "The engine does not read this run as publishable, so it is not a "
            "review this path can publish. "
            + " ".join(detail)
            + " Re-run the engine, or drop --publish to keep the bundle as a "
            "rehearsal."
        )
    # The stage ledger is the only thing that says whether every reader the arm
    # asked for actually reported. A run can reach `complete` with a stage
    # missing when the editor accepted the pool without it, and a bundle that
    # says three core reviewers and six specialists over a run where two of them
    # never answered is a claim about a panel that did not sit.
    ledger = _dict(run.get("completeness"))
    # No ledger at all is the same claim with nothing behind it. A folder whose
    # progress.json was never written still reads as complete from the
    # harness's own record of the session, and the engine calls it publishable,
    # but nothing in it says which readers the arm asked for or which of them
    # answered. That is a panel nobody can check, so it is refused here.
    if not ledger:
        raise CommandError(
            "This run carries no stage ledger, so nothing in it says which "
            "readers the arm asked for or which of them reported. A bundle "
            "built from it would describe a panel that cannot be checked "
            "against the run. Re-run the review, or drop --publish to keep the "
            "bundle as a rehearsal."
        )
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
    # What the editor read in a refusal and decided to publish anyway. Exact
    # strings, deduplicated, in the order they were given, and recorded in the
    # provenance record further down. Blank entries are dropped rather than
    # becoming an allowance that matches everything.
    allowed = tuple(
        dict.fromkeys(text for text in (args.allow_text or []) if str(text).strip())
    )
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

    # One reading of the run folder, taken through the engine, and everything
    # below is derived from it. Two readings were two status rules.
    reading = engine_reading(Path(args.run))
    run_dir = Path(str(reading["review"]))

    # What counts as naming this machine, worked out once and used by everything
    # below: the facts, with this run folder among them. It is worked out here
    # rather than after the scrub because the allowances have to be checked
    # against it first. An editor who read `file:///<checkout>/scripts/x.py` in
    # a refusal and passed it back waived a specific fact, because the flag was
    # taken at its word and nothing asked what the text it allowed was made of.
    facts = machine_facts(run_dir=run_dir, typed_run=os.path.abspath(args.run))
    refused = [text for text in allowed if names_a_specific_fact(text, facts)]
    if refused:
        raise CommandError(
            "An allowance may not contain anything that names this machine, and "
            f"{', '.join(repr(text) for text in refused)} does. A hit that "
            "carries a path on this disk or this host's own name is refused "
            "whatever it is wrapped in, and no flag publishes it. Edit the run's "
            "own copy instead."
        )

    package = review_package(reading)
    run = run_record(reading)
    if args.publish:
        require_complete_run(run_dir, run, reading)
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

    agents = agent_rows(reading)
    # The transport is the run's own, read from the start-up probe the engine ran
    # before it spent anything. A run on a transport this path cannot publish is
    # refused here even when the bundle is only a rehearsal.
    transport = transport_record(
        provider=str(run.get("provider") or ""),
        runtime=_dict(reading.get("runtime")),
        startup=_dict(reading.get("startup")),
        verified_at=startup_stamp(reading),
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
        allowed_text=allowed,
    )

    # The engine's own output is copied into the bundle, and a run folder
    # records absolute paths in several places. Scrubbing happens before
    # anything is written, so the manifest hashes the file a reader will get.
    projected: list[str] = []
    published_package = (
        without_local_paths(
            package, allowed=allowed, projected=projected, facts=facts
        )
        if args.publish
        else package
    )
    # Said out loud, every time, because the published artifact differs from the
    # engine's own output and a reader comparing the two has to be able to find
    # out why from the command that made it. The engine's own file is read back
    # off the run folder for the comparison rather than described from memory.
    if args.publish:
        engine_package = maybe_json(
            Path(str(_dict(reading.get("files")).get("editor-package.json") or ""))
        )
        print(
            projection_report(
                engine_package=engine_package,
                published=published_package if isinstance(published_package, dict) else {},
                projected=projected,
            )
        )

    # The manuscript whose own words neither scan may refuse the review for. The
    # tier 2 text the editor read and allowed is in `allowed`, checked above.
    manuscript = manuscript_text(workspace)

    if args.publish:
        leaked = local_reference_fields(
            provenance, facts=facts, manuscript=manuscript, allowed=allowed
        )
        if leaked:
            raise CommandError(
                "This record would publish the machine it was made on: "
                f"{leak_refusal(leaked)} A published record may not name the "
                "operator's filesystem or anybody's address."
            )

    # The repository's schema gate, run here rather than after the bundle is on
    # disk. `npm run check:schema` validates what is already in docs/reviews, so
    # a record carrying a value the schema does not allow used to publish with
    # exit 0 and be caught by a later check, leaving a bundle to delete by hand.
    # Rehearsals are validated too: a rehearsal exists to find out whether this
    # run would publish, and one that would be refused at the gate should say so
    # now rather than look like a clean dry run.
    try:
        assert_valid_provenance(provenance, source="provenance.json")
    except InvalidProvenance as error:
        raise CommandError(
            f"{error} Nothing was written. The record has to satisfy "
            "schemas/review-provenance.schema.json before a bundle exists, and "
            "the schema is not the thing to edit to make this pass."
        ) from error

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
            leaked = bundle_local_path_leaks(
                stage, facts=facts, manuscript=manuscript, allowed=allowed
            )
            if leaked:
                raise CommandError(
                    "This bundle names the machine that produced it: "
                    f"{leak_refusal(leaked)} Nothing was written to {dest}."
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
    print(f"asked    {model_phrase(provenance['assigned_models'])}")
    print(f"ran      {model_phrase(provenance['models'])}")
    unverified = [str(slot) for slot in _list(run.get("models_unverified"))]
    if unverified:
        print(f"warning  no model was observed for: {', '.join(unverified)}")
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
    p.add_argument(
        "--allow-text",
        action="append",
        default=[],
        metavar="TEXT",
        help="Publish this exact text although the leak scan read it as a local "
        "path or an address. Repeatable, recorded in the provenance record, and "
        "no use against a string that names this machine: read the refusal "
        "first, it prints the flag to copy",
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
