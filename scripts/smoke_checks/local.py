"""Local generator checks. No engine, no model, no network.

These cover the parts of scripts/local_review.py that can run without
peerreviewagents installed: the refusals, the documents rendered from saved
engine output, and the manifest. The schema side of the same path is checked by
scripts/check_local_provenance.mjs, which needs Node rather than Python.
"""
from __future__ import annotations

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

# Deliberately out of severity order, and one severity the engine does not emit.
FINDINGS = [
    {"severity": "minor", "title": "A typo", "comment": "Fix the spelling.", "block_id": "b7"},
    {
        "severity": "major",
        "title": "The headline effect is unguarded",
        "comment": "Report the confidence interval.",
        "quote": "effects were large",
        "block_id": "b2",
    },
    {"severity": "moderate", "title": "Missing n", "comment": "State the sample size.", "block_id": "b4"},
    {"severity": "catastrophic", "title": "Not a severity the engine emits", "comment": "Ignore."},
]

PACKAGE = {
    "summary": "One careful reading of the manuscript.",
    "findings": FINDINGS,
    "limitations": ["Did not re-run the analysis."],
}


def provenance_fixture() -> dict:
    return {
        "schema_version": local_review.PROVENANCE_SCHEMA,
        "decision": "major",
        "ingest": {"format": "markdown", "tool": "engine import", "text_sha256": "c" * 64, "chars": 40000},
        "generator": {
            "kind": local_review.GENERATOR_KIND,
            "engine": {"name": local_review.ENGINE_PACKAGE, "version": "0.7.0"},
            "model_ids": {"requested": local_review.DEFAULT_MODEL, "observed": [local_review.DEFAULT_MODEL]},
            "input": {
                "kind": "doi",
                "identifier": PAPER.doi,
                "sha256": "b" * 64,
                "bytes": 2048,
                "local_file": False,
            },
            "run": {
                "workflow": "ensemble",
                "workflow_version": "ensemble-v3",
                "reviewers": 2,
                "synthesis_policy": "debate",
                "findings": len(FINDINGS),
                "errors": [],
            },
            "decision_source": "human_editor",
            "attestation": {
                "locally_generated": True,
                "human_reviewed_before_merge": True,
                "editor": "fixture-editor",
                "statement": local_review.ATTESTATION,
            },
        },
    }


def _run_directory(root: Path, *, stage: dict | None = None, **overrides) -> Path:
    """A run directory holding the files the engine's CLI really writes.

    The layout matters, and this fixture used to get it wrong in a way that hid
    a defect. An ensemble run's top level manifest carries the paper id, the
    engine source and the plan. The synthesis policy, the tool budget and the
    validation report live in the stage folder the synthesis ran in, which is
    `debate/` under the default policy, along with that stage's tool config.
    Writing the stage's keys at the top level made a generator that looked
    there pass against a shape no run has.

    `core-artifact.json` is deliberately absent. Only
    peerreviewagents.engine.api.run_review writes one, and the skill drives the
    CLI, so anything that reads provenance out of it reads nothing.
    """
    run = Path(root)
    run.mkdir(parents=True, exist_ok=True)
    files = {
        "protocol.json": {
            "provider": "claude-code",
            "model": "claude-sonnet-5-5",
            "effort": "high",
            "mode": "ensemble",
            "reviewers": 2,
            "version": "3",
        },
        "manifest.json": {
            "paper_id": "paper-abc",
            "review_input_sha256": "d" * 64,
            "plan": {"synthesis_policy": "debate", "independent_reviewers": 2},
            "code": {"engine/reviewer.py": "e" * 64, "engine/api.py": "f" * 64},
        },
        "editor-package.json": {
            "workflow_version": "ensemble-v3",
            "reviewer_count": 2,
            "findings": FINDINGS,
            "summary": PACKAGE["summary"],
        },
        "progress.json": {"status": "complete", "usage": {"calls": 3}},
    }
    files.update(overrides)
    for name, payload in files.items():
        if payload is None:
            continue
        (run / name).write_text(json.dumps(payload), encoding="utf-8")

    stage_dir = run / "debate"
    stage_files = {"synthesis_policy": "debate", "synthesis_tool_limit": 12}
    stage_files.update(stage or {})
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / "manifest.json").write_text(json.dumps(stage_files), encoding="utf-8")
    workspace_config = stage_dir / "execution" / "workspace"
    workspace_config.mkdir(parents=True, exist_ok=True)
    (workspace_config / "tool-config.json").write_text(
        json.dumps({"literature_cutoff": "2026-11-01"}), encoding="utf-8"
    )
    return run


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


