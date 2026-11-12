"""Local generator checks. No model, no network, and no review is ever started.

These cover scripts/local_review.py: the refusals, the documents rendered from
saved engine output, and the manifest. The schema side of the same path is
checked by scripts/check_local_provenance.mjs, which needs Node rather than
Python.

Half of them need the engine. A run folder is read in 0.9 only through
`peerreviewagents.read_run`, which is the engine's supported surface and the
thing that decides whether a run is publishable, so a check of the publish path
is a check against the real reader rather than against a second one written
here. `ENGINE_BACKED` names those checks and `engine_is_importable` says whether
this interpreter can run them; smoke_test.py skips them on a laptop with no
engine and refuses to skip them in CI. The rest run anywhere.

Everything here is written against the run folder engine 0.9's plugin writes:
`protocol.json`, `manifest.json`, `progress.json`, `runtime.json`,
`startup.json`, `editor-package.json` and one `audit_<track>.md` per specialist
reader. The fixtures below copy the shapes of a real 0.9 run rather than an
idealised version of them, including the placeholder agent rows the harness
emits and the absolute paths the plugin server records, because both of those
were defects the generator had to be taught to handle.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fetch_preprint import Preprint  # noqa: E402
import local_review  # noqa: E402

PAPER = Preprint(
    url="https://www.biorxiv.org/content/10.1101/2026.03.12.711120v1",
    source="biorxiv",
    pdf_url="https://www.biorxiv.org/content/10.1101/2026.03.12.711120v1.full.pdf",
    identifier="10.1101/2026.03.12.711120",
    doi="10.1101/2026.03.12.711120",
    title="A manuscript with findings at every severity",
    authors=["Ada Lovelace"],
    version="1",
    pdf_sha256="b" * 64,
    pdf_bytes=2048,
)

TRACKS = local_review.SPECIALIST_TRACKS
CORE_SLOTS = ("core-1", "core-2", "core-3")
SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"
HAIKU = "claude-haiku-5-5"
CLAUDE_CODE_VERSION = "2.1.322"
STARTED_AT = "2026-11-11T12:00:00+00:00"
WORKFLOW_VERSION = "plugin-two-track-v1"
FINDING_SCHEMA = "review-finding-v3"

# Deliberately out of severity order, and one severity the engine does not emit.
FINDINGS = [
    {
        "severity": "minor",
        "title": "A typo",
        "comment": "Fix the spelling.",
        "finding_uid": "f-004",
        "slot": "core-2",
        "track": "citations",
        "basis": "judgement",
        "placement": "anchored",
        "block_id": "b7",
    },
    {
        "severity": "major",
        "title": "The headline effect is unguarded",
        "comment": "Report the confidence interval.",
        "quote": "effects were large",
        "finding_uid": "f-001",
        "slot": "spec-stats",
        "track": "stats",
        "basis": "computed",
        "basis_reason": "The reported mean and n do not give the stated interval.",
        "escalate": True,
        "block_id": "b2",
    },
    {
        "severity": "moderate",
        "title": "Missing n",
        "comment": "State the sample size.",
        "finding_uid": "f-002",
        "slot": "core-1",
        "track": "methods-reporting",
        "basis": "two-quotes",
        "block_id": "b4",
    },
    {
        "severity": "catastrophic",
        "title": "Not a severity the engine emits",
        "comment": "Ignore.",
        "finding_uid": "f-003",
    },
]

# What the editor agent accepted and kept out of the body of the letter.
APPENDIX = [
    {
        "severity": "moderate",
        "title": "Panel b has no axis label",
        "comment": "Label the y axis.",
        "finding_uid": "f-010",
        "slot": "spec-figures-tables",
        "track": "figures-tables",
        "basis": "two-quotes",
        "editor_placement": "appendix",
        "editor_reason": "The body was already at its cap.",
        "block_id": "b9",
    },
    {
        "severity": "minor",
        "title": "Two different totals",
        "comment": "The abstract and table 1 disagree.",
        "finding_uid": "f-011",
        "slot": "core-3",
        "track": "consistency",
        "basis": "two-quotes",
        "escalate": True,
        "block_id": "b11",
    },
]

VERDICT = {
    "significance": "A useful result on a narrow question.",
    "strength_of_evidence": "Moderate, and weaker than the abstract claims.",
    "reasoning": "The headline interval does not follow from the reported numbers.",
    "basis": "Two anchored passages and one arithmetic check.",
    "limitation": "No reader re-ran the analysis.",
}

# What the editor agent wrote into its package, which deliberately disagrees
# with the findings beside it: it counts a stats finding that is not in either
# list and a field track that raised nothing. The record is counted from the
# findings instead, so the table on the page and the findings under it cannot
# disagree, and these two numbers are what proves that.
FINDINGS_BY_TRACK = {
    "stats": 2,
    "figures-tables": 1,
    "methods-reporting": 1,
    "citations": 1,
    "consistency": 1,
    "field": 0,
}

PACKAGE = {
    "summary": "One careful reading of the manuscript.",
    "findings": FINDINGS,
    "appendix": APPENDIX,
    "limitations": ["Did not re-run the analysis."],
    "verdict": VERDICT,
    "decisions": ["Kept the stats finding in the body."],
    "escalation_rulings": [
        {
            "finding_uid": "f-001",
            "ruling": "Upheld. The interval cannot be read off the reported numbers.",
        },
        {
            "finding_uid": "f-011",
            "ruling": "Not upheld. The totals differ by a rounding step.",
        },
    ],
    "escalated_count": 2,
    "findings_by_track": FINDINGS_BY_TRACK,
    "reviewer_count": 3,
    "reviewer_provenance": [
        {
            "slot": "core-1",
            "track": "core",
            "model": SONNET,
            "attempt": 1,
            "tool_calls": 12,
            "findings": 3,
            "none_found": False,
        },
        {
            "slot": "core-2",
            "track": "core",
            "model": SONNET,
            "attempt": 2,
            "tool_calls": 14,
            "findings": 2,
            "none_found": False,
        },
        {
            "slot": "core-3",
            "track": "core",
            "model": SONNET,
            "attempt": 1,
            "tool_calls": 9,
            "findings": 0,
            "none_found": True,
        },
    ],
    "arm": "full-two-track",
    "synthesis_policy": "editor-pooled",
    "workflow_version": WORKFLOW_VERSION,
    "finding_schema_version": FINDING_SCHEMA,
    "review_guard_status": "clean",
    "findings_delivered": 6,
    "quarantined_findings_count": 0,
    "quarantined_findings": [],
}


def engine_is_importable() -> bool:
    """Whether this interpreter can read a run folder at all.

    A run is read through `peerreviewagents.read_run` and nothing else, so a
    check of the publish path has nothing to run against without the engine.
    """
    try:
        __import__(local_review.ENGINE_PACKAGE).read_run
    except (ImportError, AttributeError):
        return False
    return True


def engine_is_required() -> bool:
    """Where a missing engine is a failure rather than a reason to skip.

    The same rule, and the same two environment variables, as
    scripts/check_skill_commands.py. On a laptop the engine is optional. In CI
    it is installed from the lock file, so a missing one is the lock being
    wrong, and a check that quietly skipped itself there is a check worth
    nothing. The pipeline job runs this suite on a bare interpreter on purpose,
    to prove the engine-free half needs no engine, and waives the rule by
    setting INSILICO_REQUIRE_ENGINE to 0.
    """
    false_values = {"", "0", "false", "no", "off"}
    required = os.environ.get("INSILICO_REQUIRE_ENGINE")
    if required is not None:
        return required.strip().lower() not in false_values
    return os.environ.get("CI", "").strip().lower() not in false_values


def _counted_by_track() -> dict[str, int]:
    """The track counts a record of this fixture has to carry.

    Counted from the findings the bundle publishes rather than written out, so
    the expectation cannot drift away from the fixture's own findings. A finding
    with no track at all, which the engine does emit, counts towards nothing.
    """
    counts: dict[str, int] = {}
    for finding in [*FINDINGS, *APPENDIX]:
        track = str(finding.get("track") or "")
        if track:
            counts[track] = counts.get(track, 0) + 1
    return counts


COUNTED_BY_TRACK = _counted_by_track()


def _slot_model(slot: str) -> str | None:
    """The model the plugin's agent file pins for one slot.

    The recorder is the one slot with no model of its own in protocol.json. The
    harness reports what it actually ran it on, which is how the record ends up
    naming three models for a run whose protocol names two.
    """
    if slot == "editor":
        return OPUS
    if slot == "recorder":
        return None
    return SONNET


def _protocol_agents(tracks: tuple[str, ...]) -> dict:
    """One entry per agent slot, as the plugin server writes them."""
    agents: dict[str, dict] = {}
    for slot in CORE_SLOTS:
        agents[slot] = {
            "role": "core-reviewer",
            "track": "core",
            "attempt": 2 if slot == "core-2" else 1,
            "tool_calls": 12,
            "model": SONNET,
            "allowed_tools": ["Read", "Grep"],
        }
    for track in tracks:
        agents[f"spec-{track}"] = {
            "role": "specialist",
            "track": track,
            "attempt": 1,
            "tool_calls": 7,
            "model": SONNET,
            "allowed_tools": ["Read", "Grep"],
        }
    agents["editor"] = {
        "role": "editor",
        "attempt": 1,
        "tool_calls": 4,
        "model": OPUS,
        "allowed_tools": ["Read"],
    }
    agents["recorder"] = {
        "role": "recorder",
        "attempt": 1,
        "tool_calls": 2,
        "model": None,
        "allowed_tools": ["Read"],
    }
    return agents


def _stages(tracks: tuple[str, ...], **overrides) -> dict:
    """The stage ledger, which is what says whether the review is whole."""
    required = [*CORE_SLOTS, *(f"spec-{track}" for track in tracks)]
    attempts = {slot: 1 for slot in required}
    attempts["core-2"] = 2
    ledger = {
        "required": required,
        "reported": list(required),
        "missing": [],
        "none_found": ["spec-field"],
        "attempts": attempts,
        "editor_accepted": True,
    }
    ledger.update(overrides)
    return ledger


def _runtime_agents(tracks: tuple[str, ...]) -> list[dict]:
    """What the harness observed, placeholder rows and all.

    The first five rows are what Claude Code emits for an agent it has not
    named yet: a label and nothing else. A real 0.9 run carries them, and a
    generator that counted them published five empty reviewers on the panel,
    so the fixture keeps them.
    """
    rows: list[dict] = [{"label": f"agent-{index}"} for index in range(5)]
    for slot in CORE_SLOTS:
        rows.append(
            {
                "label": slot,
                "state": "complete",
                "attempt": 2 if slot == "core-2" else 1,
                "agentType": "pra:core-reviewer",
                "model": SONNET,
                "tokens": 48000,
                "toolCalls": 12,
                "durationMs": 210000,
            }
        )
    for track in tracks:
        rows.append(
            {
                "label": f"spec-{track}",
                "state": "complete",
                "attempt": 1,
                "agentType": f"pra:{track}",
                "model": SONNET,
                "tokens": 21000,
                "toolCalls": 7,
                "durationMs": 90000,
            }
        )
    rows.append(
        {
            "label": "editor",
            "state": "complete",
            "attempt": 1,
            "agentType": "pra:editor",
            "model": OPUS,
            "tokens": 32000,
            "toolCalls": 4,
            "durationMs": 120000,
        }
    )
    # The recorder slot runs on haiku, which protocol.json does not say, so the
    # published model map has a model in it that the protocol never named.
    rows.append(
        {
            "label": "ingest",
            "state": "complete",
            "attempt": 1,
            "agentType": "pra:recorder",
            "model": HAIKU,
            "tokens": 9000,
            "toolCalls": 2,
            "durationMs": 30000,
        }
    )
    return rows


def _expected_models() -> dict[str, str]:
    """The model map the fixture run has to produce, slot by slot."""
    models = {slot: SONNET for slot in CORE_SLOTS}
    models.update({f"spec-{track}": SONNET for track in TRACKS})
    models["editor"] = OPUS
    models["ingest"] = HAIKU
    return models


EXPECTED_MODEL_PHRASE = (
    f"{SONNET} (9 agents), {HAIKU} (1 agent), {OPUS} (1 agent)"
)

# The plugin and engine files the run loaded, hashed at the moment it started.
# `plugin-python/` deliberately does not fall under the `plugin/` prefix, which
# is what the plugin fingerprint is taken over.
CODE = {
    "plugin/workflows/review.js": "1" * 64,
    "plugin/agents/core-reviewer.md": "2" * 64,
    "plugin/agents/editor.md": "3" * 64,
    "engine/starter.py": "4" * 64,
    "plugin-python/server.py": "5" * 64,
}


def _plan(tracks: tuple[str, ...]) -> dict:
    return {
        "arm": "full-two-track",
        "reviewers": 3,
        "specialists": list(tracks),
        "editor": True,
        "revision": False,
        "summary": "Three core reviewers, six specialists, one editor.",
        "execution": "parallel",
    }


def _startup(**overrides) -> dict:
    """The engine's own start-up probe, which is the transport evidence.

    Nothing is probed at publish time in 0.9. The claim the record makes is
    that a Claude Code session started, loaded the plugin and connected its MCP
    server, and this file is where the engine wrote that down before it spent
    anything.
    """
    record = {
        "at": STARTED_AT,
        "probe": {
            "plugins": ["pra"],
            "mcp_servers": [
                {"name": "plugin:pra:peerreview", "status": "connected", "source": "plugin"}
            ],
        },
        "problems": [],
        "tools_expected": ["mcp__pra__submit_finding"],
    }
    record.update(overrides)
    return record


def _runtime(tracks: tuple[str, ...], **overrides) -> dict:
    record = {
        "status": "complete",
        "wall_seconds": 1840.5,
        "tokens_total": 412000,
        "agents": _runtime_agents(tracks),
        "claude_code_version": CLAUDE_CODE_VERSION,
    }
    record.update(overrides)
    return record


def _run_transport() -> dict:
    """The transport block the fixture run produces, built by the real code.

    `transport_record` is pure in 0.9, so the fixture does not have to stub it
    out the way the 0.8 fixtures stubbed the publish-time probe. That is the
    point of the shape: publishing needs no network and no CLI.
    """
    return local_review.transport_record(
        provider="claude-code", runtime=_runtime(TRACKS), startup=_startup()
    )


def _run_directory(
    root: Path, *, report_tracks: tuple[str, ...] | None = None, **overrides
) -> Path:
    """A run directory holding the files engine 0.9's plugin really writes.

    One flat folder: what was asked of the engine in `protocol.json`, the paper
    id and the hash of every plugin and engine file loaded in `manifest.json`,
    the final status and the stage ledger in `progress.json`, what the harness
    observed in `runtime.json`, the start-up probe in `startup.json`, the review
    in `editor-package.json`, and one `audit_<track>.md` per specialist reader.

    The manifest carries the absolute manuscript path and plugin root the plugin
    server writes into it. They are here on purpose: nothing in the published
    record may name them, and a fixture without them would let a generator that
    copied them through pass.

    An override value of None leaves that file out, which is how the refusals
    for a run missing one of them are tested.
    """
    run = Path(root)
    run.mkdir(parents=True, exist_ok=True)
    home = str(Path.home().resolve())
    files = {
        "protocol.json": {
            "provider": "claude-code",
            "model": "Each agent runs on the model its agent file pins.",
            "effort": "high",
            "mode": "plugin",
            "arm": "full-two-track",
            "reviewers": 3,
            "paper_id": "paper-abc",
            "literature_cutoff": None,
            "version": WORKFLOW_VERSION,
            "finding_schema_version": FINDING_SCHEMA,
            "body_finding_limit": 8,
            "agents": _protocol_agents(TRACKS),
            "plan": _plan(TRACKS),
        },
        "manifest.json": {
            "paper_id": "paper-abc",
            "source_sha256": "b" * 64,
            "pdf": f"{home}/runs/local/paper.pdf",
            "code": dict(CODE),
            "workflow_version": WORKFLOW_VERSION,
            "finding_schema_version": FINDING_SCHEMA,
            "claude_code_version": CLAUDE_CODE_VERSION,
            "plugin_root": f"{home}/Repos/PeerReviewAgents/plugins/pra",
            "plan": _plan(TRACKS),
        },
        "progress.json": {
            "status": "complete",
            "error": "",
            "reviewers": 3,
            "arm": "full-two-track",
            "stages": _stages(TRACKS),
            "findings_delivered": 6,
            "quarantined_findings_count": 0,
            "review_guard_status": "clean",
            "tool_calls": 64,
            "tool_calls_total": 64,
            "started": STARTED_AT,
            "updated": "2026-11-11T12:31:00+00:00",
        },
        "runtime.json": _runtime(TRACKS),
        "startup.json": _startup(),
        "editor-package.json": dict(PACKAGE, stages=_stages(TRACKS)),
    }
    files.update(overrides)
    for name, payload in files.items():
        if payload is None:
            continue
        (run / name).write_text(json.dumps(payload), encoding="utf-8")

    for track in TRACKS if report_tracks is None else report_tracks:
        (run / f"audit_{track}.md").write_text(
            f"# {track}\n\nWhat this reader checked, and what it found.\n", encoding="utf-8"
        )
    return run


def _quarantine(run: Path, *findings: dict) -> Path:
    """The guards' own ledger of what they threw out, as the engine counts it.

    `quarantined.jsonl` is where the evidence guards write a finding they
    refused, and the engine counts the rows in that file. The editor package
    carries a count of the same thing and the engine does not read it, so a
    fixture that set only that number would prove nothing.
    """
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    (run / "quarantined.jsonl").write_text(
        "".join(f"{json.dumps(finding)}\n" for finding in findings), encoding="utf-8"
    )
    return run


def _run_tree(root: Path, **overrides) -> Path:
    """The two folders `peerreview review <pdf> <out>` writes under one out dir."""
    root = Path(root)
    _run_directory(root / local_review.REVIEW_DIRECTORY, **overrides)
    _workspace(root / local_review.MANUSCRIPT_DIRECTORY)
    return root


def _workspace(root: Path, paper_id: str = "paper-abc") -> Path:
    """The folder the engine's import command writes, as publish needs it."""
    workspace = Path(root)
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "paper.json").write_text(
        json.dumps({"id": paper_id, "source_sha256": "b" * 64, "blocks": []}), encoding="utf-8"
    )
    (workspace / "manifest.json").write_text(
        json.dumps({"paper_id": paper_id, "files": {}}), encoding="utf-8"
    )
    return workspace


