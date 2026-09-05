"""Publish review artifacts, provenance, and integrity manifests."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path

from fetch_preprint import Preprint
from review_paths import ROUND_RECORD
from review_provenance import (
    configuration_record,
    environment_record,
    insilico_version,
    journal_profile_record,
    pipeline_version,
)

# Bundle documents the pipeline emits. This script only decides which files
# travel with a review. how they are labelled, ordered and presented is the
# site's business, and lives in src/lib/corpus.js.
#
# desk_screen.md carries the triage verdict and is written whenever that screen
# ran, pass or reject.
#
# The pipeline also supports an author response letter, and In Silico
# deliberately never sends one. Given a letter asserting that revisions were
# made, the compliance auditor confirmed four of them and invented supporting
# detail, a permutation test "reported in the Fig. 6 legend" that appears
# nowhere in the manuscript, and the editor moved the verdict a full grade on
# the strength of it. Re-running the identical round with no letter attached,
# the same auditor read the manuscript and got all ten items right. Authors
# still get a reply published beside the review. it simply never reaches an
# agent, because an interested party's prose is not evidence and this system
# demonstrably cannot treat it as anything else.
#
# manuscript_stats.md is counts, not opinion: how the PDF converted, how long
# the paper is, how its prose is shaped. It travels because this is an overlay
# journal, the reader has the PDF and the panel had a conversion of it, and
# without these numbers there is no way to check that those were the same
# document. Nothing in it reaches an agent. see the pipeline's ingest/prose.py.
BUNDLE_FILES = [
    "summary.md",
    "decision_letter.md",
    "desk_screen.md",
    "debate_transcript.md",
    # The synthesizer's condensed account of the debate, the version the
    # editor actually read. the transcript above is the full exchange.
    "debate_synthesis.md",
    "journal_recommendations.md",
    "manuscript_stats.md",
]

def panel_scores(state: dict) -> list[dict]:
    """Each referee's score, keeping a null one null.

    A null score means the dimension had nothing to judge in this manuscript.
    a data-analysis review of a paper with no quantitative analysis. It is
    carried through as null and left out of the mean, never filled in: the
    reviewer that had to invent a number reliably invented a generous one, and
    the resulting inflation is invisible once it has become a float.
    """
    out = []
    for report in state.get("reports", []) or []:
        if not isinstance(report, dict):
            continue
        entry = {
            "reviewer": report.get("reviewer", "unknown"),
            "score": report.get("score"),
            "confidence": report.get("confidence"),
        }
        reason = str(report.get("not_applicable_reason") or "").strip()
        if entry["score"] is None and reason:
            entry["not_applicable_reason"] = reason
        out.append(entry)
    return out


def write_bundle(
    preprint: Preprint,
    state: dict,
    run_dir: Path,
    dest: Path,
    submission_id: str,
    submitter: str,
    cost_by_node: dict[str, float] | None = None,
    revision: dict | None = None,
    # Appended rather than inserted: write_bundle is called positionally in
    # several places, and a new parameter in the middle silently rebinds them.
    submitter_is_author: str = "",
    ingest: dict | None = None,
    research: dict[str, list[dict]] | None = None,
    config: dict | None = None,
    review: dict | None = None,
) -> None:
    source_version = insilico_version()
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError(f"refusing to overwrite existing review bundle: {dest}")
    dest.mkdir(parents=True, exist_ok=True)
    cost_by_node = cost_by_node or {}
    revision = revision or {}
    research = research or {}
    review = review or {}

    # Every document is copied, including the ones a desk reject makes
    # byte-identical (it sets decision_letter and desk_screen to the same
    # body). A reader following a direct link should find the file. the site
    # is what decides not to show one text under two headings.
    for name in BUNDLE_FILES:
        src = run_dir / name
        if src.exists():
            shutil.copy2(src, dest / name)

    for src in sorted(run_dir.glob("review_*.md")) + sorted(run_dir.glob("audit_*.md")):
        shutil.copy2(src, dest / src.name)

    # Data rather than a document, but it has to travel with the bundle: it is
    # the thing a later round is pointed at.
    if (run_dir / ROUND_RECORD).exists():
        shutil.copy2(run_dir / ROUND_RECORD, dest / ROUND_RECORD)

    decision = state.get("decision", "unknown")
    scores = panel_scores(state)
    numeric = [s["score"] for s in scores if isinstance(s.get("score"), (int, float))]

    provenance = {
        "schema_version": 2,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "environment": environment_record(),
        "insilico": source_version,
        "configuration": configuration_record(config),
        "journal_profile": journal_profile_record(config),
        "review": review,
        "provider": os.environ.get("REVIEW_PROVIDER", "anthropic"),
        "model": os.environ.get("REVIEW_MODEL", ""),
        # Which model each stage actually ran on. Without these a reader sees
        # only the fallback and cannot tell which agent wrote which report:
        # `models` is keyed by tag (reviewer, audit, debate, synthesis),
        # `agent_models` by the individual agents that override their tag.
        "models": json.loads(os.environ.get("REVIEW_MODELS") or "{}"),
        "agent_models": json.loads(os.environ.get("REVIEW_AGENT_MODELS") or "{}"),
        # Always set from the resolved config before this runs. the literal is
        # only reached by a direct call in a test, and matches peerreview.toml.
        "debate_rounds": int(os.environ.get("REVIEW_DEBATE_ROUNDS", "2")),
        "decision": decision,
        # A desk reject and a panel reject are both `decision: reject` but are
        # not the same editorial act, one is a verdict after ten reports and a
        # debate, the other stops before any of that. Readers and the index
        # both need to tell them apart, and `decision` alone cannot.
        "desk_rejected": bool(state.get("desk_rejected")),
        # The review round, which is NOT the bundle's vN. Re-running a review
        # of the same manuscript under new criteria makes a new bundle at
        # round 1. only a review of a revised draft advances the round. Left
        # separate so the two can never be read off each other.
        "round": int(revision.get("round") or 1),
        "revision": revision,
        # Anyone may submit any public preprint, so a review the authors asked
        # for and one they did not are different things and the page has to
        # say which. Recorded as a claim, because nothing here verifies it.
        "submitter": submitter,
        "submitter_is_author": submitter_is_author,
        # How the manuscript was read, including the selected archive source
        # and validation result. A reader checking a quotation needs to know
        # which representation the panel saw.
        "ingest": ingest or {},
        "screens": json.loads(os.environ.get("REVIEW_SCREENS") or "{}"),
        "panel": scores,
        # The Editor-in-Chief owns the official publication-readiness score.
        # Specialist scores remain visible as advisory evidence below it.
        "readiness_score": state.get("readiness_score"),
        "readiness_breakdown": state.get("readiness_breakdown") or {},
        "contribution_profile": state.get("contribution_profile") or {},
        "score_decision_rationale": state.get("score_decision_rationale") or "",
        # Kept for older bundles and panel-level analysis. This is not the
        # publication-readiness score and does not determine the decision.
        "mean_score": round(sum(numeric) / len(numeric), 2) if numeric else None,
        # How many referees the mean is actually over. A 4.1 across eight
        # referees and a 4.1 across three are different claims, and without
        # both numbers a page showing only the mean cannot tell them apart.
        "scored_count": len(numeric),
        "panel_size": len(scores),
        "total_cost_usd": state.get("total_cost"),
        # Per-agent spend, so cost decisions are measured rather than guessed.
        "cost_by_node": dict(sorted(cost_by_node.items())) if cost_by_node else {},
        # What the referees looked up, and what came back. The site claims
        # novelty and literature search live rather than working from recall.
        # this is the only thing published that can substantiate that. An
        # entry carrying `error` and no tool name is a referee that fell back
        # to reviewing without research tools.
        "research_by_node": dict(sorted(research.items())) if research else {},
        "errors": state.get("errors", []),
        "preprint": preprint.to_dict(),
    }
    # provenance.json is the whole published record of the run. The site
    # renders every page from it, so this script writes data and no markup.
    # Changing how a review looks does not require editing its producer.
    (dest / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")

    manifest = {
        "schema_version": 1,
        "files": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(dest.iterdir())
            if path.is_file() and path.name != "manifest.json"
        },
    }
    (dest / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