def check_the_decision_is_attributed_to_a_person() -> None:
    """The engine recommends no verdict, and the documents must say who did."""
    prov = provenance_fixture()
    findings = local_review.sorted_findings(PACKAGE)
    summary = local_review.render_summary(PAPER, PACKAGE, prov, findings)
    letter = local_review.render_decision_letter(PAPER, PACKAGE, prov, findings)

    assert "human editor" in summary, "the summary must say a person chose the decision"
    assert "does not recommend a verdict" in summary, "the summary must say the engine recommends none"
    assert "editor's" in letter, "the decision letter must attribute the decision to the editor"
    assert "fixture-editor" in summary, "the summary must name the editor who read the run"
    assert "one model agreeing with itself" in summary, (
        "the summary must disclose that a single model produced every pass"
    )

    # The documents are rendered from saved output, so the reviewer's own words
    # have to appear in them verbatim.
    assert PACKAGE["summary"] in summary, "the reviewer's summary was not carried through"
    assert "Report the confidence interval." in letter, "a finding's comment was not carried through"
    assert "> effects were large" in letter, "a quoted manuscript passage was not carried through"

    # Severity decides whether a finding is required or optional. Nothing else
    # does, and in particular the decision does not.
    required = letter.split("## Required changes", 1)[1].split("## Suggestions", 1)[0]
    assert "The headline effect is unguarded" in required, "a major finding must be required"
    assert "Missing n" in required, "a moderate finding must be required"
    assert "A typo" not in required, "a minor finding must not be required"


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