def _prepared(root: Path, destination: Path, **overrides) -> Path:
    """What prepare writes, as publish reads it."""
    prepared = Path(root)
    prepared.mkdir(parents=True, exist_ok=True)
    record = {
        "publishable": True,
        "draft": 1,
        "attempt": 1,
        "plan_kind": "first review",
        "destination": str(destination),
        "input": {
            "kind": "doi",
            "identifier": PAPER.doi,
            "sha256": "b" * 64,
            "bytes": 2048,
            "local_file": False,
        },
        "preprint": PAPER.to_dict(),
    }
    record.update(overrides)
    (prepared / "prepared.json").write_text(json.dumps(record), encoding="utf-8")
    return prepared


def _publish(prepared: Path, run: Path, workspace: Path, *extra: str) -> int:
    return local_review.main(
        [
            "publish",
            "--prepared", str(prepared),
            "--run", str(run),
            "--workspace", str(workspace),
            "--decision", "major",
            "--editor", "fixture-editor",
            "--human-reviewed", "yes",
            *extra,
        ]
    )


@contextlib.contextmanager
def _stub_engine(version: str = "0.9.0"):
    """The installed distribution, which this suite runs without.

    `engine_record` reads the installed version through importlib.metadata and
    refuses when there is none, so every check that builds a record has to say
    which engine it is pretending to be.
    """
    original = local_review.engine_record
    local_review.engine_record = lambda: {"name": local_review.ENGINE_PACKAGE, "version": version}
    try:
        yield
    finally:
        local_review.engine_record = original


@contextlib.contextmanager
def _published_tree(root: Path):
    """A published tree somewhere harmless, for the checks that publish for real."""
    original = local_review.REVIEWS
    local_review.REVIEWS = Path(root)
    try:
        yield Path(root)
    finally:
        local_review.REVIEWS = original


def _stage_record(**overrides) -> dict:
    """The completeness block as the real reader produces it from the ledger."""
    return local_review.completeness(_stages(TRACKS, **overrides))


def _run_record(**overrides) -> dict:
    """The generator.run block of a published record, as read_run produces it."""
    record = {
        "arm": "full-two-track",
        "provider": "claude-code",
        "workflow_version": WORKFLOW_VERSION,
        "finding_schema_version": FINDING_SCHEMA,
        "reviewers": 3,
        "specialist_tracks": list(TRACKS),
        "paper_id": "paper-abc",
        "claude_code_version": CLAUDE_CODE_VERSION,
        "status": "complete",
        # The engine's own answer, which is the publish gate in 0.9. A record
        # carries it rather than this repository's reading of the same files.
        "publishable": True,
        "findings_source": "editor-package",
        "review_guard_status": "clean",
        "findings_delivered": 6,
        "quarantined_findings_count": 0,
        "escalated_count": 2,
        "findings_by_track": dict(COUNTED_BY_TRACK),
        "completeness": _stage_record(),
        "findings": len(local_review.sorted_findings(PACKAGE)),
        "appendix_findings": len(APPENDIX),
        "escalated_in_bundle": 2,
        "errors": [],
    }
    record.update(overrides)
    return record


def provenance_fixture() -> dict:
    """A version 4 record, in the shape build_provenance writes one."""
    return {
        "schema_version": local_review.PROVENANCE_SCHEMA,
        "decision": "major",
        "provider": "claude-code",
        "models": _expected_models(),
        "ingest": {
            "format": "markdown",
            "tool": "peerreviewagents import_paper",
            "text_sha256": "c" * 64,
            "chars": 40000,
        },
        "generator": {
            "kind": local_review.GENERATOR_KIND,
            "engine": {"name": local_review.ENGINE_PACKAGE, "version": "0.9.0"},
            "engine_fingerprint": {
                "algorithm": "sha256",
                "file_count": len(CODE),
                "sha256": "a" * 64,
                "source": "run_manifest",
            },
            "plugin": {
                "fingerprint": {
                    "algorithm": "sha256",
                    "file_count": 3,
                    "sha256": "e" * 64,
                    "source": "run_manifest",
                },
                "workflow_sha256": "1" * 64,
                "workflow_version": WORKFLOW_VERSION,
                "finding_schema_version": FINDING_SCHEMA,
            },
            "transport": _run_transport(),
            "agents": [
                {"slot": "core-1", "role": "core-reviewer", "model": SONNET, "findings": 3},
                {"slot": "editor", "role": "editor", "model": OPUS},
                {"slot": "ingest", "agent_type": "pra:recorder", "model": HAIKU},
            ],
            "input": {
                "kind": "doi",
                "identifier": PAPER.doi,
                "sha256": "b" * 64,
                "bytes": 2048,
                "local_file": False,
            },
            "run": _run_record(),
            "advisory_verdict": dict(VERDICT),
            "decision_source": "human_editor",
            "attestation": {
                "locally_generated": True,
                "human_reviewed_before_merge": True,
                "rehearsal": False,
                "editor": "fixture-editor",
                "statement": local_review.ATTESTATION,
            },
        },
    }


def _build_arguments(**overrides) -> dict:
    """Everything build_provenance needs, with one place to change it."""
    arguments = dict(
        preprint=PAPER,
        prepared={
            "input": {
                "kind": "doi",
                "identifier": PAPER.doi,
                "sha256": "b" * 64,
                "bytes": 2048,
                "local_file": False,
            },
            "plan_kind": "first review",
        },
        package=PACKAGE,
        run=_run_record(),
        fingerprint={
            "algorithm": "sha256",
            "file_count": len(CODE),
            "sha256": "a" * 64,
            "source": "run_manifest",
        },
        plugin={
            "fingerprint": {
                "algorithm": "sha256",
                "file_count": 3,
                "sha256": "e" * 64,
                "source": "run_manifest",
            },
            "workflow_sha256": "1" * 64,
            "workflow_version": WORKFLOW_VERSION,
            "finding_schema_version": FINDING_SCHEMA,
        },
        agents=[
            {"slot": "core-1", "model": SONNET},
            {"slot": "editor", "model": OPUS},
            {"slot": "ingest", "model": HAIKU},
        ],
        decision="major",
        route="v1/r1",
        draft=1,
        attempt=1,
        submitter="",
        submitter_is_author="",
        baseline_eligible=False,
        ingest={"format": "markdown", "tool": "peerreviewagents import_paper"},
        transport=_run_transport(),
        review_id="docs/reviews/2026/fixture/v1/r1",
        publishing=True,
    )
    arguments.update(overrides)
    return arguments


def _schema(name: str = "review-provenance.schema.json") -> dict:
    return json.loads(
        (Path(__file__).resolve().parents[2] / "schemas" / name).read_text(encoding="utf-8")
    )


def _schema_run_status() -> str:
    """The one run status the published schema accepts, read from the schema.

    Read rather than written out here, so a run this file calls publishable
    cannot be one `npm run check:schema` would then reject, and so the two
    cannot drift apart silently.
    """
    return _schema()["properties"]["generator"]["properties"]["run"]["properties"]["status"]["const"]


def _schema_verified_by() -> str:
    """The one transport evidence the published schema accepts."""
    generator = _schema()["properties"]["generator"]["properties"]
    return generator["transport"]["properties"]["verified_by"]["const"]


def _schema_run_requires() -> list[str]:
    return list(
        _schema()["properties"]["generator"]["properties"]["run"].get("required") or []
    )


def check_severity_is_read_from_the_engine_not_guessed() -> None:
    """An unknown severity must not be silently counted as the mildest one.

    The engine's severity vocabulary could grow. If it does, a finding this
    script does not recognise has to stay visible and stay out of the counts,
    rather than being quietly filed as minor, which would understate it.
    """
    ordered = local_review.sorted_findings(PACKAGE)
    assert [f["severity"] for f in ordered][:3] == ["major", "moderate", "minor"], (
        f"findings are not ordered by severity: {[f['severity'] for f in ordered]}"
    )
    assert ordered[-1]["severity"] == "catastrophic", "an unknown severity should sort last"

    counts = local_review.severity_counts(ordered)
    assert counts == {"major": 1, "moderate": 1, "minor": 1}, f"severity miscounted: {counts}"
    assert sum(counts.values()) < len(ordered), "an unknown severity was counted as a known one"

    # The appendix is the editor agent's overflow, not a second class of finding,
    # so it is read and ordered the same way.
    appendix = local_review.appendix_findings(PACKAGE)
    assert [f["severity"] for f in appendix] == ["moderate", "minor"], (
        f"the appendix is not ordered by severity: {appendix}"
    )
    assert [f["finding_uid"] for f in local_review.escalated(ordered)] == ["f-001"], (
        "an escalated body finding was not found"
    )
    assert [f["finding_uid"] for f in local_review.escalated(appendix)] == ["f-011"], (
        "an escalated appendix finding was not found"
    )


