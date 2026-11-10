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
            "input": {"kind": "doi", "identifier": PAPER.doi, "sha256": "b" * 64, "bytes": 2048},
            "decision_source": "human_editor",
        },
    }


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
    assert "One model wrote this review" in summary, "the summary must disclose the single reviewer"

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
        run = Path(tmp) / "run"
        run.mkdir()

        code = local_review.main(
            [
                "publish",
                "--prepared",
                str(prepared),
                "--run",
                str(run),
                "--decision",
                "major",
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
    for phrase in ("locally", "no", "paid API key", "human"):
        assert phrase in statement, f"the attestation does not mention {phrase!r}: {statement}"
    assert local_review.GENERATOR_KIND == "local-claude-code", (
        f"the generator kind is pinned by the schema: {local_review.GENERATOR_KIND}"
    )
    assert local_review.TRANSPORT_PROVIDER == "claude-code", (
        f"the transport is pinned by the schema: {local_review.TRANSPORT_PROVIDER}"
    )
    assert "—" not in statement and ";" not in statement, "the attestation is authored prose"