def check_an_unclaimed_review_is_labelled_an_experiment() -> None:
    """One model wrote it, so the page has to say so unless an editor claims it.

    The word matters because Notices.astro and the provenance panel both read
    it, and because "editorial" on a single-model run would overstate what
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
        workspace = Path(tmp) / "workspace"
        workspace.mkdir()

        code = local_review.main(
            [
                "publish",
                "--prepared",
                str(prepared),
                "--run",
                str(run),
                "--workspace",
                str(workspace),
                "--decision",
                "major",
                "--editor",
                "fixture-editor",
                "--human-reviewed",
                "yes",
                "--publish",
                "--offline",
            ]
        )
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
    assert local_review.GENERATOR_KIND == "local-claude-code", (
        f"the generator kind is pinned by the schema: {local_review.GENERATOR_KIND}"
    )
    assert local_review.TRANSPORT_PROVIDER == "claude-code", (
        f"the transport is pinned by the schema: {local_review.TRANSPORT_PROVIDER}"
    )
    assert "—" not in statement and ";" not in statement, "the attestation is authored prose"


def check_a_subscription_login_is_not_a_paid_provider() -> None:
    """A Max subscription reports apiProvider "firstParty", and must be accepted.

    The guard used to refuse any truthy apiProvider, so a real subscription
    login failed the preflight: `fingerprint` exited 2 and the skill could never
    start. The engine accepts None or firstParty, and this path has to accept
    the same set or it refuses accounts the engine would run on. It also has to
    look at loggedIn and authMethod, which it did not.
    """
    record = local_review.transport_from_status(
        {
            "loggedIn": True,
            "authMethod": "claude.ai",
            "apiProvider": "firstParty",
            "subscriptionType": "max",
        }
    )
    assert record["paid_api_key_used"] is False, "a subscription login is not a paid key"
    assert record["auth_method"] == "claude.ai", f"auth method lost: {record}"
    assert record["subscription_type"] == "max", f"subscription type lost: {record}"
    assert record["api_provider"] == "firstParty", f"api provider lost: {record}"
    assert record["billing_policy"], "the record must name the billing policy it ran under"

    # An unset apiProvider is the other shape a subscription login takes.
    assert local_review.transport_from_status(
        {"loggedIn": True, "authMethod": "oauth", "apiProvider": None}
    )["api_provider"] == "firstParty"

    refusals = {
        "not logged in": {"loggedIn": False, "authMethod": "claude.ai"},
        "a key rather than a login": {"loggedIn": True, "authMethod": "apiKey"},
        "a cloud reseller": {"loggedIn": True, "authMethod": "claude.ai", "apiProvider": "bedrock"},
        "a CLI that could not answer": {"error": "claude: command not found"},
    }
    for why, status in refusals.items():
        try:
            local_review.transport_from_status(status)
        except local_review.CommandError:
            continue
        raise AssertionError(f"{why} was accepted as a subscription login: {status}")


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
    assert checker.main() == 0, "the skill's engine commands do not parse"


def check_provenance_is_read_from_the_run() -> None:
    """Nothing in the record may be copied from an intention or a flag.

    The old code read `core-artifact.json`, which the CLI never writes, so the
    workflow, the reviewer count, the literature cutoff and the model were all
    taken from the prepare defaults or the publish flags, and the error list was
    always empty. Each of these comes from a file the run itself wrote.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = _run_directory(Path(tmp) / "run")
        assert not (run_dir / "core-artifact.json").exists(), "the CLI writes no core artifact"

        run = local_review.read_run(run_dir)
        assert run["workflow"] == "ensemble", f"workflow not read from protocol.json: {run}"
        assert run["workflow_version"] == "ensemble-v3", f"workflow version lost: {run}"
        assert run["reviewers"] == 2, f"reviewer count not read from the run: {run}"
        assert run["synthesis_policy"] == "debate", f"synthesis policy not read: {run}"
        assert run["model"] == "claude-sonnet-5-5", f"model not read from protocol.json: {run}"
        assert run["literature_cutoff"] == "2026-11-01", f"cutoff not read from the run: {run}"
        assert run["paper_id"] == "paper-abc", f"paper id not read from the manifest: {run}"
        assert run["status"] == "complete", f"status not read from progress.json: {run}"
        assert run["errors"] == [], f"a clean run should record no errors: {run}"
        assert run["synthesis_tool_limit"] == 12, f"tool budget not read from the stage: {run}"
        assert "directory" not in run, (
            f"a run outside this repository must not be named by its path: {run}"
        )

        fingerprint = local_review.fingerprint_from_manifest(run["engine_source"], "run_manifest")
        assert fingerprint["file_count"] == 2, f"fingerprint miscounted: {fingerprint}"
        assert fingerprint["source"] == "run_manifest", "the fingerprint must say where it came from"
        assert len(fingerprint["sha256"]) == 64, f"not a sha256: {fingerprint}"

        # A value the run did not record is absent, never defaulted.
        bare = local_review.read_run(Path(tmp) / "empty")
        for key in ("workflow", "reviewers", "model", "literature_cutoff", "paper_id"):
            assert key not in bare, f"{key} was invented for a run that recorded nothing: {bare}"

        # And what went wrong is read rather than assumed to be nothing.
        broken = _run_directory(
            Path(tmp) / "broken",
            **{"progress.json": {"status": "failed", "error": "the transport hung up"}},
        )
        (broken / "responses").mkdir()
        (broken / "responses" / "r1-quarantined.json").write_text("{}", encoding="utf-8")
        errors = local_review.read_run(broken)["errors"]
        assert any("hung up" in e for e in errors), f"the recorded error was dropped: {errors}"
        assert any("failed" in e for e in errors), f"a failed run should say so: {errors}"
        assert any("quarantined" in e for e in errors), f"quarantined findings are errors: {errors}"


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


