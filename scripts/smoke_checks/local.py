"""Local generator checks. No engine, no model, no network.

These cover the parts of scripts/local_review.py that can run without
peerreviewagents installed: the refusals, the documents rendered from saved
engine output, and the manifest. The schema side of the same path is checked by
scripts/check_local_provenance.mjs, which needs Node rather than Python.
"""
from __future__ import annotations

import json
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


def _run_directory(root: Path, **overrides) -> Path:
    """A run directory holding the files the engine's CLI really writes.

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
            "synthesis_policy": "debate",
            "synthesis_tool_limit": 12,
            "code": {"engine/reviewer.py": "e" * 64, "engine/api.py": "f" * 64},
        },
        "editor-package.json": {
            "workflow_version": "ensemble-v3",
            "reviewer_count": 2,
            "synthesis_policy": "debate",
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
    workspace_config = run / "execution" / "workspace"
    workspace_config.mkdir(parents=True, exist_ok=True)
    (workspace_config / "tool-config.json").write_text(
        json.dumps({"literature_cutoff": "2026-11-01"}), encoding="utf-8"
    )
    return run


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
    transport_record = local_review.transport_record
    local_review.engine_record = lambda: {"name": "engine", "version": "0.8.0"}
    local_review.transport_record = lambda **_: {"provider": "claude-code", "paid_api_key_used": False}
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
        probe=False,
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
        local_review.transport_record = transport_record