def check_the_decision_is_attributed_to_a_person() -> None:
    """The engine recommends no verdict, and the documents must say who did."""
    prov = provenance_fixture()
    findings = local_review.sorted_findings(PACKAGE)
    summary = local_review.render_summary(PAPER, PACKAGE, prov, findings)
    letter = local_review.render_decision_letter(PAPER, PACKAGE, prov, findings)

    assert "human editor" in summary, "the summary must say a person chose the decision"
    assert "recommends no verdict" in summary, "the summary must say the engine recommends none"
    assert "editor's" in letter, "the decision letter must attribute the decision to the editor"
    assert "fixture-editor" in summary, "the summary must name the editor who read the run"
    assert "agents sharing a model are not independent corroboration of one another" in summary, (
        "the summary must disclose that agents on one model do not corroborate each other"
    )
    assert "3 core reviewers" in summary, f"the panel is not described: {summary}"
    assert "6 specialist readers" in summary, f"the specialists are not described: {summary}"
    assert "2 more in the appendix" in summary, "the appendix findings are not counted"
    assert "**Escalated by a reviewer:** 2" in summary, "the escalations are not counted"
    assert "Findings raised per track" in summary, "the per-track counts were not published"

    # The documents are rendered from saved output, so the reviewer's own words
    # have to appear in them verbatim.
    assert PACKAGE["summary"] in summary, "the reviewer's summary was not carried through"
    assert "Report the confidence interval." in letter, "a finding's comment was not carried through"
    assert "> effects were large" in letter, "a quoted manuscript passage was not carried through"
    assert "The reported mean and n do not give the stated interval." in letter, (
        "the basis the reviewer recorded was not carried through"
    )
    assert "Rulings on escalated findings" in letter, "the editor agent's rulings were not published"
    assert "rounding step" in letter, "a ruling that went against the reviewer was dropped"

    # Severity decides whether a finding is required or optional. Nothing else
    # does, and in particular the decision does not.
    required = letter.split("## Required changes", 1)[1].split("## Suggestions", 1)[0]
    assert "The headline effect is unguarded" in required, "a major finding must be required"
    assert "Missing n" in required, "a moderate finding must be required"
    assert "A typo" not in required, "a minor finding must not be required"

    # And the appendix is published in full rather than summarised away.
    appendix = letter.split("## Appendix", 1)[1]
    assert "Panel b has no axis label" in appendix, "an appendix finding was dropped"
    assert "The body was already at its cap." in appendix, (
        "the editor agent's reason for moving a finding was dropped"
    )


def check_a_minor_finding_is_never_a_required_revision() -> None:
    """round.json drives the revision workflow, so the split has to hold there too."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        prov = provenance_fixture()
        findings = local_review.sorted_findings(PACKAGE)
        local_review.write_round_record(dest, PAPER, prov, findings)
        record = json.loads((dest / local_review.ROUND_RECORD).read_text())

    assert record["decision"] == "major", f"decision lost: {record.get('decision')!r}"
    assert len(record["required_revisions"]) == 2, (
        f"expected the major and the moderate: {record['required_revisions']}"
    )
    assert record["minor_suggestions"] == ["Fix the spelling."], (
        f"minor findings mangled: {record['minor_suggestions']}"
    )
    assert record["desk_rejected"] is False, "a local run has no desk screen to fail"
    assert record["manuscript_file_sha256"] == "b" * 64, "the reviewed bytes were not recorded"
    ids = [item["id"] for item in record["required_revisions"]]
    assert ids == sorted(set(ids)), f"required revision ids are not unique and ordered: {ids}"

    # A revision round has to say which finding it is answering, and an id this
    # file invented means nothing outside it. The engine's own uid travels with
    # the entry, along with the track it came from and what it rests on.
    first = record["required_revisions"][0]
    assert first["finding_uid"] == "f-001", f"the engine's own uid was dropped: {first}"
    assert first["track"] == "stats", f"the track was dropped: {first}"
    assert first["basis"] == "computed", f"the basis was dropped: {first}"
    assert first["escalated"] is True, f"the escalation was dropped: {first}"
    assert first["source_reviewer"] == "spec-stats", f"the slot was dropped: {first}"
    assert all(item["finding_uid"] for item in record["required_revisions"]), (
        f"a required revision carries no uid: {record['required_revisions']}"
    )


def check_an_unclaimed_review_is_labelled_an_experiment() -> None:
    """Agents wrote it, so the page has to say so unless an editor claims it.

    The word matters because Notices.astro and the provenance panel both read
    it, and because "editorial" on an unclaimed run would overstate what
    produced the review.
    """
    for plan_kind in ("first review", "same-draft re-review", "unpublishable local run"):
        label = local_review.review_kind(plan_kind, False)
        assert label == "experiment", f"{plan_kind!r} unclaimed should be an experiment, got {label!r}"

    assert local_review.review_kind("first review", True) == "initial"
    assert local_review.review_kind("same-draft re-review", True) == "editorial_rereview"

    # A revision round is named for what it is measured against, either way.
    assert local_review.review_kind("revision round", False) == "revision"
    assert local_review.review_kind("revision round", True) == "revision"

    # Every label has to be one the hosted panel already wrote, because the
    # site's notices switch on these exact strings.
    known = {"initial", "editorial_rereview", "revision", "experiment"}
    for plan_kind in ("first review", "same-draft re-review", "revision round", "", "nonsense"):
        for claimed in (True, False):
            label = local_review.review_kind(plan_kind, claimed)
            assert label in known, f"unknown review kind {label!r} for {plan_kind!r}"


def check_every_published_file_is_hashed() -> None:
    """The manifest is what makes a later edit to a published bundle visible."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        (dest / "summary.md").write_text("# Review Summary\n", encoding="utf-8")
        (dest / "decision_letter.md").write_text("# Decision Letter\n", encoding="utf-8")
        nested = dest / "attachments"
        nested.mkdir()
        (nested / "editor-package.json").write_text("{}", encoding="utf-8")

        local_review.write_manifest(dest)
        manifest = json.loads((dest / "manifest.json").read_text())

        assert manifest["schema_version"] == 1, f"manifest version: {manifest['schema_version']}"
        assert set(manifest["files"]) == {
            "summary.md",
            "decision_letter.md",
            "attachments/editor-package.json",
        }, f"manifest does not cover the bundle: {sorted(manifest['files'])}"
        assert all(len(h) == 64 for h in manifest["files"].values()), "a hash is not a sha256"
        assert "manifest.json" not in manifest["files"], "the manifest cannot hash itself"

        # An edit after publication must change the manifest, which is the whole
        # point of writing one.
        before = manifest["files"]["summary.md"]
        (dest / "summary.md").write_text("# Review Summary\n\nEdited.\n", encoding="utf-8")
        local_review.write_manifest(dest)
        after = json.loads((dest / "manifest.json").read_text())["files"]["summary.md"]
        assert before != after, "an edited document kept its hash"


def check_a_bare_pdf_cannot_be_published() -> None:
    """A review has to name the revision it judged, and a loose PDF does not."""
    with tempfile.TemporaryDirectory() as tmp:
        prepared = Path(tmp) / "prepared"
        prepared.mkdir()
        (prepared / "prepared.json").write_text(
            json.dumps(
                {
                    "publishable": False,
                    "destination": str(Path(tmp) / "run-out"),
                    "draft": 1,
                    "attempt": 1,
                    "input": {"kind": "pdf", "identifier": "manuscript.pdf", "sha256": "b" * 64, "bytes": 1},
                    "preprint": None,
                }
            ),
            encoding="utf-8",
        )
        run = _run_directory(Path(tmp) / "run")
        workspace = _workspace(Path(tmp) / "workspace")

        code = _publish(prepared, run, workspace, "--publish")
        assert code == 2, f"publishing an unidentified PDF should fail, got exit {code}"

    # And the decision is a closed set, so a typo cannot reach the record.
    assert local_review.DECISIONS == ("accept", "minor", "major", "reject"), (
        f"the decision vocabulary changed: {local_review.DECISIONS}"
    )
    for bad in ("accepted", "ACCEPT", "revise", ""):
        assert bad not in local_review.DECISIONS, f"{bad!r} must not be a decision"


def check_the_attestation_says_what_it_has_to_say() -> None:
    """The published claim is the point of this path, so pin its substance."""
    statement = local_review.ATTESTATION
    assert len(statement) >= 40, "the attestation is too short to be a claim"
    for phrase in ("locally", "no", "paid API key", "editor"):
        assert phrase in statement, f"the attestation does not mention {phrase!r}: {statement}"

    # The other statement is the one a rehearsal carries, and it has to be a
    # refusal rather than a softer version of the same claim.
    unread = local_review.UNREAD_STATEMENT
    assert len(unread) >= 40, "the rehearsal statement is too short to be a claim"
    assert "no editor" in unread.lower(), f"a rehearsal must say nobody read it: {unread}"
    assert "must not be published" in unread, f"a rehearsal must say so plainly: {unread}"
    assert "—" not in unread and ";" not in unread, "the rehearsal statement is authored prose"
    assert local_review.GENERATOR_KIND == "local-claude-code-plugin", (
        f"the generator kind is pinned by the schema: {local_review.GENERATOR_KIND}"
    )
    assert local_review.TRANSPORT_PROVIDER == "claude-code", (
        f"the transport is pinned by the schema: {local_review.TRANSPORT_PROVIDER}"
    )
    assert local_review.PROVENANCE_SCHEMA == 4, (
        f"the plugin record is schema version 4: {local_review.PROVENANCE_SCHEMA}"
    )
    assert len(local_review.SPECIALIST_TRACKS) == 6, (
        f"0.9 convenes six specialist readers: {local_review.SPECIALIST_TRACKS}"
    )
    assert "—" not in statement and ";" not in statement, "the attestation is authored prose"


def check_the_skill_commands_match_the_engine_parser() -> None:
    """Every engine command in the skill has to be one argparse accepts.

    The skill put `--provider` and `--model` before the `review` subcommand. The
    engine defines them on the subparser, so argparse rejected the command
    before any work began, and the only thing that would have caught it was
    spending a review.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import check_skill_commands as checker

    text = checker.SKILL.read_text(encoding="utf-8")
    found = [
        argv
        for block in checker.bash_blocks(text)
        for command in checker.commands(block)
        if (argv := checker.engine_arguments(command)) is not None
    ]
    assert found, f"no engine commands found in {checker.SKILL}"
    for argv in found:
        assert argv, "an engine command with no subcommand"
        assert not argv[0].startswith("-"), (
            f"this command passes an option before the subcommand, which argparse "
            f"rejects: {' '.join(argv)}"
        )
    assert any("review" in argv for argv in found), "the skill no longer runs a review"

    # The checker fails closed when it cannot import the engine and `CI` is
    # set, which is right for the CI step that exists to run it and wrong here:
    # this suite runs in a job with no engine by design, so an ambient `CI`
    # would make the outcome depend on where the suite happens to be running.
    # The environment is named rather than inherited. Fail-closed behaviour has
    # its own check, which names its environment too.
    waived = dict(os.environ)
    for name in ("CI", "INSILICO_REQUIRE_ENGINE"):
        waived.pop(name, None)
    restore = dict(os.environ)
    os.environ.clear()
    os.environ.update(waived)
    try:
        assert checker.main() == 0, "the skill's engine commands do not parse"
    finally:
        os.environ.clear()
        os.environ.update(restore)


def check_provenance_is_read_from_the_run() -> None:
    """Nothing in the record may be copied from an intention or a flag.

    Every field here comes from one of the five files the plugin writes. A value
    the run did not record is left out rather than defaulted, because a default
    silently becomes the published claim about a run that did something else.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = _run_directory(Path(tmp) / "run")
        run = local_review.read_run(run_dir)

        assert run["arm"] == "full-two-track", f"arm not read from protocol.json: {run}"
        assert run["provider"] == "claude-code", f"provider not read from protocol.json: {run}"
        assert run["workflow_version"] == WORKFLOW_VERSION, f"workflow version lost: {run}"
        assert run["finding_schema_version"] == FINDING_SCHEMA, f"finding schema lost: {run}"
        assert run["reviewers"] == 3, f"reviewer count not read from the run: {run}"
        assert run["specialist_tracks"] == list(TRACKS), f"the specialists were not read: {run}"
        assert run["paper_id"] == "paper-abc", f"paper id not read from the manifest: {run}"
        assert run["claude_code_version"] == CLAUDE_CODE_VERSION, f"harness version lost: {run}"
        assert run["status"] == "complete", f"status not read from the engine: {run}"
        # The engine answers the publish question itself, and the record carries
        # its answer rather than a second reading of the same files.
        assert run["publishable"] is True, f"the engine's publish flag was not read: {run}"
        assert run["findings_source"] == "editor-package", (
            f"the record must say the findings are the editor's own: {run}"
        )
        assert run["review_guard_status"] == "clean", f"the guard verdict was not read: {run}"
        assert run["findings_delivered"] == 6, f"the delivered count was not read: {run}"
        assert run["quarantined_findings_count"] == 0, f"a zero count is a count: {run}"
        assert run["escalated_count"] == 2, f"the escalations were not read: {run}"
        # Counted from the findings, not copied from the editor's own tally. The
        # fixture's package claims two stats findings and a field track, and the
        # findings beside it hold one stats finding and no field one.
        assert run["findings_by_track"] == COUNTED_BY_TRACK, f"the tracks were not counted: {run}"
        assert run["findings_by_track"] != FINDINGS_BY_TRACK, (
            "the editor's own tally was republished instead of the findings in the bundle"
        )
        assert run["wall_seconds"] == 1840.5, f"the wall time was not read from runtime.json: {run}"
        assert run["tokens_total"] == 412000, f"the token total was not read: {run}"
        assert run["errors"] == [], f"a clean run should record no errors: {run}"
        assert "directory" not in run, (
            f"a run outside this repository must not be named by its path: {run}"
        )
        # protocol.json records `literature_cutoff: null` on a run that set no
        # cutoff, and null is not a cutoff.
        assert "literature_cutoff" not in run, f"a null cutoff was published as one: {run}"
        dated = local_review.read_run(
            _run_directory(
                Path(tmp) / "dated",
                **{
                    "protocol.json": {
                        "provider": "claude-code",
                        "arm": "full-two-track",
                        "reviewers": 3,
                        "literature_cutoff": "2026-11-01",
                        "version": WORKFLOW_VERSION,
                        "agents": _protocol_agents(TRACKS),
                    }
                },
            )
        )
        assert dated["literature_cutoff"] == "2026-11-01", f"a real cutoff was dropped: {dated}"

        # The code that produced the review, hashed from the run's own manifest
        # rather than from whatever is installed at publish time.
        fingerprint = local_review.code_fingerprint(run["engine_source"], "run_manifest")
        assert fingerprint["file_count"] == len(CODE), f"fingerprint miscounted: {fingerprint}"
        assert fingerprint["source"] == "run_manifest", "the fingerprint must say where it came from"
        assert len(fingerprint["sha256"]) == 64, f"not a sha256: {fingerprint}"

        plugin = local_review.plugin_record(run["engine_source"], run)
        assert plugin["workflow_sha256"] == "1" * 64, f"the workflow hash was not read: {plugin}"
        assert plugin["fingerprint"]["file_count"] == 3, (
            f"the plugin fingerprint covers the plugin's own files: {plugin['fingerprint']}"
        )
        assert plugin["workflow_version"] == WORKFLOW_VERSION, f"workflow version lost: {plugin}"

        # Two runs can both say plugin-two-track-v1 and have run different agent
        # files, so a manifest with no workflow file cannot be published.
        for why, (code, record) in {
            "no workflow file": ({"plugin/agents/editor.md": "3" * 64}, run),
            "no workflow version": (dict(CODE), {}),
        }.items():
            try:
                local_review.plugin_record(code, record)
            except local_review.CommandError:
                continue
            raise AssertionError(f"a plugin record was written with {why}")

        # A folder that is not a run at all is refused by name rather than read
        # as a run that recorded nothing. The engine raises for both, and the
        # refusal has to point at the folder the engine writes.
        (Path(tmp) / "not-a-run").mkdir()
        for why, path in {
            "a folder that does not exist": Path(tmp) / "empty",
            "a folder holding none of the run's files": Path(tmp) / "not-a-run",
        }.items():
            try:
                local_review.read_run(path)
            except local_review.CommandError as refusal:
                assert "peerreview review" in str(refusal), (
                    f"the refusal for {why} does not say where a run comes from: {refusal}"
                )
                continue
            raise AssertionError(f"{why} was read as a run")

        # And what went wrong is read rather than assumed to be nothing. The
        # engine decides the status and the cause; what the record adds is the
        # harm a run can carry past them.
        broken = _run_directory(
            Path(tmp) / "broken",
            **{
                "progress.json": {
                    "status": "blocked",
                    "error": "the transport hung up",
                    "stages": _stages(TRACKS, reported=list(CORE_SLOTS), missing=["spec-stats"]),
                },
                "runtime.json": _runtime(TRACKS, status="blocked", blocked_reason="no plugin loaded"),
                "editor-package.json": dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    review_guard_status="partially-quarantined",
                ),
            },
        )
        _quarantine(
            broken,
            {"finding_uid": "f-020", "severity": "major", "title": "Unquotable"},
            {"finding_uid": "f-021", "severity": "minor", "title": "Unquotable too"},
        )
        record = local_review.read_run(broken)
        errors = record["errors"]
        assert record["publishable"] is False, f"a blocked run is not publishable: {record}"
        assert any("no plugin loaded" in e for e in errors), (
            f"the starter's own reason was dropped: {errors}"
        )
        assert any("blocked" in e for e in errors), f"a run that stopped should say so: {errors}"
        assert any("quarantined" in e for e in errors), f"quarantined findings are errors: {errors}"
        assert any("spec-stats" in e for e in errors), (
            f"a stage that never reported is an error: {errors}"
        )