def check_a_substituted_model_is_visible() -> None:
    """The engine records models_observed, a list, in every usage receipt.

    Looking for a scalar `model` key instead found the requested id and called
    it observed, so the drift banner could never fire.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        (run / "usage.jsonl").write_text(
            "\n".join(
                [
                    json.dumps({"models_observed": ["claude-haiku-5-5"], "input_tokens": 10}),
                    "",
                    "not json at all",
                    json.dumps({"models_observed": ["claude-haiku-5-5", "claude-sonnet-5-5"]}),
                ]
            ),
            encoding="utf-8",
        )
        observed = local_review.observed_models(run)
        assert observed == ["claude-haiku-5-5", "claude-sonnet-5-5"], (
            f"the served models were not read from the receipts: {observed}"
        )
        assert "claude-haiku-5-5" in observed, "a substituted model must be visible"

        # Nothing reported is an empty list, not the model that was asked for.
        assert local_review.observed_models(_run_directory(Path(tmp) / "quiet")) == []


def check_the_method_paragraph_describes_the_run_that_happened() -> None:
    """The fixed wording described a workflow nobody ran.

    It said one model, no debate, one reading, while the documented command runs
    an ensemble of two reviewers and the engine's default synthesis is debate.
    """
    ensemble = local_review.method_paragraph(
        {"workflow": "ensemble", "reviewers": 2, "synthesis_policy": "debate"}, "claude-sonnet-5-5"
    )
    assert "2 reviewer passes" in ensemble, f"the reviewer count is not in the text: {ensemble}"
    assert "debate" in ensemble, f"a debate synthesis is not described: {ensemble}"
    assert "One reviewer pass" not in ensemble, "an ensemble run must not be called one reading"

    single = local_review.method_paragraph({"workflow": "single", "reviewers": 1}, "claude-opus-5-5")
    assert "One reviewer pass" in single, f"a single pass is not described: {single}"
    assert "debate" not in single, f"a single pass has no debate: {single}"
    assert "claude-opus-5-5" in single, "the paragraph must name the model that ran"

    unrecorded = local_review.method_paragraph({}, "claude-sonnet-5-5")
    assert "did not record" in unrecorded, (
        f"an unmeasured run must say so rather than claim a shape: {unrecorded}"
    )
    for text in (ensemble, single, unrecorded):
        assert "—" not in text and ";" not in text, "the paragraph is authored prose"


def check_an_attestation_needs_a_named_editor() -> None:
    """`human_reviewed_before_merge: true` was a constant written before anyone acted.

    So was the editor. Both are now operator input with no default, and a run
    nobody has read must say that rather than attest to a reading that did not
    happen.
    """
    engine_record = local_review.engine_record
    local_review.engine_record = lambda: {"name": "engine", "version": "0.8.0"}
    arguments = dict(
        preprint=PAPER,
        prepared={"input": {"kind": "doi", "identifier": PAPER.doi, "sha256": "b" * 64, "bytes": 1, "local_file": False}, "plan_kind": "first review"},
        package=PACKAGE,
        run={"workflow": "ensemble", "reviewers": 2, "errors": []},
        fingerprint={"algorithm": "sha256", "file_count": 2, "sha256": "a" * 64, "source": "run_manifest"},
        decision="major",
        route="v1/r1",
        draft=1,
        attempt=1,
        submitter="",
        submitter_is_author="",
        baseline_eligible=False,
        ingest={},
        observed=["claude-haiku-5-5"],
        requested_model="claude-sonnet-5-5",
        transport={"provider": "claude-code", "paid_api_key_used": False},
        review_id="docs/reviews/2026/fixture/v1/r1",
    )
    try:
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
        assert unread["model_ids"]["substituted"] is True, (
            f"a served model nobody asked for must be flagged: {unread['model_ids']}"
        )
    finally:
        local_review.engine_record = engine_record


def check_the_model_comes_from_the_run_not_the_flag() -> None:
    """A run on opus published a record saying sonnet.

    The model came from `--model`, whose default was sonnet. The skill lets the
    operator run opus, and step five of it passed the default through, so an
    opus run was published as a sonnet run and the summary went on to say every
    pass had used that model.
    """
    # The flag may not carry a default, because a default silently becomes the
    # published claim for a run that asked for something else.
    parsed = local_review.build_parser().parse_args(
        [
            "publish", "--prepared", "p", "--run", "r", "--workspace", "w",
            "--decision", "major", "--editor", "e", "--human-reviewed", "yes",
        ]
    )
    assert not parsed.model, (
        f"--model defaults to {parsed.model!r}, so a run on another model would "
        "be published under that id"
    )

    with tempfile.TemporaryDirectory() as tmp:
        run = local_review.read_run(
            _run_directory(
                Path(tmp) / "opus",
                **{
                    "protocol.json": {
                        "provider": "claude-code",
                        "model": "claude-opus-5-5",
                        "mode": "ensemble",
                        "reviewers": 2,
                        "version": "3",
                    }
                },
            )
        )
        assert run["model"] == "claude-opus-5-5", f"the run's model was not read: {run}"
        assert local_review.resolve_requested_model(run, "") == "claude-opus-5-5", (
            "the record must name the model the run asked for"
        )
        # A dated release of the same model is the same request.
        assert local_review.resolve_requested_model(
            {"model": "claude-opus-5-5-20260929"}, "claude-opus-5-5"
        ) == "claude-opus-5-5-20260929"

        for flag in ("claude-sonnet-5-5", "claude-haiku-5-5"):
            try:
                local_review.resolve_requested_model(run, flag)
            except local_review.CommandError:
                continue
            raise AssertionError(f"--model {flag} silently overrode an opus run")

        # And a run that recorded no model cannot be described at all.
        try:
            local_review.resolve_requested_model({}, "claude-sonnet-5-5")
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a run with no recorded model was given one from a flag")


def check_a_run_with_no_manifest_paper_id_is_still_bound() -> None:
    """Only an ensemble manifest carries the paper id at the top level.

    The independent and panel modes record it in protocol.json and nest the
    protocol inside the manifest, so a run in either mode reported no paper id,
    and the binding check skipped itself rather than failing. A run of paper B
    published under paper A exited zero again, by a different route.
    """
    with tempfile.TemporaryDirectory() as tmp:
        panel = _run_directory(
            Path(tmp) / "panel",
            **{
                "protocol.json": {
                    "provider": "claude-code",
                    "model": "claude-sonnet-5-5",
                    "mode": "panel",
                    "paper_id": "paper-xyz",
                    "reviewers": 3,
                },
                "manifest.json": {
                    "protocol": {"paper_id": "paper-xyz", "model": "claude-sonnet-5-5"},
                    "source_manifest_sha256": "9" * 64,
                    "code": {"engine/reviewer.py": "e" * 64},
                },
            },
        )
        run = local_review.read_run(panel)
        assert run["paper_id"] == "paper-xyz", f"paper id not read from protocol.json: {run}"

        workspace = _workspace(Path(tmp) / "workspace", "paper-abc")
        prepared = {"input": {"sha256": "b" * 64}}
        try:
            local_review.bind_run_to_input(prepared, workspace, run)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a panel run of another paper was bound to this workspace")

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
                **{"progress.json": {"status": "blocked", "error": "Unexpected model returned"}},
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


def check_a_dated_model_id_is_not_a_substitution() -> None:
    """The drift banner fired on a model the engine had already accepted.

    `model_runtime.same_model` treats a dated release and a bracketed variant
    of the requested id as the same request, because those are the forms the
    transport reports back. Comparing the strings exactly instead called every
    dated id a substitution.
    """
    requested = "claude-sonnet-5-5"
    # The record is what the banner reads, so check it end to end first.
    engine_record = local_review.engine_record
    local_review.engine_record = lambda: {"name": "engine", "version": "0.8.0"}
    try:
        arguments = dict(
            preprint=PAPER,
            prepared={
                "input": {"kind": "doi", "identifier": PAPER.doi, "sha256": "b" * 64, "bytes": 1, "local_file": False},
                "plan_kind": "first review",
            },
            package=PACKAGE,
            run={"workflow": "ensemble", "reviewers": 2, "errors": []},
            fingerprint={"algorithm": "sha256", "file_count": 2, "sha256": "a" * 64, "source": "run_manifest"},
            decision="major",
            editor="fixture-editor",
            human_reviewed=True,
            route="v1/r1",
            draft=1,
            attempt=1,
            submitter="",
            submitter_is_author="",
            baseline_eligible=False,
            ingest={},
            requested_model=requested,
            transport={"provider": "claude-code", "paid_api_key_used": False},
            review_id="docs/reviews/2026/fixture/v1/r1",
        )
        dated = local_review.build_provenance(observed=[f"{requested}-20260929"], **arguments)
        assert "substituted" not in dated["generator"]["model_ids"], (
            "a dated release of the requested model was published as a substitution: "
            f"{dated['generator']['model_ids']}"
        )
        swapped = local_review.build_provenance(observed=["claude-haiku-5-5"], **arguments)
        assert swapped["generator"]["model_ids"]["substituted"] is True, (
            f"a genuinely different model was not flagged: {swapped['generator']['model_ids']}"
        )
    finally:
        local_review.engine_record = engine_record

    for same in (requested, f"{requested}-20260929", f"{requested}[1m]"):
        assert local_review.model_matches(same, requested), f"{same} is the requested model"
    for other in ("claude-haiku-5-5", "claude-opus-5-5", "claude-sonnet-5", ""):
        assert not local_review.model_matches(other, requested), f"{other} is a different model"

    assert local_review.substituted_models([f"{requested}-20260929"], requested) == [], (
        "a dated release of the requested model is not a substitution"
    )
    assert local_review.substituted_models(
        [f"{requested}-20260929", "claude-haiku-5-5"], requested
    ) == ["claude-haiku-5-5"], "a genuinely different model has to stay visible"


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
    here = local_review.read_run(local_review.REPO / "scripts")
    assert here.get("directory") == "scripts", (
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

    inside = local_review.REVIEWS / "2026" / "fixture-paper" / "v1" / "r1"
    assert local_review.bundle_identifier(inside) == "docs/reviews/2026/fixture-paper/v1/r1", (
        "a bundle in this repository is named by its path here"
    )
    outside = local_review.bundle_identifier(Path("/tmp/elsewhere/fixture/v1/r1"))
    assert not outside.startswith("/"), f"a bundle id must not be an absolute path: {outside}"
    assert outside == "fixture/v1/r1", f"a bundle id should still identify the bundle: {outside}"


def check_publishing_needs_a_verified_login() -> None:
    """`--publish --offline` wrote login_verified false and validated.

    The record then claimed a review billed to a subscription while saying in
    the same breath that nobody had checked which account it was. The run's own
    billing confirmation is preferred where the engine wrote one, because it
    records the account that paid rather than the one logged in at publish time.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        # A real destination, because the refusal has to come before anything is
        # written rather than after the bundle is already on disk.
        destination = local_review.REVIEWS / "2026" / "smoke-login-fixture" / "v1" / "r1"
        prepared = _prepared(Path(tmp) / "prepared", destination)
        workspace = _workspace(Path(tmp) / "workspace")
        code = _publish(prepared, run, workspace, "--publish", "--offline")
        assert code == 2, f"--publish --offline should be refused, got exit {code}"
        assert not destination.exists(), (
            f"the refusal came after the bundle was written to {destination}"
        )

        # Nothing recorded means no transport record from the run, so the
        # caller falls back to the probe rather than inventing one.
        assert local_review.transport_from_run(run) is None, "an absent confirmation is not a record"

        (run / "billing_confirmation.json").write_text(
            json.dumps(
                {
                    "policy": "claude-subscription-v1",
                    "provider": "claude-code",
                    "checked_at": "2026-11-09T12:00:00+00:00",
                    "auth_method": "claude.ai",
                    "subscription_type": "max",
                    "extra_usage_disabled": True,
                }
            ),
            encoding="utf-8",
        )
        transport = local_review.transport_from_run(run)
        assert transport["login_verified"] is True, f"a checked login is verified: {transport}"
        assert transport["auth_method"] == "claude.ai", f"auth method lost: {transport}"
        assert transport["subscription_type"] == "max", f"subscription type lost: {transport}"
        assert transport["verified_at"].startswith("2026-11-09"), (
            f"the record must say when the login was checked: {transport}"
        )
        assert transport["paid_api_key_used"] is False, "a subscription login is not a paid key"

        (run / "billing_confirmation.json").write_text(
            json.dumps({"auth_method": "apiKey", "policy": "paid"}), encoding="utf-8"
        )
        try:
            local_review.transport_from_run(run)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a run billed to an API key was accepted")


