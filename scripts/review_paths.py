"""Locations shared by review planning and publication."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"
RUNS = REPO / "runs"
ROUND_RECORD = "round.json"
# The bundle's own copy of the review, a projection of the engine's own
# issues.json. It keeps the engine's name because it is the same document
# narrowed to what a reader of the review needs, and because the next round is
# handed this file as its prior input: the ids in it are the ids the engine
# minted, so a later round can rule against them and cannot mint one again.
REVIEW_ISSUES = "issues.json"