def check_a_run_of_one_paper_cannot_be_published_as_another() -> None:
    """The reviewer published paper B's package under paper A's identity, exit 0.

    Three steps each hash something and none of them was compared: prepare
    hashes the fetched PDF, the importer hashes the bytes it was given, and the
    run records the paper id it reviewed.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        workspace.mkdir()
        (workspace / "paper.json").write_text(
            json.dumps({"id": "paper-abc", "source_sha256": "b" * 64}), encoding="utf-8"
        )
        (workspace / "manifest.json").write_text(json.dumps({"files": {}}), encoding="utf-8")
        prepared = {"input": {"sha256": "b" * 64}}
        run = {"paper_id": "paper-abc"}

        binding = local_review.bind_run_to_input(prepared, workspace, run)
        assert binding["paper_id"] == "paper-abc", f"the binding lost the paper id: {binding}"
        assert len(binding["workspace_manifest_sha256"]) == 64, f"workspace not hashed: {binding}"

        refusals = {
            "different bytes": ({"input": {"sha256": "c" * 64}}, run),
            "a different paper": (prepared, {"paper_id": "paper-xyz"}),
        }
        for why, (bad_prepared, bad_run) in refusals.items():
            try:
                local_review.bind_run_to_input(bad_prepared, workspace, bad_run)
            except local_review.CommandError:
                continue
            raise AssertionError(f"publishing {why} was allowed")

        # A workspace that recorded no hash cannot be tied to anything either.
        (workspace / "paper.json").write_text(json.dumps({"id": "paper-abc"}), encoding="utf-8")
        try:
            local_review.bind_run_to_input(prepared, workspace, run)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a workspace with no source hash was accepted")


def check_a_rehearsal_is_never_written_into_the_published_tree() -> None:
    """Without --publish the guards are relaxed, so the bundle must not land in docs/."""
    destination = local_review.REVIEWS / "2026" / "fixture-paper" / "v1" / "r1"
    prepared = {"destination": str(destination)}

    published = local_review.publish_destination(prepared, publishing=True)
    assert published == destination, f"a published bundle goes where prepare planned: {published}"

    rehearsal = local_review.publish_destination(prepared, publishing=False)
    assert not rehearsal.is_relative_to(local_review.REVIEWS), (
        f"a rehearsal was written into the published tree at {rehearsal}"
    )
    assert rehearsal.is_relative_to(local_review.RUNS), f"a rehearsal belongs under runs/: {rehearsal}"
    assert rehearsal.name == "r1" and "fixture-paper" in rehearsal.parts, (
        f"a rehearsal should still be identifiable: {rehearsal}"
    )


def check_the_method_paragraph_describes_the_run_that_happened() -> None:
    """The fixed wording described a workflow nobody ran.

    In 0.9 there is no debate stage to describe and no single model: the plugin
    pins a model per agent file, so the paragraph counts agents per model and
    says outright that agents sharing one are not corroborating each other.
    """
    models = _expected_models()
    full = local_review.method_paragraph(
        {"arm": "full-two-track", "reviewers": 3, "specialist_tracks": list(TRACKS)}, models
    )
    assert "3 core reviewers" in full, f"the reviewer count is not in the text: {full}"
    assert "6 specialist readers" in full, f"the specialists are not described: {full}"
    assert "an editor agent pooled every finding" in full, f"the editor is not described: {full}"
    assert EXPECTED_MODEL_PHRASE in full, f"the per-model counts are wrong: {full}"
    assert "no debate stage" in full, f"0.9 ran none, so the paragraph says so: {full}"
    for claim in ("debate round", "rounds of debate", "debated"):
        assert claim not in full, f"0.9 has no debate stage to describe: {full}"
    assert "One core reviewer" not in full, "a three reviewer run must not be called one reading"

    single = local_review.method_paragraph(
        {"arm": "single", "reviewers": 1}, {"core-1": OPUS}
    )
    assert "One core reviewer" in single, f"a single pass is not described: {single}"
    assert "convened no specialist readers" in single, f"an arm with no specialists: {single}"
    assert OPUS in single, "the paragraph must name the model that ran"

    unrecorded = local_review.method_paragraph({}, {})
    assert "did not record" in unrecorded, (
        f"an unmeasured run must say so rather than claim a shape: {unrecorded}"
    )
    assert "models the run did not record" in unrecorded, (
        f"a run with no model map must say so: {unrecorded}"
    )
    for text in (full, single, unrecorded):
        assert "—" not in text and ";" not in text, "the paragraph is authored prose"


def check_an_attestation_needs_a_named_editor() -> None:
    """`human_reviewed_before_merge: true` was a constant written before anyone acted.

    So was the editor. Both are now operator input with no default, and a run
    nobody has read must say that rather than attest to a reading that did not
    happen.
    """
    arguments = _build_arguments()
    with _stub_engine():
        try:
            local_review.build_provenance(editor="", human_reviewed=True, **arguments)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("an attestation was written with nobody behind it")

        attested = local_review.build_provenance(
            editor="fixture-editor", human_reviewed=True, **arguments
        )["generator"]["attestation"]
        assert attested["human_reviewed_before_merge"] is True
        assert attested["editor"] == "fixture-editor", f"the editor was not recorded: {attested}"
        assert attested["statement"] == local_review.ATTESTATION

        unread = local_review.build_provenance(
            editor="fixture-editor", human_reviewed=False, **arguments
        )["generator"]
        assert unread["attestation"]["human_reviewed_before_merge"] is False, (
            "an unread run must not claim a reading"
        )
        assert unread["attestation"]["statement"] == local_review.UNREAD_STATEMENT
        assert unread["decision_source"] == "human_editor", (
            f"the decision is a person's whoever read the run: {unread['decision_source']}"
        )


def check_a_run_with_no_manifest_paper_id_is_still_bound() -> None:
    """The paper id is written in two places, and only one of them is required.

    The plugin server writes it into both protocol.json and the run manifest. A
    run whose manifest omits it reported no paper id, and the binding check
    skipped itself rather than failing, so a run of paper B could be published
    under paper A by that route.
    """
    with tempfile.TemporaryDirectory() as tmp:
        elsewhere = _run_directory(
            Path(tmp) / "elsewhere",
            **{
                "protocol.json": {
                    "provider": "claude-code",
                    "arm": "full-two-track",
                    "reviewers": 3,
                    "paper_id": "paper-xyz",
                    "version": WORKFLOW_VERSION,
                    "agents": _protocol_agents(TRACKS),
                },
                "manifest.json": {
                    "source_sha256": "9" * 64,
                    "code": dict(CODE),
                    "workflow_version": WORKFLOW_VERSION,
                    "plan": _plan(TRACKS),
                },
            },
        )
        run = local_review.read_run(elsewhere)
        assert run["paper_id"] == "paper-xyz", f"paper id not read from protocol.json: {run}"

        workspace = _workspace(Path(tmp) / "workspace", "paper-abc")
        prepared = {"input": {"sha256": "b" * 64}}
        try:
            local_review.bind_run_to_input(prepared, workspace, run)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a run of another paper was bound to this workspace")

        # Neither side may be missing. A comparison with nothing to compare is
        # not a check that passed.
        for why, (paper_id, bad_run) in {
            "the run recorded no paper id": ("paper-abc", {}),
            "the workspace recorded no paper id": ("", {"paper_id": "paper-abc"}),
        }.items():
            ws = Path(tmp) / f"ws-{len(why)}"
            ws.mkdir()
            (ws / "paper.json").write_text(
                json.dumps({"id": paper_id, "source_sha256": "b" * 64}), encoding="utf-8"
            )
            try:
                local_review.bind_run_to_input(prepared, ws, bad_run)
            except local_review.CommandError:
                continue
            raise AssertionError(f"publishing was allowed although {why}")


def check_an_unfinished_run_cannot_be_published() -> None:
    """Publishing checked neither that the run started nor that it finished.

    A folder holding only an editor package published with an empty error list,
    and so did a run whose progress.json said blocked. Both read like a clean
    review.
    """
    with tempfile.TemporaryDirectory() as tmp:
        good = _run_directory(Path(tmp) / "good")
        local_review.require_complete_run(good, local_review.read_run(good))

        cases = {
            "no protocol.json": _run_directory(Path(tmp) / "no-protocol", **{"protocol.json": None}),
            "no progress.json": _run_directory(Path(tmp) / "no-progress", **{"progress.json": None}),
            "a blocked run": _run_directory(
                Path(tmp) / "blocked",
                **{
                    "progress.json": {
                        "status": "blocked",
                        "error": "No Claude Code login on this machine",
                        "stages": _stages(TRACKS),
                    },
                    "runtime.json": _runtime(
                        TRACKS,
                        status="blocked",
                        blocked_reason="No Claude Code login on this machine",
                    ),
                },
            ),
            # The starter writes runtime.json when the session ends, so a run
            # still going has none. A fixture that left a finished runtime.json
            # beside a running progress.json would be read as complete, because
            # the starter's status is the later of the two and wins.
            "a run still going": _run_directory(
                Path(tmp) / "running",
                **{
                    "progress.json": {"status": "running", "stages": _stages(TRACKS)},
                    "runtime.json": None,
                },
            ),
        }
        for why, run_dir in cases.items():
            try:
                local_review.require_complete_run(run_dir, local_review.read_run(run_dir))
            except local_review.CommandError:
                continue
            raise AssertionError(f"a review was published from a run with {why}")

        blocked = local_review.read_run(cases["a blocked run"])
        assert any("blocked" in e for e in blocked["errors"]), (
            f"a blocked run must say so in the record: {blocked['errors']}"
        )

        # And the refusal repeats what the run said went wrong. `blocked` is the
        # status the starter writes when the launch guard stops a run, and the
        # cause is the only part of it an operator can act on: a refusal naming
        # the state alone sends them back to read progress.json by hand.
        try:
            local_review.require_complete_run(cases["a blocked run"], blocked)
        except local_review.CommandError as error:
            assert "blocked" in str(error), f"the refusal has to name the state: {error}"
            assert "No Claude Code login" in str(error), (
                f"the refusal has to carry the cause the run recorded: {error}"
            )
        else:
            raise AssertionError("a blocked run was published")


def check_a_finished_run_that_endorses_nothing_is_a_review() -> None:
    """A run can finish every stage and raise no finding, and that is a result.

    Engine 0.9 records that outcome as `status: complete` with
    `review_guard_status: clean` and an empty findings list. Refusing it here
    would make the published corpus one that silently drops every review finding
    a manuscript sound: the papers nothing is wrong with would be exactly the
    ones that never got published, and the record would read as if the engine
    always finds something.

    A run with anything in quarantine is a third outcome, and in 0.9 it does
    not publish at all. The engine calls a run publishable only with the guard
    status `clean`, so a partially quarantined run is refused here where 0.8
    published it with a note: which findings the guards threw out, and whether
    the review still stands without them, is a judgement for a person.

    `complete-without-findings` is a different outcome and must not publish. The
    engine writes that status when every finding the reviewers raised failed the
    evidence guards and was quarantined. A review that endorses none of its own
    findings is not the claim that a manuscript was found sound, and a letter
    telling the authors the reviewers recorded no findings would be false. The
    refusal has to be an exit code, because that is the only thing that stops a
    bundle being written.
    """
    sound_package = dict(
        PACKAGE,
        findings=[],
        appendix=[],
        escalation_rulings=[],
        escalated_count=0,
        findings_by_track={track: 0 for track in TRACKS},
        findings_delivered=0,
        summary="Three reviewers read the manuscript and raised nothing.",
        stages=_stages(TRACKS),
    )
    with tempfile.TemporaryDirectory() as tmp:
        empty = _run_directory(
            Path(tmp) / "empty",
            **{
                "progress.json": {
                    "status": "complete",
                    "review_guard_status": "clean",
                    "stages": _stages(TRACKS),
                    "findings_delivered": 0,
                    "quarantined_findings_count": 0,
                },
                "editor-package.json": sound_package,
            },
        )
        reading = local_review.engine_reading(empty)
        record = local_review.run_record(reading)
        assert record["errors"] == [], (
            f"a finished run that raised nothing is not an error: {record['errors']}"
        )
        local_review.require_complete_run(empty, record, reading)
        assert record["status"] == _schema_run_status(), f"status lost: {record}"
        assert record["review_guard_status"] == "clean", f"the guard verdict was not read: {record}"
        assert local_review.sorted_findings(local_review.review_package(reading)) == [], (
            "a run with no findings has no findings"
        )

        # It publishes, documents and all, rather than refusing at the last step.
        # Only the installed engine is stubbed: the transport record is read from
        # the run's own start-up probe, so publishing needs no CLI and no network.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-sound-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    empty,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                    # Repeated deliberately. _publish types `major`, argparse keeps
                    # the last value, and a review that raised nothing is an accept.
                    "--decision", "accept",
                )
            assert code == 0, f"a review that raised nothing should publish, got exit {code}"
            letter = (destination / "decision_letter.md").read_text(encoding="utf-8")
            assert "recorded no findings" in letter, (
                "a review with no findings still owes the authors a letter that says so"
            )
            published = json.loads((destination / "provenance.json").read_text(encoding="utf-8"))
            run_record = published["generator"]["run"]
            assert run_record["status"] == _schema_run_status(), (
                f"the published status is not the one the schema accepts: {run_record}"
            )
            assert run_record["findings"] == 0, f"an empty review recorded findings: {run_record}"
            assert run_record["appendix_findings"] == 0, f"an empty review has no appendix: {run_record}"
            assert run_record["review_guard_status"] == "clean", (
                f"the published record has to carry the guard verdict: {run_record}"
            )
            assert run_record["completeness"]["missing"] == [], (
                f"a whole review has no missing stage: {run_record['completeness']}"
            )
            assert published["generator"]["decision_source"] == "human_editor", (
                "the decision is still a person's on a review that found nothing"
            )

        # Every finding quarantined is a different claim. The guard says so in
        # the record it reads, and the publish guard refuses the run.
        quarantined = _run_directory(
            Path(tmp) / "quarantined",
            **{
                "progress.json": {
                    "status": "complete-without-findings",
                    "review_guard_status": "all-findings-quarantined",
                    "stages": _stages(TRACKS),
                    "quarantined_findings_count": 4,
                },
                "editor-package.json": dict(
                    sound_package,
                    summary="Every finding the reviewers raised failed the guards.",
                    review_guard_status="all-findings-quarantined",
                    quarantined_findings_count=4,
                ),
            },
        )
        _quarantine(
            quarantined,
            *(
                {"finding_uid": f"f-03{index}", "severity": "major", "title": "Unquotable"}
                for index in range(4)
            ),
        )
        quarantined_record = local_review.read_run(quarantined)
        errors = quarantined_record["errors"]
        assert any("quarantined" in problem for problem in errors), (
            f"a run whose findings were all quarantined has to say so: {errors}"
        )
        try:
            local_review.require_complete_run(quarantined, quarantined_record)
        except local_review.CommandError as error:
            assert "quarantined" in str(error), (
                f"the refusal has to name what the guards did: {error}"
            )
        else:
            raise AssertionError("an all-quarantined run passed the publish guard")

        # And the whole command refuses, with a non-zero exit and no bundle on
        # disk. An error line printed beside a written bundle is not a refusal:
        # the folder is what gets committed.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews-quarantined") as reviews:
            destination = reviews / "2026" / "fixture-quarantined" / "v1" / "r1"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-quarantined", destination),
                    quarantined,
                    _workspace(Path(tmp) / "workspace-quarantined"),
                    "--publish",
                    "--decision", "accept",
                )
            message = stderr.getvalue()
            assert code != 0, f"an all-quarantined run was published, exit {code}"
            assert "quarantined" in message, (
                f"the refusal has to say what the guards did: {message!r}"
            )
            assert not destination.exists(), f"a bundle was written to {destination}"

        # Neither field alone carries the gate, and the guard verdict is read
        # out of the editor package rather than progress.json, so each case
        # writes it where the engine looks. A run that says `complete` and
        # reports every finding quarantined is refused on the guard, and one
        # that says `complete-without-findings` is refused on the status,
        # whatever guard value sits beside it.
        refusals = {
            "the guard alone": {
                "progress.json": {"status": "complete", "stages": _stages(TRACKS)},
                "editor-package.json": dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    review_guard_status="all-findings-quarantined",
                ),
            },
            "the status alone": {
                "progress.json": {
                    "status": "complete-without-findings",
                    "stages": _stages(TRACKS),
                },
            },
        }
        for index, (why, files) in enumerate(refusals.items()):
            run_dir = _run_directory(Path(tmp) / f"refused-{index}", **files)
            try:
                local_review.require_complete_run(run_dir, local_review.read_run(run_dir))
            except local_review.CommandError:
                continue
            raise AssertionError(f"a quarantined run was published on {why}")

        # A run that kept some findings and lost others is not published either,
        # and that is a change from 0.8, which published it with a note. The
        # engine calls any run with something in quarantine unpublishable:
        # which findings the guards threw out is a judgement for a person. The
        # refusal has to say how many and where to read them, or the operator
        # is sent back to the run folder to find out why it was refused.
        partial = _run_directory(
            Path(tmp) / "partial",
            **{
                "progress.json": {
                    "status": "complete",
                    "review_guard_status": "partially-quarantined",
                    "stages": _stages(TRACKS),
                    "quarantined_findings_count": 1,
                },
                "editor-package.json": dict(
                    PACKAGE, stages=_stages(TRACKS), review_guard_status="partially-quarantined"
                ),
            },
        )
        _quarantine(
            partial, {"finding_uid": "f-040", "severity": "moderate", "title": "Unquotable"}
        )
        partial_record = local_review.read_run(partial)
        assert partial_record["publishable"] is False, (
            f"a run with a finding in quarantine is not publishable: {partial_record}"
        )
        try:
            local_review.require_complete_run(partial, partial_record)
        except local_review.CommandError as error:
            assert "partially-quarantined" in str(error), (
                f"the refusal has to name the guard verdict: {error}"
            )
            assert "1 finding(s)" in str(error), (
                f"the refusal has to say how much was thrown out: {error}"
            )
        else:
            raise AssertionError("a run with a finding in quarantine was published")


def check_a_run_on_another_transport_is_not_published() -> None:
    """A Codex run published as a Claude Code run, with the attestation to match.

    The transport on the record was a constant, so a run whose `protocol.json`
    named `codex` still published with provider `claude-code` and this
    repository's claim about a Claude subscription paying for it. Nothing in the
    bundle said otherwise.

    In Silico publishes Claude Code runs only for now, so the run's own record
    decides: a provider this path does not publish is refused before any record
    is built, and the provider on the record is read from the run rather than
    from a constant, so the two cannot disagree.
    """
    assert local_review.PUBLISHABLE_PROVIDERS == ("claude-code",), (
        f"the publishable transports are a deliberate list: {local_review.PUBLISHABLE_PROVIDERS}"
    )

    with tempfile.TemporaryDirectory() as tmp:
        codex = _run_directory(
            Path(tmp) / "codex",
            **{
                "protocol.json": {
                    "provider": "codex",
                    "arm": "full-two-track",
                    "reviewers": 3,
                    "paper_id": "paper-abc",
                    "version": WORKFLOW_VERSION,
                    "agents": _protocol_agents(TRACKS),
                }
            },
        )
        record = local_review.read_run(codex)
        assert record["provider"] == "codex", f"the run's own transport was not read: {record}"

        try:
            local_review.require_complete_run(codex, record)
        except local_review.CommandError as error:
            assert "codex" in str(error), f"the refusal has to name the transport: {error}"
        else:
            raise AssertionError("a run on another transport passed the publish guard")

        # The transport record refuses it too, before it looks at anything else,
        # so no other provider's run is ever written up under this attestation.
        try:
            local_review.transport_record(provider="codex", runtime={}, startup=_startup())
        except local_review.CommandError as error:
            assert "codex" in str(error), f"the refusal has to name the transport: {error}"
        else:
            raise AssertionError("a transport record was written for another provider")

        # And the command refuses, with a non-zero exit and nothing on disk.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-codex-run" / "v1" / "r1"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    codex,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            message = stderr.getvalue()
            assert code != 0, f"a Codex run was published, exit {code}"
            assert "codex" in message, f"the refusal has to name the transport: {message!r}"
            assert not destination.exists(), f"a bundle was written to {destination}"

        # The published record takes the provider from the run. A transport block
        # that disagrees with the run is refused rather than written, so the two
        # cannot be made to say different things by stubbing one of them.
        with _stub_engine():
            written = local_review.build_provenance(
                **_build_arguments(editor="fixture-editor", human_reviewed=True)
            )
            assert written["generator"]["transport"]["provider"] == "claude-code"
            assert written["generator"]["run"]["provider"] == "claude-code"
            assert written["provider"] == "claude-code"

            mismatched = dict(_run_transport(), provider="codex")
            try:
                local_review.build_provenance(
                    **_build_arguments(
                        editor="fixture-editor", human_reviewed=True, transport=mismatched
                    )
                )
            except local_review.CommandError as error:
                assert "codex" in str(error), f"the refusal has to name both sides: {error}"
            else:
                raise AssertionError("a record was written whose transport disagreed with the run")

            # A run that recorded no provider at all cannot be described either.
            try:
                local_review.build_provenance(
                    **_build_arguments(
                        editor="fixture-editor",
                        human_reviewed=True,
                        run=_run_record(provider=""),
                    )
                )
            except local_review.CommandError:
                pass
            else:
                raise AssertionError("a record was written for a run with no transport")


def check_the_transport_claim_rests_on_the_runs_own_probe() -> None:
    """Nothing is probed at publish time, so the claim has to be narrower.

    0.8 shelled out to the Claude CLI while writing the bundle and published
    what it said about the account. The engine reads no authentication status in
    0.9, and this path will not guess one, so the record claims only what the
    run itself recorded: a Claude Code session started, loaded the plugin and
    connected its MCP server, which the engine writes to `startup.json` before
    it spends anything, on a Claude Code version `runtime.json` names.

    That makes publishing a pure read of the run folder. The PATH is emptied
    below to prove it, because a function that shells out to `claude` cannot be
    run by an editor on a machine where the CLI is not installed, and the whole
    point of reading the run is that it was already proved once.
    """
    assert local_review.VERIFIED_BY == _schema_verified_by(), (
        f"the schema accepts {_schema_verified_by()!r} and this path writes "
        f"{local_review.VERIFIED_BY!r}"
    )

    restore = os.environ.get("PATH", "")
    os.environ["PATH"] = ""
    try:
        record = local_review.transport_record(
            provider="claude-code", runtime=_runtime(TRACKS), startup=_startup()
        )
    finally:
        os.environ["PATH"] = restore

    assert record["provider"] == "claude-code", f"the transport was lost: {record}"
    assert record["version"] == CLAUDE_CODE_VERSION, (
        f"the harness version comes from runtime.json: {record}"
    )
    assert record["verified_at"] == STARTED_AT, f"the probe's own stamp was lost: {record}"
    assert record["verified_by"] == local_review.VERIFIED_BY, f"the evidence changed: {record}"
    assert record["login_verified"] is True, f"a session that started is a session: {record}"
    assert record["paid_api_key_used"] is False, f"this path cannot reach a paid key: {record}"
    assert record["billing_policy"] == local_review.BILLING_POLICY, (
        f"the record must name the policy it ran under: {record}"
    )

    # A run that recorded neither version says so with a null rather than a
    # guess, because the schema would rather have nothing than an invention.
    quiet = local_review.transport_record(
        provider="claude-code",
        runtime={},
        startup={"probe": {"mcp_servers": [{"name": "pra:peerreview", "status": "connected"}]}},
    )
    assert quiet["version"] is None, f"a version was invented: {quiet}"
    assert quiet["verified_at"] is None, f"a timestamp was invented: {quiet}"

    refusals = {
        "another transport": {"provider": "codex", "startup": _startup()},
        "no start-up probe at all": {"provider": "claude-code", "startup": {}},
        "a probe that reported a problem": {
            "provider": "claude-code",
            "startup": _startup(problems=["the pra plugin failed to load"]),
        },
        "no MCP server": {
            "provider": "claude-code",
            "startup": _startup(probe={"plugins": ["pra"], "mcp_servers": []}),
        },
        "an MCP server that never connected": {
            "provider": "claude-code",
            "startup": _startup(
                probe={
                    "mcp_servers": [
                        {"name": "plugin:pra:peerreview", "status": "failed", "source": "plugin"}
                    ]
                }
            ),
        },
        "somebody else's MCP server": {
            "provider": "claude-code",
            "startup": _startup(
                probe={"mcp_servers": [{"name": "plugin:other:search", "status": "connected"}]}
            ),
        },
    }
    for why, keywords in refusals.items():
        try:
            local_review.transport_record(runtime=_runtime(TRACKS), **keywords)
        except local_review.CommandError:
            continue
        raise AssertionError(f"a transport record was written for a run with {why}")

    # A run whose start-up probe is missing is refused by the command too, not
    # only by the function, and nothing is written.
    with tempfile.TemporaryDirectory() as tmp:
        unproved = _run_directory(Path(tmp) / "unproved", **{"startup.json": None})
        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-unproved" / "v1" / "r1"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    unproved,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code != 0, f"a run with no start-up probe was published, exit {code}"
            assert "startup.json" in stderr.getvalue(), (
                f"the refusal has to name the evidence it wanted: {stderr.getvalue()!r}"
            )
            assert not destination.exists(), f"a bundle was written to {destination}"


def check_a_placeholder_agent_row_is_not_a_reviewer() -> None:
    """runtime.json opens with five rows that are a label and nothing else.

    Claude Code emits one per agent it has reserved and not yet named, so a real
    0.9 run carries `agent-0` through `agent-4` beside the agents that ran, and
    the engine's reading hands them back as rows like any other. Counting them
    put five empty reviewers on the published panel and in the model table,
    which is a claim about a panel that did not sit.

    The rows are the engine's own merge of the protocol's slots with what the
    harness observed, so the fixture is a run folder rather than two
    hand-written files, and what is checked here is which of those rows reach a
    published record.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        rows = local_review.agent_rows(local_review.engine_reading(run))

        slots = [row["slot"] for row in rows]
        assert not [slot for slot in slots if slot.startswith("agent-")], (
            f"a placeholder row was published as an agent that ran: {slots}"
        )
        assert len(rows) == 12, (
            "expected three core, six specialists, an editor, a recorder and "
            f"the ingest row: {slots}"
        )
        assert all("slot" in row for row in rows), f"a row with no slot: {rows}"

        by_slot = {row["slot"]: row for row in rows}
        assert by_slot["core-1"]["role"] == "core-reviewer", (
            f"the protocol's own role for a core reviewer was lost: {by_slot['core-1']}"
        )
        assert by_slot["spec-stats"]["track"] == "stats", (
            f"the track was lost: {by_slot['spec-stats']}"
        )
        assert by_slot["core-1"]["findings"] > 0 and by_slot["editor"]["findings"] == 0, (
            "the findings each slot delivered were not counted from the findings "
            f"themselves: {by_slot['core-1']}, {by_slot['editor']}"
        )
        assert by_slot["spec-field"]["none_found"] is True, (
            f"a reader that reported nothing on its track must say so: {by_slot['spec-field']}"
        )
        assert by_slot["core-2"]["attempt"] == 2, (
            f"a retried slot lost its attempt: {by_slot['core-2']}"
        )
        assert by_slot["editor"]["model"] == OPUS, (
            f"the editor's model was lost: {by_slot['editor']}"
        )
        assert "model" not in by_slot["recorder"], (
            f"protocol.json pins no model for the recorder: {by_slot['recorder']}"
        )

        models = local_review.model_map(rows)
        assert models == _expected_models(), f"the model map is wrong: {models}"
        assert local_review.model_phrase(models) == EXPECTED_MODEL_PHRASE, (
            f"the model counts are wrong: {local_review.model_phrase(models)}"
        )
        assert local_review.model_phrase({}) == "models the run did not record", (
            "a run with no model map must say so rather than name one"
        )

        # A run whose harness record is nothing but placeholders still has the
        # protocol's own slots, and the one model only the harness knew is gone
        # from the map, so a record built from it cannot name haiku.
        unnamed = _run_directory(
            Path(tmp) / "unnamed",
            **{
                "runtime.json": _runtime(
                    TRACKS, agents=[{"label": f"agent-{index}"} for index in range(5)]
                )
            },
        )
        placeholders = local_review.agent_rows(local_review.engine_reading(unnamed))
        assert len(placeholders) == 11, (
            f"the protocol's own slots are still agents: {placeholders}"
        )
        assert HAIKU not in local_review.model_map(placeholders).values(), (
            "the recorder's model is only known from the harness"
        )
    with _stub_engine():
        try:
            local_review.build_provenance(
                **_build_arguments(editor="fixture-editor", human_reviewed=True, agents=[])
            )
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a record was written that named no model for any agent")