def check_the_synthesis_record_is_read_where_the_engine_writes_it() -> None:
    """The synthesis policy, its tool budget and its validation report.

    All three were looked for at the top of the run directory. The engine
    writes them inside the stage folder the synthesis ran in, so all three were
    always missing and every validation problem the synthesis recorded was
    dropped from the published record.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        assert not (run / "synthesis-validation.json").exists(), (
            "the engine does not write the validation report at the top level"
        )
        record = local_review.read_run(run)
        assert record["synthesis_policy"] == "debate", f"policy not read from the stage: {record}"
        assert record["synthesis_tool_limit"] == 12, f"budget not read from the stage: {record}"

        # A budget of zero is a budget, not a missing value.
        zero = local_review.read_run(
            _run_directory(Path(tmp) / "zero", stage={"synthesis_policy": "debate", "synthesis_tool_limit": 0})
        )
        assert zero["synthesis_tool_limit"] == 0, f"a zero budget was dropped: {zero}"

        (run / "debate" / "synthesis-validation.json").write_text(
            json.dumps({"problems": ["a finding quoted text not in the manuscript"]}),
            encoding="utf-8",
        )
        errors = local_review.read_run(run)["errors"]
        assert any("not in the manuscript" in e for e in errors), (
            f"a validation problem was dropped from the record: {errors}"
        )


def check_a_rehearsal_claims_no_reading() -> None:
    """A rehearsal's own documents said a human editor had read the run.

    `--human-reviewed no` writes the absence into the record, and the summary
    and the decision letter printed the attested wording anyway, so the two
    halves of the same bundle disagreed.
    """
    findings = local_review.sorted_findings(PACKAGE)
    unread = provenance_fixture()
    unread["generator"]["attestation"]["human_reviewed_before_merge"] = False
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


def check_the_locked_engine_release_contains_the_engine() -> None:
    """The pin has to name a release the check above can actually import.

    `peerreviewagents==0.6.0` has no `peerreviewagents.engine` package in it, so
    every engine-dependent check in CI was installing a wheel it could not use.
    This reads the pin rather than the installed tree, so it fails on a laptop
    with a newer engine checked out and on CI alike.
    """
    locked = (Path(local_review.__file__).resolve().parents[1] / "requirements.txt").read_text(
        encoding="utf-8"
    )
    pins = [
        line.split("==", 1)[1].split(" ", 1)[0].strip()
        for line in locked.splitlines()
        if line.startswith("peerreviewagents==")
    ]
    assert len(pins) == 1, f"expected one peerreviewagents pin, found {pins}"
    version = tuple(int(part) for part in pins[0].split(".")[:2])
    assert version >= (0, 7), (
        f"the lock pins peerreviewagents {pins[0]}, which ships no peerreviewagents.engine "
        "package, so every engine check in CI has nothing to import"
    )
