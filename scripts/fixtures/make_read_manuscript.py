#!/usr/bin/env python3
"""Seal a manuscript a model read, with no model, through the engine's own reader.

Every other fixture in this repository writes the account of the Read stage by
hand. `_workspace` in the smoke suite says so in its own docstring: a caller
asking what a bundle publishes about a manuscript a model did read gets an
`ai_read` typed into the manifest after the import, so the pages it names are
not in the fixture PDF and never could be. That is a copy of what this
repository believes the engine writes, and a release that starts writing the
account differently leaves the copy as it was typed until somebody notices.

So this generator earns one. `peerreviewagents.scripted_read` is the engine's
public way to drive the Read stage with the reader's tools called from a script
instead of by a model, which is what makes a read manuscript buildable with no
model, no key and no network. The script here does to a paper everything the
published record has something to say about: it re-reads a piece the converter
labelled as the wrong kind as the two pieces the page prints, folds a piece the
converter emitted beside it in as its debris, describes a figure, puts the two
halves of a split equation back together, and adds a piece and takes it out
again. What it hands back is a manuscript folder in the shape `publish` reads,
with an account of the stage the engine wrote rather than one this repository
believes in.

The PDF is written out by hand by the generator next door, so nothing binary is
committed and nothing has to be installed to rebuild it. The pieces the reader
acts on are supplied to `scripted_read` rather than read off that page: the
converter emits what it emits from a page of plain text, and a fixture that
waited for poppler to split an equation would be a fixture at the mercy of the
converter's version.

Run it as `python scripts/fixtures/make_read_manuscript.py --out <dir>`. It
prints one JSON line naming the folder it sealed, the digest of the PDF it read
and the paper id the engine derived, which is what a caller needs to tie a run
to this manuscript.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from make_engine_rounds import pdf_bytes  # noqa: E402

import peerreviewagents  # noqa: E402

# The paper itself, as a page of plain text. It says enough to be a paper and
# names the equation and the figure the pieces below stand in for, because a
# reader of this fixture should be able to see what the page was supposed to
# print.
PAGE = [
    "A bench measurement of the widget current",
    "",
    "Pat Garrett and A Colleague",
    "",
    "1 Introduction",
    "",
    "The current through each widget was logged every hour for two whole days,",
    "and the totals below are what the instrument reported over that period.",
    "",
    "2 Results",
    "",
    "The cohort totals follow the displayed equation on this page, and each",
    "widget was measured twice under the same clamp and the same scale.",
    "",
    "3 Discussion",
    "",
    "The measurement agrees with the bench reading to within one division,",
    "which is what the instrument manual says to expect of this clamp.",
    "",
    "References",
    "",
    "[1] A Colleague. The widget bench. Journal of Benches, 2024.",
]

# What the converter is taken to have emitted from the displayed material on
# that page, which is where every fact the published record carries about the
# Read stage comes from. The equation arrived with the sentence after it run
# together, its left brace arrived as a heading of its own, and the second
# equation arrived in halves, all three of which are what a converter does to
# displayed mathematics. The two low confidences are what makes the halves
# outstanding work the reader has to answer for before the seal.
CONVERTED = (
    {
        "kind": "equation",
        "text": "",
        "latex": "n total 4 8 The cohort totals follow it.",
        "number": "(1)",
        "section": "2 Results",
        "confidence": 1.0,
    },
    {"kind": "heading", "text": "with {", "section": "2 Results"},
    {
        "kind": "caption",
        "text": "Figure 1: The bench, the instrument and three widgets.",
        "section": "2 Results",
    },
    {
        "kind": "equation",
        "text": "",
        "latex": "I = V",
        "number": "(2)",
        "section": "3 Discussion",
        "confidence": 0.4,
    },
    {
        "kind": "equation",
        "text": "",
        "latex": "/ R",
        "number": "",
        "section": "3 Discussion",
        "confidence": 0.4,
    },
)

# The two pieces the reader reads the first equation as: the equation itself,
# written from the page image, and the sentence that was run together with it,
# which is the authors' own prose and is kept rather than rewritten.
REREAD = (
    {"kind": "equation", "latex": r"\sum_i n_i = 12", "number": "(1)"},
    {"kind": "paragraph", "keep": "The cohort totals follow it."},
)

NOTE = (
    "The displayed equation on page 1 came through with the sentence after it "
    "run together, and its left brace as a heading of its own. The second "
    "equation came through in halves."
)


def seal(out: Path) -> dict:
    """Read the fixture paper with the engine's scripted reader and seal it."""
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / "manuscript.pdf"
    pdf.write_bytes(pdf_bytes([PAGE]))
    # The engine is handed an out directory and writes the two folders a run
    # holds under it, the manuscript and the review, which is the same shape
    # `peerreview review` leaves behind. The manuscript folder is the one a
    # publish is pointed at.
    folder = out / "run"
    with peerreviewagents.scripted_read(pdf, folder, CONVERTED) as read:
        # Every page is looked at, because a reader that sealed a manuscript
        # without viewing the page it rewrote would be a fixture of a stage
        # nobody wants.
        read.view_page(1)
        read.reread_piece(
            read.find("n total 4 8"),
            1,
            [dict(piece) for piece in REREAD],
            absorb=[read.find("with {")],
        )
        read.describe_figure(
            read.find("Figure 1: The bench"),
            1,
            "A photograph of the bench with three widgets in a row.",
        )
        read.merge_equations([read.find("I = V"), read.find("/ R")], 1, r"I = V / R", number="(2)")
        # And a piece added and taken back out, which is the third way a piece
        # leaves the manuscript and the only one of the three that leaves
        # nothing of itself behind in another piece.
        added = read.add_piece(
            read.find("The cohort totals follow it."),
            "caption",
            1,
            text="Table 1: Current by hour.",
        )
        read.withdraw_piece(added.get("piece"))
        read.seal(note=NOTE)
    base = read.base()
    return {
        "out": str(folder),
        "workspace": str(folder / "manuscript"),
        "run": str(folder / "review"),
        "pdf": str(pdf),
        "source_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "paper_id": str(base.manifest.get("paper_id") or ""),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="where to write the PDF and the folder")
    arguments = parser.parse_args(argv)
    print(json.dumps(seal(Path(arguments.out))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