def check_a_stage_that_never_reported_is_not_a_whole_review() -> None:
    """The stage ledger is the only thing that says the panel actually sat.

    A run reaches `complete` when the editor accepts the pooled findings, and it
    can do that with a specialist that never answered. A bundle saying three
    core reviewers and six specialists over such a run describes readers that
    did not report, so the ledger travels with the record and a missing stage is
    refused.
    """
    ledger = _stage_record()
    assert ledger["required"] == [*CORE_SLOTS, *(f"spec-{t}" for t in TRACKS)], (
        f"the required stages are the arm's own: {ledger}"
    )
    assert ledger["missing"] == [], f"a whole review has no missing stage: {ledger}"
    assert ledger["none_found"] == ["spec-field"], (
        f"a reader that found nothing is not a reader that did not report: {ledger}"
    )
    assert ledger["editor_accepted"] is True, f"the editor accepted the pool: {ledger}"
    assert ledger["retried"] == ["core-2"], f"a retried slot has to be visible: {ledger}"

    assert "completeness" in _schema_run_requires(), (
        "the schema requires the stage ledger, so a run without one cannot publish"
    )
    assert local_review.completeness({}) == {}, (
        "a run with no ledger records none rather than an empty one that reads as whole"
    )

    with tempfile.TemporaryDirectory() as tmp:
        no_ledger_dir = _run_directory(
            Path(tmp) / "no-ledger",
            **{
                "progress.json": {"status": "complete", "review_guard_status": "clean"},
                "editor-package.json": dict(PACKAGE),
            },
        )
        no_ledger = local_review.read_run(no_ledger_dir)
        assert "completeness" not in no_ledger, (
            f"a run that kept no ledger must not be described as whole: {no_ledger}"
        )
        # The engine calls it publishable, because every file it reads is whole
        # and the review is there. What it cannot say is which readers the arm
        # asked for, and that is the claim the bundle makes, so it is refused
        # here rather than published with the ledger left out.
        assert no_ledger["publishable"] is True, (
            f"the engine's own flag is not what refuses this run: {no_ledger}"
        )
        try:
            local_review.require_complete_run(no_ledger_dir, no_ledger)
        except local_review.CommandError as error:
            assert "stage ledger" in str(error), (
                f"the refusal has to say what is missing: {error}"
            )
        else:
            raise AssertionError("a review was published from a run with no stage ledger")

        short = _run_directory(
            Path(tmp) / "short",
            **{
                "progress.json": {
                    "status": "complete",
                    "review_guard_status": "clean",
                    "stages": _stages(
                        TRACKS,
                        reported=[*CORE_SLOTS, "spec-stats"],
                        missing=["spec-citations", "spec-field"],
                    ),
                }
            },
        )
        record = local_review.read_run(short)
        assert record["completeness"]["missing"] == ["spec-citations", "spec-field"], (
            f"the missing stages were not read: {record['completeness']}"
        )
        assert any("never reported" in problem for problem in record["errors"]), (
            f"a stage that never reported is an error: {record['errors']}"
        )
        try:
            local_review.require_complete_run(short, record)
        except local_review.CommandError as error:
            assert "spec-citations" in str(error), f"the refusal has to name the stage: {error}"
            assert "full-two-track" in str(error), f"the refusal has to name the arm: {error}"
        else:
            raise AssertionError("a review was published over a specialist that never reported")

        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-short-run" / "v1" / "r1"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    short,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code != 0, f"a run with a missing stage was published, exit {code}"
            assert not destination.exists(), f"a bundle was written to {destination}"

        # An editor that never accepted the pool is recorded as a problem rather
        # than smoothed over, because the findings in the bundle were pooled by
        # something that did not finish.
        unaccepted = local_review.read_run(
            _run_directory(
                Path(tmp) / "unaccepted",
                **{
                    "progress.json": {
                        "status": "complete",
                        "review_guard_status": "clean",
                        "stages": _stages(TRACKS, editor_accepted=False),
                    }
                },
            )
        )
        assert unaccepted["completeness"]["editor_accepted"] is False, (
            f"the acceptance was not read: {unaccepted['completeness']}"
        )
        assert any("did not accept" in problem for problem in unaccepted["errors"]), (
            f"an editor that did not accept the pool is an error: {unaccepted['errors']}"
        )


