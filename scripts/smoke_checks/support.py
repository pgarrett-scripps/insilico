"""Write a synthetic review bundle and assert it comes out well-formed.

Hermetic: no network, no API key, no model call.

What this guards is the *data contract* between the pipeline and the site.
run_review.py writes documents and provenance.json. the site reads them and
renders every page. So the failure that matters is a bundle the site cannot
read, a missing field, a score that never reaches provenance, reports that
bleed between versions, not the shape of any particular page. Page rendering
is checked by the site's own build, which CI runs on every PR and which fails
if any published bundle goes unrendered.

    python scripts/smoke_test.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[2]

from fetch_preprint import Preprint  # noqa: E402
from run_review import (  # noqa: E402
    BUNDLE_FILES,
    write_bundle,
)


def provenance_of(bundle: Path) -> dict:
    return json.loads((bundle / "provenance.json").read_text(encoding="utf-8"))


# Titles that have historically broken naive metadata handling.
NASTY_TITLES = [
    'A Study of "Attention": Colons, Quotes & Ampersands',
    "Backslashes \\ and [brackets] in a title",
    "Ünïcödé, emoji 🧬, and a | pipe",
]


def build_fixture(title: str, dest: Path) -> None:
    preprint = Preprint(
        url="https://arxiv.org/abs/0000.00000",
        source="arxiv",
        pdf_url="https://arxiv.org/pdf/0000.00000",
        identifier="0000.00000",
        doi="10.48550/arXiv.0000.00000",
        title=title,
        authors=["Ada Lovelace", "Alan Turing"],
        abstract='An abstract with a colon: quotes "like this" and a | pipe.',
        published="2024-01-01",
    )
    run_dir = Path(tempfile.mkdtemp())
    for name in BUNDLE_FILES:
        (run_dir / name).write_text(f"# {name}\n\nfixture body\n")
    for reviewer in ("methodology", "novelty", "clarity", "rigor"):
        (run_dir / f"review_{reviewer}.md").write_text(f"# {reviewer}\n\nfixture\n")
    # The audit lane writes these. an earlier bundler dropped them silently.
    for auditor in ("methods_completeness", "citation_integrity"):
        (run_dir / f"audit_{auditor}.md").write_text(f"# {auditor}\n\nfixture\n")

    os.environ["REVIEW_MODELS"] = json.dumps(
        {"reviewer": {"model": "claude-haiku-4-5"}, "synthesis": {"model": "claude-opus-5"}}
    )
    os.environ["REVIEW_AGENT_MODELS"] = "{}"
    state = {
        "decision": "major",
        "readiness_score": 78,
        "readiness_breakdown": {
            "scientific_validity": 28,
            "methods_and_evidence": 20,
            "reproducibility_and_reporting": 15,
            "clarity_and_completeness": 15,
        },
        "contribution_profile": {
            "novelty": "moderate",
            "significance": "moderate",
            "usefulness": "high",
        },
        "score_decision_rationale": (
            "The score reflects a sound foundation with unresolved work that "
            "requires major revision before publication."
        ),
        "manuscript_title": title,
        "total_cost": 1.23,
        "errors": [],
        "reports": [
            {"reviewer": r, "score": s, "confidence": 3}
            for r, s in [("methodology", 3), ("novelty", 4), ("clarity", 2), ("rigor", 3)]
        ],
    }
    write_bundle(preprint, state, run_dir, dest, "1", "octocat")
