"""Locations shared by review planning and publication."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"
RUNS = REPO / "runs"
ROUND_RECORD = "round.json"