def check_every_specialist_report_reaches_the_bundle() -> None:
    """Six readers each wrote a report, and the bundle publishes all six.

    The editor agent keeps what it keeps, and `audit_<track>.md` is the only
    place a reader can see what the statistics reader looked for rather than
    only what survived the pooling. `src/lib/corpus.js` already lists any
    `audit_<track>.md` in a bundle as a report of its own, so copying them in is
    all that is needed.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        reports = local_review.track_reports(run)
        assert sorted(reports) == sorted(f"audit_{track}.md" for track in TRACKS), (
            f"the specialist reports were not found: {sorted(reports)}"
        )

        # An empty file is not a report. The engine writes one for a reader that
        # was convened and never answered, and publishing it would show a reader
        # with nothing to say as a reader that said nothing.
        (run / "audit_field.md").write_text("", encoding="utf-8")
        assert "audit_field.md" not in local_review.track_reports(run), (
            "an empty specialist report was published as a report"
        )
        (run / "audit_field.md").write_text("# field\n\nNothing found.\n", encoding="utf-8")

        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-reports" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"
            written = sorted(path.name for path in destination.iterdir())
            for track in TRACKS:
                assert f"audit_{track}.md" in written, (
                    f"the {track} report did not reach the bundle: {written}"
                )
            manifest = json.loads((destination / "manifest.json").read_text())["files"]
            assert all(f"audit_{track}.md" in manifest for track in TRACKS), (
                f"a copied report was left out of the manifest: {sorted(manifest)}"
            )
            assert "reports  6 specialist track report(s) copied in" in out.getvalue(), (
                f"the command has to say what it copied: {out.getvalue()!r}"
            )

        # A run that wrote only one of them publishes, and says which readers
        # left no report rather than letting the bundle imply six.
        thin = _run_directory(Path(tmp) / "thin", report_tracks=("stats",))
        with _stub_engine(), _published_tree(Path(tmp) / "reviews-thin") as reviews:
            destination = reviews / "2026" / "fixture-thin-reports" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-thin", destination),
                    thin,
                    _workspace(Path(tmp) / "workspace-thin"),
                    "--publish",
                )
            assert code == 0, f"a run with one report should still publish, got exit {code}"
            printed = out.getvalue()
            assert "warning  no specialist report written for:" in printed, (
                f"the absent readers were not named: {printed!r}"
            )
            for track in TRACKS:
                if track != "stats":
                    assert track in printed.split("warning", 1)[1], (
                        f"{track} wrote no report and was not named: {printed!r}"
                    )


def check_the_run_folder_is_found_whichever_path_is_typed() -> None:
    """`peerreview review <pdf> <out>` writes two folders, and both are typed.

    The review lands in `<out>/review` and the imported manuscript in
    `<out>/manuscript`. An editor types one or the other, and pointing --run at
    the out directory used to read an empty folder and report a run that
    recorded nothing.
    """
    with tempfile.TemporaryDirectory() as tmp:
        out = _run_tree(Path(tmp) / "out")
        review_dir = out / local_review.REVIEW_DIRECTORY

        assert local_review.resolve_review_dir(out) == review_dir, (
            "the out directory has to resolve to the review folder inside it"
        )
        assert local_review.resolve_review_dir(review_dir) == review_dir, (
            "the review folder itself has to resolve to itself"
        )
        assert local_review.read_run(out) == local_review.read_run(review_dir), (
            "the two paths describe one run"
        )
        assert local_review.review_package(
            local_review.engine_reading(out)
        ) == local_review.review_package(local_review.engine_reading(review_dir)), (
            "the review read from either path is the same review"
        )
        assert sorted(local_review.track_reports(out)) == sorted(
            local_review.track_reports(review_dir)
        ), "the specialist reports have to be found from either path"

        # The workspace defaults to the one the run actually used, which is the
        # manuscript folder beside it, and the flag still wins when it is given.
        assert local_review.resolve_workspace(review_dir, "") == (
            out / local_review.MANUSCRIPT_DIRECTORY
        ), "the manuscript folder beside the run is the default workspace"
        elsewhere = _workspace(Path(tmp) / "elsewhere")
        assert local_review.resolve_workspace(review_dir, str(elsewhere)) == elsewhere, (
            "a named workspace has to be used"
        )

        lonely = _run_directory(Path(tmp) / "lonely")
        try:
            local_review.resolve_workspace(lonely, "")
        except local_review.CommandError as error:
            assert "paper.json" in str(error), f"the refusal has to say what it wanted: {error}"
        else:
            raise AssertionError("a run with no manuscript workspace beside it was accepted")

        # And the command publishes from the out directory with no --workspace,
        # which is the shortest thing an editor can type.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-whole-out" / "v1" / "r1"
            prepared = _prepared(Path(tmp) / "prepared", destination)
            with contextlib.redirect_stdout(io.StringIO()):
                code = local_review.main(
                    [
                        "publish",
                        "--prepared", str(prepared),
                        "--run", str(out),
                        "--decision", "major",
                        "--editor", "fixture-editor",
                        "--human-reviewed", "yes",
                        "--publish",
                    ]
                )
            assert code == 0, f"publishing from the out directory failed with exit {code}"
            assert (destination / "provenance.json").is_file(), "no record was written"


def check_the_advisory_verdict_is_labelled_advisory() -> None:
    """The editor agent's judgement is published, and it is not the decision.

    It is the most useful thing in the run for a reader deciding whether to read
    the paper, so it is published rather than dropped. It is one model's reading,
    so every place it appears says so and says the decision came from a person.
    """
    lines = local_review.verdict_section(VERDICT)
    assert lines[0] == "## Advisory judgement from the engine", f"the heading changed: {lines[:1]}"
    body = "\n".join(lines)
    assert "not the decision" in body, f"the verdict has to be labelled: {body}"
    assert "recommends no" in body, f"the verdict has to recommend nothing: {body}"
    assert "one model's judgement" in body, f"the verdict has to name what it is: {body}"
    for value in VERDICT.values():
        assert value in body, f"a field of the verdict was dropped: {body}"
    assert "—" not in body and ";" not in body, "the section is authored prose"

    # A run that recorded no verdict publishes no section, rather than an empty
    # heading a reader would read as a verdict withheld.
    assert local_review.verdict_section({}) == [], "an absent verdict renders nothing"
    assert local_review.verdict_section({"significance": "   "}) == [], (
        "a blank verdict renders nothing"
    )

    prov = provenance_fixture()
    findings = local_review.sorted_findings(PACKAGE)
    summary = local_review.render_summary(PAPER, PACKAGE, prov, findings)
    assert "## Advisory judgement from the engine" in summary, (
        "the summary has to carry the engine's judgement"
    )
    assert summary.index("human editor") < summary.index("Advisory judgement"), (
        "the person who decided comes before the engine's reading"
    )

    with _stub_engine():
        record = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=True)
        )
    assert record["generator"]["advisory_verdict"] == VERDICT, (
        f"the verdict was not published as recorded: {record['generator']['advisory_verdict']}"
    )
    assert record["generator"]["decision_source"] == "human_editor", (
        "the decision source is the person, whatever the engine judged"
    )
    assert record["decision"] == "major", "the published decision is the editor's"
    bare = local_review.build_provenance.__doc__ or ""
    assert "advisory" in bare, "the record's own documentation has to say what it publishes"


def check_a_published_record_names_no_local_path() -> None:
    """Two fields published the operator's filesystem.

    `generator.run.directory` carried the absolute run path on every record,
    and `review.id` carried an absolute destination whenever the bundle was
    written outside the repository. Both describe the machine that wrote the
    record rather than the review, and the record is published.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = local_review.read_run(_run_directory(Path(tmp) / "run"))
        assert "directory" not in run, f"the run path was published: {run}"
    # A run inside this repository is named relative to it, because that path
    # is a fact about the repository rather than about the operator's disk. The
    # fixture has to sit inside the tree to be read that way, so it is written
    # into a temporary folder there and removed again.
    with tempfile.TemporaryDirectory(dir=local_review.REPO) as inside_repo:
        run_dir = _run_directory(Path(inside_repo) / "run")
        here = local_review.read_run(run_dir)
        expected = run_dir.relative_to(local_review.REPO).as_posix()
        assert here.get("directory") == expected, (
            f"a run inside the repository is named relative to it: {here.get('directory')!r}"
        )

    assert local_review.absolute_path_fields({"a": {"b": "/home/someone/run"}}) == ["a.b"]
    assert local_review.absolute_path_fields({"u": "file:///home/someone"}) == ["u"]
    assert local_review.absolute_path_fields(
        {"ok": "docs/reviews/2026/p/v1/r1", "url": "https://arxiv.org/abs/1"}
    ) == [], "a relative path and a URL are not local paths"
    assert local_review.absolute_path_fields({"runs": [{"directory": "/tmp/x"}]}) == [
        "runs[0].directory"
    ], "a leak inside a list has to be named"

    # The whole record, built from a run whose manifest carries the absolute
    # manuscript path and plugin root the plugin server writes into it.
    with _stub_engine():
        record = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=True)
        )
    assert local_review.absolute_path_fields(record) == [], (
        f"the record names the machine that wrote it: "
        f"{local_review.absolute_path_fields(record)}"
    )

    inside = local_review.REVIEWS / "2026" / "fixture-paper" / "v1" / "r1"
    assert local_review.bundle_identifier(inside) == "docs/reviews/2026/fixture-paper/v1/r1", (
        "a bundle in this repository is named by its path here"
    )
    outside = local_review.bundle_identifier(Path("/tmp/elsewhere/fixture/v1/r1"))
    assert not outside.startswith("/"), f"a bundle id must not be an absolute path: {outside}"
    assert outside == "fixture/v1/r1", f"a bundle id should still identify the bundle: {outside}"


