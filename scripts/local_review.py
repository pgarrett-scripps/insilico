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
from review_paths import REPO, REVIEW_ISSUES, REVIEWS, ROUND_RECORD, RUNS  # noqa: E402
from review_plan import (  # noqa: E402
    CommandError,
    draft_number,
    existing_bundles,
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
# What the engine calls the manuscript itself inside that folder. Engine 0.10
# writes the whole paper as one Markdown file, one piece of it per line, and a
# finding cites a line of this file by name; a supplement is a document of its
# own beside it. The engine publishes the name on its own surface, and this copy
# exists because half of this pipeline reads a published bundle with no engine
# installed and still has to say which document a line belongs to. The copy is
# checked against the engine's own in `bind_run_to_input`, so a release that
# renamed the file is refused there rather than published under a label this
# file invented.
MAIN_DOCUMENT = "paper.md"

# The six specialist tracks the plugin ships, each writing one `audit_<track>.md`
# report into the run. Named here so a bundle can say which reports are missing
# rather than quietly publishing fewer.
SPECIALIST_TRACKS = (
    "stats",
    "figures-tables",
    "methods-reporting",
    "citations",
    "numbers",
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
SUGGESTION_SEVERITY = "minor"
# The two statuses that close a prior round's issue out. Such an issue is
# reported against the round that raised it, carries no rank, and is not one of
# the changes the authors have to answer now, so it is neither a required
# change nor a suggestion here.
#
# `resolved` is the editor agent's own ruling that a prior issue was fixed, and
# `unverified` is a prior issue nobody raised again and nobody ruled fixed,
# which is still open. The two are never printed as one number and `unverified`
# is never printed as a fix: a finding can disappear from text nobody touched,
# so nothing being filed this round is not evidence of anything.
RESOLVED_STATUS = "resolved"
UNVERIFIED_STATUS = "unverified"
CLOSED_STATUSES = (RESOLVED_STATUS, UNVERIFIED_STATUS)
# Every standing an issue may hold against the previous round, which is the
# engine's own `ISSUE_STATUSES`. `assert_issue_vocabulary` checks this tuple
# against the installed engine's, so the words are here for the sake of the
# publish path on a machine where the engine is not importable rather than as a
# second opinion about what the engine writes. A status outside the five is
# refused rather than printed: a letter telling the authors an item was `fixed`
# is a word the engine never wrote and a ruling nobody made.
ISSUE_STATUSES = ("new", "persisting", "regressed", RESOLVED_STATUS, UNVERIFIED_STATUS)
# What an issue id looks like, so a published record can be checked against the
# engine's own minting rule rather than trusted. The engine mints `i01`, `i02`
# and so on, and a published request id is that id unchanged.
ISSUE_ID_PATTERN = re.compile(r"^i\d{2,}$")

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

# An arm that convenes no core reviewers is not a review of somebody else's
# manuscript, and so is not a thing this path can publish as one. `draft-check`
# is the one the engine ships: what it runs on a draft of your own, chosen
# specialists and no core track, with nothing in it written by a reader of a
# submitted paper.
#
# The rule has to live here because the engine does not hold such a run back.
# Its publishability rule reads the status, the findings source and the guards,
# none of which a finished draft check fails, so `not_publishable_reasons` comes
# back empty for one and there is no engine sentence to print. What refused it
# before was the panel rule further down, "a published review needs at least one
# reviewer", which is true but reads as a broken run rather than as the wrong
# kind of run.
#
# The arm names themselves are the engine's, read from `review_arms()` rather
# than copied into a list here. A list went stale in one direction only, and
# silently: a new arm with no core track would have published as a peer review
# until somebody noticed the name was missing.
NO_REVIEWERS = 0

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


def maybe_json_list(path: Path) -> list:
    """What one run file holds when it holds a list, and nothing otherwise.

    The same reading as `maybe_json`, for the files the engine writes as an
    array rather than an object. `map.json` is one: a row per piece of the
    manuscript, in the order they were laid down.
    """
    path = Path(path)
    if not path.is_file():
        return []
    try:
        value = read_json(path)
    except (OSError, ValueError):
        return []
    return value if isinstance(value, list) else []


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
            "PeerReviewAgents 0.10.0 or newer, or run this with the virtual "
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
            "PeerReviewAgents 0.10.0 or newer, or run this with the virtual "
            "environment the review ran in."
        ) from exc


def planned_arms() -> dict | None:
    """The engine's own table of what each arm runs, or `None` with no engine.

    `review_arms()` is the engine's public answer to "what does this arm do",
    one row per arm, and it is the only honest source for whether an arm
    convenes core reviewers at all. `None` rather than a refusal because the
    gate below has a second source for that one fact, the reviewer count the
    run itself recorded, and refusing a publish over a missing arm table would
    turn a question this path can still answer into a dead end.
    """
    try:
        arms = getattr(importlib.import_module(ENGINE_PACKAGE), "review_arms")
    except (ImportError, AttributeError):
        return None
    table = arms()
    return table if isinstance(table, dict) else None


def not_a_review_arm(run: dict, arms: dict | None) -> str:
    """Why this run's arm is no review of a submitted manuscript, or "".

    Two sources for one fact, in order. The engine's table says what the arm
    convenes, which is the answer for any run on any machine with the engine
    installed, and it names an arm the installed engine does not define rather
    than waving it through. Without a table the run's own recorded reviewer
    count stands in: it is the same number for the arms that ship, and a run
    that convened nobody is not a review whichever source said so.
    """
    arm = str(run.get("arm") or "")
    if arms is None:
        reviewers = run.get("reviewers")
        if isinstance(reviewers, int) and not isinstance(reviewers, bool):
            if reviewers > NO_REVIEWERS:
                return ""
        else:
            return ""
        described = "an arm that convenes no core reviewers"
    else:
        planned = arms.get(arm)
        if planned is None:
            return (
                f"This run used the {arm} arm, which the installed engine does "
                f"not define. It runs {', '.join(sorted(arms))}. Publish with "
                "the engine the review ran on, so what the record says the arm "
                "did is what the arm does."
            )
        if planned.get("reviewers") != NO_REVIEWERS:
            return ""
        described = str(planned.get("summary") or "").strip() or (
            "an arm that convenes no core reviewers"
        )
    return (
        f"This run used the {arm} arm, which the engine describes as "
        f"\"{described}\". It convenes no core reviewers, so nobody outside the "
        "authorship read the paper and there is no review in it to publish. Run "
        "the review arm the study asks for, or drop --publish to keep this "
        "bundle as a rehearsal."
    )


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
    if (sibling / "manifest.json").is_file():
        return sibling
    raise CommandError(
        f"No manuscript workspace at {sibling}, so this run cannot be tied to "
        "the paper that was prepared. Pass --workspace with the folder holding "
        "manifest.json beside paper.md and map.json."
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


# The role engine 0.9.0 gives the `cite-1..cite-N` slots of its citation lane.
# A worker looks references up and writes rows into the citation ledger. It
# writes no finding, no track report and no part of the letter, so it is never
# counted among the agents that reviewed the manuscript, and a worker observed
# running a model family other than its assigned one does not make the run
# unpublishable. Both facts follow from the same thing: nothing a worker did is
# quoted in the review.
CITATION_WORKER_ROLE = "citation-worker"

# The role engine 0.10 gives the slot that reads the manuscript against its own
# page images before any reviewer starts. The reader rewrites an equation the
# converter mangled, describes each figure, transcribes a page the converter
# returned nothing from, and then the manuscript is sealed and its line numbers
# stop moving. It files no finding and writes no report, so it did not review
# the paper and is not counted among the agents that did. What it did is
# published in `ingest` instead, beside the other measurements of the text the
# panel was handed, because that is what it is a statement about.
READER_ROLE = "reader"


def is_citation_worker(row: dict) -> bool:
    """Whether this agent row is a citation lane worker rather than a reviewer."""
    return str(_dict(row).get("role") or "") == CITATION_WORKER_ROLE


def is_reader(row: dict) -> bool:
    """Whether this agent row read the manuscript rather than reviewed it."""
    return str(_dict(row).get("role") or "") == READER_ROLE


def reader_slots(agents: list[dict]) -> list[str]:
    """The slots that read the manuscript against its pages, by name.

    Named rather than counted, for the same reason the citation lane's workers
    are: a reader of the model table needs to be able to find those rows and see
    that the model beside them wrote no part of the review.
    """
    return sorted(
        str(row.get("slot"))
        for row in _list(agents)
        if is_reader(row) and _dict(row).get("slot")
    )


def citation_workers(agents: list[dict]) -> list[str]:
    """The slots of the citation lane, named so no count can mistake them.

    Returned as a list of slot names rather than a count, because the thing a
    reader needs is the ability to find those rows in the model table and see
    that they are not reviewers. The role is read off the row the engine wrote
    rather than matched against the `cite-` prefix, so a lane the engine renames
    keeps working as long as it keeps writing the role.
    """
    return sorted(
        str(row.get("slot"))
        for row in _list(agents)
        if is_citation_worker(row) and _dict(row).get("slot")
    )


def reviewing_agents(agents: list[dict]) -> list[dict]:
    """The rows that wrote some part of the review, workers and reader left out.

    Every statement about who reviewed the manuscript is counted over this
    rather than over every row: how many agents ran, which models wrote the
    review, and whether one model wrote all of it. Four citation workers on a
    cheaper model would otherwise make a panel look more varied than it was,
    which is the wrong answer in the one direction that matters.

    The reader is left out for a second reason as well. The published model map
    says which model wrote which report, and the reader wrote none: it produced
    the text the panel then read. Its model is published where that fact
    belongs, in the manuscript's own record.
    """
    return [
        row for row in _list(agents)
        if not is_citation_worker(row) and not is_reader(row)
    ]


def citation_record(reading: dict) -> dict:
    """The state of the run's citation lane, for the published record.

    The engine hands back `citations` with `enabled`, `ledger`, `counts`,
    `complete`, `summary` and `problems`. Three of those are reshaped here.

    The ledger path is dropped, both the absolute one in `citations['ledger']`
    and the relative one in `counts['ledger']`. The bundle does not carry the
    ledger file, so a path in a published record points at nothing a reader can
    open, and the absolute form names the machine that wrote the record.

    `counts['stages']` is dropped too. It is the lane's own stage record, which
    is useful while a run is going and says nothing a reader of a finished
    review can act on, and leaving it in would put a nested object inside a map
    of tallies where every other value is a number.

    `complete` and `stages_done` are promoted out of the counts, because they
    are answers rather than tallies, and they answer different questions: every
    stage ran to the end, against the table actually checked something. An
    empty ledger satisfies the first and fails the second.

    Nothing here decides whether the lane finished well. An unfinished ledger
    does not hold a review back, the engine says so, and the lines it wrote
    about what was not checked are carried through word for word.
    """
    citations = _dict(reading.get("citations"))
    if not citations:
        return {}
    counts = _dict(citations.get("counts"))
    record: dict = {
        "enabled": bool(citations.get("enabled")),
        "complete": bool(citations.get("complete")),
        "counts": {
            str(key): int(value)
            for key, value in counts.items()
            if isinstance(value, int) and not isinstance(value, bool)
        },
        "problems": [str(p).strip() for p in _list(citations.get("problems")) if str(p).strip()],
    }
    if isinstance(counts.get("stages_done"), bool):
        record["stages_done"] = counts["stages_done"]
    summary = str(citations.get("summary") or "").strip()
    if summary:
        record["summary"] = summary
    workers = citation_workers(reading.get("agents"))
    if workers:
        record["workers"] = workers
    return record


# What the code under review was taken from, in the engine's words: a
# repository it cloned, or a folder on the machine that ran the review. The
# difference decides what a published record can say about where the code came
# from, because one of the two is an address a reader can open and the other is
# a directory on somebody's computer.
CODE_CLONE = "git-clone"
CODE_FOLDER = "folder"

# The keys of the engine's code block that are a count or a word, copied as
# they are. `snapshot` and `manifest` are deliberately not among them, which
# `code_record` explains.
#
# `source_cut` is the count that limits what the review may claim: above zero a
# cap left program source out of the snapshot, so the code reader did not have
# the whole of the code and no finding from it may say the code never does
# something. The five `data_` counts are the data the code ships, which the
# engine lists rather than copies and fetches only when a reviewer asks for a
# file, so what was there and what was read are two different numbers and the
# second is the one that says what the review rests on.
CODE_COUNTS = ("files_in_snapshot", "files_skipped", "opened", "searches", "source_cut",
               "data_listed", "data_fetched", "data_partial", "data_refused", "data_bytes")


def code_record(reading: dict) -> dict:
    """Whether code was reviewed beside the paper, for the published record.

    The engine answers this for every run, including every run that was given
    no code, so the record answers it too rather than leaving a reader of a
    review with no code block to wonder whether the question was asked. A run
    with none publishes `reviewed: false` and nothing else, because the rest of
    the engine's block is empty for it.

    Two of the engine's fields are not published. `snapshot` is the absolute
    path of `<run>/code/` on the machine that ran the review, and the bundle
    does not carry that folder, so the path names a stranger's computer and
    points at nothing a reader has. `manifest` is the snapshot's own manifest,
    one row per file taken with its digest and one per path left out, and it
    carries the origin as an absolute path as well. What a reader of a finding
    needs out of it, the file and the lines and the digest of the file they were
    read from, the finding itself carries.

    Where the code came from is published as the caller named it only when that
    is an address rather than a directory. A clone's source is the repository
    URL, which is the one fact that lets a reader fetch the code and check the
    commit for themselves, so it is published whole and beside the commit. A
    folder's source is a resolved path on one machine, so only its own name is
    published, which is what the engine's own REVIEW.md prints for the same
    reason.
    """
    code = _dict(reading.get("code"))
    if not code:
        return {}
    record: dict = {"reviewed": bool(code.get("reviewed"))}
    if not record["reviewed"]:
        return record
    kind = str(code.get("kind") or "")
    if kind:
        record["kind"] = kind
    source = str(code.get("source") or "").strip()
    if source and kind == CODE_CLONE and not looks_like_a_path(source):
        record["source"] = source
    elif source:
        record["source_name"] = Path(source).name
    for key in ("commit", "branch", "truncated"):
        value = str(code.get(key) or "").strip()
        if value:
            record[key] = value
    # A folder that is not a checkout has no clean or dirty state to report, and
    # the engine says so with `None` rather than with `False`.
    if isinstance(code.get("dirty"), bool):
        record["dirty"] = code["dirty"]
    for key in CODE_COUNTS:
        if isinstance(code.get(key), int) and not isinstance(code.get(key), bool):
            record[key] = code[key]
    # Which files the lane actually opened, by their path inside the snapshot.
    # The counts above say how much there was to read and the engine counts the
    # opening, and this says which files they were, because a code reader that
    # opened the one file the paper names and no other is a narrower claim than
    # the count alone can make.
    opened = [str(path) for path in _list(code.get("files_opened")) if str(path).strip()]
    if opened:
        record["files_opened"] = opened
    return record


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


def issues_document(reading: dict) -> dict:
    """The two facts about `issues.json` that belong to the file, not the review.

    `read_run` answers everything about the review itself, and a bundle needs
    two things that are properties of the document instead: the schema it was
    stamped with, and every issue id this manuscript has spent. The ids matter
    because the next round is handed this bundle's own `issues.json` as its
    prior round, and a prior file that cannot account for the ids already used
    lets round two mint an id round one had already given out.

    The file is located through `reading['reports']`, the engine's own map of
    what is on disk, the same way `startup_stamp` locates `startup.json`.
    Nothing else is read out of it. The status rule, the issues and the
    findings all stay the engine's reading, so there is still one reader.

    The stamp is checked rather than copied. A document written under a schema
    this release does not publish may mean something else by the same field
    names, and a letter rendered from a half-understood file is worse than no
    letter, so an unknown stamp is a refusal here as it is in the engine.
    """
    why = "an issues document cannot be checked"
    path = _dict(reading.get("reports")).get("issues")
    document = maybe_json(Path(str(path))) if path else {}
    if not document:
        return {}
    stamp = str(document.get("schema_version") or "")
    known = str(engine_public("ISSUES_SCHEMA_VERSION", why) or "")
    if stamp != known:
        raise CommandError(
            f"The run's issues.json is stamped {stamp or 'with nothing'} and this "
            f"pipeline publishes {known}. The engine that wrote the run and the "
            "engine installed here are different releases. Install the release "
            "the run was written by, or rerun the review."
        )
    return {
        "schema_version": stamp,
        "issue_ids_used": [str(i) for i in _list(document.get("issue_ids_used"))],
        # The code check lives in this document and nowhere else a reader of the
        # run can reach: `read_run` answers the review, and the rows that say
        # which findings the code threw out are written here beside the issues.
        "code_check": code_check_record(document),
    }


# How the code check can answer one finding. `contradicted` is the one with
# teeth: the code does not do what the finding said, the engine refuses the
# editor if it groups such a finding into an issue, and so this pipeline may
# never print one as something the authors have to change.
CODE_CHECK_VERDICTS = ("contradicted", "confirmed", "not-shown")

# What one answer of the code check publishes. `recorded`, the moment the row
# was written, is deliberately not among them: the run record already says when
# the run happened, and the minute one finding was answered tells a reader of
# the review nothing it can use.
CODE_CHECK_FIELDS = ("finding_uid", "verdict", "slot", "track", "title", "severity",
                     "document", "line", "end_line", "quote", "finding_slot",
                     "finding_track", "basis", "assumed_method", "note")

# The fields of the code the check read to decide one finding, which the engine
# verified against the snapshot before it stored the row. The quoted text and
# its address, and nothing else of the file.
CODE_EVIDENCE_FIELDS = ("path", "start_line", "end_line", "text", "sha256")


def code_check_record(document: dict) -> dict | None:
    """What reading the code did to the findings that rested on a method.

    `None` on a run that was given no code, which is the engine's own answer
    for one and is kept as `None` rather than as an empty record: a review with
    no snapshot had no such stage, and an empty block would read as a stage
    that ran and found nothing to say.

    Every row is copied field by field rather than passed through. The rows are
    the only place a thrown-out finding appears at all, so they go into the
    published bundle, and a bundle is read by strangers: what is published is
    the finding the check was about, the verdict, the quoted lines of code that
    decided it and the note written for the authors. The timestamps and the
    engine's own bookkeeping stay in the run folder.
    """
    record = _dict(document.get("code_check"))
    if not document.get("code_check") or not record:
        return None
    rows = []
    for row in _list(record.get("checks")):
        row = _dict(row)
        kept = {key: row.get(key) for key in CODE_CHECK_FIELDS if row.get(key) not in (None, "")}
        kept["verdict"] = str(row.get("verdict") or "")
        evidence = _dict(row.get("code_evidence"))
        if evidence:
            kept["code_evidence"] = {
                key: evidence.get(key) for key in CODE_EVIDENCE_FIELDS
                if evidence.get(key) not in (None, "")
            }
        searched = [str(one).strip() for one in _list(row.get("searches")) if str(one).strip()]
        if searched:
            kept["searches"] = searched
        rows.append(kept)
    counts = _dict(record.get("counts"))
    return {
        "cap": record.get("cap"),
        "checked": record.get("checked"),
        "over_cap": record.get("over_cap"),
        "counts": {word: counts.get(word, 0) for word in CODE_CHECK_VERDICTS},
        "checks": rows,
    }


def contradicted_findings(package: dict) -> set[str]:
    """Every finding the code check threw out, by uid.

    One set, read by the publish gate and by the renderer. A finding in it was
    raised by a reviewer, read against the code, and found to rest on a claim
    the code contradicts. It stays on the ledger and in this review's own
    account of what was thrown out, and it may not appear anywhere in the
    bundle as something the authors are being asked to do.
    """
    record = _dict(package.get("code_check"))
    return {
        str(_dict(row).get("finding_uid") or "")
        for row in _list(record.get("checks"))
        if str(_dict(row).get("verdict") or "") == "contradicted"
    } - {""}


def assert_issue_vocabulary() -> None:
    """Check this file's copies of the issue words against the engine's own.

    The ordering rules below are a line each and they are written here rather
    than imported: `peerreviewagents.issues` is a module inside the engine, and
    the surface the engine supports is the package, so importing it would be
    reaching into internals that are free to move between releases.

    What that costs is the risk of the words drifting apart, so the words are
    checked instead of trusted. A release that renamed a severity or a status
    would otherwise file every issue as a suggestion, or publish a prior issue
    nobody ruled on as one of this round's required changes, and both would be
    silent. This refuses instead, naming the word that moved.
    """
    why = "the issue vocabularies cannot be checked"
    # The engine publishes these as tuples, and `_list` is for values read out
    # of JSON, where a tuple cannot appear. Reading them with it found no words
    # at all and refused every run, so the sequence is taken as it comes and a
    # value that is not one is reported as unreadable below.
    def words(name: str) -> list[str]:
        value = engine_public(name, why)
        if isinstance(value, (list, tuple)):
            return [str(word) for word in value]
        return []

    severities = words("ISSUE_SEVERITIES")
    statuses = words("ISSUE_STATUSES")
    missing = [w for w in (*REQUIRED_SEVERITIES, SUGGESTION_SEVERITY) if w not in severities]
    missing += [w for w in ISSUE_STATUSES if w not in statuses]
    # And the other direction, for the statuses alone. A release that added a
    # sixth standing would have every row carrying it refused by
    # `assert_publishable_issues`, with a message about a word the engine does
    # write, so the gap is reported here instead and names the new word.
    missing += [w for w in statuses if w not in ISSUE_STATUSES]
    if missing:
        raise CommandError(
            "This pipeline and engine "
            f"{ENGINE_PACKAGE} do not agree on the issue words: "
            f"{', '.join(sorted(set(missing)))}. The engine's severities are "
            f"{', '.join(severities) or 'unreadable'} and its statuses are "
            f"{', '.join(statuses) or 'unreadable'}. Update the publish path "
            "before publishing a run from this release."
        )


def review_package(reading: dict) -> dict:
    """The editor's review, in the shape the documents are rendered from.

    Engine 0.10.0 reports one review rather than a letter and an appendix: the
    issues the editor raised, each carrying the findings it was raised from.
    Nothing is placed out of sight any more, so there are no two lists to
    gather. The major and moderate issues in `rank` order are the required
    changes, the minor ones are the suggestions, and a prior issue this round
    closed out is reported against the round that raised it.

    The findings ledger is carried beside the issues because an issue member
    holds the evidence fields and not the reviewer's own words: `comment`,
    `basis_reason` and `counterevidence` are on the finding, and the letter
    joins them back on by `finding_uid`.

    `schema_version` and `issue_ids_used` come from the document rather than the
    reading, and they are published because this record is what the next round
    is handed as its prior round.
    """
    document = issues_document(reading)
    return {
        "schema_version": document.get("schema_version"),
        "issues_source": reading.get("issues_source"),
        "issue_ids_used": [str(i) for i in _list(document.get("issue_ids_used"))],
        "issues": [_dict(issue) for issue in _list(reading.get("issues"))],
        "prior_round": _dict(reading.get("prior_round")),
        # The ledger, de-duplicated by the engine, in full. Every issue member
        # names a row in it.
        "findings": [_dict(finding) for finding in _list(reading.get("findings"))],
        "summary": reading.get("summary"),
        "verdict": _dict(reading.get("verdict")),
        "limitations": _list(reading.get("limitations")),
        "escalation_rulings": _list(reading.get("escalation_rulings")),
        "review_guard_status": reading.get("guard_status"),
        "findings_source": reading.get("findings_source"),
        "quarantined_findings": _list(reading.get("quarantined")),
        # What the code check did, or `None` on a run that was given no code.
        # It is carried in the package rather than derived at render time
        # because a thrown-out finding appears nowhere else: it is in no issue,
        # and the next round is handed this bundle.
        "code_check": document.get("code_check"),
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
    put("citations", citation_record(reading))
    # Whether code was reviewed beside the paper. This one is published for
    # every run and not only for the runs that had code, because `reviewed:
    # false` is the answer a reader of a review of a computational paper needs
    # and an absent block is not that answer.
    put("code", code_record(reading))
    record["errors"] = run_errors(reading)
    return record


def unfinished_lane_lines(reading: dict) -> set[str]:
    """The problems lines that are unfinished work rather than harm.

    Engine 0.9.0 appends two kinds of line to `problems` after it has already
    decided `publishable`, so a run it publishes can carry them: the citation
    lane's own account of what it did not check, and a citation worker slot
    observed running a model family other than the one it was assigned. Neither
    is a thing that went wrong with the review, and the engine's own
    instruction is to show them beside the findings and not to gate on them.

    The citation lines are taken from `citations['problems']`, where the engine
    repeats them. The worker lines are found by their slot: the engine writes
    each one as `<slot> was assigned ... but ran ...`, so a line whose first
    word is one of this run's citation worker slots is one of them. Matching the
    slot rather than the sentence means a reworded engine message is still
    recognised, and a reviewer slot's substitution line is still an error here,
    which it has to be: that one does make the run unpublishable.
    """
    lines = {
        str(p).strip()
        for p in _list(_dict(reading.get("citations")).get("problems"))
        if str(p).strip()
    }
    workers = set(citation_workers(reading.get("agents")))
    if workers:
        for problem in _list(reading.get("problems")):
            text = str(problem).strip()
            if text and text.split(" ", 1)[0] in workers:
                lines.add(text)
    return lines


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

    Nor is the citation lane's unfinished work. Engine 0.9.0 appends a line to
    `problems` for each citation stage that did not answer and for each
    citation worker that ran another model family, and it appends them after it
    has decided the run publishable, which says plainly that it does not read
    them as harm. Filing them here would publish "4 references could not be
    checked because the lookups did not answer" as something that went wrong
    with the review, when what it describes is work the lane did not get to.
    They are published as the lane's own state instead, in `citations`, and
    `unfinished_lane_lines` is what keeps the two apart.
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
    # the record carries the engine's own list of them. The lane lines the
    # engine appends to the same list after it has called the run publishable
    # are not those, and they are left out here and published as the lane's own
    # state instead.
    lane = unfinished_lane_lines(reading)
    for problem in _list(reading.get("problems")):
        text = str(problem).strip()
        if text and text not in errors and text not in lane:
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

    The workspace is read through the engine's own `verify_workspace`, which
    re-digests every file the import manifest lists before it answers. A folder
    whose `paper.md` was edited after the import is refused there by name, and
    that matters more now than it did: a finding cites a line of that file, so
    an edited manuscript turns every citation in the review into a line number
    about text nobody reviewed.
    """
    manifest_path = Path(workspace) / "manifest.json"
    why = "this run cannot be tied to the paper that was prepared"
    if not manifest_path.is_file():
        legacy = (
            " It holds paper.json, which is an import from before the engine "
            "wrote paper.md, and this pipeline does not read it: re-import the "
            "manuscript."
            if (Path(workspace) / "paper.json").is_file() else ""
        )
        raise CommandError(
            f"No manifest.json in {workspace}, so {why}. Point --workspace at "
            "the manuscript folder the run imported, the one holding paper.md, "
            f"map.json and manifest.json.{legacy}"
        )
    verify = engine_public("verify_workspace", why)
    try:
        base = verify(str(workspace))
    except (ValueError, KeyError, OSError) as exc:
        raise CommandError(
            f"The engine refused the manuscript workspace at {workspace}, so "
            f"{why}: {exc}. Every finding in this run cites a line of that "
            "folder's paper.md, so a folder that no longer matches its own "
            "import manifest cannot be published as what was reviewed."
        ) from exc
    paper = _dict(getattr(base, "manifest", None))
    # The engine's own name for the main document, against the copy this file
    # keeps for the engine-free half. Checked here rather than trusted: a
    # release that renamed the file would otherwise be refused below for holding
    # no paper.md, which names the wrong problem and sends the operator looking
    # at their own import.
    engine_main = str(engine_public("MAIN_DOCUMENT", why) or "")
    if engine_main != MAIN_DOCUMENT:
        raise CommandError(
            f"The engine calls a manuscript's main document {engine_main} and "
            f"this pipeline reads {MAIN_DOCUMENT}, so {why}. The engine that "
            "wrote the run and the publish path here are different releases. "
            "Update the publish path before publishing a run from this release."
        )
    # What shape the folder is in is the engine's question, and `verify_workspace`
    # answers it above: it refuses a base stamped `paper-base-v1`, a manifest
    # carrying no stamp at all and a base with no manifest beside it, each by
    # name. What this pipeline needs from that stamp is what the engine needs
    # from it, since a v1 map records where every piece sits and not where its
    # text came from, so a review published over one could not say which of its
    # lines a model wrote. Reading the field again here would be this
    # repository's second opinion about a folder the engine has already refused,
    # in wording the operator would then see twice.
    documents = [str(name) for name in _list(base.document_names())]
    if MAIN_DOCUMENT not in documents:
        raise CommandError(
            f"The manuscript workspace at {workspace} holds no {MAIN_DOCUMENT}, "
            f"so {why}. It holds {', '.join(documents) or 'no documents'}. This "
            "publish path names the manuscript's own document when it prints "
            "where a passage stands, and naming a file the import does not hold "
            "would tell the authors to look in a document that is not there."
        )
    imported = str(_dict(paper.get("source")).get("sha256") or "")
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
    workspace_paper_id = str(getattr(base, "paper_id", "") or paper.get("paper_id") or "")
    run_paper_id = str(run.get("paper_id") or "")
    if not workspace_paper_id:
        raise CommandError(
            f"The manifest.json in {workspace} records no paper id, so this run "
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
    return {
        "workspace_manifest_sha256": digest(manifest_path.read_bytes()),
        "paper_id": workspace_paper_id,
    }


def issue_rank(issue: dict) -> int:
    """One issue's place in the editor's order, or last for a row without one.

    The engine ranks the issues a round raised from 1, and leaves `rank` null on
    a prior issue it closed out, which is ranked against the round it came from
    and carries `prior_rank` instead.
    """
    rank = _dict(issue).get("rank")
    return rank if isinstance(rank, int) else 10 ** 6


def prior_rank(issue: dict) -> int:
    """Where a closed-out issue sat in the round that raised it."""
    rank = _dict(issue).get("prior_rank")
    return rank if isinstance(rank, int) else 10 ** 6


def all_issues(package: dict) -> list[dict]:
    """Every issue row the run reported, in the order the document holds them."""
    return [i for i in _list(package.get("issues")) if isinstance(i, dict)]


def live_issues(package: dict) -> list[dict]:
    """Every issue this round raised, in the editor's rank order.

    A prior issue this round closed out is not one of them: it is reported
    against the round that raised it and the authors have nothing to answer for
    it now.
    """
    live = [i for i in all_issues(package) if str(i.get("status")) not in CLOSED_STATUSES]
    return sorted(live, key=issue_rank)


def required_issues(package: dict) -> list[dict]:
    """The required changes: the major and moderate issues, in rank order.

    This is the whole list. Nothing is capped and nothing is held back, which is
    why there is no appendix any more.
    """
    return [i for i in live_issues(package)
            if str(i.get("severity")) in REQUIRED_SEVERITIES]


def suggestion_issues(package: dict) -> list[dict]:
    """The suggestions: the minor issues, in rank order."""
    return [i for i in live_issues(package)
            if str(i.get("severity")) == SUGGESTION_SEVERITY]


def resolved_issues(package: dict) -> list[dict]:
    """The prior issues the editor agent ruled fixed, in their prior order."""
    return sorted((i for i in all_issues(package)
                   if str(i.get("status")) == RESOLVED_STATUS), key=prior_rank)


def unverified_issues(package: dict) -> list[dict]:
    """The prior issues nobody raised again and nobody ruled fixed.

    Still open. The status exists precisely because it is not a fix.
    """
    return sorted((i for i in all_issues(package)
                   if str(i.get("status")) == UNVERIFIED_STATUS), key=prior_rank)


def closed_issues(package: dict) -> list[dict]:
    """Every prior issue closed out this round, the ruled ones first."""
    return resolved_issues(package) + unverified_issues(package)


def issue_members(issue: dict) -> list[dict]:
    """The findings one issue is raised from, as the issue keeps them."""
    return [m for m in _list(_dict(issue).get("members")) if isinstance(m, dict)]


def surviving_passages(issue: dict) -> list[dict]:
    """The prior issue's quoted passages the engine still found in this draft.

    The engine writes one object per passage, `{finding_uid, quote, document,
    line, fingerprint, matched_by}`, so the quote is a field of the row and not
    the row itself. Taking the row for the quote printed a Python dict into a
    real decision letter, under a heading telling the authors that was the text
    still standing in their manuscript. A row carrying no quote is dropped
    rather than printed empty.

    What the engine means by one of these is narrow, and `matched_by` says which
    of two narrow things. `quote` is the earlier finding's words found in this
    draft word for word. `fingerprint` is the passage they were quoted from,
    found by the digest of its own text, so the passage is unchanged while the
    quoted words were not matched: the wording of the quote moved inside it. The
    `line` is where this draft holds it and has nothing to do with the line the
    earlier round cited, because the file is rewritten at every import.

    Either way it is evidence about the text and not a ruling, and where it sits
    under `resolved` the editor agent had to say why the issue is fixed anyway.
    """
    passages = []
    for row in _list(_dict(issue).get("surviving_quotes")):
        if not isinstance(row, dict):
            continue
        quote = str(row.get("quote") or "").strip()
        if not quote:
            continue
        line = row.get("line")
        passages.append({
            "finding_uid": str(row.get("finding_uid") or ""),
            "document": str(row.get("document") or ""),
            "line": line if isinstance(line, int) else None,
            "fingerprint": str(row.get("fingerprint") or ""),
            "matched_by": str(row.get("matched_by") or ""),
            "quote": quote,
        })
    return passages


def finding_index(package: dict) -> dict[str, dict]:
    """The ledger by `finding_uid`, for joining a member back to its finding.

    A member carries the evidence fields and not the reviewer's own prose. The
    comment, what the basis rests on and the strongest counterpoint are on the
    finding in the ledger, and this is how the letter gets them back.
    """
    index: dict[str, dict] = {}
    for finding in _list(package.get("findings")):
        uid = str(_dict(finding).get("finding_uid") or "")
        if uid:
            index[uid] = _dict(finding)
    return index


def issue_finding(package: dict, member: dict) -> dict:
    """The ledger row behind one member, or the member itself as a fallback.

    A run whose ledger file is gone is read by the engine off the issue members
    themselves, so the member is all there is, and rendering from it loses the
    prose rather than the finding.
    """
    uid = str(_dict(member).get("finding_uid") or "")
    return finding_index(package).get(uid) or _dict(member)


def issue_slots(issue: dict) -> list[str]:
    """The reviewer slots that raised one issue, in order and without repeats."""
    slots: list[str] = []
    for member in issue_members(issue):
        slot = str(member.get("slot") or "").strip()
        if slot and slot not in slots:
            slots.append(slot)
    return slots


def issue_is_escalated(issue: dict) -> bool:
    """Whether any reviewer escalated a finding this issue is raised from."""
    return any(member.get("escalate") for member in issue_members(issue))


def escalated_issues(issues: list[dict]) -> list[dict]:
    return [i for i in issues if issue_is_escalated(i)]


def severity_counts(rows: list[dict]) -> dict[str, int]:
    """Major, moderate and minor over issues or findings, which share the word."""
    counts = {"major": 0, "moderate": 0, "minor": 0}
    for row in rows:
        severity = str(_dict(row).get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def escalated(findings: list[dict]) -> list[dict]:
    return [f for f in findings if f.get("escalate")]


def _location(finding: dict) -> str:
    """Where in the manuscript one finding was placed, as the engine placed it.

    Engine 0.10 anchors a quote in the manuscript text itself and records the
    line it reads on, the last line where it runs over several, and the document
    when that is a supplement rather than the paper. A finding with no line is
    not located, which is what an unplaced quote is.
    """
    placement = finding.get("placement")
    if placement not in (None, "anchored"):
        return f"unplaced ({placement})"
    line = finding.get("line")
    if not isinstance(line, int) or line <= 0:
        return "not located"
    end = finding.get("end_line")
    where = f"lines {line}-{end}" if isinstance(end, int) and end > line else f"line {line}"
    document = str(finding.get("document") or "")
    return f"{where} of {document}" if document and document != MAIN_DOCUMENT else where


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


def citation_lane_clause(run: dict) -> str:
    """What the citation lane did, for the method paragraph, or nothing.

    Only a run that planned the lane gets a sentence. A run whose arm convened
    no lane is not a run whose references went unexamined: the citations
    specialist reads the works cited either way, and the tracks clause above
    has already said so, so claiming here that no citation was checked would be
    false in the direction that matters.

    What the sentence says is how much the lane got through and that it did not
    get through all of it. It gives no bucket its own number, because this is a
    paragraph of prose and three numbers that must never be added together do
    not belong in one. They are on the record and on the page, each labelled
    with what it does and does not mean.
    """
    citations = _dict(run.get("citations"))
    if not citations.get("enabled"):
        return ""
    counts = _dict(citations.get("counts"))
    references = counts.get("references")
    if not isinstance(references, int) or references <= 0:
        return (
            " The run planned a citation lane and left no table behind, so that "
            "lane checked no reference and no in-text use."
        )
    judged = counts.get("uses_judged") if isinstance(counts.get("uses_judged"), int) else 0
    uses = counts.get("uses") if isinstance(counts.get("uses"), int) else 0
    clause = (
        f" A citation lane ran beside the panel, looking up the {references} works "
        f"in the reference list and checking {judged} of {uses} in-text uses "
        "against the source each one names."
    )
    if citations.get("problems"):
        clause += (
            " It did not get through all of that, and what it did not check is "
            "listed with the record rather than left to read as checked."
        )
    return clause


def citation_lane_report(run: dict) -> list[str]:
    """What publish prints about the citation lane, one line at a time.

    The editor reading this is about to decide whether to publish, so the three
    states that are not a clean resolution each get their own line with their
    own number and are never summed. A reference nobody could look up and a
    reference two indexes do not list are different facts, and a single
    "unverified: 7" would invite the one reading neither of them supports.
    """
    citations = _dict(run.get("citations"))
    workers = [str(slot) for slot in _list(citations.get("workers"))]
    if not citations.get("enabled"):
        if workers:
            return [
                f"note     {len(workers)} citation worker slot(s) ran and this arm "
                f"planned no citation lane: {', '.join(workers)}"
            ]
        return []
    counts = _dict(citations.get("counts"))
    lines: list[str] = []

    def tally(key: str) -> int:
        value = counts.get(key)
        return value if isinstance(value, int) and not isinstance(value, bool) else 0

    references = tally("references")
    if references:
        lines.append(
            f"cites    {references} reference(s) in the list, {tally('resolved')} confirmed "
            f"against an index, {tally('uses_judged')} of {tally('uses')} in-text use(s) judged"
        )
        states = [
            ("not_found", "with a DOI the registry has no record of"),
            ("not_located", "not listed in either index checked"),
            ("could_not_check", "the lookups could not answer for"),
        ]
        for key, says in states:
            if tally(key):
                lines.append(f"cites    {tally(key)} reference(s) {says}")
        if not citations.get("complete"):
            lines.append("cites    the ledger is unfinished, which does not hold the review back")
    for problem in _list(citations.get("problems")):
        text = str(problem).strip()
        if text:
            lines.append(f"cites    {text}")
    if workers:
        lines.append(
            f"note     {len(workers)} citation worker slot(s) fetched the lookups and wrote "
            f"no part of the review: {', '.join(workers)}"
        )
    return lines


def code_lane_clause(run: dict) -> str:
    """Whether the code behind the paper was read, for the method paragraph.

    Both answers are published. A review that read the code says where the code
    came from and which commit, because a reader who cannot tell which revision
    was read cannot check anything the review says about it, and a review that
    read none says so, because a reader of a computational paper would otherwise
    have to guess whether the panel had the software in front of it. Guessing
    wrong in that direction credits this review with work it did not do.

    A record written by an engine with no code block at all gets no sentence.
    That is a run read by a release older than the one that answers the
    question, and inventing either answer for it would be making it up.
    """
    code = _dict(run.get("code"))
    if not code:
        return ""
    if not code.get("reviewed"):
        return (
            " No code was reviewed beside the manuscript, so everything this "
            "review says about what was computed rests on the manuscript's own "
            "account of it."
        )
    source = str(code.get("source") or "").strip()
    name = str(code.get("source_name") or "").strip()
    commit = str(code.get("commit") or "").strip()
    where = source or (f"the {name} folder" if name else "code the editor supplied")
    at = f" at commit {commit[:12]}" if commit else " at a revision the run did not record"
    dirty = ", which had uncommitted changes in it" if code.get("dirty") is True else ""
    opened = code.get("opened")
    held = code.get("files_in_snapshot")
    read = ""
    if isinstance(opened, int) and isinstance(held, int):
        read = (
            f" That reader opened {opened} of the {held} file(s) the engine took "
            "a copy of, and a finding that rests on the code names the file and "
            "the lines it read, checked against that copy."
        )
    skipped = code.get("files_skipped")
    left = ""
    if isinstance(skipped, int) and skipped:
        left = (
            f" {skipped} path(s) were left out of that copy, so the code reader "
            "did not see them."
        )
    return (
        f" The code behind the paper was reviewed beside it, from {where}{at}"
        f"{dirty}, by one more specialist reading a copy the engine took.{read}{left}"
        f"{code_data_clause(code)}{code_cut_clause(code)}"
    )


def code_data_clause(code: dict) -> str:
    """How much of the data the code ships the reviewer actually read.

    The engine lists a repository's data files and copies one in only when a
    reviewer asks to read it, because the data can run to gigabytes while one
    small table may hold the answer to a finding. So there are two numbers and
    they are not the same claim: how many data files were there to ask for, and
    how many were fetched. A file too large to serve whole comes back as its
    first lines only, and a finding may quote nothing but the lines that were
    stored, which is why a partial read is named rather than counted in with
    the rest. A refused one was never opened at all.

    A run whose snapshot listed no data file gets no sentence. There is nothing
    to report and a sentence saying zero of zero would read as a limitation of
    the review rather than as a fact about the repository.
    """
    listed = code.get("data_listed")
    fetched = code.get("data_fetched")
    if not isinstance(listed, int) or not listed or not isinstance(fetched, int):
        return ""
    clause = (
        f" The snapshot listed {listed} data file(s) the code ships, of which the "
        f"code reader fetched {fetched}"
    )
    partial = code.get("data_partial")
    refused = code.get("data_refused")
    said = []
    if isinstance(partial, int) and partial:
        said.append(
            f"{partial} of those came back as a head of the file only, so a finding "
            "about one may quote only the lines that were stored"
        )
    if isinstance(refused, int) and refused:
        said.append(f"{refused} were refused and never opened")
    if said:
        return clause + ": " + ", and ".join(said) + "."
    return clause + "."


def code_cut_clause(code: dict) -> str:
    """What a size cap left out of the snapshot, where it cut the code itself.

    `files_skipped` counts paths left out for every reason, most of them
    reasons that change nothing about the review: a binary, a file the
    repository does not track, a folder of this tool's own runs. `source_cut`
    is the one that does change something. Above zero, a cap stopped the
    snapshot before it held all of the program source, so the code reader read
    part of the code, and a reader of this review has to be told that before
    reading anything the review says the code does not do.
    """
    cut = code.get("source_cut")
    if not isinstance(cut, int) or isinstance(cut, bool) or cut <= 0:
        return ""
    return (
        f" A size cap left {cut} program source file(s) out of that copy, so the "
        "code reader read part of the code and not all of it, and nothing here "
        "can be read as saying the code never does something."
    )


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
            "finding, ruled on the ones a reviewer escalated, and wrote the "
            "numbered issues the letter asks for."
        )
    elif arm:
        shape += f" The run used the {arm} arm, which convened no specialist readers."
    shape += citation_lane_clause(run)
    shape += code_lane_clause(run)

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


def has_prior_round(package: dict) -> bool:
    """Whether this run was given an earlier round's issues at all.

    The engine records the prior round as the file it read and a digest of it,
    and records nothing on a first round. Every status word is a standing
    against that round, so on a first round there is no round for an issue to
    stand against and the word is left off rather than printed: a first letter
    announcing every item as `new` against a previous round that does not exist
    told the authors a second round had happened.
    """
    return bool(str(_dict(package.get("prior_round")).get("file") or "").strip())


def _issue_tags(issue: dict, package: dict) -> str:
    """How a reader should weigh one issue, in the engine's own vocabulary.

    The id first, because it is the id the authors answer and the id this issue
    keeps in every later round. Then the severity, the category the editor filed
    it under, how many reviewer slots raised it, and, where there was a previous
    round, its standing against it.
    """
    parts = [f"`{str(issue.get('id') or 'no id')}`",
             str(issue.get("severity") or "unstated")]
    category = str(issue.get("category") or "")
    if category:
        parts.append(category)
    raised = issue.get("raised_by")
    if isinstance(raised, int) and raised:
        parts.append(f"raised by {raised} reader{'' if raised == 1 else 's'}")
    status = str(issue.get("status") or "")
    if status and has_prior_round(package):
        parts.append(status)
    if issue_is_escalated(issue):
        parts.append("escalated")
    return ", ".join(parts)


def render_summary(preprint: Preprint, package: dict, provenance: dict) -> str:
    generator = provenance["generator"]
    run = generator["run"]
    required = required_issues(package)
    suggestions = suggestion_issues(package)
    counts = severity_counts(required)
    escalations = escalated_issues([*required, *suggestions])
    closed = closed_issues(package)
    lines = [
        f"# Review Summary: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "**Target venue:** In Silico",
        f"**Generated by:** {generator['engine']['name']} {generator['engine']['version']}, "
        f"{generator['plugin']['workflow_version']}, run locally on the "
        f"{run.get('arm') or 'unrecorded'} arm",
        f"**Required changes:** {len(required)} "
        f"({counts['major']} major, {counts['moderate']} moderate)",
        f"**Suggestions:** {len(suggestions)}",
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
            "Findings raised per track, before the editor pooled them into issues: "
            + ", ".join(f"{track} {count}" for track, count in sorted(tracks.items()))
            + ".",
            "",
        ]
    summary = str(package.get("summary") or "").strip()
    if summary:
        lines += ["## The editor agent's summary of the review", "", summary, ""]
    lines += verdict_section(package.get("verdict"))
    if not required and not suggestions:
        lines += ["## What the review found", "", no_findings_note(run), ""]
    if required:
        lines += ["## Required changes", ""]
        for number, issue in enumerate(required, 1):
            name = str(issue.get("name") or "Unnamed issue").strip()
            lines.append(f"{number}. **{name}** ({_issue_tags(issue, package)})")
        lines.append("")
    if suggestions:
        lines += ["## Suggestions", ""]
        for number, issue in enumerate(suggestions, 1):
            name = str(issue.get("name") or "Unnamed issue").strip()
            lines.append(f"{number}. **{name}** ({_issue_tags(issue, package)})")
        lines.append("")
    if closed:
        lines += [
            "## Carried over from the previous round",
            "",
            f"{len(resolved_issues(package))} ruled fixed and "
            f"{len(unverified_issues(package))} left unverified, which is still "
            "open. The decision letter says what each one was and what the "
            "editor agent said about it.",
            "",
        ]
    limitations = [str(v).strip() for v in _list(package.get("limitations")) if str(v).strip()]
    if limitations:
        lines += ["## Stated limitations of this review", ""]
        lines += [f"- {item}" for item in limitations]
        lines.append("")
    return "\n".join(lines)


def manuscript_citations(workspace: Path, package: dict) -> dict:
    """The manuscript's own line under every quote the issues cite, by finding.

    Engine 0.10 records where a quote reads: the line, and the start and end of
    the quoted characters within it. That is what lets the letter mark the words
    in the line they stand in rather than name a line number and leave the
    authors to find the sentence.

    The characters come back from the engine's own `cited_text` instead of being
    searched for here. The engine placed the quote against its normal form of
    the document, so a second search in this script would pick the wrong one of
    two identical sentences, would miss a quote whose spacing the normal form
    folded, and would not follow a quote over a line break at all. A finding
    with no placement, or one whose offsets the engine left null, gets no row
    and is cited at its line as before.
    """
    why = "the manuscript lines the findings cite cannot be read"
    read_manuscript = engine_public("read_manuscript", why)
    cited_text = engine_public("cited_text", why)
    base = read_manuscript(str(workspace))
    rows: dict[str, dict] = {}
    for issue in _list(package.get("issues")):
        for member in issue_members(issue):
            uid = str(_dict(member).get("finding_uid") or "")
            if not uid or uid in rows:
                continue
            row = _citation_row(base, cited_text, _dict(member))
            if row:
                rows[uid] = row
    return rows


def _citation_row(base: object, cited_text: object, member: dict) -> dict:
    """One member's quote, with the line of the manuscript it was read on."""
    line = member.get("line")
    start = member.get("start")
    end = member.get("end")
    if not isinstance(line, int) or line <= 0:
        return {}
    if not isinstance(start, int) or not isinstance(end, int) or end <= start:
        return {}
    document = str(member.get("document") or MAIN_DOCUMENT)
    text = str(base.line_text(line, document) or "")  # type: ignore[attr-defined]
    if not text or start >= len(text):
        return {}
    anchored = str(cited_text(base, member) or "")  # type: ignore[operator]
    if not anchored:
        return {}
    end_line = member.get("end_line")
    row = {
        "document": document,
        "line": line,
        "end_line": end_line if isinstance(end_line, int) and end_line > line else line,
        "start": start,
        "end": end,
        "line_text": text,
        "anchor_text": anchored,
    }
    # Where this line came from, carried from the map the import wrote. A line
    # a model wrote is quoted the same way as any other and reads the same in
    # the letter, so the fact has to travel with the quote or the letter cannot
    # tell the authors which of the two they are being asked about.
    piece = _dict(base.piece_at(line, document))  # type: ignore[attr-defined]
    source = str(piece.get("source") or "")
    if source:
        row["source"] = source
    if isinstance(piece.get("page"), int):
        row["page"] = piece["page"]
    kind = str(piece.get("kind") or "")
    if kind:
        row["kind"] = kind
    return row


def _quoted_line(citation: dict) -> list[str]:
    """The line a quote was read on, with the quoted characters underlined.

    Printed as code, with a row of carets beneath, because the offsets count
    characters of the line as the engine converted it and only a monospaced
    block puts a caret under the character it marks. A line holding a tab would
    still be marked a column out, which is why the block is the manuscript's
    line rather than a claim about where on the page it sits.

    A quote that runs over a line break is underlined to the end of the line it
    starts on and the line it ends on is named: one row of carets cannot reach
    across two lines, and silently marking only the first part without saying so
    would make a part-quote read as the whole of it.
    """
    text = str(citation.get("line_text") or "")
    start = citation.get("start")
    end = citation.get("end")
    line = citation.get("line")
    if not text or not isinstance(start, int) or not isinstance(end, int):
        return []
    if not isinstance(line, int) or line <= 0 or start >= len(text) or end <= start:
        return []
    end_line = citation.get("end_line")
    runs_on = isinstance(end_line, int) and end_line > line
    stop = len(text) if runs_on else min(end, len(text))
    document = str(citation.get("document") or "")
    where = f"Line {line}"
    if document and document != MAIN_DOCUMENT:
        where = f"Line {line} of {document}"
    # A fence longer than any run of backticks the line itself holds, so a
    # manuscript quoting code cannot close the block early.
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    lines = [
        f"  {where} of the manuscript as the engine converted it, "
        "with the quoted words marked:",
        "",
        f"  {fence}text",
        f"  {text}",
        f"  {' ' * start}{'^' * (stop - start)}",
        f"  {fence}",
        "",
    ]
    if runs_on:
        lines += [
            f"  The quote runs on to line {end_line}, and the marks above reach "
            "only to the end of the line it starts on.",
            "",
        ]
    return lines


def render_decision_letter(
    preprint: Preprint,
    package: dict,
    provenance: dict,
    citations: dict | None = None,
) -> str:
    required = required_issues(package)
    optional = suggestion_issues(package)
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
        lines += [
            "## Required changes",
            "",
            "Numbered in the editor agent's own order of priority. The id in "
            "brackets is this item's name for the life of the manuscript: it is "
            "the id the engine minted for it, and a later round reporting on "
            "this item uses the same one.",
            "",
        ]
        for number, issue in enumerate(required, 1):
            lines += _issue_entry(f"{number}", issue, package, citations)
    if optional:
        lines += [
            "## Suggestions",
            "",
            "Worth doing, and not conditions of the decision.",
            "",
        ]
        for number, issue in enumerate(optional, 1):
            lines += _issue_entry(f"S{number}", issue, package, citations)
    if not required and not optional:
        lines += [
            "## Findings",
            "",
            no_findings_note(provenance["generator"]["run"]),
            "",
        ]
    lines += _prior_round_section(package)
    lines += _code_check_section(package)
    rulings = [r for r in _list(package.get("escalation_rulings")) if isinstance(r, dict)]
    if rulings:
        index = finding_index(package)
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
            title = str(_dict(index.get(uid)).get("title") or "").strip()
            lines += [f"### {title or uid or 'Unidentified finding'}", ""]
            if uid:
                lines += [f"`{uid}`", ""]
            text = str(ruling.get("ruling") or "").strip()
            if text:
                lines += [text, ""]
    return "\n".join(lines)


def _code_check_section(package: dict) -> list[str]:
    """What the code said about the findings that rested on a method claim.

    Nothing at all on a run with no code, and nothing on a run whose code check
    answered nothing and left nothing over its cap.

    The section exists for the thrown-out findings. A finding the code
    contradicts is in no issue, in no required change and in no suggestion, so
    without this section an author would never learn that it was raised at all,
    or that it was read against the code and dropped. Each one is printed with
    the sentence of the paper it was raised against, the lines of code that
    decided it and the note the check wrote, because the reason a finding was
    dropped is itself something an author may want to argue with. The confirmed
    ones are printed too, with their code, so an author can see that a method
    claim in the letter was not taken on trust, and the unsettled ones say what
    was searched rather than leaving the code's silence to be read as a verdict.
    """
    record = _dict(package.get("code_check"))
    if not package.get("code_check"):
        return []
    rows = [_dict(row) for row in _list(record.get("checks"))]
    over_cap = record.get("over_cap")
    over_cap = over_cap if isinstance(over_cap, int) and not isinstance(over_cap, bool) else 0
    if not rows and not over_cap:
        return []
    lines = [
        "## Checked against the code",
        "",
        "Each finding below asserted how something was computed, sampled, "
        "filtered or selected. The code behind the paper was read at the "
        "passage that decides it, before the finding was allowed to become one "
        "of this review's asks.",
        "",
    ]
    headings = {
        "contradicted": "Thrown out: the code does not do what the finding said",
        "confirmed": "Confirmed by the code",
        "not-shown": "The code does not settle it",
    }
    leads = {
        "contradicted": (
            "These are in no issue above, in no required change and in no "
            "suggestion. They are printed here because they were raised, and "
            "because the reason they were dropped is itself something an author "
            "may want to argue with."
        ),
        "confirmed": (
            "The code says what the finding said it says. These findings are in "
            "the letter above like any other, and the code they were checked "
            "against is printed here."
        ),
        "not-shown": (
            "The code neither bore these out nor contradicted them. What was "
            "searched is printed so the silence is not read as a verdict either "
            "way, and each finding stands on its reviewer's reading of the "
            "manuscript alone."
        ),
    }
    for verdict in CODE_CHECK_VERDICTS:
        group = [row for row in rows if str(row.get("verdict") or "") == verdict]
        if not group:
            continue
        lines += [f"### {headings[verdict]}", "", leads[verdict], ""]
        for row in group:
            lines += _code_check_entry(row)
    if over_cap:
        lines += [
            f"**Not checked:** {over_cap} further finding(s) rested on a method "
            "claim and fell past the limit on this stage. They were left exactly "
            "as their reviewers filed them, and the code was not read against "
            "them, which is neither a check nor a clearance.",
            "",
        ]
    return lines


def _code_check_entry(row: dict) -> list[str]:
    """One answer of the code check, with the code it rests on.

    The tags describe the finding and not the lane that checked it. A check row
    carries two slots and two tracks, its own and the finding's, and reading its
    own would label every entry here as the work of the code reader rather than
    of the reviewer who raised it.
    """
    title = str(row.get("title") or "Untitled finding").strip()
    about = dict(row, track=row.get("finding_track") or "", slot=row.get("finding_slot") or "")
    lines = [f"- **{title}** ({_tags(about)})", ""]
    quote = str(row.get("quote") or "").strip()
    if quote:
        lines += [f"  > {quote}", ""]
    assumed = str(row.get("assumed_method") or "").strip()
    if assumed:
        lines += [f"  **The step it assumed:** {assumed}", ""]
    lines += code_evidence_lines(row)
    searched = [str(one) for one in _list(row.get("searches")) if str(one).strip()]
    if searched:
        lines += [f"  **Searched for:** {', '.join(f'`{one}`' for one in searched)}", ""]
    note = str(row.get("note") or "").strip()
    if note:
        lines += [f"  {note}", ""]
    uid = str(row.get("finding_uid") or "").strip()
    if uid:
        lines += [f"  `{uid}`", ""]
    return lines


def _prior_round_section(package: dict) -> list[str]:
    """What this round says about the round before it, and no more than that.

    Two lists, never added together and never printed as one number. The
    editor agent ruled the first fixed and said why, which is one model's
    reading of this draft against the item, not an audit and not a rerun of
    anything. The second it did not rule on at all: nobody raised the item
    again and nobody ruled it fixed, so it is still open, and the quotes the
    engine found still standing in the manuscript are printed with it.
    """
    resolved = resolved_issues(package)
    unverified = unverified_issues(package)
    if not resolved and not unverified:
        return []
    prior = _dict(package.get("prior_round"))
    lines = ["## The previous round's items", ""]
    carried = prior.get("issues")
    if isinstance(carried, int) and carried:
        lines += [
            f"This round was given the previous round's {carried} open item"
            f"{'' if carried == 1 else 's'} and ruled on each one as follows.",
            "",
        ]
    if resolved:
        lines += [
            "### Ruled fixed",
            "",
            "The editor agent read this draft against each item and ruled it "
            "addressed, for the reason given. That is one editor agent's "
            "reading of the text in front of it. Nothing was re-run, no "
            "analysis was reproduced, and this is not an independent audit of "
            "compliance.",
            "",
        ]
        for issue in resolved:
            lines += _closed_entry(issue)
    if unverified:
        lines += [
            "### Left unverified, and still open",
            "",
            "No reviewer raised these again and the editor agent did not rule "
            "them fixed. That is not a fix and it is not evidence of one: a "
            "finding can disappear from text nobody touched. They stand as "
            "open items and are carried into the next round.",
            "",
        ]
        for issue in unverified:
            lines += _closed_entry(issue)
    return lines


def _closed_entry(issue: dict) -> list[str]:
    """One prior-round item, with the engine's own words for where it stands."""
    name = str(issue.get("name") or "Unnamed issue").strip()
    identifier = str(issue.get("id") or "")
    lines = [f"### {identifier or 'no id'}. {name}" if identifier else f"### {name}", ""]
    rank = issue.get("prior_rank")
    standing = [str(issue.get("status") or "unstated")]
    if isinstance(rank, int):
        standing.append(f"item {rank} of the previous round")
    severity = str(issue.get("severity") or "")
    if severity:
        standing.append(severity)
    lines += [f"**Standing:** {', '.join(standing)}", ""]
    statement = str(issue.get("statement") or "").strip()
    if statement:
        lines += [statement, ""]
    reason = str(issue.get("status_reason") or "").strip()
    if reason:
        lines += [f"**The editor agent's reason:** {reason}", ""]
    unchanged = str(issue.get("text_unchanged_reason") or "").strip()
    if unchanged:
        lines += [f"**On the manuscript text:** {unchanged}", ""]
    surviving = surviving_passages(issue)
    if surviving:
        # Labelled, because an unlabelled block quote under the editor agent's
        # reason reads as part of that reason, and the authors could not tell
        # whether they were being shown their own revision or the complaint the
        # issue was raised with. This is the revision as it now reads.
        lines += [
            "**This draft, where the earlier finding's passage still stands:**",
            "",
        ]
        for passage in surviving:
            lines += [f"> {passage['quote']}", ""]
            where = _passage_standing(passage)
            if where:
                lines += [where, ""]
    return lines


def _passage_standing(passage: dict) -> str:
    """How this draft still holds one passage, in the engine's own terms.

    `matched_by` is the whole of the claim. `quote` is the earlier words found
    again word for word. `fingerprint` is the passage found by the digest of its
    text while those words were not matched, which is a weaker thing to tell
    authors and was published as though it were the stronger one. The line is
    this draft's own, so it is named as such: the earlier round's numbering is
    gone, and an author told `line 11` of a file they do not have would look for
    it in the one they do.
    """
    matched = str(passage.get("matched_by") or "")
    line = passage.get("line")
    document = str(passage.get("document") or "")
    where = ""
    if isinstance(line, int) and line > 0:
        where = f"line {line} of this draft as the engine converted it"
        if document and document != MAIN_DOCUMENT:
            where = f"line {line} of {document}, as the engine converted it"
    if matched == "quote":
        reads = "still reads word for word"
    elif matched == "fingerprint":
        reads = (
            "is the same passage by the digest of its text, so the quoted "
            "wording has moved inside it rather than out of the paper"
        )
    else:
        reads = ""
    if not reads:
        return f"Found at {where}." if where else ""
    if not where:
        return f"It {reads}."
    return f"At {where}, it {reads}."


def _issue_entry(
    label: str, issue: dict, package: dict, citations: dict | None = None
) -> list[str]:
    """One issue, with every finding it was raised from under it.

    The issue carries the editor agent's statement of what has to change. The
    evidence under it is the reviewers' own: the member holds the quote and the
    lines it was read on, and the reviewer's comment and what the finding rests
    on are joined back on from the ledger by `finding_uid`.
    """
    name = str(issue.get("name") or "Unnamed issue").strip()
    identifier = str(issue.get("id") or "")
    heading = f"### {label}. {name}"
    if identifier:
        heading += f" [`{identifier}`]"
    lines = [heading, ""]
    slots = issue_slots(issue)
    standing = [f"**Severity:** {str(issue.get('severity') or 'unstated')}  "]
    category = str(issue.get("category") or "")
    if category:
        standing.append(f"**Category:** {category}  ")
    standing.append(
        "**Raised by:** "
        + (", ".join(slots) if slots else "an unrecorded slot")
        + "  "
    )
    status = str(issue.get("status") or "")
    if status and has_prior_round(package):
        prior = str(issue.get("prior_id") or "")
        standing.append(
            f"**Against the previous round:** {status}"
            + (f", as item `{prior}`" if prior else "")
        )
    lines += standing + [""]
    if issue_is_escalated(issue):
        lines += [
            "**A reviewer escalated a finding behind this item as bearing on "
            "the paper's central claim.**",
            "",
        ]
    statement = str(issue.get("statement") or "").strip()
    if statement:
        lines += [statement, ""]
    rebuttal = str(issue.get("rebuttal_quote") or "").strip()
    if rebuttal:
        line = issue.get("rebuttal_line")
        # Which file the passage reads in. A manuscript can be imported as more
        # than one document, and the engine carries the rebuttal's document as
        # a field of its own, empty for the main one. An author sent to a line
        # number with no file beside it would look for it in the paper, which
        # is the wrong file whenever the passage is in a supplement.
        document = str(issue.get("rebuttal_document") or "").strip() or MAIN_DOCUMENT
        at = f", on line {line}" if isinstance(line, int) and line > 0 else ""
        if document != MAIN_DOCUMENT:
            at = f"{at}, in {document}" if at else f", in {document}"
        lines += [
            f"What the manuscript says about it{at}:",
            "",
            f"> {rebuttal}",
            "",
        ]
    audits = [str(a).strip() for a in _list(issue.get("audits")) if str(a).strip()]
    if audits:
        lines += [
            "**Specialist audits behind it:** " + ", ".join(f"`{a}`" for a in audits),
            "",
        ]
    members = issue_members(issue)
    if members:
        lines += [
            f"**Raised from {len(members)} finding"
            f"{'' if len(members) == 1 else 's'}:**",
            "",
        ]
    for member in members:
        lines += _member_entry(member, package, citations)
    return lines


def _written_by_a_model(citation: dict) -> list[str]:
    """What to say under a quote that reads on a line a model wrote.

    An author answering a finding has to know whose words it is about. A figure
    description is a model's account of a picture and appears nowhere in the
    paper, so a finding against it is a finding about the reading rather than
    about the manuscript, and the answer to it is not a revision. A repaired
    equation is printed in the paper and was rewritten because the converter
    misread the page, so the finding is about the authors' own line and the
    marked characters are the model's transcription of it.

    Anything else carrying a source this release does not know by name is
    reported for what the map says and nothing more, which is the only honest
    reading of a word that was added after this code was written.
    """
    source = str(_dict(citation).get("source") or "")
    if not source or source == CONVERTER_SOURCE:
        return []
    page = citation.get("page")
    where = f", page {page} of the original" if isinstance(page, int) else ""
    if source == "ai":
        return [
            "  These are not the authors' words. The line was written by a "
            f"model reading the page image{where}, as a description of a figure "
            "or as text the converter did not return, and it is not printed in "
            "the manuscript.",
            "",
        ]
    if source == "ai-reconstructed":
        return [
            "  This line is printed in the manuscript and the converter misread "
            f"it, so a model rewrote it from the page image{where}. The marked "
            "characters are the model's transcription, and the converter's own "
            "reading is kept beside it in the imported manuscript.",
            "",
        ]
    return [
        f"  The imported manuscript records this line's source as `{source}`, "
        "which this release does not know by name. It is not the converter's "
        "own text layer, so the line may not be the authors' words.",
        "",
    ]


def code_evidence_lines(finding: dict) -> list[str]:
    """The lines of code one finding rests on, and nothing else from the copy.

    A code-checked finding carries the file, the first and last line, the text
    at those lines and the digest of the file they were read from, and the
    engine refuses the finding if the text is not what stands at those lines in
    the copy it took. So this is quotation of checked evidence, and what is
    published is the quotation and the address of it: the file by its path
    inside the copy, the lines by number, the digest so a reader who fetches the
    same commit can confirm they are reading the same file.

    No other part of the copy is published, here or anywhere else in the bundle.
    The author's code is the author's, and a review earns the right to print the
    lines it makes a claim about rather than the right to redistribute the
    repository.
    """
    evidence = _dict(finding.get("code_evidence"))
    path = str(evidence.get("path") or "").strip()
    start = evidence.get("start_line")
    if not path or not isinstance(start, int) or start <= 0:
        return []
    end = evidence.get("end_line")
    where = f"lines {start}-{end}" if isinstance(end, int) and end > start else f"line {start}"
    lines = [f"  **Checked in the code:** `{path}`, {where}.", ""]
    text = str(evidence.get("text") or "")
    if text:
        # An indented block, so every character of the quoted code reads as
        # code. A fence would be opened and closed by the code itself if the
        # code happened to contain one.
        lines += [f"      {row}" for row in text.replace("\t", "    ").splitlines()]
        lines.append("")
    digest = str(evidence.get("sha256") or "").strip()
    if digest:
        lines += [
            f"  That file reads as `{digest[:16]}` in the copy the review read, "
            "which is how a reader who fetches the same commit can tell they "
            "have the same file in front of them.",
            "",
        ]
    return lines


def _member_entry(member: dict, package: dict, citations: dict | None = None) -> list[str]:
    """One finding behind an issue, as the reviewer wrote it."""
    finding = issue_finding(package, member)
    # The member's own values win where it has one, and a field it carries as
    # null does not blank out the ledger's: every member field is present on
    # every member, so a plain merge would hide what the finding recorded.
    row = dict(finding)
    row.update({k: v for k, v in _dict(member).items() if v not in (None, "", [])})
    title = str(row.get("title") or "Untitled finding").strip()
    uid = str(member.get("finding_uid") or "").strip()
    lines = [f"- **{title}** ({_tags(row)})", ""]
    quote = str(row.get("quote") or "").strip()
    if quote:
        lines += [f"  > {quote}", ""]
    # Where those words read, marked in the line itself. `quote` is what the
    # reviewer typed and `anchor_text` is the manuscript's own characters, which
    # can differ in a dash or a capital, so when they differ the letter says
    # which of the two is marked rather than leaving an author to wonder why
    # the underlined words are not the quoted ones.
    citation = _dict(_dict(citations).get(str(member.get("finding_uid") or "")))
    marked = _quoted_line(citation)
    if marked:
        lines += marked
        anchor = str(citation.get("anchor_text") or "").strip()
        if quote and anchor and anchor != quote:
            lines += [
                "  The marked characters are the manuscript's own. The quotation "
                "above it is the reviewer's, and the two differ in how they are "
                "written rather than in where they read.",
                "",
            ]
        lines += _written_by_a_model(citation)
    lines += code_evidence_lines(row)
    comment = str(row.get("comment") or "").strip()
    if comment:
        lines += [f"  {comment}", ""]
    for label, key in (("What it rests on", "basis_reason"),
                       ("Suggested replacement", "replacement"),
                       ("Strongest counterpoint", "counterevidence")):
        text = str(row.get(key) or "").strip()
        if text:
            lines += [f"  **{label}:** {text}", ""]
    if uid:
        lines += [f"  `{uid}`", ""]
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
    pieces = ingest.get("pieces")
    if pieces:
        lines.append(f"- Pieces of the paper mapped: {pieces}")
    text_lines = ingest.get("lines")
    if text_lines:
        lines.append(f"- Numbered lines of {MAIN_DOCUMENT}: {text_lines}")
    lines += [
        "",
        "## How the text was read",
        "",
        f"Imported by {ingest.get('tool') or 'the engine importer'} into one "
        f"Markdown file, {MAIN_DOCUMENT}, holding one piece of the paper per "
        "numbered line, with a map recording each piece's kind, section and "
        "page in the original. Every quotation in this review was found in that "
        "text, and the line it reads on was recorded, before the review was "
        "saved.",
        "",
    ]
    return "\n".join(lines + render_read_stage(ingest))


# What each reason a piece left the manuscript means, in the words a reader of
# the review is owed. The engine names the reason and counts it. The account of
# what was done to the paper is this repository's to give, because `absorbed`
# and `merged` are the engine's vocabulary and not an author's.
GONE_MEANINGS = {
    "absorbed": (
        "A piece counted as `absorbed` is one the converter emitted on its own "
        "that the reader read as debris of another piece, folded into that "
        "piece."
    ),
    "merged": (
        "A piece counted as `merged` is a half of an equation the converter "
        "split, put back into the whole, which is counted above under what the "
        "reader did to the whole."
    ),
    "withdrawn": (
        "A piece counted as `withdrawn` is one this stage added and took out "
        "again."
    ),
}


def render_read_stage(ingest: dict) -> list[str]:
    """What a model wrote into the manuscript, for the statistics page.

    The converted text is not all the converter's. Before any reviewer saw this
    paper a model read its page images, rewrote what the converter mangled,
    wrote a description under every figure and transcribed the pages the
    converter returned nothing from. A reader of the review is owed both halves
    of that: which lines of the manuscript it was, so a quotation can be checked
    against the list, and which pages of the paper exist in the review only
    because a model read them.

    A manuscript nothing read is reported just as plainly. That the equations
    in it are a converter's reading of a picture, and that its figures reached
    the panel as captions with nothing behind them, is as much a limit on what
    the review can be trusted to have seen.
    """
    read = _dict(ingest.get("ai_read"))
    per_source = _dict(ingest.get("pieces_per_source"))
    said = _dict(ingest.get("source_values"))
    written = [row for row in _list(ingest.get("model_written")) if _dict(row)]
    if not read and not per_source and not written:
        return []
    lines = ["## What a model wrote", ""]
    if read.get("read"):
        model = str(read.get("reader_model") or "an unnamed model")
        viewed = read.get("pages_viewed")
        pages = read.get("pages")
        counted = ""
        if isinstance(viewed, int) and isinstance(pages, int) and pages:
            counted = f", which looked at {viewed} of its {pages} pages"
        lines += [
            f"The pages of this paper were read by {model}{counted} before any "
            "reviewer was given the text. It repaired what the converter "
            "misread, re-read a piece the converter had labelled as the wrong "
            "kind as the pieces the page actually prints, described the figures "
            "and transcribed what the converter missed. Every line of the "
            "result that is not the converter's own reading is listed here.",
            "",
        ]
        acted = _dict(read.get("actions"))
        done = [
            f"{name}: {count}"
            for name, count in sorted(acted.items())
            if isinstance(count, int) and count
        ]
        if done:
            lines += [
                "- Pieces of the sealed manuscript by what the reader did to "
                f"each: {', '.join(done)}. This counts the manuscript, so a "
                "piece that is no longer in it is counted below instead.",
                "",
            ]
        gone = _dict(read.get("gone"))
        left = [
            f"{name}: {count}"
            for name, count in sorted(gone.items())
            if isinstance(count, int) and count
        ]
        if left:
            # The pieces the reader took out of the paper, which the count above
            # cannot hold: it walks the pieces the sealed documents have, and
            # these are the ones they do not. A stage that folded three headings
            # away and said so nowhere would leave an author to find the gap by
            # comparing the manuscript against their own PDF.
            # And only the reasons this record carries are explained. A page
            # that glossed every reason the engine knows would tell an author
            # about a merge that never happened to their paper.
            held = [
                name
                for name in sorted(gone)
                if isinstance(gone[name], int) and gone[name]
            ]
            meanings = [GONE_MEANINGS[name] for name in held if name in GONE_MEANINGS]
            unnamed = [name for name in held if name not in GONE_MEANINGS]
            if unnamed:
                # A release that counted a new kind of departure would otherwise
                # print a bare word, and an author cannot be left to guess what
                # was done to a piece of their own paper.
                meanings.append(
                    "A piece counted as "
                    + " or ".join(f"`{name}`" for name in unnamed)
                    + " left the manuscript for a reason this release has no "
                    "account of, and what that was can be read from the engine "
                    "release named in the record."
                )
            lines += [
                "- Pieces that are no longer in the manuscript, by why they "
                f"left it: {', '.join(left)}. {' '.join(meanings)} These do not "
                "add up with the counts above, because the piece that holds a "
                "fold is counted there under what was done to it.",
                "",
            ]
    else:
        reason = str(read.get("reason") or "").strip()
        because = f" The import's own reason: {reason}" if reason else ""
        composed = str(read.get("ai_model") or "").strip()
        pieces = read.get("ai_pieces")
        if composed:
            # A manuscript an application composed from its own source, rather
            # than one converted from a page image. Nothing read a page, and
            # some of the text is still a model's: saying only that no model
            # read the pages would leave a reader to assume the rest is the
            # authors' own words.
            many = (
                f"{pieces} pieces of it were"
                if isinstance(pieces, int) and pieces != 1
                else "one piece of it was"
            )
            lines += [
                "No model read the pages of this paper, because this manuscript "
                "was not converted from page images. It was written from an "
                f"application's own source, and {many} written by {composed} "
                f"rather than taken from that source.{because}",
                "",
            ]
        else:
            lines += [
                "No model read the pages of this paper. Every line of the text "
                "is the converter's, which means an equation or a table in a "
                "quotation is the converter's reading of a picture of it, and "
                f"no figure in the paper has a description behind it.{because}",
                "",
            ]
    note = " ".join(str(read.get("note") or "").split())
    if note:
        # What the reading model knew and no reviewer could find out. On the
        # engine's first real run the reader knew the converter had dropped a
        # table and garbled two others, and said so in a report that reached no
        # file. It is served here under the same label the engine serves it
        # under: that model's account of the document, and not a sentence of
        # the paper or a finding of the review.
        lines += [
            "The model that read the pages left this note about the document. "
            "It is that model's own account of what it found while reading "
            "them, not the authors' text and not a finding of this review:",
            "",
            f"> {note}",
            "",
        ]
    for name, count in sorted(per_source.items()):
        description = str(said.get(name) or "").strip()
        about = f": {description}" if description else ""
        lines.append(f"- `{name}`, {count} pieces{about}")
    if per_source:
        lines.append("")
    if written:
        lines += ["Lines that are not the converter's own reading of the paper:", ""]
        for row in written:
            piece = _dict(row)
            span = [n for n in _list(piece.get("lines")) if isinstance(n, int)]
            where = str(span[0]) if len(span) == 2 and span[0] == span[1] else (
                f"{span[0]} to {span[1]}" if len(span) == 2 else "unrecorded"
            )
            page = piece.get("page")
            printed = f", page {page} of the original" if isinstance(page, int) else ""
            part, of = piece.get("part"), piece.get("of")
            split = (
                f", part {part} of {of} of one piece of the converter's"
                if isinstance(part, int) and isinstance(of, int)
                else ""
            )
            count = piece.get("absorbed")
            folded = ""
            if isinstance(count, int) and count:
                many = "one piece" if count == 1 else f"{count} pieces"
                folded = f", with {many} the converter emitted beside it folded in"
            lines.append(
                f"- {piece.get('document') or MAIN_DOCUMENT} line {where}, "
                f"{piece.get('kind') or 'piece'}, `{piece.get('source')}`"
                f"{split}{folded}{printed}"
            )
        lines.append("")
        if any(isinstance(_dict(row).get("of"), int) for row in written):
            # A part of a re-read is not the same claim as a transcription, and
            # the difference is the whole point of how the engine does it. A
            # table or an equation part was written from the page image. A prose
            # part was not written at all: the reader named the spans to cut and
            # the engine cut them, so the words left on the line are the
            # converter's own. Saying "a model wrote this line" of one of those
            # would tell an author their own sentence was a machine's.
            lines += [
                "A line given as a part of a piece is one of several the reader "
                "read a single piece of the converter's as, because the "
                "converter had labelled that piece as the wrong kind. Where "
                "such a part is a table or an equation, the reader wrote it "
                "from the page image. Where it is prose, the reader wrote "
                "nothing: it named the spans to cut and the engine cut them, so "
                "the words left on the line are the converter's own.",
                "",
            ]
        if any(_dict(row).get("absorbed") for row in written):
            lines += [
                "A line given as holding folded pieces took in what the "
                "converter had emitted beside it as pieces of their own, the "
                "edge of a displayed equation or the numbers off a chart's "
                "axis, which the reader read as part of this piece. Those "
                "pieces are in the manuscript nowhere else. Where a re-read "
                "wrote several lines, the fold is counted on the one the debris "
                "was printed as part of, because one fold is one fold.",
                "",
            ]
    lost = [_dict(row) for row in _list(read.get("lost_pages"))]
    if lost:
        numbers = ", ".join(str(row.get("page")) for row in lost)
        lines += [
            f"Pages the converter returned no text from at all: {numbers}. What "
            "those pages contribute to this review was transcribed from the page "
            "image by the model named above, so nothing on them is the "
            "converter's reading and no part of them was checked against a text "
            "layer. Where each of those pages landed in the text:",
            "",
        ]
        for row in lost:
            # The lines are the point. A page number tells a reader which page
            # of their own PDF nothing was converted from, and the lines tell
            # them which sentences of the review's manuscript came off it, which
            # is what a quotation in the letter can be checked against.
            places = [
                f"{_dict(place).get('document') or MAIN_DOCUMENT} lines "
                f"{_list(_dict(place).get('lines'))[0]} to "
                f"{_list(_dict(place).get('lines'))[1]}"
                for place in _list(row.get("added"))
                if len(_list(_dict(place).get("lines"))) == 2
            ]
            where = ", ".join(places) if places else "nowhere the import recorded"
            lines.append(f"- Page {row.get('page')}: {where}")
        lines.append("")
    return lines


# The fields of the import's own account of the Read stage that a bundle
# publishes. Taken by name rather than copied whole: the account is the
# engine's object and a release that added a path to it would otherwise publish
# this machine's directories with everything else.
AI_READ_FIELDS = (
    "read",
    "reason",
    "reader_model",
    "reader_slot",
    "attempt",
    "pages",
    "pages_viewed",
    "actions",
    # The pieces that are no longer in the manuscript, by why they left it. The
    # counts above are the pieces the sealed documents hold, counted by what was
    # done to each, so a piece folded into the one it was debris of, or added and
    # taken back out, is in no document to be counted there. The engine keeps
    # these as the pieces go, and a stage that folded three headings away would
    # otherwise leave no number anywhere saying it had.
    "gone",
    "tool_calls",
    # A manuscript composed from an application's own source reads `read: false`
    # and still holds lines a model wrote: a description of a figure, an
    # equation the application rebuilt. The engine refuses to write one without
    # the model's name, and records it here with how many pieces it wrote. A
    # bundle publishes both, because a reader asking who wrote a marked line
    # would otherwise be told only that nothing read the pages.
    "ai_model",
    "ai_pieces",
    # The reader's own account of the document, in its words. It exists because
    # the things a reading model learns from the page images are things no
    # reviewer can work out from the text: that the converter dropped a table,
    # that two more came out garbled, that a footnote letter on a sideways page
    # is a best guess. It is published, and labelled as that model's account
    # rather than the authors' prose or a finding of the review, because a note
    # kept in the engine's manifest alone reaches nobody who reads the review.
    "note",
)

# What a map row's `source` says about where that row's text came from. The
# engine publishes its own sentence for each value in the manifest, under
# `source_values`, and that is what a bundle carries: a second wording here
# would be this repository's belief about the engine rather than the engine's
# own account of what it wrote.
CONVERTER_SOURCE = "text"


def ingest_record(workspace: Path | None, manuscript_state: str = "") -> dict:
    """What the reviewers were handed, measured off the workspace with no model.

    Some of those measurements are about a model. Engine 0.10 reads a manuscript
    before any reviewer sees it: a model looks at the page images, rewrites an
    equation the converter mangled, writes a description under every figure, and
    transcribes a page the converter returned no text from at all. So a line the
    panel quoted can be a model's words rather than the authors', and a page of
    the paper can have reached the review only because a model read it off the
    image.

    Both are recorded here, from two places that are written separately. The
    manifest's `ai_read` is the stage's own account of itself, including the
    pages nothing was converted from. The `source` on each row of `map.json` is
    the per-line fact, and it is the one the letter marks a quote against, so
    the record carries the lines and not only the tally.

    `manuscript_state` is the engine's own name for how the folder came to be
    sealed, read off the run rather than worked out here. A base sealed by a
    reader and one sealed with no page read at all hold the same files and are
    not the same manuscript, and the three roads to the second of them look
    alike from the outside: the Read stage was switched off, a reader failed and
    the run sealed what the converter had, or the pieces are an application's
    own source. `ai_read['reason']` is the engine's sentence for which.
    """
    record = {"format": "markdown", "tool": "peerreviewagents import_paper"}
    if manuscript_state:
        record["manuscript_state"] = str(manuscript_state)
    if workspace is None:
        return record
    workspace = Path(workspace)
    manuscript = workspace / MAIN_DOCUMENT
    if manuscript.is_file():
        text = manuscript.read_text(encoding="utf-8")
        record["chars"] = len(text)
        record["text_sha256"] = digest(text.encode())
        record["lines"] = len(text.splitlines())
    manifest = maybe_json(workspace / "manifest.json")
    pieces = _dict(manifest.get("counts")).get("pieces")
    if isinstance(pieces, int):
        record["pieces"] = pieces
    record["base_schema_version"] = str(manifest.get("schema_version") or "")
    record["ai_read"] = read_stage_record(manifest)
    record["pieces_per_source"] = {
        str(name): count
        for name, count in _dict(manifest.get("pieces_per_source")).items()
        if isinstance(count, int)
    }
    record["source_values"] = {
        str(name): str(said)
        for name, said in _dict(manifest.get("source_values")).items()
    }
    record["model_written"] = model_written_lines(workspace)
    return record


def read_stage_record(manifest: dict) -> dict:
    """The import's account of the Read stage, as a bundle publishes it.

    A workspace that was never read carries `read: false` and the import's own
    reason, which is as much a fact about the review as a reader's model is: it
    says the equations in every quotation are the converter's reading of a
    picture of them and that no figure in the paper has a description behind it.

    `lost_pages` is reshaped rather than copied. Each page the engine lists
    carries the pieces it added off it, each one with the draft's own id for it,
    the document it landed in and the lines it became. The id names nothing in a
    bundle, since `map.json` has no ids and a citation is a document and a line,
    so what travels is the page, the words the converter found on it and where
    each transcribed piece ended up. A reader of the review can then go from a
    page the converter returned nothing from to the lines of the manuscript that
    exist only because a model read it, and quote them against the letter.
    """
    account = _dict(manifest.get("ai_read"))
    record = {
        name: account[name] for name in AI_READ_FIELDS if account.get(name) is not None
    }
    record["read"] = bool(account.get("read"))
    # The note travels only where there is one. The engine writes the key on
    # every seal and leaves it empty when the reader filed nothing, and an empty
    # note published as a field reads as a model that had nothing to say about
    # the paper rather than one that was never asked for an account.
    note = " ".join(str(account.get("note") or "").split())
    record.pop("note", None)
    if note:
        record["note"] = note
    # The pieces that left the manuscript, kept only where there is a number to
    # keep. The engine leaves out a reason nothing happened under, and a count
    # that is not a positive number is nothing happening written down, so what
    # travels is the reasons a piece actually left this manuscript.
    gone = {
        str(why): count
        for why, count in _dict(account.get("gone")).items()
        if isinstance(count, int) and count > 0
    }
    record.pop("gone", None)
    if gone:
        record["gone"] = gone
    lost = []
    for page in _list(account.get("lost_pages")):
        row = _dict(page)
        number = row.get("page")
        if not isinstance(number, int):
            continue
        added = []
        for piece in _list(row.get("added")):
            place = _dict(piece)
            span = [int(n) for n in _list(place.get("lines")) if isinstance(n, int)]
            if len(span) != 2:
                continue
            added.append(
                {"document": str(place.get("document") or MAIN_DOCUMENT), "lines": span}
            )
        entry = {
            "page": number,
            "pieces": len(_list(row.get("added"))),
            "added": sorted(added, key=lambda place: (place["document"], place["lines"])),
        }
        words = row.get("words")
        if isinstance(words, int):
            entry["words"] = words
        lost.append(entry)
    record["lost_pages"] = sorted(lost, key=lambda row: row["page"])
    return record


def model_written_lines(workspace: Path) -> list[dict]:
    """Every line of the manuscript a model wrote rather than the converter.

    One row per piece whose `source` is not the converter's own text layer, with
    the lines it occupies, what kind of piece it is and the page it was read
    off. The lines are published and not only counted because they are what a
    reader of the review can check: a quotation in the letter sits on one of
    them or it does not.
    """
    rows = []
    for row in _list(maybe_json_list(workspace / "map.json")):
        piece = _dict(row)
        source = str(piece.get("source") or "")
        if not source or source == CONVERTER_SOURCE:
            continue
        span = [int(n) for n in _list(piece.get("lines")) if isinstance(n, int)]
        if len(span) != 2:
            continue
        entry = {
            "document": str(piece.get("document") or MAIN_DOCUMENT),
            "lines": span,
            "kind": str(piece.get("kind") or ""),
            "source": source,
        }
        page = piece.get("page")
        if isinstance(page, int):
            entry["page"] = page
        original = _dict(piece.get("original"))
        part, of = original.get("part"), original.get("of")
        if isinstance(part, int) and isinstance(of, int) and of > 1:
            # This line is one of several the reader read a single piece of the
            # converter's as, because the converter had labelled that piece as
            # the wrong kind: a table emitted as a paragraph of run-together
            # cells, an equation left in the prose after it. Which part of how
            # many is what tells a reader of the review that the line beside
            # this one came out of the same piece of the paper.
            entry["part"] = part
            entry["of"] = of
        absorbed = _list(original.get("absorbed"))
        if absorbed:
            # How many pieces the converter emitted on their own were folded
            # into this one as its debris, which is in the manuscript nowhere
            # else. A re-read that wrote several lines records the fold on one
            # of them, the line the debris was printed as part of, so the count
            # here is a fold and not a fold once per line the re-read wrote.
            # The count travels and the characters do not: they are the
            # converter's reading of a few marks on a page with no line of the
            # manuscript to cite, and the engine's own map is where they are
            # kept. An author is told that something went in here and can find
            # it on the page.
            entry["absorbed"] = len(absorbed)
        rows.append(entry)
    return sorted(rows, key=lambda row: (row["document"], row["lines"]))


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
    live = live_issues(package)
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
    # What this bundle published, counted off the issues it published rather
    # than off the findings the reviewers wrote. The two are different numbers
    # and always were: the editor agent pools findings into issues, so a round
    # with six findings can publish four items, and the old `findings` count
    # described neither the letter nor the ledger once pooling existed. The
    # ledger's own total stays in `findings_delivered`, which the engine sets.
    #
    # `issues` counts the issues this round raised, which is the engine's own
    # meaning of the word: a prior issue ruled fixed or left unverified is
    # counted under its own name below and is not one of this round's asks.
    run_record["issues"] = len(live)
    run_record["required"] = len(required_issues(package))
    run_record["suggestions"] = len(suggestion_issues(package))
    run_record["resolved"] = len(resolved_issues(package))
    run_record["unverified"] = len(unverified_issues(package))
    run_record["escalated_in_bundle"] = len(escalated_issues(live))
    run_record["issues_source"] = str(package.get("issues_source") or "")
    run_record["issues_schema_version"] = str(package.get("schema_version") or "")
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
    # Both maps say which model wrote which report, so the citation lane's
    # workers are left out of them: a worker writes no report. Their rows stay
    # in `agents` above, with their own models beside them, which is where a
    # reader can see what the lane ran without it being counted as a reading of
    # the manuscript.
    reviewers_only = reviewing_agents(agents)
    models = model_map(reviewers_only)
    assigned = assigned_map(reviewers_only)
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
        # Which round of review this is, counted by the prepare step from the
        # drafts of this paper already reviewed here. It used to be the literal
        # 1 in every record, including the second round published against the
        # same paper, which is the kind of field a reader checks a claim
        # against. Nothing in the ids depends on it now: an item is named by the
        # engine's issue id, which does not carry a round in it.
        "round": int(prepared.get("round") or 1),
        # What this round was given to rule against: the file, its digest and
        # how many items were in it, as the engine reports them. No path, and
        # nothing from this machine.
        "prior_round": _dict(package.get("prior_round")),
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
    """Hash every file in the bundle, so a later edit to one is visible.

    Every file but the bundle's own manifest, which cannot hold its own digest.
    A file named `manifest.json` anywhere below the bundle is hashed like any
    other: excluding it by name would let a copied workspace manifest sit inside
    a published bundle as the one file nothing covers.
    """
    dest = Path(dest)
    own = dest / "manifest.json"
    files = {
        path.relative_to(dest).as_posix(): digest(path.read_bytes())
        for path in sorted(dest.rglob("*"))
        if path.is_file() and path != own
    }
    write_json(dest / "manifest.json", {"schema_version": 1, "files": files})


def _closed_row(issue: dict) -> dict:
    """One prior-round item as the round record carries it, ruling and evidence.

    `text_unchanged_reason` and the surviving passages belong on a `resolved`
    row as much as on an `unverified` one. The engine asks for that reason
    exactly where the text a prior finding quoted still reads the same, so a
    record that dropped it kept the ruling and threw away what the ruling had
    to answer for.
    """
    return {
        "id": str(issue.get("id") or ""),
        "prior_id": str(issue.get("prior_id") or ""),
        "prior_rank": prior_rank(issue),
        "name": str(issue.get("name") or "").strip(),
        "status_reason": str(issue.get("status_reason") or "").strip(),
        "text_unchanged_reason": str(issue.get("text_unchanged_reason") or "").strip(),
        "surviving_quotes": surviving_passages(issue),
    }


def write_round_record(
    dest: Path, preprint: Preprint, provenance: dict, package: dict
) -> None:
    """The machine-readable round record a later revision round is measured against.

    Every item is named by the engine's own issue id, and that is the whole
    point of the file. `R1-01` was minted here, counted from the top of this
    round's own list, so the two rounds published against the same paper both
    opened with an `R1-01` and they were different asks. An id that is spent
    the moment the list is reordered cannot be checked off in a later round,
    which is exactly what a round record is for. The engine's id is minted once,
    carried through every round the issue survives, and never reused, so an
    `i03` here is the `i03` the next round rules on.

    `closed_issues` is what this round said about the round before it, and the
    two lists in it are kept apart on purpose. `resolved` is the editor agent's
    own ruling, with its reason. `unverified` is an item nobody raised again and
    nobody ruled on, which is still open, and `carried_forward` counts it as
    open. Adding the two together would publish a compliance figure that the
    run does not support.
    """
    rows = [
        {
            "id": str(issue.get("id") or ""),
            "severity": str(issue.get("severity") or ""),
            "category": str(issue.get("category") or ""),
            "rank": issue_rank(issue),
            "name": str(issue.get("name") or "").strip(),
            "text": str(issue.get("statement") or issue.get("name") or "").strip(),
            "finding_uids": [
                str(_dict(member).get("finding_uid") or "")
                for member in issue_members(issue)
                if str(_dict(member).get("finding_uid") or "")
            ],
            "raised_by": issue_slots(issue),
            "escalated": issue_is_escalated(issue),
            "status": str(issue.get("status") or ""),
            "prior_id": str(issue.get("prior_id") or ""),
            "blocking": False,
        }
        for issue in required_issues(package)
    ]
    write_json(
        dest / ROUND_RECORD,
        {
            "schema_version": 1,
            "round": int(provenance.get("round") or 1),
            "manuscript_title": preprint.title,
            "decision": provenance["decision"],
            "required_revisions": rows,
            "minor_suggestions": [
                {
                    "id": str(issue.get("id") or ""),
                    "rank": issue_rank(issue),
                    "name": str(issue.get("name") or "").strip(),
                    "text": str(issue.get("statement") or issue.get("name") or "").strip(),
                }
                for issue in suggestion_issues(package)
            ],
            # Both closed lists carry the same fields. A `resolved` row used to
            # drop `text_unchanged_reason` and the surviving passages, which are
            # the two things that say what the ruling was made against: the
            # engine demands that reason precisely where the text a finding
            # quoted still reads the same, so dropping it left the strongest
            # ruling in the round as the one with no evidence recorded under it.
            "closed_issues": {
                name: [_closed_row(issue) for issue in rulings]
                for name, rulings in (
                    ("resolved", resolved_issues(package)),
                    ("unverified", unverified_issues(package)),
                )
            },
            # Every item a later round still has to answer: this round's own
            # list plus the previous round's items nobody ruled fixed.
            "carried_forward": [
                str(issue.get("id") or "")
                for issue in all_issues(package)
                if str(issue.get("status") or "") != RESOLVED_STATUS
            ],
            "issue_ids_used": [str(i) for i in _list(package.get("issue_ids_used"))],
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


def review_round(paper_dir: Path, draft: int) -> int:
    """Which round of review this is for the manuscript, counting from one.

    A round is a review of a draft, so the number is one more than the number of
    earlier drafts of this paper that have been reviewed here. A revision round
    increments it and a second attempt on the same draft does not: a re-review
    of identical text is this round read again, and numbering it as a new one
    would tell the authors they had been through a round they were never sent.

    The ids do not depend on this. They are the engine's, minted once per issue
    and stable across rounds, which is what lets a later round rule on an item
    by name. The number is published because a reader asks which round they are
    looking at, and the record used to answer 1 whatever the answer was.
    """
    try:
        published = existing_bundles(Path(paper_dir))
    except OSError:
        return 1
    return 1 + len([number for number in published if number < int(draft)])


def prior_issues_file(prior: Path | None) -> Path | None:
    """The previous round's published items, which this round rules against.

    The engine's `--prior-issues` takes a document in its own issues schema, and
    the bundle's copy is one: the ids, the ranks, the statements and the ids
    already spent, as the engine wrote them. Handing it back is what makes the
    second round a second round rather than a fresh look, and what stops it
    minting an id the first round already used.

    A bundle published before this file existed has none, and the answer is None
    rather than a refusal. The round still runs, with no prior input, which is
    the same thing the engine does on a first look.

    A round that ended with every item ruled fixed is the same answer for a
    different reason. The engine refuses a prior file with nothing open in it,
    and rightly: there is nothing in it to match. Naming it anyway would stop
    the run with an error over a round that went well.
    """
    if prior is None:
        return None
    path = Path(prior) / REVIEW_ISSUES
    if not path.is_file():
        return None
    assert_prior_items_are_the_published_bytes(path)
    open_items = [
        row
        for row in _list(maybe_json(path).get("issues"))
        if isinstance(row, dict)
        and str(row.get("id") or "")
        and str(row.get("status") or "") != RESOLVED_STATUS
    ]
    return path if open_items else None


def assert_prior_items_are_the_published_bytes(path: Path) -> None:
    """The prior round's items have to be the bytes that round published.

    The file sits in a published bundle, in a public repository, and the next
    round rules against it: an id, a statement and a severity in it become the
    standing of a request the authors already answered. A row deleted or a
    statement rewritten by hand would be read as the previous round's own words,
    and the only sign of it would be in this file's history.

    Every bundle hashes its own files into `manifest.json` when it is published,
    so there is a recorded digest to check against, and it is checked here,
    where the file is named as an input, rather than trusted because of where it
    sits. A bundle whose manifest does not account for the file is refused the
    same way: an unaccounted file and an edited one read identically from here.
    """
    path = Path(path)
    recorded = _dict(maybe_json(path.parent / "manifest.json").get("files"))
    stated = recorded.get(path.name)
    if not isinstance(stated, str) or not stated:
        raise CommandError(
            f"The previous round at {path.parent.name} does not account for its "
            f"own {path.name} in manifest.json, so there is no published digest "
            "to check the items against. A later round rules against that file, "
            "so it is not read until the bundle that published it says what it "
            "held."
        )
    actual = digest(path.read_bytes())
    if actual != stated:
        raise CommandError(
            f"The {path.name} of the previous round at {path.parent.name} is not "
            f"the file that bundle published: it hashes to {actual[:16]} and the "
            f"bundle's manifest records {stated[:16]}. The items in it are what "
            "the authors were asked for and what this round would rule against, "
            "so an edited copy is refused. Restore the published file from git."
        )


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
        record["round"] = review_round(paper_dir, plan.draft)
        prior_issues = prior_issues_file(plan.prior)
        record["prior_issues"] = str(prior_issues) if prior_issues else ""
    else:
        record["destination"] = str(RUNS / f"local-{digest(data)[:12]}")
        record["draft"] = 1
        record["attempt"] = 1
        record["plan_kind"] = "unpublishable local run"
        record["round"] = 1
        record["prior_issues"] = ""

    write_json(out / "prepared.json", record)
    print(json.dumps(record, indent=2))
    if record.get("prior_issues"):
        # Printed because it is the one part of the plan the operator has to act
        # on: the engine does not find the previous round by itself, and a
        # revision round run without it reads the manuscript as a first look and
        # mints a fresh set of ids for items the authors were already given.
        print(
            "\nThis is round "
            f"{record['round']}. Pass the previous round's items to the engine "
            f"with --prior-issues {shlex.quote(str(record['prior_issues']))}, "
            "or the run cannot rule on any of them.",
            file=sys.stderr,
        )
    elif record.get("publishable") and int(record.get("round") or 1) > 1:
        print(
            "\nThis is round "
            f"{record['round']} and the previous round published no "
            f"{REVIEW_ISSUES}, so there is nothing for this run to rule "
            "against. It will read the manuscript as a first look.",
            file=sys.stderr,
        )
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
# hole. `/home/opal` with a boundary on the left published `file:/home/opal/x.pdf`,
# `box:/home/opal/x`, `//home/opal/x`, `a~/home/opal/x` and
# `http://localhost:8000/home/opal/x`; `lab-ws-01` with one published
# `node.lab-ws-01` and `run_lab-ws-01_1`; and the fields a fact was not read
# in published the host name as a JSON key and as an `id`. None of that needs
# protecting from a substring test, because `/home/opal` and `lab-ws-01` cannot
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

# A credential, which is not a path and not a machine name and has no business
# in anything this repository publishes. These were not scanned for at all: the
# scan was built to keep the operator's filesystem out of a published page, and
# a key pasted into a refusal, printed by a tool into a run log, or sitting in
# an environment line copied into a comment would have travelled with it.
#
# They are tier 1, like a specific fact: nothing waives one. A hit here is
# either a live secret, in which case publishing it is the worst thing on this
# page, or it is a dead or made-up one, in which case the cost of refusing is
# that someone rewrites an example. That trade only goes one way.
#
# Each shape is a vendor's own prefix and length, so there is nothing for a
# reviewer's prose to collide with. No generic `password = ...` rule is here on
# purpose: it matches documentation, test fixtures and the word in a sentence,
# and a rule that fires on those gets waived by habit, which is how the shapes
# that matter stop being read.
SECRET_PATTERNS = (
    (
        "an API key",
        # `sk-` covers this project's own provider and the other vendors that
        # copied the prefix, `sk-ant-api03-...` among them.
        re.compile(r"(?<![\w-])sk-(?:[A-Za-z0-9_-]*-)?[A-Za-z0-9_-]{24,}"),
    ),
    (
        "a GitHub token",
        re.compile(r"(?<![\w-])(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[\w]{20,})"),
    ),
    (
        "an AWS access key id",
        re.compile(r"(?<![A-Z0-9])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Z0-9])"),
    ),
    (
        "a Google API key",
        re.compile(r"(?<![\w-])AIza[A-Za-z0-9_-]{30,}"),
    ),
    (
        "a Slack token",
        re.compile(r"(?<![\w-])xox[abprs]-[A-Za-z0-9-]{10,}"),
    ),
    (
        "a bearer token",
        re.compile(r"(?i:bearer)\s+[A-Za-z0-9._~+/-]{24,}={0,2}(?![\w.~+/-])"),
    ),
    (
        "a private key block",
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ),
)

# How a path opens: a leading slash, or two, under the rules worked out for the
# absolute path pattern above. Named here because the shapes below reuse it.
_PATH_OPENER = r"(?:(?<![\w~./:])//|(?<![\w~./])/)"

# A path under somebody's home directory or a temporary directory, whoever's
# machine it is on. These are tier 1 wherever they appear, and nothing waives
# one: not `--allow-text`, not the manuscript printing it.
#
# The machine facts below cover this machine's own home and temporary
# directories, looked up at publish time. These cover the rest: `/home/runner`
# from a CI log, `/Users/someone` from a collaborator's laptop, `/tmp/pdf-cache`
# from a container the run passed through. The absolute path pattern already
# finds all of them, as tier 2, which meant any of them could be published by
# reading the refusal and passing the path back, and a path in a home or
# temporary directory is never the review's own words. There is nothing in a
# review of a paper for this to be wrong about: a manuscript does not quote
# `/home/<name>/<file>`, and if one ever does, the answer is to edit the run's
# own copy rather than to publish a path.
UNWAIVABLE_PATH_SHAPES = (
    (
        "a path in a home directory",
        re.compile(rf"{_PATH_OPENER}(?i:home|users)(?:/{_SEGMENT})+/?"),
    ),
    (
        "a path in a temporary directory",
        re.compile(
            rf"{_PATH_OPENER}"
            r"(?i:tmp|temp|var/tmp|var/folders|private/tmp|private/var/folders)"
            rf"(?:/{_SEGMENT})+/?"
        ),
    ),
    (
        "a path in a home directory",
        re.compile(rf"(?<![\w/])~(?:{_SEGMENT})?/{_FIRST_SEGMENT}(?:/{_SEGMENT})*"),
    ),
    (
        "a path under $HOME",
        re.compile(rf"\$(?:HOME|\{{HOME\}})/{_SEGMENT}(?:/{_SEGMENT})*"),
    ),
    (
        "a path in a Windows user profile",
        re.compile(rf"(?<![\w:])[A-Za-z]:[\\/]+(?i:users)[\\/]+{_SEGMENT}(?:[\\/]+{_SEGMENT})*"),
    ),
    (
        "a path inside an installed environment",
        # `usr` and `run` are not roots of the absolute-path shape, for the
        # reason given there: `/usr/bin` says nothing about the operator and
        # reads as a word in a sentence too often to refuse review prose over.
        # That left the longest paths on the machine unscanned, because the
        # engine is installed under one:
        # `/usr/lib/python3.12/site-packages/peerreviewagents/plugin/server.py`
        # names the interpreter, its version and the layout of this install, and
        # a traceback out of a run is full of them.
        #
        # So the marker is the install tree rather than the root. A segment
        # called `site-packages`, `dist-packages`, `node_modules` or
        # `virtualenvs` with a path on both sides of it is a file inside an
        # installed environment, wherever that environment sits. It is here
        # rather than among the waivable shapes for the same reason a home path
        # is: no review of a paper contains one, so there is nothing for an
        # allowance to be for.
        re.compile(
            rf"{_PATH_OPENER}{_SEGMENT}(?:/{_SEGMENT})*"
            rf"/(?i:site-packages|dist-packages|node_modules|virtualenvs)"
            rf"(?:/{_SEGMENT})+"
        ),
    ),
    (
        "a per-user runtime directory",
        # `/run/user/1000` is where a session's sockets live, and the number in
        # it is the operator's own account id, which is as specific to this
        # machine as the home directory is.
        re.compile(r"(?<![\w~./])/run/user/\d+(?:/[\w.+~%-]+)*"),
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
    and it published `lab-WS-01` as a JSON key and as an `id`. Fixing which
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
    boundary on either side. `lab-ws-01` typed in a comment is this machine as
    surely as `lab-WS-01` is, and so are `node.lab-ws-01`, `run_lab-ws-01_1`
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

    `/home/opal` has two, `/tmp` has one, and that count is the whole of the
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
    one. There is nothing to protect from that test: `/home/opal` and `lab-ws-01`
    do not occur in a review of a paper or in this repository's own vocabulary,
    which is why the boundaries that were there to protect ordinary text are
    gone, and with them every hole they left. `file:/home/opal/x.pdf`,
    `//home/opal/x`, `a~/home/opal/x`, `http://localhost:8000/home/opal/x`,
    `node.lab-ws-01`, `run_lab-ws-01_1` and the host as a JSON key were all
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
        the name every tool prints was not a fact at all. `/home/opal`
        resolving to `/export/people/opal` meant a run under `/home/opal`
        published `/home/opal`
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
            # else has to be looked for in both: HOME written `/home//opal/.`
            # is the same machine as HOME written `/home/opal`.
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
    # The shapes nothing waives, carried as facts so that one scan reads them
    # with everything else: the same canonical forms, the same longest-hit
    # folding, the same refusal. Registering them as specific is also what makes
    # `names_a_specific_fact` refuse an allowance that contains one, so an
    # editor cannot publish a home directory by passing the refusal's own text
    # back on the command line.
    facts += [Fact(why, pattern) for why, pattern in UNWAIVABLE_PATH_SHAPES]
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
    manuscript = Path(workspace) / MAIN_DOCUMENT
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
# and `\home\opal\x` are the paths they read as, and the shapes that need the
# backslash itself still see it, because the raw string is scanned as well. The
# hyphens matter for the host name, which is the one fact with a hyphen in it:
# `lab‑WS‑01` written with U+2011 is this machine.
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
# `\/home\/opal` out of a JSON string and `lab\-WS\-01` out of a regular
# expression are both this machine, written by something that quoted them.
# Dropped before the look-alikes are folded, so that `\home\opal\x` still
# becomes `/home/opal/x` while `\/home` does not become `//home`.
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
    another: `%252Fhome%252Fopal` is a percent sign that decodes to a percent
    sign, and `&#37;2Fhome` is an HTML entity hiding one. The steps are NFKC,
    HTML entities, percent-decoding, dropping the format characters that print
    as nothing (U+200B through U+200D, U+2060, U+FEFF and the soft hyphen are
    all Cf), dropping a backslash that is escaping punctuation, folding the
    slash and hyphen look-alikes, and reducing `//` and `/./` to `/`. The loop
    stops when the string stops changing, which it always does, because every
    step either shortens the string or replaces a character with an ASCII one.

    A backslash is two things at once and the order decides which one it is
    read as, so there is no order that is right. With `escapes_first`, which is
    the default, `\\/home\\/opal` is a quoted `/home/opal` and `lab\\-WS\\-01` is a
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
    `&#47;home&#47;opal`, `/home/./opal`, `\\/home\\/opal` and `∕home∕opal` are all the
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

    A credential counts here too, though it is not a fact about this machine.
    What the two have in common is the only thing this test is for: neither may
    be published, and an allowance naming one would publish it.
    """
    forms = _scan_forms(text)
    if any(pattern.search(form) for _, pattern in SECRET_PATTERNS for form in forms):
        return True
    return any(
        fact.pattern.search(form)
        for fact in facts
        if fact.specific
        for form in forms
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
    # A credential is reported in the same tier as a specific fact and before
    # the shapes, so a key sitting inside a longer path or header is the hit
    # that carries the tier rather than the path around it.
    for why, pattern in SECRET_PATTERNS:
        for index, form in enumerate(forms):
            found += [
                (Leak(why, match.group(0), True), index > 0)
                for match in pattern.finditer(form)
            ]
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
    # folding, `%2Fhome%2Fopal` being a path only once decoded, and it stays, in
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
            " rather than recognised, a path under a home or temporary"
            " directory, or a credential, and no flag and no manuscript waives"
            " one."
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
    `lab-WS-01` as a JSON key and as an `id`, a `status` and a `basis`. The
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

    `issues.json` is the engine's own output copied into the bundle, and a run
    folder records absolute paths in several places. Only a value in one
    of `PATH_FIELDS` that is actually a path is touched, so the review's own
    words reach the reader as the reviewer wrote them. Every change is appended
    to `projected`, which the caller prints: a published artifact that differs
    from the engine's own output says so on the command that published it, and
    nothing is altered silently.

    A key is never rewritten. A mapping keyed by a path leaks through the key
    rather than the value, and the version that rewrote a key inside this
    repository to a relative one turned `<checkout>/docs/figs/a.png` into
    `docs/figs/a.png` with nothing said. Engine 0.10 writes no mapping keyed by
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


def assert_publishable_issues(package: dict) -> None:
    """The published items have to be an input the next round can rule against.

    This is the other half of a stable id. Publishing the engine's ids is no
    use if the file they are published in is one the next round refuses, and the
    refusal would arrive a round later, in front of the authors, with the ids
    already printed in a decision letter.

    So the rules the engine's own prior-round loader applies are applied here,
    to the file about to be written, and a bundle that would not survive them is
    refused before it exists. They are few and they are not guesses: the
    document carries the schema stamp this pipeline publishes, every row is an
    object with an id in the engine's own form, no id appears twice, and
    `issue_ids_used` accounts for every id in the file. That last one is what
    stops a resolved issue's id being minted again for a different problem two
    rounds later.

    Two more rules are about what the letter would say rather than what the next
    round would read, and they are here because this is the one place every
    published run passes through: a standing has to be one of the engine's five,
    and a surviving passage has to be an object carrying the manuscript text it
    quotes.
    """
    stamp = str(package.get("schema_version") or "")
    if not stamp:
        raise CommandError(
            f"The run's {REVIEW_ISSUES} carries no schema_version, so a later "
            "round could not tell what the ids in it mean and would refuse the "
            "file. Re-run the review on an engine that writes the issues "
            "document."
        )
    rows = _list(package.get("issues"))
    strange = [type(row).__name__ for row in rows if not isinstance(row, dict)]
    if strange:
        raise CommandError(
            f"{len(strange)} issue row(s) in this run are not objects "
            f"({', '.join(sorted(set(strange)))}), so the published "
            f"{REVIEW_ISSUES} would not be a file a later round can read."
        )
    identifiers = [str(_dict(row).get("id") or "") for row in rows]
    malformed = sorted({name or "(absent)" for name in identifiers
                        if not ISSUE_ID_PATTERN.match(name)})
    if malformed:
        raise CommandError(
            f"{len(malformed)} issue(s) in this run carry an id that is not an "
            f"id of this engine ({', '.join(malformed[:5])}). An id is text of "
            "the form i01 upwards, and it is what a later round rules against, "
            "so a bundle cannot publish one it cannot match."
        )
    repeated = sorted({name for name in identifiers if identifiers.count(name) > 1})
    if repeated:
        raise CommandError(
            f"The issue id(s) {', '.join(repeated)} appear more than once in "
            "this run. One id is one problem across every round, so a file "
            "holding the same id twice is one a later round refuses."
        )
    # A severity this release does not sort is an issue that would appear in
    # neither list: not a required change, not a suggestion, and so not in the
    # letter at all. The engine's vocabulary can grow, and the answer to a word
    # this pipeline has no place for is to refuse and name it, never to publish
    # a letter that quietly drops an issue the editor agent raised.
    known = (*REQUIRED_SEVERITIES, SUGGESTION_SEVERITY)
    unsorted_rows = [
        f"{row.get('id')} ({row.get('severity') or 'no severity'})"
        for row in live_issues(package)
        if str(_dict(row).get("severity")) not in known
    ]
    if unsorted_rows:
        raise CommandError(
            f"{len(unsorted_rows)} issue(s) in this run carry a severity this "
            f"pipeline does not sort: {', '.join(unsorted_rows[:5])}. It sorts "
            f"{', '.join(known)}, and an issue outside that list would be "
            "neither a required change nor a suggestion, so it would not appear "
            "in the letter at all. Update the publish path before publishing a "
            "run from this release."
        )
    # A standing outside the engine's five. The word is published in the letter
    # and in the round record, and a reader takes it for the engine's own, so a
    # run carrying `fixed` or `addressed` is refused and the word is named. The
    # five are the engine's `ISSUE_STATUSES`, checked against the installed
    # engine by `assert_issue_vocabulary`.
    strange_status = sorted({
        f"{_dict(row).get('id')} ({_dict(row).get('status') or 'no status'})"
        for row in rows
        if str(_dict(row).get("status") or "") not in ISSUE_STATUSES
    })
    if strange_status:
        raise CommandError(
            f"{len(strange_status)} issue(s) in this run carry a standing this "
            f"engine does not write: {', '.join(strange_status[:5])}. The five "
            f"are {', '.join(ISSUE_STATUSES)}, each of them a statement about "
            "the previous round, and a word outside them would be published in "
            "the letter as though the engine had ruled it."
        )
    # The surviving passages are objects, `{finding_uid, quote, document, line,
    # fingerprint, matched_by}`, and the letter prints the quote out of each
    # one. A row that is not an object, or that carries no quote, is refused
    # rather than published: a row read as a string printed a Python dict into
    # a letter under a heading telling the authors that was their own text.
    shapeless = sorted({
        f"{_dict(row).get('id')} ({type(passage).__name__})"
        for row in rows
        for passage in _list(_dict(row).get("surviving_quotes"))
        if not isinstance(passage, dict) or not str(passage.get("quote") or "").strip()
    })
    if shapeless:
        raise CommandError(
            f"{len(shapeless)} issue(s) in this run carry a surviving passage "
            f"that holds no quote: {', '.join(shapeless[:5])}. The engine writes "
            "one object per passage with the manuscript text in `quote`, the "
            "letter prints that text, and a row without it would be published "
            "as an empty quotation of the authors' own manuscript."
        )
    used = {str(name) for name in _list(package.get("issue_ids_used"))}
    unlisted = sorted(set(identifiers) - used)
    if unlisted:
        raise CommandError(
            f"{len(unlisted)} issue id(s) in this run are missing from "
            f"issue_ids_used ({', '.join(unlisted[:5])}). That list is every id "
            "the round and its own prior rounds spent, and a later round mints "
            "above it, so an id left out of it would be handed to a different "
            "problem once this one is resolved."
        )
    # A finding the code check threw out may not be published as an ask. The
    # engine refuses the editor that groups one, so a bundle holding one is a
    # bundle built from something the engine would not have accepted, and the
    # answer is to refuse it here rather than to drop the member quietly: a
    # letter is what the authors read, and a required change resting on a
    # finding the code contradicts is the one mistake this stage exists to
    # prevent. The finding is still published, in the thrown-out section, which
    # is where a reader can see both the claim and the code that answered it.
    thrown_out = contradicted_findings(package)
    if thrown_out:
        published = sorted({
            f"{_dict(row).get('id')} ({uid})"
            for row in rows
            for member in _list(_dict(row).get("members"))
            for uid in [str(_dict(member).get("finding_uid") or "")]
            if uid in thrown_out
        })
        if published:
            raise CommandError(
                f"{len(published)} issue member(s) in this run name a finding "
                f"the code check threw out: {', '.join(published[:5])}. The code "
                "was read at the passage that decides the claim and does not do "
                "what the finding said, so the finding is published in the "
                "thrown-out section of the letter and in no issue. An issue "
                "holding one would put it to the authors as a change they have "
                "to make. Re-run the review on an engine that refuses the "
                "grouping rather than publishing this bundle."
            )


def assert_the_round_ruled_against_its_prior(prepared: dict, package: dict) -> None:
    """Did this run read the round it is about to be published after?

    `prepare` works out the round number from the bundles already published and
    names the previous round's items as the engine's `--prior-issues`. The
    engine takes that file or it does not, and nothing joined the two up: a run
    made without the flag published as round 3 with no prior round recorded,
    every item `new`, and `i01` `i02` `i03` minted again for problems that had
    nothing to do with the ones the authors were sent under those numbers. The
    page promises the opposite, that an id is one problem for the life of the
    manuscript, and that promise is what breaks first and most quietly.

    So the two are compared here, at the one gate every published bundle passes.
    The engine records the prior round as the file it read and a digest of it,
    `sha256` of the file's text cut to sixteen characters, which was checked
    against the engine's own code rather than assumed. A round above the first
    whose plan names a prior file publishes only if the engine read a file and
    the digest is of that file.

    A round above the first whose plan names no prior file is a different case
    and not an error: the previous bundle published no items, or ruled every one
    of them fixed, and the engine refuses a prior file with nothing open in it.
    What is refused there is the reverse surprise, a run that ruled against some
    file the plan knows nothing about, because then nobody can say which round
    the rulings in the letter are about.
    """
    round_number = int(prepared.get("round") or 1)
    named = str(prepared.get("prior_issues") or "").strip()
    prior = _dict(package.get("prior_round"))
    read_file = str(prior.get("file") or "").strip()
    read_digest = str(prior.get("digest") or "").strip()

    if named and not read_file:
        raise CommandError(
            f"This is round {round_number} and the run was made without the "
            "previous round's items: the engine records no prior round, so "
            "every issue in it is new and its ids start again from the "
            "beginning. The authors were already sent items under those "
            "numbers. Re-run the review with --prior-issues "
            f"{shlex.quote(named)}, which is the file prepare named."
        )
    if not named and read_file:
        raise CommandError(
            f"This run ruled against a prior round ({read_file}) that the plan "
            f"for round {round_number} does not name. Either the previous round "
            "published no open items, in which case there is nothing to rule "
            "against, or some other file was passed, in which case nothing here "
            "can say which round the rulings in this letter are about. Re-run "
            "prepare, and pass the file it names or no file at all."
        )
    if not named:
        return

    source = Path(named)
    if not source.is_file():
        raise CommandError(
            f"The previous round's items are no longer at {source.name}, so "
            "what this run ruled against cannot be checked. The file is "
            "published in a bundle in this repository. Restore it from git."
        )
    assert_prior_items_are_the_published_bytes(source)
    # The engine's own digest of the prior file: `sha256` of the text it read,
    # cut to sixteen characters. Read off the engine's source rather than
    # guessed at, and it covers the whole file, so a row deleted or a statement
    # rewritten moves it.
    actual = digest(source.read_bytes())
    if actual[: len(read_digest)] != read_digest:
        raise CommandError(
            f"This is round {round_number} and the file the run ruled against "
            "is not the one the previous round published: the engine recorded "
            f"{read_file} at {read_digest} and the published {source.name} "
            f"hashes to {actual[:len(read_digest)]}. The rulings in the letter "
            "would be about items the authors were never sent. Re-run the "
            f"review with --prior-issues {shlex.quote(named)}."
        )


def projection_report(
    *,
    engine_package: dict,
    published: dict,
    projected: Sequence[str] = (),
) -> str:
    """How the published issues.json differs from the engine's own.

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
            f"the engine's own {REVIEW_ISSUES} could not be read, so the keys "
            "carried into the bundle were not compared with it"
        )
    if left_out:
        parts.append(f"not carried: {', '.join(left_out)}")
    if added:
        parts.append(f"added by this bundle: {', '.join(added)}")
    if projected:
        parts.append(f"path fields projected: {', '.join(projected)}")
    if engine_keys and not left_out and not added and not projected:
        parts.append("every key the engine wrote, published as written")
    return f"{REVIEW_ISSUES}, " + ". ".join(parts)


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
    when the run finished, the review came from a readable `issues.json` the
    editor agent wrote rather than from the findings ledger, a guard verdict was
    recorded, the guards did not empty the review, and every run file could be
    read in full. That is the whole gate, and it is the engine's own rule rather
    than a second copy of it here, down to the words the refusal prints, which
    are the engine's `not_publishable_reasons`.

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
    refusal = not_a_review_arm(run, planned_arms())
    if refusal:
        raise CommandError(refusal)
    if not reading.get("publishable"):
        # The engine names its own reasons, one sentence each, and that list is
        # never empty while the flag is false. Printing its words rather than a
        # second copy of its rules is the only way the refusal here and the rule
        # there cannot drift apart. There used to be a fallback here that
        # reconstructed a reason from the old flat-findings fields when the list
        # was missing, for an engine too old to carry it. This release requires
        # 0.10, which always carries it, and the fallback described a run shape
        # the engine no longer writes, so an empty list is reported as what it
        # is rather than explained by guesswork.
        reasons = [
            str(reason).strip()
            for reason in _list(reading.get("not_publishable_reasons"))
            if str(reason).strip()
        ]
        cause = str(reading.get("cause") or "").strip()
        detail = [f"The engine read it as {status or 'unknown'}."]
        if cause:
            detail.append(f"It stopped because: {cause}")
        if reasons:
            detail.append("The engine holds it back because:")
            detail += [f"({n}) {reason}." for n, reason in enumerate(reasons, start=1)]
        else:
            detail.append(
                "It gave no reason for holding the run back, which this "
                "release's engine does whenever it withholds a run, so read "
                "the run folder before trusting anything in it."
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

    # The words this pipeline sorts and publishes by, checked against the
    # engine's own public vocabulary before anything is read with them. A
    # severity or a status that moved in the engine would otherwise sort every
    # issue into the wrong list silently, which is the one failure a published
    # review cannot carry.
    assert_issue_vocabulary()
    package = review_package(reading)
    run = run_record(reading)
    if args.publish:
        require_complete_run(run_dir, run, reading)
        assert_publishable_issues(package)
        assert_the_round_ruled_against_its_prior(prepared, package)
    workspace = resolve_workspace(run_dir, args.workspace)
    preprint_data = prepared.get("preprint")
    if preprint_data is None:
        raise CommandError("A bundle needs preprint metadata. Prepare with --paper.")
    preprint = Preprint(**preprint_data)

    # Before anything is written: is this a run of the paper that was prepared?
    binding = bind_run_to_input(prepared, workspace, run)
    if binding["workspace_manifest_sha256"]:
        prepared["input"]["workspace_manifest_sha256"] = binding["workspace_manifest_sha256"]
    # The engine says what state the run's own manuscript folder is in, and it
    # means that folder. `--workspace` may name another one, and two folders can
    # agree on the paper by hash without being the same seal, so the state
    # travels only where the run is talking about the folder being published.
    # The folder itself never travels, being a path on this machine.
    reported = _dict(reading.get("manuscript"))
    named = str(reported.get("folder") or "")
    published_state = ""
    if named and Path(named).resolve() == Path(workspace).resolve():
        published_state = str(reported.get("state") or "")
    ingest = ingest_record(workspace, published_state)

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
            Path(str(_dict(reading.get("reports")).get("issues") or ""))
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
    reports = track_reports(run_dir)
    # The manuscript's own lines under the quotes this round cites, read back
    # through the engine from the folder the run was bound to above. The letter
    # marks each quote where it stands, so the authors see the sentence rather
    # than a line number to go and look up.
    citations = manuscript_citations(workspace, published_package)
    if dest.exists() and any(dest.iterdir()):
        raise CommandError(f"Refusing to overwrite an existing review bundle: {dest}")

    # The bundle is built outside the published tree and moved in once every
    # guard has passed. The guards used to run after six files had already been
    # written into docs/reviews, so a refusal left most of a bundle behind, with
    # no manifest and nothing saying it was rejected.
    with tempfile.TemporaryDirectory(prefix="local-review-bundle-") as staging:
        stage = Path(staging)

        (stage / "summary.md").write_text(
            render_summary(preprint, published_package, provenance), encoding="utf-8"
        )
        (stage / "decision_letter.md").write_text(
            render_decision_letter(
                preprint, published_package, provenance, citations=citations
            ),
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
        write_round_record(stage, preprint, provenance, published_package)
        # Kept beside the documents so a reader can check a quotation against
        # the structured record the reviewers actually produced, and so the next
        # round can be handed this round's items by name.
        write_json(stage / REVIEW_ISSUES, published_package)

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

    counts = _dict(provenance["generator"]["run"])
    print(f"bundle   {dest}")
    print(f"round    {provenance['round']}")
    print(f"decision {provenance['decision']} (chosen by {args.editor})")
    print(
        f"items    {counts.get('required', 0)} required change(s) and "
        f"{counts.get('suggestions', 0)} suggestion(s), pooled by the editor "
        f"agent from {counts.get('findings_delivered', 0)} finding(s)"
    )
    if counts.get("resolved") or counts.get("unverified"):
        print(
            f"prior    {counts.get('resolved', 0)} item(s) the editor agent "
            f"ruled fixed, {counts.get('unverified', 0)} left unverified and "
            "still open"
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
    for line in citation_lane_report(run):
        print(line)
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
        "folder beside the run, whose manifest.json is what ties this run to the "
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