def check_a_rehearsal_claims_no_reading() -> None:
    """A rehearsal's own documents said a human editor had read the run.

    `--human-reviewed no` writes the absence into the record, and the summary
    and the decision letter printed the attested wording anyway, so the two
    halves of the same bundle disagreed.
    """
    findings = local_review.sorted_findings(PACKAGE)
    unread = provenance_fixture()
    unread["generator"]["attestation"]["human_reviewed_before_merge"] = False
    unread["generator"]["attestation"]["rehearsal"] = True
    unread["generator"]["attestation"]["statement"] = local_review.UNREAD_STATEMENT

    summary = local_review.render_summary(PAPER, PACKAGE, unread, findings)
    letter = local_review.render_decision_letter(PAPER, PACKAGE, unread, findings)
    for name, text in (("summary", summary), ("decision letter", letter)):
        assert "after reading the run" not in text, (
            f"the {name} of a rehearsal claims a reading that did not happen"
        )
        assert "must not be published" in text, f"the {name} of a rehearsal must say so: {text}"
        assert "—" not in text and ";" not in text, f"the {name} is authored prose"
    assert "fixture-editor" in summary, "the rehearsal still names who typed the decision"
    assert "recommends no verdict" in summary, (
        "a rehearsal still has to say the engine recommends nothing"
    )

    # And the attested wording is still there when somebody did read it.
    attested = local_review.render_summary(PAPER, PACKAGE, provenance_fixture(), findings)
    assert "after reading the run" in attested, "an attested review must say the editor read it"
    assert "must not be published" not in attested, "an attested review is publishable"


def check_a_destination_outside_its_tree_is_refused() -> None:
    """Publishing wrote wherever prepared.json pointed.

    `publishing=True` returned the recorded destination unchanged, so any path
    in that file was written to. The rehearsal path was assembled from
    unresolved parts, so `..` segments passed through it, which is why the
    refusal guarding it could never fire.
    """
    for bad in ("/etc/insilico/v1/r1", "/tmp/anywhere/v1/r1"):
        try:
            local_review.publish_destination({"destination": bad}, publishing=True)
        except local_review.CommandError:
            continue
        raise AssertionError(f"a published bundle was allowed at {bad}")

    escape = str(local_review.REVIEWS / "2026" / ".." / ".." / ".." / "etc" / "v1" / "r1")
    try:
        local_review.publish_destination({"destination": escape}, publishing=True)
    except local_review.CommandError:
        pass
    else:
        raise AssertionError("a destination that climbs out of docs/reviews was published to")

    rehearsal_root = (local_review.RUNS / "rehearsal").resolve()
    for destination in (escape, "/etc/insilico/v1/r1", "r1"):
        rehearsal = local_review.publish_destination(
            {"destination": destination}, publishing=False
        )
        assert rehearsal.is_relative_to(rehearsal_root), (
            f"a rehearsal of {destination} landed outside {rehearsal_root}: {rehearsal}"
        )
        assert ".." not in rehearsal.parts, f"an unresolved path reached disk: {rehearsal}"

    planned = local_review.REVIEWS / "2026" / "fixture-paper" / "v1" / "r1"
    assert local_review.publish_destination(
        {"destination": str(planned)}, publishing=True
    ) == planned, "a bundle prepare planned inside docs/reviews still goes there"


# Running the checker in a subprocess that cannot import the engine is the only
# way to ask what CI would have seen, because this interpreter's engine, or lack
# of one, is fixed by the time the check runs.
_BLOCK_THE_ENGINE = """
import sys

class Refuse:
    def find_module(self, name, path=None):
        return None

    def find_spec(self, name, target=None, path=None):
        if name == "peerreviewagents" or name.startswith("peerreviewagents."):
            raise ImportError("no engine in this interpreter")
        return None

sys.meta_path.insert(0, Refuse())
for name in list(sys.modules):
    if name == "peerreviewagents" or name.startswith("peerreviewagents."):
        del sys.modules[name]
sys.path.insert(0, {scripts!r})
import check_skill_commands
raise SystemExit(check_skill_commands.main())
"""


def _skill_check_without_an_engine(**environment: str) -> int:
    """The checker's exit code in an interpreter with no engine to import."""
    scripts = str(Path(__file__).resolve().parents[1])
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"CI", "INSILICO_REQUIRE_ENGINE"}
    }
    env.update(environment)
    finished = subprocess.run(
        [sys.executable, "-I", "-c", _BLOCK_THE_ENGINE.format(scripts=scripts)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return finished.returncode


def check_a_missing_engine_fails_the_skill_check_in_ci() -> None:
    """The guard has to fail where it cannot do its job, not pass.

    The checker exited 0 with the word "skipped" whenever the engine was not
    importable, and the lock file pinned a release that contains no engine
    package, so CI ran the guard, imported nothing, printed "skipped" and went
    green. Two things that were each individually defensible added up to a
    check that could not fail. In CI a missing engine is now the lock file
    being wrong, which is a failure.
    """
    assert _skill_check_without_an_engine(CI="true") == 1, (
        "CI accepted a run of this check that could not import the engine"
    )
    assert _skill_check_without_an_engine(INSILICO_REQUIRE_ENGINE="1") == 1, (
        "an editor asking for the real answer was given a skip"
    )

    # And it still has to be runnable on a laptop with no engine installed,
    # which is the reason the skip existed.
    assert _skill_check_without_an_engine() == 0, (
        "a local interpreter with no engine can no longer run the check at all"
    )
    assert _skill_check_without_an_engine(CI="false") == 0, "CI=false is not CI"
    assert _skill_check_without_an_engine(CI="true", INSILICO_REQUIRE_ENGINE="0") == 0, (
        "a deliberate waiver in CI was not honoured"
    )


def check_no_published_file_in_a_bundle_names_a_local_path() -> None:
    """What gets scrubbed is a list of fields, and what gets scanned is a string.

    editor-package.json is copied out of the run as it stands, and a run folder
    records absolute paths in several places: the plugin server writes the
    manuscript's path as `pdf` and the loaded plugin's as `plugin_root`, a
    reviewer's package is recorded at `source_review_path`, each evidence memo at
    `memo_path`, and a figure map is keyed by the absolute path of every figure.
    Those are the leaks.

    Deciding by value rather than by field made the cure worse: a finding whose
    comment began with a slash was deleted from the published package, and one
    that merely mentioned a path aborted the publish. Meanwhile the scan read
    only JSON values beginning with a slash, so it saw neither a path keyed by
    itself, nor `~/`, nor a Windows path, nor any of the Markdown rendered from
    the same package.
    """
    home = str(Path.home().resolve())
    leaky = {
        "workflow_version": WORKFLOW_VERSION,
        "summary": "One reading.",
        "pdf": f"{home}/runs/local/paper.pdf",
        "plugin_root": f"{home}/Repos/PeerReviewAgents/plugins/pra",
        "reviewer_provenance": [
            {"slot": "core-1", "source_review_path": f"{home}/runs/out/core-1/editor-package.json"},
            {"slot": "core-2", "source_review_path": f"{home}/runs/out/core-2/editor-package.json"},
        ],
        "focused_evidence_provenance": [{"memo_sha256": "a" * 64, "memo_path": f"{home}/memo.md"}],
        "synthesis_provenance": {"shared_images": {f"{home}/runs/fig1.png": "b" * 64}},
        "findings": [
            {"severity": "major", "comment": "/ 2 is the wrong denominator here."},
            {"severity": "minor", "comment": "See /dev/null for the logs they cite."},
        ],
        "reference": "https://www.biorxiv.org/content/10.1101/2026.03.12.711120v1",
        "notes": "Section 3 of the manuscript",
    }

    scrubbed = local_review.without_local_paths(leaky)

    # The review's own words, first. Scrubbing by value rather than by field
    # deleted a finding whose comment opened with a slash, and aborted the
    # publish on the one that only mentioned a path.
    assert scrubbed["findings"] == leaky["findings"], (
        f"a reviewer's own comments were rewritten: {scrubbed['findings']}"
    )
    assert scrubbed["summary"] == leaky["summary"], "the review's own words were altered"
    assert scrubbed["reference"] == leaky["reference"], "a URL is not a local path"
    assert scrubbed["notes"] == leaky["notes"], "ordinary prose was altered"

    # Then the fields the engine really fills with a path, including the one
    # where the path is the dictionary key.
    flat = json.dumps(scrubbed)
    assert home not in flat, f"a local path survived the scrub: {flat}"
    assert "pdf" not in scrubbed, f"the manuscript's own path was published: {scrubbed}"
    assert "plugin_root" not in scrubbed, f"the loaded plugin's path was published: {scrubbed}"
    assert len(scrubbed["reviewer_provenance"]) == 2, (
        f"the reviewers themselves must survive: {scrubbed['reviewer_provenance']}"
    )
    assert scrubbed["reviewer_provenance"][0]["slot"] == "core-1", "a sibling field was dropped"
    assert scrubbed["focused_evidence_provenance"][0]["memo_sha256"] == "a" * 64, (
        "the hash that tied the memo to its bytes was dropped with the path"
    )
    assert scrubbed["synthesis_provenance"]["shared_images"] == {}, (
        "a figure keyed by its absolute path published that path as a key: "
        f"{scrubbed['synthesis_provenance']['shared_images']}"
    )

    # A path inside this repository is still a path, but it names something a
    # reader has, so it is rewritten rather than dropped.
    inside = local_review.without_local_paths(
        {"source_review_path": str(local_review.REPO / "runs" / "local")}
    )
    assert inside == {"source_review_path": "runs/local"}, (
        f"a repository path should be made relative: {inside}"
    )

    # And the bundle is scanned as a bundle, in every text file, for the two
    # strings that reach a published review only by mistake.
    needles = local_review.local_path_needles()
    assert str(local_review.REPO.resolve()) in needles, "the checkout has to be one of the needles"
    assert home in needles, "the operator's home directory has to be one of the needles"

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        (dest / "provenance.json").write_text(json.dumps({"review": {"id": "p/v1/r1"}}), encoding="utf-8")
        (dest / "summary.md").write_text("# Review Summary\n\nSee /dev/null.\n", encoding="utf-8")
        assert local_review.bundle_local_path_leaks(dest) == [], (
            "a clean bundle must not be reported as leaking"
        )

        # The forms the old scan could not see: a path inside a sentence in the
        # Markdown, a path used as a key, a path in a specialist report copied
        # out of the run, and a path in a nested receipt file.
        (dest / "decision_letter.md").write_text(
            f"The reviewer read {home}/runs/out/core-1.\n", encoding="utf-8"
        )
        (dest / "editor-package.json").write_text(
            json.dumps({"shared_images": {f"{home}/fig1.png": "b" * 64}}), encoding="utf-8"
        )
        (dest / "audit_stats.md").write_text(
            f"Checked the tables in {home}/runs/local.\n", encoding="utf-8"
        )
        nested = dest / "attachments"
        nested.mkdir()
        (nested / "runtime.json").write_text(
            json.dumps({"cwd": f"{home}/Repos"}) + "\n", encoding="utf-8"
        )
        found = local_review.bundle_local_path_leaks(dest)
        assert len(found) == 4, f"every text file in the bundle has to be read: {found}"
        assert any(line.startswith("decision_letter.md") for line in found), (
            f"the rendered Markdown was not scanned: {found}"
        )
        assert any(line.startswith("editor-package.json") for line in found), (
            f"a path used as a key was not seen: {found}"
        )
        assert any(line.startswith("audit_stats.md") for line in found), (
            f"a specialist report copied out of the run was not scanned: {found}"
        )
        assert any(line.startswith("attachments/runtime.json") for line in found), (
            f"a nested receipt was not scanned: {found}"
        )


def check_an_empty_protocol_file_is_not_a_record_of_the_run() -> None:
    """Only `is_file()` was checked, so a zero byte protocol.json passed.

    The guard exists to make publishing require a record of what was asked of
    the engine. A file that parses to nothing answers none of the questions it
    was added to ask, and the fields read out of it then published as empty.
    """
    with tempfile.TemporaryDirectory() as tmp:
        sound = _run_directory(Path(tmp) / "sound")
        local_review.require_complete_run(sound, local_review.read_run(sound))

        broken = {
            "a zero byte file": "",
            "whitespace": "\n  \n",
            "a JSON list": "[]",
            "a JSON null": "null",
            "truncated JSON": '{"provider": "claude-code"',
            "a file with no arm, provider or workflow": "{}",
            "a file naming no provider": '{"arm": "full-two-track"}',
        }
        for why, content in broken.items():
            run = _run_directory(Path(tmp) / why.replace(" ", "-"))
            (run / "protocol.json").write_text(content, encoding="utf-8")
            # The workflow version and the arm are also written in the package
            # and the manifest, so the fixture drops them from there too. What
            # is being tested is that the run has to say what was asked of the
            # engine, not that one field survives in a second file.
            (run / "manifest.json").write_text(
                json.dumps({"paper_id": "paper-abc", "code": dict(CODE)}), encoding="utf-8"
            )
            (run / "editor-package.json").write_text(
                json.dumps({"summary": "A reading.", "findings": []}), encoding="utf-8"
            )
            try:
                local_review.require_complete_run(run, local_review.read_run(run))
            except local_review.CommandError:
                continue
            raise AssertionError(f"a run whose protocol.json is {why} was published")


def check_a_rehearsal_cannot_be_copied_into_place_as_a_review() -> None:
    """A rehearsal bundle moved by hand into docs/reviews passed every check.

    `--human-reviewed yes` without `--publish` wrote a bundle with a true
    attestation and whatever run status it had, and once that folder sat in the
    published tree the schema, the local provenance check, the manifests and the
    attempt ledger all passed it. So the only thing keeping a rehearsal out of
    the record was which directory it had been written to, and a directory can
    be copied.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        destination = local_review.REVIEWS / "2026" / "smoke-rehearsal-fixture" / "v1" / "r1"
        prepared = _prepared(Path(tmp) / "prepared", destination)
        workspace = _workspace(Path(tmp) / "workspace")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = _publish(prepared, run, workspace)
        message = stderr.getvalue()
        assert code == 2, f"an attestation on a rehearsal should be refused, got exit {code}"
        assert "--human-reviewed" in message and "--publish" in message, (
            f"the refusal has to name the pair that cannot be asked for together: {message!r}"
        )
        assert not destination.exists(), f"a bundle was written to {destination}"

    # And the record says so outright, because the schema refuses a true value
    # here. Said in the record rather than implied by the folder, the claim
    # survives the folder being moved.
    with _stub_engine():
        published = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=True, publishing=True)
        )["generator"]["attestation"]
        assert published["rehearsal"] is False, f"a published review is not a rehearsal: {published}"

        rehearsed = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=False, publishing=False)
        )["generator"]["attestation"]
        assert rehearsed["rehearsal"] is True, f"a rehearsal has to say so: {rehearsed}"
        assert rehearsed["human_reviewed_before_merge"] is False, (
            f"a rehearsal cannot carry a reading: {rehearsed}"
        )


def check_a_written_bundle_carries_no_local_path() -> None:
    """Publish a run whose package is full of paths, then read the bundle back.

    Every earlier version of this guard tested a function. The leak was in the
    wiring: the documents were rendered from the unscrubbed package, so a path
    dropped from editor-package.json was printed in decision_letter.md, where
    nothing was looking. This publishes for real, with the field names engine
    0.9 writes, and reads every file of the finished bundle, including the
    specialist reports copied in from the run.

    It also checks what a refusal leaves behind. The guards used to run after
    six files were already in docs/reviews, so a refused publish left most of a
    bundle there, unmanifested and with nothing to say it had been rejected.
    """
    home = str(Path.home().resolve())
    package = dict(
        PACKAGE,
        stages=_stages(TRACKS),
        reviewer_provenance=[
            dict(entry, source_review_path=f"{home}/runs/out/{entry['slot']}/package.json")
            for entry in PACKAGE["reviewer_provenance"]
        ],
        candidate_origins={
            "f-001": {"slot": "spec-stats", "source_review_path": f"{home}/runs/out/spec-stats.json"}
        },
        focused_evidence_provenance=[{"memo_sha256": "c" * 64, "memo_path": f"{home}/memo.md"}],
        synthesis_provenance={"shared_images": {f"{home}/runs/fig1.png": "d" * 64}},
    )

    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run", **{"editor-package.json": package})
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            prepared = _prepared(Path(tmp) / "prepared", destination)
            workspace = _workspace(Path(tmp) / "workspace")

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(prepared, run, workspace, "--publish")
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"

            written = sorted(path.name for path in destination.iterdir())
            assert "manifest.json" in written, f"the bundle was not finished: {written}"
            assert "audit_stats.md" in written, f"the specialist reports were not copied: {written}"
            for path in sorted(destination.rglob("*")):
                if path.is_file():
                    text = path.read_text(encoding="utf-8", errors="replace")
                    assert home not in text, f"{path.name} names the machine that wrote it"
            assert local_review.bundle_local_path_leaks(destination) == [], (
                "the bundle's own scan disagrees with reading it back"
            )

            # The review's own words survived, in the JSON and in the documents
            # rendered from it.
            published = json.loads((destination / "editor-package.json").read_text())
            assert [f["comment"] for f in published["findings"]] == [
                f["comment"] for f in package["findings"]
            ], f"a finding was rewritten or dropped on the way out: {published['findings']}"
            # The fields that carried those paths do not reach the bundle at
            # all. The engine's reading carries the review rather than the
            # plugin server's own bookkeeping, so the class of leak is gone
            # instead of scrubbed field by field, and the scan above is what
            # says nothing that is published carries one.
            for field in (
                "reviewer_provenance",
                "candidate_origins",
                "focused_evidence_provenance",
                "synthesis_provenance",
                "working_directory",
            ):
                assert field not in published, (
                    f"{field} is not part of the engine's reading of a run and "
                    f"must not be published from it: {published.get(field)}"
                )
            letter = (destination / "decision_letter.md").read_text(encoding="utf-8")
            assert "Report the confidence interval." in letter, (
                "the reviewer's own comment did not reach the decision letter"
            )
            round_record = json.loads((destination / local_review.ROUND_RECORD).read_text())
            assert round_record["required_revisions"][0]["finding_uid"] == "f-001", (
                f"the round record lost the finding: {round_record['required_revisions']}"
            )

            # And a path in a field nothing here knows about refuses, leaving
            # the published tree as it found it. The field is inside a finding,
            # because a finding is published whole: a stray key beside the
            # package is dropped with everything else the engine's reading does
            # not carry, and would prove nothing about the guard.
            unknown = reviews / "2026" / "fixture-paper" / "v1" / "r2"
            second_run = _run_directory(
                Path(tmp) / "run-2",
                **{
                    "editor-package.json": dict(
                        package,
                        findings=[
                            dict(package["findings"][0], evidence_log=f"{home}/runs/out/log.txt"),
                            *package["findings"][1:],
                        ],
                    )
                },
            )
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                second = _publish(
                    _prepared(Path(tmp) / "prepared-2", unknown, attempt=2),
                    second_run,
                    workspace,
                    "--publish",
                )
            assert second == 2, f"a path in an unknown field should refuse, got exit {second}"
            assert not unknown.exists(), f"a refused publish left a bundle at {unknown}"
            assert "Nothing was written" in stderr.getvalue(), (
                f"the refusal has to say the tree was left alone: {stderr.getvalue()!r}"
            )


def check_the_locked_engine_release_is_the_one_declared() -> None:
    """The lock has to name the engine release requirements.in asks for.

    It used to assert a version floor, on the grounds that an older release
    ships no engine package and every engine check in CI was installing a wheel
    it could not use. A floor passes a lock one release behind the declared pin,
    which is the same defect at a different version: the checks run against an
    engine whose commands, flags and modules are not the ones this repo is
    written for.

    This reads both files rather than the installed tree, so it fails on a
    laptop with a newer engine checked out and on CI alike.
    """
    root = Path(local_review.__file__).resolve().parents[1]

    def pinned(name: str) -> str:
        pins = [
            line.split("==", 1)[1].split(" ", 1)[0].strip()
            for line in (root / name).read_text(encoding="utf-8").splitlines()
            if line.startswith("peerreviewagents==")
        ]
        assert len(pins) == 1, f"expected one peerreviewagents pin in {name}, found {pins}"
        return pins[0]

    declared, locked = pinned("requirements.in"), pinned("requirements.txt")
    assert declared == locked, (
        f"requirements.in asks for peerreviewagents {declared} and requirements.txt "
        f"locks {locked}, so CI installs an engine this repository is not written for. "
        "Recompile the lock."
    )
    version = tuple(int(part) for part in locked.split(".")[:2])
    assert version >= (0, 9), (
        f"the lock pins peerreviewagents {locked}. The plugin, the commands and the "
        "run folder this repository reads are the 0.9 ones"
    )


# The checks that read a run folder, which in 0.9 means the engine reads it.
# They write a fixture run to disk and hand it to `peerreviewagents.read_run`,
# so they are checks against the real reader, and there is nothing for them to
# run against when the engine is not installed.
ENGINE_BACKED = (
    (check_a_bare_pdf_cannot_be_published, "a review of an unidentified PDF cannot be published"),
    (
        check_provenance_is_read_from_the_run,
        "the provenance record is read from what the run wrote",
    ),
    (
        check_a_run_with_no_manifest_paper_id_is_still_bound,
        "a run that records its paper id outside the manifest is still bound",
    ),
    (
        check_an_unfinished_run_cannot_be_published,
        "a run that did not finish cannot be published, and the cause is named",
    ),
    (
        check_a_finished_run_that_endorses_nothing_is_a_review,
        "a run that finished and raised nothing publishes, a quarantined one does not",
    ),
    (
        check_a_run_on_another_transport_is_not_published,
        "a run on another transport is refused rather than labelled claude-code",
    ),
    (
        check_the_transport_claim_rests_on_the_runs_own_probe,
        "the transport claim is read from the run's own start-up probe",
    ),
    (
        check_a_placeholder_agent_row_is_not_a_reviewer,
        "the harness's placeholder agent rows are not published as reviewers",
    ),
    (
        check_a_stage_that_never_reported_is_not_a_whole_review,
        "a specialist that never reported is refused, not rounded up",
    ),
    (
        check_every_specialist_report_reaches_the_bundle,
        "every specialist track report is copied into the bundle",
    ),
    (
        check_the_run_folder_is_found_whichever_path_is_typed,
        "the run folder is found from the out directory or from review/",
    ),
    (
        check_a_published_record_names_no_local_path,
        "a published record names no path on the operator's disk",
    ),
    (
        check_no_published_file_in_a_bundle_names_a_local_path,
        "the engine's path fields are scrubbed and every bundle file is scanned",
    ),
    (
        check_an_empty_protocol_file_is_not_a_record_of_the_run,
        "an empty protocol.json is not a record of what the engine was asked",
    ),
    (
        check_a_rehearsal_cannot_be_copied_into_place_as_a_review,
        "a rehearsal cannot be copied into place as a published review",
    ),
    (
        check_a_written_bundle_carries_no_local_path,
        "a published bundle, read back off disk, names no local path",
    ),
)


def run_engine_backed_checks() -> None:
    """Run the run-folder checks, or say why they did not run.

    A missing engine is a reason to skip on a laptop and a failure in CI. The
    pipeline job runs this suite on a bare interpreter on purpose, to prove the
    engine-free half needs no engine, and waives the rule by setting
    INSILICO_REQUIRE_ENGINE to 0, which is the only way a skip is reached where
    CI is set.
    """
    if not engine_is_importable():
        if engine_is_required():
            raise AssertionError(
                f"{local_review.ENGINE_PACKAGE}.read_run is not importable, so the "
                f"{len(ENGINE_BACKED)} checks that read a run folder cannot run, and this "
                "environment says they are required. Install the engine from the lock "
                "file, or set INSILICO_REQUIRE_ENGINE=0 to waive it on purpose."
            )
        print(
            f"skip {len(ENGINE_BACKED)} run-folder checks: "
            f"{local_review.ENGINE_PACKAGE}.read_run is not importable here"
        )
        return
    for check_function, label in ENGINE_BACKED:
        check_function()
        print(f"ok  {label}")
