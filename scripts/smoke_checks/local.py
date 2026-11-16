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
this interpreter can run them. smoke_test.py skips them on a laptop with no
engine and refuses to skip them in CI. The rest run anywhere.

Everything here is written against the run folder engine 0.10's plugin writes:
`protocol.json`, `manifest.json`, `progress.json`, `runtime.json`,
`startup.json`, `findings.jsonl`, `issues.json` and one `audit_<track>.md` per
specialist reader. The two review files are different things and both are read:
`findings.jsonl` is the ledger of what the readers filed, and `issues.json` is
what the editor agent pooled them into and ranked, which is what a review is
rendered from. The fixtures below copy the shapes of a real 0.10 run rather than
an idealised version of them, including the placeholder agent rows the harness
emits and the absolute paths the plugin server records, because both of those
were defects the generator had to be taught to handle.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fetch_preprint import Preprint  # noqa: E402
import local_review  # noqa: E402
import review_schema  # noqa: E402

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
# The citation lane's workers. They look up references and judge in-text uses
# against the source text, and they write no part of the review, so every
# reviewer count and every published model map here has to leave them out
# while the identity still lists them. Two is enough to prove a map that
# counts reviewers does not grow when the lane does.
CITATION_WORKERS = ("cite-1", "cite-2")
SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"
HAIKU = "claude-haiku-5-5"
FABLE = "claude-fable-5-2"
# The models 0.9 hands out when nothing asks for anything else: the core
# reviewers take this list in order, every specialist runs sonnet, the editor
# runs fable and the recorder haiku. The fixture runs the defaults because a
# panel where every reviewer shared one model is the shape 0.9 exists to stop,
# and a fixture in that shape would let code that still assumes it pass.
REVIEWER_MODELS = (SONNET, OPUS, HAIKU)
SPECIALIST_MODEL = SONNET
EDITOR_MODEL = FABLE
RECORDER_MODEL = HAIKU
# 0.9's own default for a citation worker, which is the cheap model: a worker
# reads a stored abstract and answers one question about one sentence.
CITATION_WORKER_MODEL = HAIKU
CLAUDE_CODE_VERSION = "2.1.322"
STARTED_AT = "2026-11-11T12:00:00+00:00"
WORKFLOW_VERSION = "plugin-two-track-v1"
FINDING_SCHEMA = "review-finding-v4"

# Engine 0.10's issues document, stamped v4 since an issue carries the document
# its rebuttal passage reads in. The engine refuses a v3 document by name, so a
# bundle of the older shape is not half-read: nothing here reads one.
ISSUES_SCHEMA = "review-issues-v4"

# The one document the fixture paper was imported into. An import writes the
# whole paper as `paper.md` and a supplement as `supplement-<name>.md`, and a
# finding names the document it quoted, so even a one-document fixture says
# which.
MAIN_DOCUMENT = local_review.MAIN_DOCUMENT

# The fixture paper, as the pieces an import is given rather than as the file
# one writes: `_workspace` hands these to the engine's own `write_manuscript`,
# which renders them into `paper.md` and writes the map and the manifest beside
# it. Nothing here says where a piece lands or what the file looks like, because
# a fixture that wrote the format itself would be a second copy of it, agreeing
# with this repository's belief about the engine rather than with the engine.
#
# A finding carries no block id any more, it carries a quote and the line that
# quote was read on, so each piece here holds the words the finding that cites
# it quotes. A fixture whose lines did not hold their own quotes would let the
# letter print a line number that means nothing and no check here would see it.
PAPER_PIECES = (
    {
        "kind": "title",
        "section": "Front matter",
        "text": "A manuscript with findings at every severity",
    },
    {
        "kind": "paragraph",
        "section": "Abstract",
        "text": "Across both cohorts the effects were large.",
    },
    {
        "kind": "paragraph",
        "section": "Abstract",
        "text": "A fuller account is given in the appendix, where the interval "
        "is reported in the appendix table.",
    },
    {
        "kind": "paragraph",
        "section": "Methods",
        "text": "Both groups were treated identically and animals were assigned "
        "at random.",
    },
    {
        "kind": "paragraph",
        "section": "Methods",
        "text": "Counts were read from the plates, and the assay was run as "
        "described.",
    },
    {
        "kind": "paragraph",
        "section": "Methods",
        "text": "Per-well counts are available on request.",
    },
    {
        "kind": "paragraph",
        "section": "Introduction",
        "text": "The receptor is blocked by the same compound, as shown "
        "previously.",
    },
    {
        "kind": "paragraph",
        "section": "Results",
        "text": "Figure 2, panel b, gives the counts for the second cohort.",
    },
    {
        "kind": "paragraph",
        "section": "Abstract",
        "text": "The abstract reports n = 48 across both cohorts.",
    },
    {
        "kind": "paragraph",
        "section": "Results",
        "text": "Table 1 totals the same cohorts at n = 46.",
    },
    # The two pieces no converter produced. Engine 0.10 reads a manuscript
    # against its page images before any reviewer sees it, and what the model
    # writes there is carried on the map row as `source`: `ai` for words that
    # are nowhere in the paper, a description of a figure among them, and
    # `ai-reconstructed` for a line that is printed in the paper and that the
    # converter misread, with the converter's own reading kept beside it. A
    # fixture of ten clean paragraphs could not exercise a letter that has to
    # tell the authors whose words they are being asked about.
    {
        "kind": "figure-description",
        "section": "Results",
        "page": 3,
        "source": "ai",
        "text": "Two bars for each cohort, with panel b unlabelled on the "
        "vertical axis.",
    },
    {
        "kind": "equation",
        "section": "Results",
        "page": 3,
        "source": "ai-reconstructed",
        "latex": "n_{total} = 48",
        "number": "1",
        "text": "",
        "original": {"latex": "n total 4 8"},
    },
)

# The lines the fixture findings quote, named rather than typed at each use so
# a line can be moved in one place. These are not the layout: they are what the
# fixture's citations claim, and `_workspace` reads the map the engine wrote and
# fails if a piece landed anywhere else. A release that laid the pieces out
# differently would otherwise leave every citation here pointing at a line of
# text nobody quoted, which is exactly the failure a line number can hide.
HEADLINE_LINE = 3
APPENDIX_LINE = 5
RANDOMISED_LINE = 7
ASSAY_LINE = 9
COUNTS_LINE = 11
CITATION_LINE = 13
PANEL_LINE = 15
ABSTRACT_TOTAL_LINE = 17
TABLE_TOTAL_LINE = 19
DESCRIPTION_LINE = 21
EQUATION_LINE = 23

# One line per piece above, in that order: where the fixture expects the engine
# to have put it. The title is the first line of the file and is quoted by
# nothing.
PIECE_LINES = (
    1,
    HEADLINE_LINE,
    APPENDIX_LINE,
    RANDOMISED_LINE,
    ASSAY_LINE,
    COUNTS_LINE,
    CITATION_LINE,
    PANEL_LINE,
    ABSTRACT_TOTAL_LINE,
    TABLE_TOTAL_LINE,
    DESCRIPTION_LINE,
    EQUATION_LINE,
)

# Each piece's own words against the line the fixture expects it on, which is
# what a citation's offsets are counted in. `_workspace` reads the file the
# engine wrote and fails if a line does not hold these words, so this is a
# claim the engine-backed half of the suite checks rather than a copy of the
# engine's rendering. The title is left out: it is the one piece the engine
# renders as something other than its own text, and nothing cites it.
# The two pieces the engine writes as something other than their own words. A
# figure description carries its prefix into the file, so a machine's account of
# an image never reads as the manuscript's own prose, and an equation is written
# as LaTeX between dollars with its number beside it. Both are claims about the
# engine's rendering rather than copies of it: `_workspace` reads the file the
# engine wrote and fails if the line does not hold these characters.
RENDERED_TEXT = {
    DESCRIPTION_LINE: "Figure description: " + str(PAPER_PIECES[-2]["text"]),
    EQUATION_LINE: "$$ " + str(PAPER_PIECES[-1]["latex"])
    + " \\tag{" + str(PAPER_PIECES[-1]["number"]) + "} $$",
}

PIECE_TEXT = {
    line: RENDERED_TEXT.get(line, str(piece["text"]))
    for line, piece in zip(PIECE_LINES[1:], PAPER_PIECES[1:], strict=True)
}


def _cited(line: int, anchor: str, quote: str | None = None) -> dict:
    """Where a finding's quote reads, as engine 0.10 records a citation.

    The line, the start and end of the quoted characters within it, and the
    manuscript's own characters at those offsets. The offsets are found in the
    fixture's own piece text rather than typed, so a fixture citing words that
    are not on the line it claims fails here instead of printing a letter that
    marks the wrong part of a sentence.

    `anchor` is the manuscript's words and `quote` is what the reviewer typed,
    which the engine allows to differ in case or in how a dash is written. They
    are the same words unless a caller says otherwise.
    """
    text = PIECE_TEXT[line]
    start = text.index(anchor)
    return {
        "line": line,
        "end_line": line,
        "start": start,
        "end": start + len(anchor),
        "anchor_text": anchor,
        "quote": anchor if quote is None else quote,
    }


# The findings ledger, `findings.jsonl`, in the order the readers filed rows.
# Deliberately out of severity order, because nothing downstream may depend on
# the order rows were written in, and one row carries a severity no engine
# emits: a finding is evidence, and the issue over it is what carries the
# severity a reader is shown.
LEDGER = [
    {
        "severity": "minor",
        "title": "A typo",
        "comment": "Fix the spelling.",
        "finding_uid": "f-004",
        "slot": "core-2",
        "track": "citations",
        "basis": "judgement",
        "placement": "anchored",
        "document": MAIN_DOCUMENT,
        "line": CITATION_LINE,
        "end_line": CITATION_LINE,
    },
    {
        "severity": "major",
        "title": "The headline effect is unguarded",
        "comment": "Report the confidence interval.",
        "finding_uid": "f-001",
        "slot": "spec-stats",
        "track": "stats",
        "basis": "computed",
        "basis_reason": "The reported mean and n do not give the stated interval.",
        "counterevidence": "The appendix reports a wider interval for the same effect.",
        "escalate": True,
        "document": MAIN_DOCUMENT,
        **_cited(HEADLINE_LINE, "effects were large"),
        "evidence_lines": [HEADLINE_LINE, APPENDIX_LINE],
    },
    {
        "severity": "moderate",
        "title": "Missing n",
        "comment": "State the sample size.",
        "finding_uid": "f-002",
        "slot": "core-1",
        "track": "methods-reporting",
        "basis": "two-quotes",
        "document": MAIN_DOCUMENT,
        "line": RANDOMISED_LINE,
        "end_line": RANDOMISED_LINE,
    },
    {
        "severity": "catastrophic",
        "title": "Not a severity the engine emits",
        "comment": "Ignore.",
        "finding_uid": "f-003",
    },
    {
        "severity": "moderate",
        "title": "Panel b has no axis label",
        "comment": "Label the y axis.",
        "replacement": "Counts per field of view, mean of three wells.",
        "finding_uid": "f-010",
        "slot": "spec-figures-tables",
        "track": "figures-tables",
        "basis": "two-quotes",
        "document": MAIN_DOCUMENT,
        # Read on the line a model wrote. A reviewer who cannot see the figure
        # reads the description under it, so a finding about a panel is the one
        # a letter is most likely to raise against words no author wrote, and
        # the letter has to say so before an author answers it.
        "line": DESCRIPTION_LINE,
        "end_line": DESCRIPTION_LINE,
    },
    {
        "severity": "minor",
        "title": "Two different totals",
        "comment": "The abstract and table 1 disagree.",
        "finding_uid": "f-011",
        "slot": "core-3",
        "track": "numbers",
        "basis": "two-quotes",
        "escalate": True,
        "document": MAIN_DOCUMENT,
        "line": ABSTRACT_TOTAL_LINE,
        "end_line": ABSTRACT_TOTAL_LINE,
    },
]

# The editor agent's own issues, the thing a review is rendered from in 0.10.
# One of every kind the publish path has to tell apart: a major carrying one
# finding and an escalation, a moderate pooling two findings from two tracks,
# a plain minor, a minor whose finding was escalated and ruled on, a prior
# issue this round ruled fixed and a prior issue it could not verify. The ranks
# are deliberately not the order the rows are written in, because rank is what
# orders the letter and nothing may fall back to file order.
ISSUES = [
    {
        "id": "i08",
        "name": "The sample size is not stated",
        "severity": "moderate",
        "category": "methods-and-reporting",
        "rank": 2,
        "statement": "Two readers could not find the number of animals per group.",
        "members": [
            {
                "finding_uid": "f-002",
                "slot": "core-1",
                "track": "methods-reporting",
                "severity": "moderate",
                "kind": "omission",
                "basis": "two-quotes",
                "escalate": False,
                "title": "Missing n",
                "document": MAIN_DOCUMENT,
                **_cited(RANDOMISED_LINE, "animals were assigned at random"),
                "evidence_lines": [RANDOMISED_LINE],
                "fingerprint": "4" * 64,
            },
            {
                "finding_uid": "f-010",
                "slot": "spec-figures-tables",
                "track": "figures-tables",
                "severity": "moderate",
                "kind": "omission",
                "basis": "two-quotes",
                "escalate": False,
                "title": "Panel b has no axis label",
                "document": MAIN_DOCUMENT,
                # The one member whose quote is not the manuscript's own
                # characters: the reviewer capitalised the panel at the start of
                # its own sentence, which the engine matches and records as the
                # quote beside the words it marked. The letter has to show both
                # and say which is which.
                **_cited(DESCRIPTION_LINE, "panel b", quote="Panel b"),
                "evidence_lines": [DESCRIPTION_LINE],
                "fingerprint": "9" * 64,
            },
        ],
        # How many reviewer slots raised it, counted from the members. The
        # engine publishes the number and not the slot names, so this is an int
        # on every row, zero included.
        "raised_by": 2,
        "rebuttal_document": None,
        "rebuttal_line": None,
        "rebuttal_quote": None,
        "prior_id": None,
        "prior_rank": None,
        "status": "new",
        "status_reason": None,
        "text_unchanged_reason": None,
        "surviving_quotes": [],
        "audits": ["audit_figures-tables.md"],
    },
    {
        "id": "i07",
        "name": "The headline interval is not supported by the reported numbers",
        "severity": "major",
        "category": "statistics-and-inference",
        "rank": 1,
        "statement": "The interval in the abstract cannot be computed from the mean and n given.",
        "members": [
            {
                "finding_uid": "f-001",
                "slot": "spec-stats",
                "track": "stats",
                "severity": "major",
                "kind": "unsupported-claim",
                "basis": "computed",
                "escalate": True,
                "title": "The headline effect is unguarded",
                "document": MAIN_DOCUMENT,
                **_cited(HEADLINE_LINE, "effects were large"),
                "evidence_lines": [HEADLINE_LINE, APPENDIX_LINE],
                "fingerprint": "2" * 64,
            },
        ],
        "raised_by": 1,
        # Null for the paper itself. The engine names a document here only
        # where the passage answering an issue is in a supplement, and the
        # fixture manuscript is one document, so a name here would claim a file
        # the review never read.
        "rebuttal_document": None,
        "rebuttal_line": APPENDIX_LINE,
        "rebuttal_quote": "the interval is reported in the appendix",
        "prior_id": None,
        "prior_rank": None,
        "status": "new",
        "status_reason": None,
        "text_unchanged_reason": None,
        "surviving_quotes": [],
        "audits": ["audit_stats.md"],
    },
    {
        "id": "i09",
        "name": "A reference is cited for the wrong claim",
        "severity": "minor",
        "category": "literature-and-citations",
        "rank": 3,
        "statement": (
            "The citation on that line supports a weaker statement than the sentence makes."
        ),
        "members": [
            {
                "finding_uid": "f-004",
                "slot": "core-2",
                "track": "citations",
                "severity": "minor",
                "kind": "citation",
                "basis": "judgement",
                "escalate": False,
                "title": "A typo",
                "document": MAIN_DOCUMENT,
                **_cited(CITATION_LINE, "as shown previously"),
                "evidence_lines": [CITATION_LINE],
                "fingerprint": "7" * 64,
            },
        ],
        "raised_by": 1,
        "rebuttal_document": None,
        "rebuttal_line": None,
        "rebuttal_quote": None,
        "prior_id": None,
        "prior_rank": None,
        "status": "new",
        "status_reason": None,
        "text_unchanged_reason": None,
        "surviving_quotes": [],
        "audits": [],
    },
    {
        "id": "i10",
        "name": "Two totals for the same cohort",
        "severity": "minor",
        "category": "results-and-numbers",
        "rank": 4,
        "statement": "The abstract and table 1 give different totals.",
        "members": [
            {
                "finding_uid": "f-011",
                "slot": "core-3",
                "track": "numbers",
                "severity": "minor",
                "kind": "inconsistency",
                "basis": "two-quotes",
                "escalate": True,
                "title": "Two different totals",
                "document": MAIN_DOCUMENT,
                **_cited(ABSTRACT_TOTAL_LINE, "n = 48"),
                "evidence_lines": [ABSTRACT_TOTAL_LINE, TABLE_TOTAL_LINE],
                "fingerprint": "1" * 64,
            },
        ],
        "raised_by": 1,
        "rebuttal_document": None,
        "rebuttal_line": None,
        "rebuttal_quote": None,
        "prior_id": None,
        "prior_rank": None,
        "status": "new",
        "status_reason": None,
        "text_unchanged_reason": None,
        "surviving_quotes": [],
        "audits": ["audit_numbers.md"],
    },
    {
        "id": "i05",
        "name": "The earlier round asked for the assay to be named",
        "severity": "moderate",
        "category": "methods-and-reporting",
        "rank": None,
        "statement": "The previous round could not tell which assay the counts came from.",
        "members": [],
        "raised_by": 0,
        "rebuttal_document": None,
        "rebuttal_line": None,
        "rebuttal_quote": None,
        "prior_id": "i05",
        "prior_rank": 2,
        "status": "resolved",
        "status_reason": "The methods now name the assay and its catalogue number.",
        # Ruled fixed although one passage the earlier finding quoted is still
        # in this draft word for word. The engine refuses that ruling unless the
        # editor says why, and it publishes the passage beside the reason, so
        # the letter has to print the quote itself rather than the row.
        "text_unchanged_reason": (
            "The sentence is unchanged, and the assay is named in the one after it."
        ),
        "surviving_quotes": [
            {
                "finding_uid": "f-021",
                "line": ASSAY_LINE,
                "document": MAIN_DOCUMENT,
                "fingerprint": "5" * 64,
                # Found by the words the earlier round quoted, which is the one
                # of the two matches that lets the letter say the sentence still
                # reads as it did.
                "matched_by": "quote",
                "quote": "the assay was run as described",
            },
        ],
        "audits": [],
    },
    {
        "id": "i06",
        "name": "The earlier round asked for the raw counts",
        "severity": "major",
        "category": "reproducibility",
        # A closed-out prior issue carries no rank. It is reported against the
        # round that raised it rather than ordered among this round's asks, so a
        # rank here would collide with the ranks of the issues that have one.
        "rank": None,
        "statement": "The previous round asked for the per-well counts behind figure 2.",
        "members": [],
        "raised_by": 0,
        "rebuttal_document": None,
        "rebuttal_line": None,
        "rebuttal_quote": None,
        "prior_id": "i06",
        "prior_rank": 1,
        "status": "unverified",
        "status_reason": "Nothing in this draft says where the counts are, and no reader found them.",
        "text_unchanged_reason": "The methods section is unchanged from the previous draft.",
        # Rows, not strings. The engine writes each surviving passage as the
        # finding that quoted it, the document and line it was found on in this
        # draft, how it was matched and the quote itself, and a fixture of bare
        # strings let a renderer publish the row as Python text without any
        # check here seeing it. This one was matched by its fingerprint, so the
        # passage is the same passage and the quoted words have moved inside it,
        # which is a different sentence for the letter to write.
        "surviving_quotes": [
            {
                "finding_uid": "f-022",
                "line": COUNTS_LINE,
                "document": MAIN_DOCUMENT,
                "fingerprint": "6" * 64,
                "matched_by": "fingerprint",
                "quote": "counts are available on request",
            },
        ],
        "audits": [],
    },
]

# The manuscript lines behind this round's citations, as `manuscript_citations`
# reads them back off a workspace: a member's offsets with the line they are
# counted in. The engine-backed half builds this from the folder the run was
# bound to, through the engine's own reader; here it is derived from the pieces
# the fixture manuscript is written from, so the letter's marking can be checked
# with no engine installed.
#
# A citation carries where its line came from as well as what it says, because
# the letter has to tell an author quoting a model's description of a figure
# apart from one quoting the paper. That is a field of the map row the engine
# wrote, read back with the line.
PIECE_SOURCE = {
    DESCRIPTION_LINE: {"source": "ai", "page": 3, "kind": "figure-description"},
    EQUATION_LINE: {"source": "ai-reconstructed", "page": 3, "kind": "equation"},
}

CITATIONS = {
    member["finding_uid"]: {
        "document": member["document"],
        "line": member["line"],
        "end_line": member["end_line"],
        "start": member["start"],
        "end": member["end"],
        "line_text": PIECE_TEXT[member["line"]],
        "anchor_text": member["anchor_text"],
        **PIECE_SOURCE.get(member["line"], {"source": "text"}),
    }
    for issue in ISSUES
    for member in issue["members"]
}

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
    "numbers": 1,
    "field": 0,
}

# The previous round's own published issues.json, which is the file this run was
# handed as its prior round. It is a real document on disk in the checks that
# publish, because the publish path now compares what the engine read against
# what the plan named and hashes the file against the bundle that published it:
# a fixture that only claimed a prior round could not exercise either rule.
#
# The round before this one was itself a later round of the same line. It raised
# `i05` and `i06` as new problems, ruled the four items it inherited fixed, and
# so published the six ids its line had spent while carrying only two rows.
PRIOR_ISSUES_DOCUMENT = {
    "schema_version": ISSUES_SCHEMA,
    "issues_source": "editor",
    "issues_source_reason": None,
    "summary": "The round before this one, as it was published.",
    "issues": [
        {
            "id": "i06",
            "name": "The earlier round asked for the raw counts",
            "severity": "major",
            "category": "reproducibility",
            "rank": 1,
            "statement": "The previous round asked for the per-well counts behind figure 2.",
            "members": [
                {
                    "finding_uid": "f-022",
                    "slot": "core-1",
                    "track": "numbers",
                    "severity": "major",
                    "kind": "omission",
                    "basis": "judgement",
                    "escalate": False,
                    "title": "The counts behind figure 2 are not available",
                    "document": MAIN_DOCUMENT,
                    **_cited(COUNTS_LINE, "counts are available on request"),
                    "evidence_lines": [COUNTS_LINE],
                    "fingerprint": "6" * 64,
                },
            ],
            "raised_by": 1,
            "rebuttal_document": None,
            "rebuttal_line": None,
            "rebuttal_quote": None,
            "prior_id": None,
            "prior_rank": None,
            "status": "new",
            "status_reason": None,
            "text_unchanged_reason": None,
            "surviving_quotes": [],
            "audits": ["audit_numbers.md"],
        },
        {
            "id": "i05",
            "name": "The earlier round asked for the assay to be named",
            "severity": "moderate",
            "category": "methods-and-reporting",
            "rank": 2,
            "statement": "The previous round could not tell which assay the counts came from.",
            "members": [
                {
                    "finding_uid": "f-021",
                    "slot": "spec-methods-reporting",
                    "track": "methods-reporting",
                    "severity": "moderate",
                    "kind": "omission",
                    "basis": "judgement",
                    "escalate": False,
                    "title": "The assay is not named",
                    "document": MAIN_DOCUMENT,
                    **_cited(ASSAY_LINE, "the assay was run as described"),
                    "evidence_lines": [ASSAY_LINE],
                    "fingerprint": "5" * 64,
                },
            ],
            "raised_by": 1,
            "rebuttal_document": None,
            "rebuttal_line": None,
            "rebuttal_quote": None,
            "prior_id": None,
            "prior_rank": None,
            "status": "new",
            "status_reason": None,
            "text_unchanged_reason": None,
            "surviving_quotes": [],
            "audits": ["audit_methods-reporting.md"],
        },
    ],
    "counts": {
        "issues": 2,
        "required": 2,
        "suggestions": 0,
        "resolved": 0,
        "unverified": 0,
        "issue_members": 2,
        "by_severity": {"major": 1, "moderate": 1, "minor": 0},
        "by_category": {"reproducibility": 1, "methods-and-reporting": 1},
        "by_status": {
            "new": 2,
            "persisting": 0,
            "regressed": 0,
            "resolved": 0,
            "unverified": 0,
        },
    },
    "prior_round": {
        "file": "issues.json",
        "digest": "d" * 16,
        "issues": 4,
        "tally": {
            "new": 2,
            "persisting": 0,
            "regressed": 0,
            "resolved": 4,
            "unverified": 0,
        },
    },
    "issue_ids_used": ["i01", "i02", "i03", "i04", "i05", "i06"],
    "audits": ["audit_numbers.md", "audit_methods-reporting.md"],
    "limitations": ["Did not re-run the analysis."],
}

# The bytes of that file, written the way the publish path writes every JSON
# file of a bundle, because the two digests below are over these bytes and the
# helper that puts the file on disk writes exactly this text.
PRIOR_ISSUES_TEXT = json.dumps(PRIOR_ISSUES_DOCUMENT, indent=2, ensure_ascii=False) + "\n"
PRIOR_ISSUES_SHA256 = local_review.digest(PRIOR_ISSUES_TEXT.encode())

# What the prior round left this one, as the engine publishes it: the file's
# own name and a digest of its content, never the path it was read from, the
# number of open items it handed over, and this round's tally of rulings over
# them. Two items came in, one was ruled fixed and one could not be verified.
# The digest is the engine's own rule, `sha256` of the file's text cut to
# sixteen characters, computed here over the file the checks write rather than
# typed in, so the publish path's comparison of the two is a real comparison.
PRIOR_ROUND = {
    "file": "issues.json",
    "digest": PRIOR_ISSUES_SHA256[:16],
    "issues": 2,
    "tally": {
        "new": 4,
        "persisting": 0,
        "regressed": 0,
        "resolved": 1,
        "unverified": 1,
    },
}

# The same prior round as protocol.json carries it, which is written at ingest,
# before any ruling exists: the file, its digest and how many items came over,
# and no tally.
PRIOR_ROUND_PROTOCOL = {key: value for key, value in PRIOR_ROUND.items() if key != "tally"}

# Every id this line of rounds has spent, this round's included, which is what
# the engine publishes: the ids its own prior file listed, plus the ids of the
# rows in this round. The four this round minted start above every id the line
# had already used, because the engine mints from `i01` upwards and skips what
# is taken: the earlier rounds of this line spent `i01` to `i06`, so a new
# problem here is `i07`. The retired ids stay in the list because a resolved
# issue is reported once and then dropped from the carry: without them the next
# round would hand `i05` to a different problem.
ISSUE_IDS_USED = [
    "i01", "i02", "i03", "i04", "i05", "i06", "i07", "i08", "i09", "i10",
]

PACKAGE = {
    "schema_version": ISSUES_SCHEMA,
    # `editor` because an editor agent pooled and ranked these findings itself.
    # `server` is the other word, and a run that carries it is one the engine
    # itself reports as not publishable, so no fixture of a publishable run may
    # say it.
    "issues_source": "editor",
    "issues_source_reason": None,
    "summary": "One careful reading of the manuscript.",
    "issues": ISSUES,
    "prior_round": PRIOR_ROUND,
    "issue_ids_used": list(ISSUE_IDS_USED),
    # The specialist audits on disk, by name. Each issue names the ones it
    # rests on and this is the whole set in one place.
    "audits": [f"audit_{track}.md" for track in TRACKS],
    "limitations": ["Did not re-run the analysis."],
    "verdict": VERDICT,
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
    # The engine writes its own tally into the document and recomputes the same
    # one when it reads the run back, so these numbers are written out here
    # rather than derived: a check compares them against the reader's own, and
    # a fixture that quietly derived them could not disagree with it.
    "counts": {
        # Four live issues: the resolved one and the unverified one are reported
        # against the round that raised them and are not this round's asks.
        "issues": 4,
        "required": 2,
        "suggestions": 2,
        "resolved": 1,
        "unverified": 1,
        "issue_members": 5,
        "by_severity": {"major": 1, "moderate": 1, "minor": 2},
        "by_category": {
            "methods-and-reporting": 1,
            "statistics-and-inference": 1,
            "literature-and-citations": 1,
            "results-and-numbers": 1,
        },
        "by_status": {
            "new": 4,
            "persisting": 0,
            "regressed": 0,
            "resolved": 1,
            "unverified": 1,
        },
    },
    "findings_by_track": FINDINGS_BY_TRACK,
    "reviewer_count": 3,
    # Each row carries both model facts, as 0.9 writes them: the model the slot
    # was asked to run and the one it reported running. The three core reviewers
    # are three different models on purpose, which is the whole reason the
    # engine stopped recording one model for the panel.
    "reviewer_provenance": [
        {
            "slot": "core-1",
            "track": "core",
            "model": REVIEWER_MODELS[0],
            "assigned_model": REVIEWER_MODELS[0],
            "attempt": 1,
            "tool_calls": 12,
            "findings": 3,
            "none_found": False,
        },
        {
            "slot": "core-2",
            "track": "core",
            "model": REVIEWER_MODELS[1],
            "assigned_model": REVIEWER_MODELS[1],
            "attempt": 2,
            "tool_calls": 14,
            "findings": 2,
            "none_found": False,
        },
        {
            "slot": "core-3",
            "track": "core",
            "model": REVIEWER_MODELS[2],
            "assigned_model": REVIEWER_MODELS[2],
            "attempt": 1,
            "tool_calls": 9,
            "findings": 0,
            "none_found": True,
        },
    ],
    "arm": "full-two-track",
    # `editor` or `none`, the two words the engine writes: `editor` when an
    # editor agent pooled the findings and `none` when nothing pooled them. This
    # fixture used to say `editor-pooled`, which no engine writes, so every
    # check that read it was reading a shape the publish path never meets.
    "synthesis_policy": "editor",
    "workflow_version": WORKFLOW_VERSION,
    "finding_schema_version": FINDING_SCHEMA,
    "review_guard_status": "clean",
    "findings_delivered": 6,
    "findings_submitted": 6,
    "quarantined_findings_count": 0,
    "quarantined_findings": [],
}

# What `review_package` hands the renderers for the run `_run_directory`
# writes: the issues document with the ledger beside it. The two are separate
# files in the run and separate things in the review, and they are one mapping
# here because an issue member carries the evidence fields while the reviewer's
# own words stay on the finding, so the letter needs both to render one issue.
READING = dict(PACKAGE, findings=LEDGER)


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

    Counted from the ledger rather than written out, so the expectation cannot
    drift away from the fixture's own findings. A finding with no track at all,
    which the engine does emit, counts towards nothing.
    """
    counts: dict[str, int] = {}
    for finding in LEDGER:
        track = str(finding.get("track") or "")
        if track:
            counts[track] = counts.get(track, 0) + 1
    return counts


COUNTED_BY_TRACK = _counted_by_track()


def _assigned_model(slot: str) -> str:
    """The model the run asked one slot to use, by 0.9's own rule.

    Core reviewer `i` takes `REVIEWER_MODELS[(i - 1) % len(REVIEWER_MODELS)]`,
    every specialist takes one model, and the editor, the recorder and each
    citation worker take one each. This is the plan, so every slot has one,
    the recorder included.
    """
    if slot == "editor":
        return EDITOR_MODEL
    if slot == "recorder":
        return RECORDER_MODEL
    if slot.startswith("spec-"):
        return SPECIALIST_MODEL
    # Before the trailing-integer rule below, because `cite-1` would otherwise
    # be read as the first entry of the reviewer list.
    if slot.startswith("cite-"):
        return CITATION_WORKER_MODEL
    index = int(slot.rsplit("-", 1)[1])
    return REVIEWER_MODELS[(index - 1) % len(REVIEWER_MODELS)]


def _slot_model(slot: str) -> str | None:
    """The model one slot reported running, as protocol.json carries it.

    This is an observation rather than the plan: the server writes what the
    agent itself said it ran on, which is why the recorder, the one slot that
    reported nothing, has no model here. The harness saw it anyway, which is
    how the record ends up naming a model for a slot the protocol left blank.
    """
    if slot == "recorder":
        return None
    return _assigned_model(slot)


def _protocol_agents(tracks: tuple[str, ...]) -> dict:
    """One entry per agent slot, as the plugin server writes them.

    `model` and `assigned_model` are two facts: what the slot reported running
    and what the run asked it to run. The fixture keeps them equal everywhere
    they are both known, because a substitution is a run the engine refuses to
    publish, and the checks that want one build it from here.
    """
    agents: dict[str, dict] = {}
    for slot in CORE_SLOTS:
        agents[slot] = {
            "role": "core-reviewer",
            "track": "core",
            "attempt": 2 if slot == "core-2" else 1,
            "tool_calls": 12,
            "model": _slot_model(slot),
            "assigned_model": _assigned_model(slot),
            "allowed_tools": ["Read", "Grep"],
        }
    for track in tracks:
        agents[f"spec-{track}"] = {
            "role": "specialist",
            "track": track,
            "attempt": 1,
            "tool_calls": 7,
            "model": _slot_model(f"spec-{track}"),
            "assigned_model": _assigned_model(f"spec-{track}"),
            "allowed_tools": ["Read", "Grep"],
        }
    agents["editor"] = {
        "role": "editor",
        "attempt": 1,
        "tool_calls": 4,
        "model": _slot_model("editor"),
        "assigned_model": _assigned_model("editor"),
        "allowed_tools": ["Read"],
    }
    agents["recorder"] = {
        "role": "recorder",
        "attempt": 1,
        "tool_calls": 2,
        "model": None,
        "assigned_model": _assigned_model("recorder"),
        "allowed_tools": ["Read"],
    }
    # The citation workers sit in the same map as the readers, with a role and
    # a track of their own. They are agents of the run and the identity has to
    # name them, and they wrote no finding, so anything that counts reviewers
    # or publishes a panel has to tell them apart by role rather than by being
    # given a shorter list.
    for slot in CITATION_WORKERS:
        agents[slot] = {
            "role": "citation-worker",
            "track": "citation-worker",
            "attempt": 1,
            "tool_calls": 5,
            "model": _slot_model(slot),
            "assigned_model": _assigned_model(slot),
            "allowed_tools": ["Read"],
        }
    return agents


def _tool_calls(tracks: tuple[str, ...]) -> dict[str, int]:
    """Tool calls per agent slot, which is the shape `progress.json` carries.

    The plugin server writes `{slot: agent.calls}` and the run total beside it
    as `tool_calls_total`. This fixture used to write a single integer as
    `tool_calls`, a shape no engine produces, so anything here that read it was
    reading a run that could not exist. Derived from the protocol agents so the
    slots are the ones the protocol declares and the total is their sum.
    """
    return {slot: int(agent["tool_calls"]) for slot, agent in _protocol_agents(tracks).items()}


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
                "model": _assigned_model(slot),
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
                "model": SPECIALIST_MODEL,
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
            "model": EDITOR_MODEL,
            "tokens": 32000,
            "toolCalls": 4,
            "durationMs": 120000,
        }
    )
    # The recorder reported no model of its own, so protocol.json carries none
    # for it and the harness is the only thing that saw one. The published map
    # has a model in it for a slot the protocol left blank, and it is an
    # observation rather than the recorder's share of the plan.
    rows.append(
        {
            "label": "ingest",
            "state": "complete",
            "attempt": 1,
            "agentType": "pra:recorder",
            "model": RECORDER_MODEL,
            "tokens": 9000,
            "toolCalls": 2,
            "durationMs": 30000,
        }
    )
    for slot in CITATION_WORKERS:
        rows.append(
            {
                "label": slot,
                "state": "complete",
                "attempt": 1,
                "agentType": "pra:citation-worker",
                "model": CITATION_WORKER_MODEL,
                "tokens": 6000,
                "toolCalls": 5,
                "durationMs": 40000,
            }
        )
    return rows


def _expected_models() -> dict[str, str]:
    """The observed model map the fixture run has to produce, slot by slot."""
    models = {slot: _assigned_model(slot) for slot in CORE_SLOTS}
    models.update({f"spec-{track}": SPECIALIST_MODEL for track in TRACKS})
    models["editor"] = EDITOR_MODEL
    # Keyed by the slot, not by the label the harness ran it under. The run's
    # own record calls that agent `ingest`, and 0.9 merges it into the
    # protocol's `recorder` slot, which is what a reader can match to a report.
    models["recorder"] = RECORDER_MODEL
    return models


def _expected_assigned() -> dict[str, str]:
    """The plan the fixture run has to publish beside it, slot by slot.

    Every slot is in here, the recorder included, because the plan is written
    before anything runs. The observed map can be shorter, and the gap between
    the two is what `models_unverified` names.
    """
    slots = [*CORE_SLOTS, *(f"spec-{track}" for track in TRACKS), "editor", "recorder"]
    return {slot: _assigned_model(slot) for slot in slots}


def _planned_models() -> dict[str, str]:
    """Every slot the run assigned a model to, citation workers included.

    This is what `protocol.json` and the manifest plan carry, and it is wider
    than the map a record publishes: 0.9 assigns a worker a model like any
    other slot, and the published panel is the agents that wrote the review.
    The two maps differ by exactly the workers, which is the point of having
    both here.
    """
    planned = _expected_assigned()
    planned.update({slot: _assigned_model(slot) for slot in CITATION_WORKERS})
    return planned


EXPECTED_MODEL_PHRASE = (
    f"{SONNET} (7 agents), {HAIKU} (2 agents), {FABLE} (1 agent), {OPUS} (1 agent)"
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
        # Both strings are the engine's own. `summary` is copied verbatim out of
        # the arm table (`ARMS['full-two-track']['summary']`) and `execution` is
        # one fixed sentence the manifest writer always writes. The fixture used
        # to paraphrase both, so a generator could have invented any wording
        # here and still passed.
        "summary": "N core reviewers plus all six specialists, then the editor",
        # The plan carries the models too, and the manifest is where `read_run`
        # looks for them when the protocol has none. Workers and all: the plan
        # is what the run assigned, and the record decides who is on the panel.
        "models": _planned_models(),
        "citation_workers": list(CITATION_WORKERS),
        "reviewer_models": list(REVIEWER_MODELS),
        "execution": (
            "Claude Code plugin workflow; agents in parallel, server-owned ledger."
        ),
    }


def _protocol(**overrides) -> dict:
    """What the engine was asked for, as `write_protocol` records it."""
    record = {
        "provider": "claude-code",
        # `model` is a sentence rather than an id, because no run picks one
        # model for the whole panel and every existing consumer of this file
        # reads a string here. It is `models.describe` of the plan, and the
        # per-slot answer is in `models` beside it. `effort` is still the one
        # fixed sentence the server always writes. The fixture used to say
        # `high`, a value no engine writes.
        "model": ", ".join(
            dict.fromkeys(_planned_models().values())
        ) + " (per slot; see models)",
        "effort": "per-agent, pinned in the plugin agent files",
        "models": _planned_models(),
        "reviewer_models": list(REVIEWER_MODELS),
        # The engine writes the arm here, twice: `mode` and `arm` are the
        # same word. The fixture used to say `plugin`, which the engine
        # never writes, and the publish path reads `mode` to say which arm
        # ran, so the one value a reader of the page sees was a word no run
        # could have produced.
        "mode": "full-two-track",
        "arm": "full-two-track",
        "reviewers": 3,
        "paper_id": "paper-abc",
        "literature_cutoff": None,
        "version": WORKFLOW_VERSION,
        "finding_schema_version": FINDING_SCHEMA,
        # No `body_finding_limit`. That field capped the findings a letter body
        # could carry, and engine 0.10 writes no letter body: the editor's
        # issues are what the review asks for, so the protocol records the issue
        # schema and how many issues one submission may carry instead.
        "issues_schema_version": ISSUES_SCHEMA,
        "issue_batch_limit": 12,
        "prior_round_issues": dict(PRIOR_ROUND_PROTOCOL),
        "agents": _protocol_agents(TRACKS),
        "plan": _plan(TRACKS),
    }
    record.update(overrides)
    return record


def _progress(**overrides) -> dict:
    """The stage ledger the plugin server keeps as the run goes."""
    record = {
        "status": "complete",
        "error": "",
        "reviewers": 3,
        "arm": "full-two-track",
        "stages": _stages(TRACKS),
        "findings_delivered": 6,
        # Both counts, as the engine writes them: what the reviewers submitted
        # and what survived pooling into the ledger the editor read. They are
        # equal here because nothing was merged away, and they are two fields
        # because a run where they differ has to be able to say so.
        "findings_submitted": 6,
        "quarantined_findings_count": 0,
        "review_guard_status": "clean",
        "tool_calls": _tool_calls(TRACKS),
        "tool_calls_total": sum(_tool_calls(TRACKS).values()),
        "started": STARTED_AT,
        "updated": "2026-11-11T12:31:00+00:00",
    }
    record.update(overrides)
    return record


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
            # Claude Code's own `system`/`init` event, copied through by the
            # engine's probe: each plugin is an object with a name and the path
            # it was loaded from, never a bare string. The path is why this
            # matters here — it is a machine path in a copied artifact, and the
            # publish path has to see it.
            "plugins": [{"name": "pra", "path": "/plugins/pra"}],
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

    The probe and its problems come from the engine's reading of the run, and
    the stamp does not: `read_run` carries no time for the probe, so the
    publish path reads that one field out of `startup.json` itself and passes
    it in. The fixture passes the same stamp the folder holds, so a record
    built here is the record the command builds from the same run.
    """
    return local_review.transport_record(
        provider="claude-code",
        runtime=_runtime(TRACKS),
        startup=_startup(),
        verified_at=STARTED_AT,
    )


def _citation_lane(run: Path) -> bool:
    """Write the citation lane a 0.9 run writes, under `citations/`.

    `scripts/fixtures/make_citation_ledger.py` holds the rows of a tiny
    synthetic manuscript as JSON lines, in the shape `docs/INTEGRATIONS.md`
    documents, along with the stage record, the lookups cache and the two empty
    lock sentinels a real lane leaves beside them.

    False means the engine is not importable, which is the bare suite. The rows
    need no engine to write, but their tallies are read back off them by the
    engine's own reader, and a lane nothing can count is a lane no record can
    carry, so the fixture leaves it out rather than typing the numbers in.
    """
    if not engine_is_importable():
        return False
    from fixtures import make_citation_ledger

    run = Path(run)
    # A run writes its ledger once. Some checks build the same run folder twice
    # over, and writing it again is harmless only because the rows are the same
    # rows: a ledger is append only, and a second pass must not double it.
    if not (run / CITATION_LEDGER_PATH).exists():
        make_citation_ledger.fill(run, slot=CITATION_WORKERS[0])
    return True


def _citation_counts(run: Path) -> dict:
    """What the engine's own reader counts off the ledger in this run folder.

    Through `read_citation_ledger`, which wants a run folder rather than a bare
    directory, so this is called once the run's own files are on disk.
    """
    from fixtures import make_citation_ledger

    return make_citation_ledger.counts(Path(run))


CITATION_LEDGER_PATH = "citations/ledger.jsonl"

# What the fixture ledger holds, counted by the engine's own reader. Written
# out rather than computed because the bare suite has no engine to run the
# writer with, and `check_the_citation_counts_are_the_engines_own` fills a
# ledger with the engine and compares every number here against it, so nothing
# in this block can drift away from what 0.9 would really report.
#
# One reference of each state the table can hold: one resolved against
# Crossref, one whose printed DOI no agency registered, one neither index
# lists, and one whose lookups never answered. Four in-text uses, three judged
# and one left owed, so the lane is reported unfinished and the review is
# published anyway.
#
# 0.9.1 tallies five more states off those same rows: references the lookups
# were never asked about, printed DOIs the reader found damaged and the ones it
# repaired, and references carrying an abstract or a passage of full text. The
# rows did not change, so every number the older reader reported is the number
# it reports now.
CITATION_COUNTS = {
    "references": 4,
    "resolved": 1,
    "not_found": 1,
    "not_located": 1,
    "could_not_check": 1,
    "no_lookup": 0,
    "damaged_dois": 0,
    "repaired_dois": 0,
    "candidates": 0,
    "errors": 0,
    "unresolved": 0,
    "mismatched": 0,
    "retracted": 0,
    "with_source_text": 1,
    "with_abstract": 1,
    "with_full_text": 0,
    "uses": 4,
    "uses_unmatched": 0,
    "uses_judged": 3,
    "supported": 1,
    "partly_supported": 0,
    "not_supported": 0,
    "cannot_tell": 2,
    "uses_unjudged": 1,
    "lookups": 15,
    "unreadable_rows": 0,
}

# The engine's own one-sentence summary of the lane. The record carries it word
# for word and the published page never prints it: it bundles the three states
# that are not findings about a reference in with the one that is, and it
# carries a count of uses the citations specialist did not confirm.
CITATION_SUMMARY = (
    "4 references: 1 resolved, 0 with a metadata mismatch, 1 with an unregistered DOI, "
    "1 not located in either index, 1 could not be checked, 0 never looked up, "
    "0 retracted. 4 in-text uses, 3 judged (1 supported, 0 partly, 0 not supported, "
    "2 cannot tell)."
)

# What the engine says the lane did not settle. These are carried through word
# for word, because the engine wrote each of them to stop a reader turning a
# lookup that failed into a claim about the work.
CITATION_PROBLEMS = [
    "1 reference(s) could not be checked because the lookups did not answer, "
    "which says nothing about whether they exist",
    "1 reference(s) are listed in neither Crossref nor Europe PMC, and much of "
    "the literature is in neither, so this is weak evidence about the references "
    "themselves",
    "1 of 4 in-text citation uses were never judged against the source",
]


def _citation_record() -> dict:
    """The citations block of a published record, as citation_record writes one."""
    return {
        "enabled": True,
        "complete": False,
        "stages_done": False,
        "counts": dict(CITATION_COUNTS),
        "problems": list(CITATION_PROBLEMS),
        "summary": CITATION_SUMMARY,
        "workers": list(CITATION_WORKERS),
    }


def _run_directory(
    root: Path,
    *,
    report_tracks: tuple[str, ...] | None = None,
    citations: bool = True,
    **overrides,
) -> Path:
    """A run directory holding the files engine 0.10's plugin really writes.

    One flat folder: what was asked of the engine in `protocol.json`, the paper
    id and the hash of every plugin and engine file loaded in `manifest.json`,
    the final status and the stage ledger in `progress.json`, what the harness
    observed in `runtime.json`, the start-up probe in `startup.json`, every
    finding as it was filed in `findings.jsonl`, the review itself in
    `issues.json`, and one `audit_<track>.md` per specialist reader.

    The two review files are both here because they are two different things. A
    row in the ledger is one reader's finding, and an issue is the editor
    agent's own problem statement over one or more of those rows. The engine
    reads the ledger to say how much was found and the issues to say what the
    review asks for, and a fixture with only one of them could not tell a
    missing review from a review of nothing.

    The manifest carries the absolute manuscript path and plugin root the plugin
    server writes into it. They are here on purpose: nothing in the published
    record may name them, and a fixture without them would let a generator that
    copied them through pass.

    An override value of None leaves that file out, which is how the refusals
    for a run missing one of them are tested. `findings.jsonl` is overridden
    with a list of rows rather than a mapping, because it is one JSON document
    per line and not one document.

    `citations=False` writes the run without a citation ledger while the plan
    still declares the lane, which is the shape the engine reports as a lane
    that checked nothing.
    """
    run = Path(root)
    run.mkdir(parents=True, exist_ok=True)
    lane = _citation_lane(run) if citations else False
    home = str(Path.home().resolve())
    rows = overrides.pop("findings.jsonl", LEDGER)
    files = {
        "protocol.json": _protocol(),
        "progress.json": _progress(),
        "runtime.json": _runtime(TRACKS),
        "startup.json": _startup(),
        "issues.json": dict(PACKAGE, stages=_stages(TRACKS)),
    }
    files.update({
        name: payload for name, payload in overrides.items() if name != "manifest.json"
    })
    if rows is not None:
        (run / "findings.jsonl").write_text(
            "".join(f"{json.dumps(row)}\n" for row in rows), encoding="utf-8"
        )
    for name, payload in files.items():
        if payload is None:
            continue
        (run / name).write_text(json.dumps(payload), encoding="utf-8")

    # The manifest goes last because it repeats the ledger's tallies, and those
    # are read off the run by the engine's own reader rather than typed in here.
    # That reader wants a run folder, and the files above are what make this one.
    totals = _citation_counts(run) if lane else None
    manifest = overrides.get("manifest.json", {
        "paper_id": "paper-abc",
        "source_sha256": "b" * 64,
        "pdf": f"{home}/runs/local/paper.pdf",
        "code": dict(CODE),
        "workflow_version": WORKFLOW_VERSION,
        "finding_schema_version": FINDING_SCHEMA,
        "claude_code_version": CLAUDE_CODE_VERSION,
        "plugin_root": f"{home}/Repos/PeerReviewAgents/plugins/pra",
        "plan": _plan(TRACKS),
        # The manifest names the ledger and repeats its tallies. Relative,
        # because the engine writes it relative to the run folder, and the
        # record drops it either way: the bundle carries no ledger file,
        # so a path in a published record points at nothing.
        "citation_ledger": CITATION_LEDGER_PATH if totals else None,
        "citations": dict(totals) if totals else None,
    })
    if manifest is not None:
        (run / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

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


def _workspace(
    root: Path,
    paper_id: str = "paper-abc",
    pieces: list | None = None,
    source_sha256: str = "b" * 64,
    read: dict | None = None,
) -> Path:
    """The folder the engine's import command writes, as publish needs it.

    Written by the engine's own `write_manuscript`, from the pieces above: it
    renders `paper.md`, writes `map.json` over it and `manifest.json` digesting
    all of it, and hands back the manifest it wrote. Nothing about the format is
    repeated here. A fixture that laid out the file itself could only agree with
    what this repository believes the engine writes, and the publish path reads
    this folder through the engine's `verify_workspace`, so the one thing worth
    publishing against is a folder the engine made.

    The leak scan reads the rendered Markdown, because a hit that appears in the
    paper is the paper's own text rather than this machine's, and a check of the
    allowance has to be able to say what the paper said.

    Three things are asked of this fixture that an import cannot be asked for,
    and they are done to the manifest after the call, which is safe because the
    manifest is the one file not digested in its own `files` map:

    * a workspace carrying no `paper_id` at all, which no import writes, since
      the engine derives one from the text when it is given none;
    * `source.sha256`, which is passed through rather than patched: the digest of
      a PDF nobody has, so the run binding has something to agree with;
    * `read`, an account of the Read stage. `write_manuscript` always records
      `read: false`, because reading a manuscript means a model looking at the
      page images and no model runs in this suite. A caller that passes one is
      asking what a bundle publishes about a manuscript a model read, and the
      answer is written into the manifest here rather than earned, which is why
      the pages it names are not in the fixture PDF and never could be.
    """
    why = "the fixture manuscript cannot be written"
    write_manuscript = local_review.engine_public("write_manuscript", why)
    workspace = Path(root)
    workspace.mkdir(parents=True, exist_ok=True)
    manifest = write_manuscript(
        workspace,
        [dict(piece) for piece in (PAPER_PIECES if pieces is None else pieces)],
        paper_id=paper_id or None,
        parser="fixture",
        source={
            "file": "original/original.pdf",
            "sha256": source_sha256,
            "pages": 1,
        },
    )
    if pieces is None:
        # Where the engine actually put each piece, against where every
        # citation in this fixture says it is. A release that put a blank line
        # somewhere else would leave the quotes intact and every line number
        # wrong, and a wrong line number reads exactly like a right one.
        rows = json.loads((workspace / "map.json").read_text(encoding="utf-8"))
        landed = tuple(int(row["lines"][0]) for row in rows)
        assert landed == PIECE_LINES, (
            f"the engine rendered the fixture's pieces onto lines {landed}, and "
            f"this fixture's findings cite {PIECE_LINES}"
        )
        # And what those lines hold, because a citation's offsets are counted in
        # the characters of the rendered line. A release that folded a piece
        # differently would leave each quote on the line that claims it and
        # every offset into it a column or two out, which is the kind of wrong
        # that reads as right until an author looks at the marked words.
        written = (workspace / MAIN_DOCUMENT).read_text(encoding="utf-8").split("\n")
        for number, text in PIECE_TEXT.items():
            assert written[number - 1] == text, (
                f"the engine rendered line {number} as {written[number - 1]!r} and "
                f"this fixture counts its citations' offsets in {text!r}"
            )
    patched = {k: v for k, v in manifest.items() if k != "paper_id" or paper_id}
    if read is not None:
        patched["ai_read"] = read
        pages = [row["page"] for row in read.get("lost_pages") or [] if row.get("page")]
        if pages:
            # Where the import itself records a page it got nothing from, beside
            # the reader's own account of transcribing it. The two are written
            # separately by the engine and a bundle publishes both.
            patched["known_gaps"] = dict(patched.get("known_gaps") or {}, converter_pages=pages)
    if patched != manifest:
        (workspace / "manifest.json").write_text(json.dumps(patched), encoding="utf-8")
    return workspace


def _prior_bundle(root: Path) -> Path:
    """The previous round's bundle, as far as this round reads it.

    Two files: the items that round published, and the manifest that bundle
    hashed its own files into. Both are needed, because the publish path checks
    the file it was handed against the digest the engine recorded and against
    the digest the bundle published, and the second of those lives here.
    """
    bundle = Path(root)
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / local_review.REVIEW_ISSUES).write_text(PRIOR_ISSUES_TEXT, encoding="utf-8")
    (bundle / "manifest.json").write_text(
        json.dumps(
            {
                "bundle": "r1",
                "files": {local_review.REVIEW_ISSUES: PRIOR_ISSUES_SHA256},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return bundle


def _prepared(root: Path, destination: Path, **overrides) -> Path:
    """What prepare writes, as publish reads it.

    A revision round by default, because the fixture run is one: its package
    rules on two items of an earlier round. The plan therefore names that
    round's published items, and the file is written beside the plan so the
    publish path can hash it. A check of a first round passes `round=1` and
    `prior_issues=""`, which is what prepare writes when there is no round
    before this one.
    """
    prepared = Path(root)
    prepared.mkdir(parents=True, exist_ok=True)
    record = {
        "publishable": True,
        "draft": 3,
        "attempt": 1,
        "plan_kind": "revision round",
        "round": 3,
        "prior_issues": str(_prior_bundle(prepared / "prior-round") / local_review.REVIEW_ISSUES),
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
def _stub_engine(version: str = "0.10.0"):
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
        # The engine's own two answers about the plan: the ordered list the core
        # reviewers were drawn from, and the slots it assigned a model and
        # nothing observed. Empty here, which is what a fully observed run says.
        "reviewer_models": list(REVIEWER_MODELS),
        "models_unverified": [],
        "paper_id": "paper-abc",
        "claude_code_version": CLAUDE_CODE_VERSION,
        "status": "complete",
        # The engine's own answer, which is the publish gate in 0.9. A record
        # carries it rather than this repository's reading of the same files.
        "publishable": True,
        "findings_source": "issues",
        "review_guard_status": "clean",
        "findings_delivered": 6,
        "findings_submitted": 6,
        "quarantined_findings_count": 0,
        "escalated_count": 2,
        "findings_by_track": dict(COUNTED_BY_TRACK),
        "completeness": _stage_record(),
        # No `findings` count and no `appendix_findings`. Those two described a
        # letter body and an appendix, and engine 0.10 writes neither: the
        # ledger's own total is `findings_delivered` above, and what the review
        # asks for is counted in issues below.
        # The issue counts a record carries, counted off the fixture's own
        # issues so the expectation cannot drift from them. `issues` is the live
        # set: the prior issue ruled fixed and the one left unverified are
        # counted under their own names and are not this round's asks.
        "issues": len(local_review.live_issues(PACKAGE)),
        "required": len(local_review.required_issues(PACKAGE)),
        "suggestions": len(local_review.suggestion_issues(PACKAGE)),
        "resolved": len(local_review.resolved_issues(PACKAGE)),
        "unverified": len(local_review.unverified_issues(PACKAGE)),
        "issues_source": "editor",
        "issues_schema_version": ISSUES_SCHEMA,
        # Two of the live issues rest on a finding a reader escalated: the major
        # one and one of the suggestions.
        "escalated_in_bundle": 2,
        "errors": [],
        # The citation lane, as the engine reports it. It is beside `errors`
        # rather than in it: a lane with rows still owed is a lane that has
        # more to do, and 0.9 publishes the review regardless.
        "citations": _citation_record(),
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
        "assigned_models": _expected_assigned(),
        # The second round of this manuscript, against the file the first round
        # published. The prior block is the engine's own: the file's name, a
        # digest of it and how many items came over, and no path.
        "round": 2,
        "prior_round": dict(PRIOR_ROUND),
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
                {
                    "slot": "core-1",
                    "role": "core-reviewer",
                    "model": SONNET,
                    "assigned_model": SONNET,
                    "findings": 3,
                },
                {
                    "slot": "editor",
                    "role": "editor",
                    "model": EDITOR_MODEL,
                    "assigned_model": EDITOR_MODEL,
                },
                {
                    "slot": "ingest",
                    "agent_type": "pra:recorder",
                    "model": RECORDER_MODEL,
                    "assigned_model": RECORDER_MODEL,
                },
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
        # What `ingest_record` reads off an imported workspace, in the shape a
        # published record has to carry. Typed here because this builds a record
        # with no workspace behind it. `check_a_bundle_says_which_lines_a_model
        # _wrote` publishes for real off a folder the engine wrote, and that is
        # what keeps this shape honest rather than merely passing the schema.
        ingest=dict(
            INGEST_READ,
            format="markdown",
            tool="peerreviewagents import_paper",
        ),
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


def _schema_run_statuses() -> list[str]:
    """The run statuses the published schema accepts, read from the schema.

    Read rather than written out here, so a run this file calls publishable
    cannot be one `npm run check:schema` would then reject, and so the two
    cannot drift apart silently.

    There are two of them in 0.9, because the engine finishes a review with no
    findings in it as `complete-without-findings` and that is a review when the
    guards took nothing. Which of the two a bundle may carry is not a question
    the status answers, so the schema accepts both and the publish gate is the
    engine's `publishable` flag.
    """
    run = _schema()["properties"]["generator"]["properties"]["run"]
    return list(run["properties"]["status"]["enum"])


def _schema_verified_by() -> str:
    """The one transport evidence the published schema accepts."""
    generator = _schema()["properties"]["generator"]["properties"]
    return generator["transport"]["properties"]["verified_by"]["const"]


def _schema_run_requires() -> list[str]:
    return list(
        _schema()["properties"]["generator"]["properties"]["run"].get("required") or []
    )


def _schema_guard_verdicts() -> list[str]:
    """The guard verdicts the published schema accepts, read from the schema.

    The engine writes `clean` or `quarantined` and nothing else. Reading the
    enum here rather than repeating it keeps a fixture from publishing a verdict
    `npm run check:schema` would reject at the site build instead.
    """
    run = _schema()["properties"]["generator"]["properties"]["run"]["properties"]
    return list(run["review_guard_status"]["enum"])


def _provenance_component_fields() -> str:
    """The provenance component's source, so a published field is not orphaned.

    The page is Astro and is rendered by the site build, not by this suite. What
    this check can still prove offline is that the component reads the field the
    bundle carries, so a record that counts held-back findings is not published
    into a page that never mentions them.
    """
    page = Path(__file__).resolve().parents[2] / "src" / "components" / "Provenance.astro"
    return page.read_text(encoding="utf-8")


def check_the_issues_are_split_by_severity_and_ordered_by_rank() -> None:
    """What the authors must do comes from severity, and its order from rank.

    Two rules, and neither of them may fall back to the order the rows happen
    to sit in. Major and moderate issues are the required changes, minor ones
    are the suggestions, and the editor agent's own rank decides what comes
    first. A prior issue this round closed out is in neither list: it is
    reported against the round that raised it.
    """
    required = local_review.required_issues(PACKAGE)
    suggestions = local_review.suggestion_issues(PACKAGE)
    assert [i["id"] for i in required] == ["i07", "i08"], (
        f"the required changes are not the major and moderate issues in rank order: "
        f"{[i['id'] for i in required]}"
    )
    assert [i["id"] for i in suggestions] == ["i09", "i10"], (
        f"the suggestions are not the minor issues in rank order: "
        f"{[i['id'] for i in suggestions]}"
    )
    assert [i["rank"] for i in [*required, *suggestions]] == [1, 2, 3, 4], (
        "the issues are not in the editor agent's own rank order"
    )

    counts = local_review.severity_counts(required)
    assert counts == {"major": 1, "moderate": 1, "minor": 0}, f"severity miscounted: {counts}"

    # The closed-out items are counted and reported under their own names, and
    # an unverified item is not a resolved one.
    assert [i["id"] for i in local_review.resolved_issues(PACKAGE)] == ["i05"], (
        "the issue the editor agent ruled fixed was not found"
    )
    assert [i["id"] for i in local_review.unverified_issues(PACKAGE)] == ["i06"], (
        "the issue left unverified was not found"
    )
    assert [i["id"] for i in local_review.live_issues(PACKAGE)] == ["i07", "i08", "i09", "i10"], (
        "a closed-out prior issue was counted among this round's own issues"
    )

    # An escalation is a property of the findings an issue was raised from, so
    # it survives pooling: the major one and one of the suggestions rest on a
    # finding a reader escalated, and the other two do not.
    escalated = local_review.escalated_issues(local_review.live_issues(PACKAGE))
    assert [i["id"] for i in escalated] == ["i07", "i10"], (
        f"the escalated issues were not found: {[i['id'] for i in escalated]}"
    )


def check_the_decision_is_attributed_to_a_person() -> None:
    """The engine recommends no verdict, and the documents must say who did."""
    prov = provenance_fixture()
    summary = local_review.render_summary(PAPER, READING, prov)
    letter = local_review.render_decision_letter(PAPER, READING, prov)

    assert "human editor" in summary, "the summary must say a person chose the decision"
    assert "recommends no verdict" in summary, "the summary must say the engine recommends none"
    assert "editor's" in letter, "the decision letter must attribute the decision to the editor"
    assert "fixture-editor" in summary, "the summary must name the editor who read the run"
    assert "agents sharing a model are not independent corroboration of one another" in summary, (
        "the summary must disclose that agents on one model do not corroborate each other"
    )
    assert "3 core reviewers" in summary, f"the panel is not described: {summary}"
    assert "6 specialist readers" in summary, f"the specialists are not described: {summary}"
    assert "**Required changes:** 2 (1 major, 1 moderate)" in summary, (
        f"the required changes are not counted on the summary: {summary}"
    )
    assert "**Suggestions:** 2" in summary, "the suggestions are not counted"
    assert "**Escalated by a reviewer:** 2" in summary, "the escalations are not counted"
    assert "Findings raised per track" in summary, "the per-track counts were not published"

    # The documents are rendered from saved output, so the reviewers' and the
    # editor agent's own words have to appear in them verbatim.
    assert PACKAGE["summary"] in summary, "the editor agent's summary was not carried through"
    assert "The interval in the abstract cannot be computed" in letter, (
        "an issue's own statement was not carried through"
    )
    assert "Report the confidence interval." in letter, (
        "a finding's comment was not carried through"
    )
    assert "> effects were large" in letter, "a quoted manuscript passage was not carried through"
    assert "The reported mean and n do not give the stated interval." in letter, (
        "the basis the reviewer recorded was not carried through"
    )
    assert "the interval is reported in the appendix" in letter, (
        "the passage the editor agent read as an answer to the issue was dropped"
    )
    assert "audit_stats.md" in letter, "the specialist audit an issue rests on was not named"
    assert "Rulings on escalated findings" in letter, (
        "the editor agent's rulings were not published"
    )
    assert "rounding step" in letter, "a ruling that went against the reviewer was dropped"

    # Severity decides whether an issue is a required change or a suggestion.
    # Nothing else does, and in particular the decision does not.
    required = letter.split("## Required changes", 1)[1].split("## Suggestions", 1)[0]
    assert "The headline interval is not supported" in required, "a major issue must be required"
    assert "The sample size is not stated" in required, "a moderate issue must be required"
    assert "A reference is cited for the wrong claim" not in required, (
        "a minor issue must not be a required change"
    )

    # The id is published as the engine minted it, because that is the id a
    # later round rules against.
    assert "[`i07`]" in required, f"the engine's own issue id was not published: {required}"
    assert "`i09`" in letter.split("## Suggestions", 1)[1], (
        "a suggestion was published without its id"
    )

    # An issue pooled from two readers prints both findings under it, with the
    # slot that raised each.
    pooled = required.split("The sample size is not stated", 1)[1]
    assert "Raised from 2 findings" in pooled, f"the findings behind an issue were dropped: {pooled}"
    assert "Panel b has no axis label" in pooled and "Missing n" in pooled, (
        "a member finding was dropped from the issue it was pooled into"
    )


def check_the_letter_marks_a_quote_in_the_line_it_reads_on() -> None:
    """The authors are shown the words, where they stand, not a line number.

    Engine 0.10 records the start and end of a quote within the line it reads
    on. The letter prints that line and marks those characters beneath it, in a
    monospaced block, because the offsets are counted in the characters of the
    converted line and a caret only means anything under the character it sits
    on.

    Two things the marking has to get right, and both are here. A quote the
    reviewer wrote differently from the manuscript — a capital at the start of
    their sentence — is marked as the manuscript's own characters, and the
    letter says that is what the marks are, so an author reading the quotation
    above and the marks below is not left to guess which is the paper's. And a
    finding the engine placed nowhere has nothing to mark, so it keeps the line
    it was cited at and gains no block of carets under a line it never read.
    """
    prov = provenance_fixture()
    letter = local_review.render_decision_letter(PAPER, READING, prov, citations=CITATIONS)

    # The line of the manuscript, and the carets under the quoted words.
    headline = PIECE_TEXT[HEADLINE_LINE]
    start = headline.index("effects were large")
    assert f"  {headline}" in letter, (
        f"the line a finding reads on is not printed: {letter}"
    )
    assert f"  {' ' * start}{'^' * len('effects were large')}" in letter, (
        f"the quoted words are not marked where they stand: {letter}"
    )
    assert f"Line {HEADLINE_LINE} of the manuscript" in letter, (
        f"the marked line is not named: {letter}"
    )

    # The reviewer's quotation and the manuscript's own characters, told apart
    # where the two differ.
    assert "> Panel b" in letter, "the reviewer's own quotation was not printed"
    panel = PIECE_TEXT[DESCRIPTION_LINE]
    column = panel.index("panel b")
    assert f"  {' ' * column}{'^' * len('panel b')}" in letter, (
        f"a quote the reviewer wrote differently was not marked: {letter}"
    )
    assert "The marked characters are the manuscript's own" in letter, (
        f"the letter marks characters it never says are the paper's: {letter}"
    )

    # That quote reads on a line a model wrote, and the letter has to say so.
    # A figure description is an account of an image and appears nowhere in the
    # paper, so an author told to answer a finding against it is being asked
    # about words they never wrote, and the answer to that is not a revision.
    assert "These are not the authors' words" in letter, (
        f"a quote from a line a model wrote is printed as the paper's: {letter}"
    )
    assert "page 3 of the original" in letter, (
        f"the page the model read that line off was dropped: {letter}"
    )

    # The other thing a model writes, for the same reason and with a different
    # answer: a line that is printed in the paper and that the converter
    # misread, which the model rewrote from the page image. The authors' own
    # line, in a model's transcription of it.
    repaired = local_review._written_by_a_model(
        {"source": "ai-reconstructed", "page": 3}
    )
    assert any("the converter misread" in row for row in repaired), (
        f"a repaired line is not told apart from one the authors never wrote: {repaired}"
    )
    assert local_review._written_by_a_model({"source": "text", "page": 3}) == [], (
        "a line of the converter's own text was reported as a model's"
    )
    unknown = local_review._written_by_a_model({"source": "ai-translated"})
    assert any("`ai-translated`" in row for row in unknown), (
        f"a source this release does not know was passed over in silence: {unknown}"
    )

    # The passage answering an issue can be in a supplement, and a line number
    # with no file beside it sends the authors to the wrong file.
    supplement = dict(
        READING,
        issues=[dict(ISSUES[1], rebuttal_document="supplement-methods.md")],
    )
    elsewhere = local_review.render_decision_letter(
        PAPER, supplement, prov, citations=CITATIONS
    )
    assert "in supplement-methods.md" in elsewhere, (
        f"a rebuttal quoted from a supplement is reported as the paper's: {elsewhere}"
    )
    assert "in supplement-methods.md" not in letter, (
        "a rebuttal read in the paper itself names a second file"
    )

    # A citation the engine placed nowhere, and a letter rendered with no lines
    # read back at all: both print the finding and mark nothing.
    unplaced = {
        uid: dict(row, line=None, start=None, end=None)
        for uid, row in CITATIONS.items()
    }
    for rendered in (
        local_review.render_decision_letter(PAPER, READING, prov, citations=unplaced),
        local_review.render_decision_letter(PAPER, READING, prov),
    ):
        assert "> effects were large" in rendered, (
            "a finding with no placed quote lost the words the reviewer quoted"
        )
        marks = [row for row in rendered.splitlines() if row.strip() and set(row.strip()) == {"^"}]
        assert not marks, f"an unplaced quote was marked in a line anyway: {marks}"


def check_a_minor_issue_is_never_a_required_revision() -> None:
    """round.json drives the revision workflow, so the split has to hold there too."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        prov = provenance_fixture()
        local_review.write_round_record(dest, PAPER, prov, READING)
        record = json.loads((dest / local_review.ROUND_RECORD).read_text())

    assert record["decision"] == "major", f"decision lost: {record.get('decision')!r}"
    assert record["round"] == 2, f"the round number was dropped: {record.get('round')!r}"
    assert [item["id"] for item in record["required_revisions"]] == ["i07", "i08"], (
        f"expected the major and the moderate in rank order: {record['required_revisions']}"
    )
    assert [item["id"] for item in record["minor_suggestions"]] == ["i09", "i10"], (
        f"minor issues mangled: {record['minor_suggestions']}"
    )
    assert record["desk_rejected"] is False, "a local run has no desk screen to fail"
    assert record["manuscript_file_sha256"] == "b" * 64, "the reviewed bytes were not recorded"

    # Every item is named by the id the engine minted, and that id is what the
    # next round rules against, so no entry may be nameless and no two may
    # share a name.
    ids = [item["id"] for item in record["required_revisions"]]
    ids += [item["id"] for item in record["minor_suggestions"]]
    assert all(ids) and len(set(ids)) == len(ids), f"the issue ids are not unique: {ids}"
    assert record["issue_ids_used"] == ISSUE_IDS_USED, (
        f"the spent ids were not carried: {record['issue_ids_used']}"
    )

    # A revision round has to say which findings an item was raised from, and
    # the engine's own uids are what travel with it, along with the slots that
    # raised it and whether a reader escalated it.
    first = record["required_revisions"][0]
    assert first["rank"] == 1, f"the editor agent's rank was dropped: {first}"
    assert first["finding_uids"] == ["f-001"], f"the engine's own uids were dropped: {first}"
    assert first["raised_by"] == ["spec-stats"], f"the slot was dropped: {first}"
    assert first["escalated"] is True, f"the escalation was dropped: {first}"
    assert first["category"] == "statistics-and-inference", f"the category was dropped: {first}"
    assert record["required_revisions"][1]["finding_uids"] == ["f-002", "f-010"], (
        "a pooled issue did not carry both findings it was raised from"
    )
    assert all(item["finding_uids"] for item in record["required_revisions"]), (
        f"a required revision rests on no finding: {record['required_revisions']}"
    )

    # What this round said about the round before it, in two lists that are
    # never added together, and a carry that counts an unverified item as open.
    closed = record["closed_issues"]
    assert [item["id"] for item in closed["resolved"]] == ["i05"], f"resolved lost: {closed}"
    assert [item["id"] for item in closed["unverified"]] == ["i06"], f"unverified lost: {closed}"
    assert closed["resolved"][0]["prior_rank"] == 2, "the prior rank was dropped"
    assert "name the assay" in closed["resolved"][0]["status_reason"], (
        "the editor agent's reason for ruling an item fixed was dropped"
    )
    # The quotes the engine still found in this draft, as it writes them: a row
    # per passage, naming the finding that quoted it, the document and line it
    # was found on in this draft and how it was matched. The record used to
    # carry them for the unverified list alone, so a reader of round.json could
    # not see what a ruling of `resolved` was made against, and the reason the
    # editor gave for ruling it fixed anyway was nowhere in the record at all.
    assert closed["unverified"][0]["surviving_quotes"] == [
        {
            "finding_uid": "f-022",
            "document": MAIN_DOCUMENT,
            "line": COUNTS_LINE,
            "fingerprint": "6" * 64,
            "matched_by": "fingerprint",
            "quote": "counts are available on request",
        },
    ], f"the quotes still standing in the manuscript were dropped: {closed['unverified'][0]}"
    assert "unchanged from the previous draft" in (
        closed["unverified"][0]["text_unchanged_reason"] or ""
    ), f"the reason the text is unchanged was dropped: {closed['unverified'][0]}"
    resolved_row = closed["resolved"][0]
    assert resolved_row["surviving_quotes"] == [
        {
            "finding_uid": "f-021",
            "document": MAIN_DOCUMENT,
            "line": ASSAY_LINE,
            "fingerprint": "5" * 64,
            "matched_by": "quote",
            "quote": "the assay was run as described",
        },
    ], f"a resolved item's surviving quotes were dropped: {resolved_row}"
    assert "named in the one after it" in (resolved_row["text_unchanged_reason"] or ""), (
        f"the editor's reason for ruling it fixed anyway was dropped: {resolved_row}"
    )
    assert record["carried_forward"] == ["i08", "i07", "i09", "i10", "i06"], (
        f"the carry is not this round's items plus what was left open: {record['carried_forward']}"
    )
    assert "i05" not in record["carried_forward"], (
        "an item the editor agent ruled fixed was carried into the next round"
    )


def check_a_severity_this_release_cannot_sort_is_refused() -> None:
    """A word that would put an issue in neither list stops the publish.

    The letter has two lists and they are built from severity: major and
    moderate are the required changes, minor are the suggestions. The engine's
    vocabulary can grow, and an issue carrying a word this release has no place
    for would appear in neither list, which is an issue the editor agent raised
    and the authors never see. So it is refused and the word is named, which is
    a bug report rather than a quietly shorter letter.

    A closed-out issue is the deliberate exception. It is reported against the
    round that raised it rather than sorted into either list, so a severity on
    one of those rows is nothing this release has to sort.
    """
    strange = dict(
        ISSUES[1],
        id="i11",
        severity="blocking",
        rank=5,
    )
    package = dict(PACKAGE, issues=[*ISSUES, strange], issue_ids_used=[*ISSUE_IDS_USED, "i11"])
    try:
        local_review.assert_publishable_issues(package)
    except local_review.CommandError as refusal:
        message = str(refusal)
        assert "i11" in message and "blocking" in message, (
            f"the refusal has to name the issue and the word: {message}"
        )
        assert "major" in message and "minor" in message, (
            f"the refusal has to say which words it does sort: {message}"
        )
    else:
        raise AssertionError("an issue this release cannot sort was accepted for publication")

    # The same word on a closed-out row is not a problem, because that row is
    # reported against the round that raised it and sorted into neither list.
    closed = dict(ISSUES[5], severity="blocking")
    local_review.assert_publishable_issues(
        dict(PACKAGE, issues=[*ISSUES[:5], closed])
    )

    # And the fixture itself has to pass, or the refusal above proves nothing.
    local_review.assert_publishable_issues(PACKAGE)


def check_a_surviving_quote_is_printed_as_the_authors_own_words() -> None:
    """A passage that still reads the same is printed, never the row holding it.

    The engine records a surviving passage as a row: the finding it came from,
    the document and the line it was found on in this draft, how it was matched
    and the quoted words. The letter printed the row itself, so the authors were
    shown a line of Python where their own sentence belonged. Nothing caught it
    because the fixture carried bare strings, which the old renderer printed
    unchanged, so the check restated the fixture rather than testing the
    renderer.

    Both closed lists carry such a row now, a ruled-fixed item and an unverified
    one, because the two are rendered by the same entry and a fixture that
    exercised one proved nothing about the other. The two are matched
    differently as well: one was found by the words the earlier round quoted and
    one by the digest of the passage they were read in, and the letter has to
    say which, because "the wording has moved inside the passage" is not "the
    sentence is unchanged".
    """
    letter = local_review.render_decision_letter(PAPER, READING, provenance_fixture())
    assert "## The previous round's items" in letter, (
        f"the round's rulings are not in the letter: {letter}"
    )
    prior = letter.split("## The previous round's items", 1)[1]

    for quote in ("the assay was run as described", "counts are available on request"):
        assert f"> {quote}" in prior, (
            f"a surviving passage was not printed as the authors' words: {prior}"
        )
    # The row's own field names, which is what the letter printed when it
    # printed the row. One of these in a published letter is the bug.
    for leaked in (
        "finding_uid", "matched_by", "fingerprint", "'quote'", "{'", "f-021", "f-022",
    ):
        assert leaked not in prior, (
            f"the letter printed the record of a passage rather than the passage: {prior}"
        )
    assert "This draft, where the earlier finding's passage still stands" in prior, (
        f"an unlabelled block quote reads as part of the editor agent's reason: {prior}"
    )
    # The two matches, told apart in the authors' own terms. The line is named
    # too, because a passage found in this draft is at a line of this draft.
    assert f"line {ASSAY_LINE} of this draft" in prior and "still reads word for word" in prior, (
        f"a passage found by its quoted words is not reported as unchanged: {prior}"
    )
    assert f"line {COUNTS_LINE} of this draft" in prior and "wording has moved" in prior, (
        f"a passage found by its digest is reported as though the words were unchanged: {prior}"
    )

    # A row with no quote in it is a row with nothing to show the authors, and
    # printing the heading over nothing would say the text survived and then
    # show no text.
    empty = dict(
        ISSUES[5],
        surviving_quotes=[
            {
                "finding_uid": "f-099",
                "document": MAIN_DOCUMENT,
                "line": PANEL_LINE,
                "matched_by": "quote",
                "quote": "",
            }
        ],
    )
    assert local_review.surviving_passages(empty) == [], (
        "a row carrying no quoted words is not a surviving passage"
    )


def check_a_later_round_cannot_publish_without_the_round_before_it() -> None:
    """The plan names the previous round's items and the run has to have read them.

    Nothing joined the two up. A run made without `--prior-issues` published as
    round three with no prior round recorded, every item `new`, and the first
    ids minted again for problems that had nothing to do with the ones the
    authors were sent under those numbers. Four pairs are refused here, and the
    pair that agrees publishes.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bundle = _prior_bundle(root / "r2")
        named = str(bundle / local_review.REVIEW_ISSUES)
        plan = {"round": 3, "prior_issues": named}

        # The pair that agrees: the plan names the file, the engine read a file,
        # and the digest the engine recorded is of the file on disk.
        local_review.assert_the_round_ruled_against_its_prior(plan, PACKAGE)

        # The plan named the previous round and the run never read it.
        try:
            local_review.assert_the_round_ruled_against_its_prior(
                plan, dict(PACKAGE, prior_round={})
            )
        except local_review.CommandError as refusal:
            message = str(refusal)
            assert "round 3" in message and "--prior-issues" in message, (
                f"the refusal has to name the round and the flag to re-run with: {message}"
            )
        else:
            raise AssertionError("a later round published without the items it rules against")

        # The reverse surprise: the run ruled against some file the plan knows
        # nothing about, so nothing can say which round the letter is about.
        try:
            local_review.assert_the_round_ruled_against_its_prior(
                {"round": 3, "prior_issues": ""}, PACKAGE
            )
        except local_review.CommandError as refusal:
            assert "does not name" in str(refusal), (
                f"the refusal has to say the plan does not name the file: {refusal}"
            )
        else:
            raise AssertionError("a run ruled against a round the plan never named")

        # The file the plan named is gone, so what was ruled against cannot be
        # checked at all.
        try:
            local_review.assert_the_round_ruled_against_its_prior(
                {"round": 3, "prior_issues": str(root / "gone" / local_review.REVIEW_ISSUES)},
                PACKAGE,
            )
        except local_review.CommandError as refusal:
            assert "no longer at" in str(refusal), (
                f"a missing prior file has to be reported as missing: {refusal}"
            )
        else:
            raise AssertionError("a prior file that is not there was read anyway")

        # A different file, hashed into its own bundle so the manifest agrees
        # with it: what fails is the engine's digest, which is of the file the
        # run actually read.
        other = root / "r2-other"
        other.mkdir()
        text = PRIOR_ISSUES_TEXT.replace("the per-well counts", "the per-plate counts")
        (other / local_review.REVIEW_ISSUES).write_text(text, encoding="utf-8")
        (other / "manifest.json").write_text(
            json.dumps(
                {"files": {local_review.REVIEW_ISSUES: local_review.digest(text.encode())}},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        try:
            local_review.assert_the_round_ruled_against_its_prior(
                {
                    "round": 3,
                    "prior_issues": str(other / local_review.REVIEW_ISSUES),
                },
                PACKAGE,
            )
        except local_review.CommandError as refusal:
            message = str(refusal)
            assert PRIOR_ROUND["digest"] in message, (
                f"the refusal has to print the digest the engine recorded: {message}"
            )
            assert "never sent" in message, (
                f"the refusal has to say what the letter would be about: {message}"
            )
        else:
            raise AssertionError("a round published against a file the previous round never wrote")

        # A first round names no prior file and the engine read none, which is
        # the ordinary case and not an error.
        local_review.assert_the_round_ruled_against_its_prior(
            {"round": 1, "prior_issues": ""}, dict(PACKAGE, prior_round={})
        )


def check_a_hand_edited_prior_file_is_not_the_one_that_round_published() -> None:
    """The previous round's items are read only as the bytes that bundle published.

    The file sits in a published bundle in a public repository, and the next
    round rules against it: an id, a statement or a severity in it becomes the
    standing of a request the authors already answered. A row deleted or a
    statement rewritten by hand was read as the previous round's own words, and
    the only sign of it was in the file's history. Every bundle hashes its own
    files into `manifest.json`, so there is a published digest, and it is
    checked where the file is named as an input.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # The published bundle, untouched, is accepted and is the file a later
        # round is handed.
        clean = _prior_bundle(root / "v1" / "r2")
        assert local_review.prior_issues_file(clean) == clean / local_review.REVIEW_ISSUES, (
            "the previous round's own file was not read back"
        )

        # The same bundle with one statement rewritten by hand, and the
        # manifest left as it was published.
        edited = _prior_bundle(root / "v1" / "r2-edited")
        (edited / local_review.REVIEW_ISSUES).write_text(
            PRIOR_ISSUES_TEXT.replace("major", "minor"), encoding="utf-8"
        )
        try:
            local_review.prior_issues_file(edited)
        except local_review.CommandError as refusal:
            message = str(refusal)
            assert "not the file that bundle published" in message, (
                f"an edited prior file has to be refused as edited: {message}"
            )
            assert PRIOR_ISSUES_SHA256[:16] in message, (
                f"the refusal has to print the digest the bundle recorded: {message}"
            )
        else:
            raise AssertionError("a hand-edited prior file was accepted as the published one")

        # A bundle whose manifest does not account for the file reads the same
        # way from here: there is no published digest to check against.
        unaccounted = root / "v1" / "r2-unaccounted"
        unaccounted.mkdir(parents=True)
        (unaccounted / local_review.REVIEW_ISSUES).write_text(
            PRIOR_ISSUES_TEXT, encoding="utf-8"
        )
        (unaccounted / "manifest.json").write_text(
            json.dumps({"files": {"summary.md": "a" * 64}}, indent=2) + "\n", encoding="utf-8"
        )
        try:
            local_review.prior_issues_file(unaccounted)
        except local_review.CommandError as refusal:
            assert "does not account for" in str(refusal), (
                f"an unaccounted prior file has to be refused as unaccounted: {refusal}"
            )
        else:
            raise AssertionError("a prior file no manifest accounts for was read anyway")


def check_a_first_round_claims_no_standing_against_a_round_that_never_ran() -> None:
    """With no round before it, there is no previous round to be new against.

    Every item of a first round printed `Against the previous round: new`, which
    says there was a previous round and that this item is not in it. The word is
    the engine's and it is right in the record, where `new` is one of five
    standings. What was wrong was printing it in a letter to authors who have
    had no earlier letter.
    """
    # A first round as the engine writes one: no prior round, and so no row
    # ruling on an item of a round that does not exist.
    first = dict(PACKAGE, prior_round={}, issues=list(local_review.live_issues(PACKAGE)))
    assert not local_review.has_prior_round(first), (
        "a package the engine gave no prior round is a first round"
    )
    letter = local_review.render_decision_letter(
        PAPER,
        dict(first, findings=LEDGER),
        dict(provenance_fixture(), round=1, prior_round={}),
    )
    assert "Against the previous round" not in letter, (
        f"a first round told the authors where an item stands against nothing: {letter}"
    )
    assert "The previous round's items" not in letter, (
        f"a first round reported on a round that never ran: {letter}"
    )

    # And the standing is printed when there is a round for it to be about.
    later = local_review.render_decision_letter(PAPER, READING, provenance_fixture())
    assert "**Against the previous round:** new" in later, (
        f"a later round owes the authors each item's standing: {later}"
    )


def check_a_standing_this_release_never_publishes_is_refused() -> None:
    """Five words are published as a standing, and a sixth is refused by name.

    The five are the engine's own vocabulary. A word outside them would print in
    the letter as the item's standing against the previous round, meaning
    whatever the reader took it to mean, and a shape outside the three fields of
    a surviving passage would print as a line of Python. Both are refused at the
    publish gate rather than rendered.
    """
    assert local_review.ISSUE_STATUSES == (
        "new",
        "persisting",
        "regressed",
        local_review.RESOLVED_STATUS,
        local_review.UNVERIFIED_STATUS,
    ), f"the published standings are not the five the engine mints: {local_review.ISSUE_STATUSES}"

    strange = dict(ISSUES[1], status="fixed")
    try:
        local_review.assert_publishable_issues(
            dict(PACKAGE, issues=[*ISSUES[:1], strange, *ISSUES[2:]])
        )
    except local_review.CommandError as refusal:
        message = str(refusal)
        assert "fixed" in message and strange["id"] in message, (
            f"the refusal has to name the word and the issue carrying it: {message}"
        )
        assert "persisting" in message, (
            f"the refusal has to say which words this release does publish: {message}"
        )
    else:
        raise AssertionError("a standing no publish ever mints was accepted")

    shapeless = dict(ISSUES[5], surviving_quotes=["counts are available on request"])
    try:
        local_review.assert_publishable_issues(
            dict(PACKAGE, issues=[*ISSUES[:5], shapeless])
        )
    except local_review.CommandError as refusal:
        assert shapeless["id"] in str(refusal), (
            f"the refusal has to name the issue carrying the row: {refusal}"
        )
    else:
        raise AssertionError("a surviving passage that is not a row of the engine's was accepted")

    # The fixture itself passes both, or the refusals above prove nothing.
    local_review.assert_publishable_issues(PACKAGE)


def check_a_credential_or_an_installed_path_is_a_fact_and_never_prose() -> None:
    """The scan was built for the operator's filesystem and missed two things.

    A key pasted into a refusal, printed by a tool into a run log, or sitting in
    an environment line copied into a comment would have travelled into a
    published bundle untouched, because nothing scanned for one. And the longest
    paths on the machine went unscanned: the engine is installed under one, and
    a traceback out of a run is full of them, naming the interpreter, its
    version and the layout of the install.

    Both are tier 1, which is the tier nothing waives: not the manuscript
    printing it, not `--allow-text`. A credential is not a fact about this
    machine, but it shares the only property that tier is for.
    """
    secrets = (
        "sk-ant-api03-" + "A" * 40,
        "ghp_" + "b" * 36,
        "AKIAZZZZZZZZZZZZZZZZ",
        "AIza" + "c" * 35,
        "xoxb-1234567890-" + "d" * 24,
        "Authorization: Bearer " + "e" * 40,
        "-----BEGIN RSA PRIVATE KEY-----",
    )
    for secret in secrets:
        leaks = local_review.local_references(f"the log line read {secret} and stopped")
        assert leaks, f"a credential reached a published file unscanned: {secret}"
        assert all(leak.machine_fact for leak in leaks), (
            f"a credential is tier 1, which nothing waives: {secret}"
        )
        assert local_review.names_a_specific_fact(secret, ()), (
            f"an allowance naming a credential would publish it: {secret}"
        )
        # And an allowance cannot waive it, whichever way it is offered.
        waived = local_review.local_references(
            secret, manuscript=secret, allowed=[secret]
        )
        assert waived, f"an allowance waived a credential: {secret}"
        assert "allow-text" not in local_review.leak_refusal(waived), (
            f"the refusal offered a flag for a credential: {secret}"
        )

    installed = (
        "/usr/lib/python3.12/site-packages/peerreviewagents/plugin/server.py",
        "/opt/node/lib/node_modules/astro/dist/core/build.js",
        "/var/lib/pyenv/versions/3.12.1/lib/python3.12/dist-packages/engine/runs.py",
        "/run/user/1000/gnupg/S.gpg-agent",
    )
    for path in installed:
        leaks = local_review.local_references(f"the traceback printed {path}")
        assert leaks, f"a path inside an installed environment was not scanned: {path}"
        assert all(leak.machine_fact for leak in leaks), (
            f"a path inside an installed environment is tier 1: {path}"
        )

    # And ordinary review prose still publishes. `/usr/bin` and the words these
    # shapes are made of are not refused on their own, because a scan that
    # fires on a reviewer's sentence gets waived by habit.
    for ordinary in (
        "the method runs on a site packages install of the toolkit",
        "the authors bear the burden of showing the effect",
        "the node modules in figure 3 are the lymph nodes",
        "the run user was not reported",
    ):
        assert local_review.local_references(ordinary) == [], (
            f"ordinary review prose was refused as a machine fact: {ordinary}"
        )


def check_a_withheld_run_with_no_reason_is_reported_as_having_none() -> None:
    """When the engine withholds a run it says why, and a silence is not a reason.

    There used to be a fallback here that rebuilt a reason out of the old flat
    findings fields when the list was missing, for an engine too old to carry
    one. This release requires an engine that always carries it, and the
    fallback described a run shape the engine no longer writes, so it told the
    operator a story about a run nobody could have read that way. An empty list
    is now reported as what it is.
    """
    run = _run_record()
    reading = {
        "status": "blocked",
        "publishable": False,
        "not_publishable_reasons": [],
        "cause": "",
    }
    try:
        local_review.require_complete_run(Path("."), run, reading)
    except local_review.CommandError as refusal:
        message = str(refusal)
        assert "gave no reason" in message, (
            f"a silence has to be reported as a silence: {message}"
        )
        assert "read the run folder" in message, (
            f"the refusal has to say what is left to do: {message}"
        )
        for invented in ("findings", "lane", "guard took"):
            assert invented not in message, (
                f"the refusal explained a withheld run by guesswork: {message}"
            )
    else:
        raise AssertionError("a run the engine withheld without a reason was published")

    # With reasons, they are the engine's own words and all of them.
    with_reasons = dict(
        reading,
        not_publishable_reasons=["the editor agent wrote no issues", "a reader never reported"],
        cause="the editor slot ran out of turns",
    )
    try:
        local_review.require_complete_run(Path("."), run, with_reasons)
    except local_review.CommandError as refusal:
        message = str(refusal)
        for reason in with_reasons["not_publishable_reasons"]:
            assert reason in message, f"the engine's own reason was dropped: {message}"
        assert with_reasons["cause"] in message, f"the cause was dropped: {message}"
    else:
        raise AssertionError("a run the engine withheld with reasons was published")


def check_no_published_document_overstates_what_the_editor_agent_did() -> None:
    """Two sentences said more than the run supports, and they are authored here.

    The method paragraph said the editor agent chose which findings belong in
    the body of the letter, which was a sentence about a limit that no longer
    exists: every issue it raises is in the letter, split by severity. And the
    provenance page called an unverified item one the editor agent could not
    verify, where the word means no reviewer raised it again and nothing showed
    it fixed. Both are checked here because both are prose in this repository,
    not output from the engine.
    """
    paragraph = local_review.method_paragraph(
        {"arm": "full-two-track", "reviewers": 3, "specialist_tracks": list(TRACKS)},
        _expected_models(),
    )
    assert "wrote the numbered issues the letter asks for" in paragraph, (
        f"the paragraph has to say what the editor agent produced: {paragraph}"
    )
    for retired in ("belong in the body", "chose which", "most important"):
        assert retired not in paragraph, (
            f"the paragraph still describes a limit this release does not apply: {paragraph}"
        )

    skill = (
        Path(__file__).resolve().parents[2]
        / ".claude" / "skills" / "local-review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "writes the numbered issues the letter asks for" in skill, (
        "the skill has to describe the editor agent's own output"
    )
    for retired in ("belong in the body", "chose which"):
        assert retired not in skill, (
            f"the skill still says the editor agent picked what the letter carries: {retired}"
        )

    # The page is JSX, so its sentences are wrapped over several lines. What is
    # checked is the sentence, with the wrapping taken out.
    page = " ".join(_provenance_component_fields().split())
    assert "raised again by no reviewer and shown fixed by nothing" in page, (
        "the page has to say what unverified means"
    )
    assert "Neither word is a test that ran" in page, (
        "the page has to say that neither ruling is a check that ran"
    )
    for retired in ("could not be verified", "could not verify", "unverified by the editor"):
        assert retired not in page, (
            f"the page still reads as though a verification was attempted: {retired}"
        )


def check_no_editorial_page_names_the_machine_it_was_written_on() -> None:
    """The scan covered published bundles and not the pages beside them.

    Every file in a review bundle is scanned before it is published, because a
    path out of a run folder had reached one. The editorial pages were written
    by hand and never scanned, and they are on the same site: the owner's home
    directory and the hostname of the machine this pipeline was built on sat in
    the development page and in comments in these scripts, where they were read
    by nobody and published to everybody.

    Tier 1 is refused on every page. Those are facts that can only be one
    machine, and they are the running machine's: the home directory and
    hostname are looked up at scan time, so a path belonging to somebody else's
    computer is refused here only on the computer that holds it, and the
    general shapes below catch the rest.

    A shape is refused on every page but the development page. That page
    documents this scan, so it prints example paths on purpose, and a scan that
    refused them would be a scan nobody could write about. What is still
    refused there is this machine: the home directory, the checkout, the host
    name and the rest of what the scan looks up, and a credential. An example
    path belonging to no computer is a shape and may be printed, the real one
    may not.
    """
    root = Path(__file__).resolve().parents[2]
    pages = re.findall(r'slug:\s*"([\w-]+)"', (root / "src" / "lib" / "pages.js").read_text())
    assert pages, "the editorial pages could not be read from src/lib/pages.js"
    documents = [root / "docs" / f"{slug}.md" for slug in pages] + [root / "README.md"]
    # The page that documents the scan, and the only one allowed a shape.
    documenting = root / "docs" / "development.md"

    facts = local_review.machine_facts()
    # What the scan looked up on this computer, without the shapes that are
    # carried as facts so nothing waives them. A shape names no machine, so on
    # the page that documents the scan it is an example and not a leak.
    shapes = {why for why, _ in local_review.UNWAIVABLE_PATH_SHAPES}
    looked_up = tuple(fact for fact in facts if fact.why not in shapes)
    for document in documents:
        text = document.read_text(encoding="utf-8")
        leaks = local_review.local_references(text, facts=facts)
        if document == documenting:
            leaks = [
                leak for leak in leaks if local_review.names_a_specific_fact(leak.text, looked_up)
            ]
        assert leaks == [], (
            f"{document.name} names this machine or a path on it: "
            f"{[leak.line for leak in leaks]}"
        )

    # And the check can fail: a home path in a page is refused, and on the
    # documenting page a specific fact still is while an example shape is not.
    planted = "the run wrote it to /home/someone/reviews/r1/summary.md"
    assert local_review.local_references(planted, facts=facts), (
        "a home path in an editorial page has to be refused"
    )
    own = str(Path.home() / "Repos" / "insilico")
    assert any(
        leak.machine_fact
        for leak in local_review.local_references(f"built in {own}", facts=facts)
    ), "this machine's own home directory is a fact no page may print"


def check_the_fixtures_counts_are_the_ones_the_reader_computes() -> None:
    """The tallies written into the fixture are the ones the publish path counts.

    The engine writes a `counts` block into its issues document and recomputes
    the same tally when it reads the run back. This suite writes that block out
    by hand on purpose, so that a check can compare it against what this
    repository's own sorting produces. A fixture that derived the numbers from
    the issues could not disagree with the code under test, and would pass
    whatever either of them did.
    """
    counts = PACKAGE["counts"]
    computed = {
        "issues": len(local_review.live_issues(PACKAGE)),
        "required": len(local_review.required_issues(PACKAGE)),
        "suggestions": len(local_review.suggestion_issues(PACKAGE)),
        "resolved": len(local_review.resolved_issues(PACKAGE)),
        "unverified": len(local_review.unverified_issues(PACKAGE)),
    }
    for name, value in computed.items():
        assert counts[name] == value, (
            f"the fixture says {name} is {counts[name]} and the publish path counts {value}"
        )

    # The required changes and the suggestions are the whole of this round's
    # issues, with nothing in both and nothing in neither.
    required = {issue["id"] for issue in local_review.required_issues(PACKAGE)}
    suggested = {issue["id"] for issue in local_review.suggestion_issues(PACKAGE)}
    live = {issue["id"] for issue in local_review.live_issues(PACKAGE)}
    assert not (required & suggested), f"an issue is both required and suggested: {required & suggested}"
    assert required | suggested == live, (
        f"an issue of this round is in neither list: {live - (required | suggested)}"
    )

    # The members are the findings the issues were pooled from, counted once
    # each however many issues name them, and the ledger holds every one.
    members = {
        str(member.get("finding_uid"))
        for issue in PACKAGE["issues"]
        for member in issue["members"]
    }
    assert counts["issue_members"] == len(members), (
        f"the fixture says {counts['issue_members']} members over {len(members)} findings"
    )
    ledger = {str(row.get("finding_uid")) for row in LEDGER}
    assert members <= ledger, f"an issue rests on a finding the ledger does not hold: {members - ledger}"

    # Every status the engine writes is in the tally, with all five keys, and
    # the two closed ones are counted apart from each other. The five are named
    # here rather than read off the engine because this check runs on a bare
    # interpreter too, and the engine's own vocabulary is checked against this
    # pipeline's words by `assert_issue_vocabulary` at publish time.
    assert set(counts["by_status"]) == {
        "new", "persisting", "regressed", "resolved", "unverified",
    }, f"the status tally does not carry every status the engine writes: {counts['by_status']}"
    assert counts["by_status"]["resolved"] == counts["resolved"], "two tallies of resolved disagree"
    assert counts["by_status"]["unverified"] == counts["unverified"], (
        "two tallies of unverified disagree"
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
        (nested / "issues.json").write_text("{}", encoding="utf-8")

        local_review.write_manifest(dest)
        manifest = json.loads((dest / "manifest.json").read_text())

        assert manifest["schema_version"] == 1, f"manifest version: {manifest['schema_version']}"
        assert set(manifest["files"]) == {
            "summary.md",
            "decision_letter.md",
            "attachments/issues.json",
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


def check_every_documented_command_runs_against_a_real_parser() -> None:
    """A command or a flag in the documents has to be one something accepts.

    The skill's engine commands were checked against the engine's parsers while
    `docs/development.md` went on documenting `--model` and `--offline` on
    `publish`, which this repository's own parser had stopped accepting. An
    editor following the page got an argparse rejection. So the checker reads
    every document a reader is handed and routes each command to whatever would
    really run it, and this asserts that the routing bites: the live command
    parses, the two dead flags do not, an npm target that is not in
    package.json does not, and a program nothing here knows is a failure rather
    than a silent pass.

    The engine is not needed for any of it. These are this repository's own
    parsers, `package.json`, and the documents.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import check_skill_commands as checker

    targets = checker.npm_targets()

    def outcome(command: str) -> tuple[str, str | None]:
        return checker.check_command(command, engine=None, targets=targets)

    publish = (
        "python scripts/local_review.py publish --prepared runs/p --run runs/r "
        "--decision major --editor someone --human-reviewed yes --publish"
    )
    where, reason = outcome(publish)
    assert reason is None, f"the documented publish command does not parse: {reason}"
    assert where == "python local_review.py", f"publish was routed to {where!r}"

    for dead in ("--model claude-sonnet-4", "--offline"):
        _, reason = outcome(f"{publish} {dead}")
        assert reason and "unrecognized arguments" in reason, (
            f"publish {dead} is not a flag this repository has, and the check let it "
            f"through: {reason!r}"
        )

    _, reason = outcome("npm run check:schema")
    assert reason is None, f"a real npm target was rejected: {reason}"
    _, reason = outcome("npm run check:everything")
    assert reason and "package.json" in reason, f"an invented npm target passed: {reason!r}"
    _, reason = outcome("npm run check:markdown  npm run build")
    assert reason and "one script name" in reason, (
        f"two npm commands on one line is not a command: {reason!r}"
    )

    _, reason = outcome("rustypaper review runs/example")
    assert reason and "OUTSIDE_PROGRAMS" in reason, (
        f"a program this check knows nothing about passed silently: {reason!r}"
    )
    _, reason = outcome("python scripts/check_review_manifests.py --everything")
    assert reason and "no arguments" in reason, (
        f"a script with no parser was given arguments: {reason!r}"
    )
    _, reason = outcome("python scripts/not_a_script.py")
    assert reason and "not a file" in reason, f"a missing script passed: {reason!r}"

    accepted = checker.accepted_flags(None)
    for flag in ("--publish", "--editor", "--human-reviewed", "--replace", "--baseline-eligible"):
        assert flag in accepted, f"{flag} is a flag this repository has, and was not found"
    for flag in checker.ABSENT_FLAGS:
        assert flag not in accepted, (
            f"{flag} is listed as gone from these documents, but a parser accepts it"
        )

    found = dict(checker.documented_flags("Pass `--offline` to skip the probe.\n"))
    assert "--offline" in found, f"a flag named in prose was not found: {found}"

    # The documents themselves, read the way the checker reads them. Where the
    # engine is installed its flags count too; where it is not, a flag that is
    # not local can only be checked for being gone, and the checker says the
    # same thing in its own note rather than failing on half a parser set.
    try:
        engine = checker.load_parsers()
    except Exception:  # pragma: no cover - depends on the interpreter
        engine = None
    everything = checker.accepted_flags(engine)
    for document in checker.published_documents():
        for flag, context in checker.documented_flags(document.read_text(encoding="utf-8")):
            if flag in checker.ABSENT_FLAGS:
                assert flag not in everything, (
                    f"{document.name} says {flag} is gone, but a parser accepts it: {context}"
                )
            elif engine is not None:
                assert flag in everything, (
                    f"{document.name} documents {flag}, which no parser accepts: {context}"
                )


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
        assert run["findings_source"] == "issues", (
            f"the record must say where the engine read the findings: {run}"
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
        # engine decides the status and the cause, and what the record adds is
        # the harm a run can carry past them.
        broken = _run_directory(
            Path(tmp) / "broken",
            **{
                "progress.json": {
                    "status": "blocked",
                    "error": "the transport hung up",
                    "stages": _stages(TRACKS, reported=list(CORE_SLOTS), missing=["spec-stats"]),
                },
                "runtime.json": _runtime(TRACKS, status="blocked", blocked_reason="no plugin loaded"),
                "issues.json": dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    review_guard_status="quarantined",
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
        assert any("spec-stats" in e for e in errors), (
            f"a stage that never reported is an error: {errors}"
        )
        # What the guards threw out is counted and carried, and it is not filed
        # under what went wrong. The engine publishes a run that lost a finding
        # it could not anchor, because that is the guard doing its job, so
        # listing it as an error would describe a working review as a damaged
        # one.
        assert record["quarantined_findings_count"] == 2, (
            f"the quarantined rows were not counted: {record}"
        )
        assert not any("quarantined" in error for error in errors), (
            f"a guard catch is not an error: {errors}"
        )


def check_a_run_of_one_paper_cannot_be_published_as_another() -> None:
    """The reviewer published paper B's package under paper A's identity, exit 0.

    Three steps each hash something and none of them was compared: prepare
    hashes the fetched PDF, the importer hashes the bytes it was given, and the
    run records the paper id it reviewed.

    The workspace is read through the engine's own `verify_workspace` now, so
    this is a check against the real reader: the paper's identity comes out of
    the folder the importer wrote, and the same call re-digests `paper.md`,
    which is the file every line number in the review points into.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = _workspace(Path(tmp) / "workspace")
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
        manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
        manifest.pop("source")
        (workspace / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        try:
            local_review.bind_run_to_input(prepared, workspace, run)
        except local_review.CommandError:
            pass
        else:
            raise AssertionError("a workspace with no source hash was accepted")

        # And the folder itself has to be the one the import left behind. The
        # review's quotations are lines of `paper.md`, so a `paper.md` edited
        # after the import is a folder whose line numbers mean nothing, and the
        # engine refuses it by name rather than letting the publish path read
        # the identity out of a manifest that no longer describes the files.
        edited = _workspace(Path(tmp) / "edited")
        (edited / MAIN_DOCUMENT).write_text("Another paper entirely.\n", encoding="utf-8")
        try:
            local_review.bind_run_to_input(prepared, edited, run)
        except local_review.CommandError as refusal:
            assert MAIN_DOCUMENT in str(refusal), (
                f"the refusal has to name the file that changed: {refusal}"
            )
        else:
            raise AssertionError("a workspace edited after the import was accepted")

        # A folder from before the engine wrote `paper.md` is refused for what
        # it is, with the one thing that fixes it, rather than for a missing
        # file whose name says nothing.
        legacy = Path(tmp) / "legacy"
        legacy.mkdir()
        (legacy / "paper.json").write_text(
            json.dumps({"id": "paper-abc", "source_sha256": "b" * 64, "blocks": []}),
            encoding="utf-8",
        )
        try:
            local_review.bind_run_to_input(prepared, legacy, run)
        except local_review.CommandError as refusal:
            message = str(refusal)
            assert "paper.json" in message and "re-import" in message, (
                f"a folder from the old shape has to be named as one: {message}"
            )
        else:
            raise AssertionError("a manuscript folder from before paper.md was accepted")


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

    In 0.9 there is no debate stage to describe and no single model: every slot
    is assigned one of its own, so the paragraph counts agents per model and
    says outright that agents sharing one are not corroborating each other. It
    counts the models that were observed running, never the ones the run asked
    for, and when a slot's model went unobserved it says that in a sentence of
    its own rather than letting the plan stand in for the measurement.
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
    assert "no slot's model was observed" in unrecorded, (
        f"a run with no observed model must say so: {unrecorded}"
    )
    for named in _expected_assigned().values():
        assert named not in unrecorded, (
            f"the plan was named as the models that ran: {unrecorded}"
        )

    # A run where some slots were observed and others were not says both: the
    # count over what ran, and one sentence naming the slots nobody saw.
    partial = local_review.method_paragraph(
        {
            "arm": "full-two-track",
            "reviewers": 3,
            "specialist_tracks": list(TRACKS),
            "models_unverified": ["spec-field", "recorder"],
        },
        {slot: model for slot, model in models.items() if slot not in ("spec-field", "recorder")},
    )
    assert "not recorded for 2 slots (spec-field, recorder)" in partial, (
        f"the slots nobody observed are not named: {partial}"
    )
    assert "the plan is all this record has" in partial, (
        f"the paragraph must say what is left when nothing was observed: {partial}"
    )
    one = local_review.method_paragraph(
        {"arm": "single", "reviewers": 1, "models_unverified": ["core-1"]}, {"editor": OPUS}
    )
    assert "1 slot (core-1)" in one, f"one slot is one slot: {one}"

    for text in (full, single, unrecorded, partial, one):
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
            ws = _workspace(Path(tmp) / f"ws-{len(why)}", paper_id)
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
            # The engine keeps its own list of why it holds a run back, one
            # sentence each, never empty while the flag is false. The refusal
            # repeats those sentences rather than a second copy of the rule
            # behind them, so the two cannot drift apart as the engine's rule
            # changes.
            reading = local_review.engine_reading(cases["a blocked run"])
            reasons = [
                str(reason).strip()
                for reason in reading.get("not_publishable_reasons") or []
                if str(reason).strip()
            ]
            assert reasons, f"the engine held the run back without saying why: {reading}"
            assert all(reason.rstrip(".") in str(error) for reason in reasons), (
                f"the refusal dropped the engine's reasons {reasons}: {error}"
            )
        else:
            raise AssertionError("a blocked run was published")


def check_a_finished_run_that_endorses_nothing_is_a_review() -> None:
    """A run can finish every stage and raise no finding, and that is a result.

    Engine 0.10 records that outcome as `status: complete-without-findings` with
    `review_guard_status: clean`, an issues document that holds no issue and no
    ledger beside it, and it calls that run publishable. An issues document with
    nothing in it is a reading of a manuscript nobody raised anything about,
    which is why it is the ledger rather than the document that is absent here:
    findings with no issue over them is the other outcome, and the engine holds
    that one back. Refusing this one here would make
    the published corpus one that silently drops every review finding a
    manuscript sound: the papers nothing is wrong with would be exactly the
    ones that never got published, and the record would read as if the engine
    always finds something.

    The same status covers the opposite outcome, and the engine is what tells
    the two apart. A review the evidence guards emptied reaches
    `complete-without-findings` with a quarantined count, and the engine holds
    it back with a reason that names how many it took. Nothing here reads the
    status to decide: the gate is `publishable` and the refusal prints
    `not_publishable_reasons`, so a run the engine publishes and a run it holds
    can share a status word without this file having to know which is which.

    A run that kept some findings and lost others is a third outcome and does
    publish, with the held-back count travelling in the record, because a guard
    that could not anchor one quote has done its job and the review that
    survives it is still a review.
    """
    sound_package = dict(
        PACKAGE,
        issues=[],
        issue_ids_used=[],
        prior_round=None,
        counts={
            "issues": 0,
            "required": 0,
            "suggestions": 0,
            "resolved": 0,
            "unverified": 0,
            "issue_members": 0,
            "by_severity": {"major": 0, "moderate": 0, "minor": 0},
            "by_category": {},
            "by_status": {
                "new": 0,
                "persisting": 0,
                "regressed": 0,
                "resolved": 0,
                "unverified": 0,
            },
        },
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
                    "status": local_review.WITHOUT_FINDINGS_STATUS,
                    "review_guard_status": "clean",
                    "stages": _stages(TRACKS),
                    "findings_delivered": 0,
                    "quarantined_findings_count": 0,
                },
                "issues.json": sound_package,
                # No ledger at all, because nobody filed a row. A ledger with
                # rows in it and no issue over them is a run the engine holds
                # back, and that is a different check.
                "findings.jsonl": None,
            },
        )
        reading = local_review.engine_reading(empty)
        assert reading["publishable"] is True, (
            "the engine publishes a review that raised nothing: "
            f"{reading.get('not_publishable_reasons')}"
        )
        record = local_review.run_record(reading)
        assert record["errors"] == [], (
            f"a finished run that raised nothing is not an error: {record['errors']}"
        )
        local_review.require_complete_run(empty, record, reading)
        assert record["status"] == local_review.WITHOUT_FINDINGS_STATUS, f"status lost: {record}"
        assert record["status"] in _schema_run_statuses(), (
            f"the schema has to accept the status of a review that raised nothing: {record}"
        )
        assert record["review_guard_status"] == "clean", f"the guard verdict was not read: {record}"
        sound_read = local_review.review_package(reading)
        assert local_review.required_issues(sound_read) == [], (
            "a run that raised nothing asks for nothing"
        )
        assert local_review.suggestion_issues(sound_read) == [], (
            "a run that raised nothing suggests nothing"
        )
        assert record["findings_source"] == "issues", (
            f"an empty review is still read from its issues document: {record}"
        )

        # It publishes, documents and all, rather than refusing at the last step.
        # Only the installed engine is stubbed: the transport record is read from
        # the run's own start-up probe, so publishing needs no CLI and no network.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-sound-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    # A first round: the run was given nothing to rule against,
                    # so the plan names no prior items either. The two have to
                    # agree, and the publish path refuses the pair where the
                    # plan names a file the run never read.
                    _prepared(
                        Path(tmp) / "prepared", destination, round=1, prior_issues="",
                        draft=1, plan_kind="first review",
                    ),
                    empty,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                    # Repeated deliberately. _publish types `major`, argparse keeps
                    # the last value, and a review that raised nothing is an accept.
                    "--decision", "accept",
                )
            assert code == 0, f"a review that raised nothing should publish, got exit {code}"
            # The one sentence the three documents owe a reader of such a
            # review, and it is the same sentence in all three, built once in
            # `no_findings_note` so the letter, the summary and the page cannot
            # tell the authors three different things about the same zero.
            sound = local_review.no_findings_note({"quarantined_findings_count": 0})
            assert "no make-or-break findings" in sound, (
                f"the note for a sound manuscript has to say so plainly: {sound}"
            )
            letter = (destination / "decision_letter.md").read_text(encoding="utf-8")
            assert sound in letter, (
                "a review with no findings still owes the authors a letter that says so: "
                f"{letter}"
            )
            summary = (destination / "summary.md").read_text(encoding="utf-8")
            assert sound in summary, f"the summary owes a reader the same sentence: {summary}"
            assert "no make-or-break findings" in _provenance_component_fields(), (
                "the provenance page has to say plainly that nothing was raised"
            )
            published = json.loads((destination / "provenance.json").read_text(encoding="utf-8"))
            run_record = published["generator"]["run"]
            assert run_record["status"] in _schema_run_statuses(), (
                f"the published status is not one the schema accepts: {run_record}"
            )
            assert run_record["findings_delivered"] == 0, (
                f"an empty review delivered no finding to the ledger either: {run_record}"
            )
            assert run_record["issues"] == 0, f"an empty review recorded issues: {run_record}"
            assert run_record["required"] == 0 and run_record["suggestions"] == 0, (
                f"an empty review asks for nothing: {run_record}"
            )
            assert run_record["resolved"] == 0 and run_record["unverified"] == 0, (
                f"a first round rules on no prior issue: {run_record}"
            )
            assert run_record["issues_source"] == "editor", (
                f"the published record has to say who pooled the issues: {run_record}"
            )
            # A first round was given nothing to rule against, and the record
            # says so with an empty object rather than by leaving the field out.
            assert published["prior_round"] == {}, (
                f"a first round has no prior round: {published['prior_round']}"
            )
            assert run_record["review_guard_status"] == "clean", (
                f"the published record has to carry the guard verdict: {run_record}"
            )
            assert run_record["completeness"]["missing"] == [], (
                f"a whole review has no missing stage: {run_record['completeness']}"
            )
            assert published["generator"]["decision_source"] == "human_editor", (
                "the decision is still a person's on a review that found nothing"
            )

        # Every finding quarantined is a different claim, and the engine makes
        # it on the count beside the status rather than on the status alone.
        # There is no guard word for it either: the verdict is `quarantined`,
        # exactly as it is for a run that lost one finding. So the fixture turns
        # the count, and the refusal rests on the engine's flag, which is what
        # reads the count.
        quarantined = _run_directory(
            Path(tmp) / "quarantined",
            **{
                "progress.json": {
                    "status": "complete-without-findings",
                    "review_guard_status": "quarantined",
                    "stages": _stages(TRACKS),
                    "quarantined_findings_count": 4,
                },
                "issues.json": dict(
                    sound_package,
                    summary="Every finding the reviewers raised failed the guards.",
                    review_guard_status="quarantined",
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

        # Neither word is the gate. The engine writes only `clean` or
        # `quarantined`, and it writes `quarantined` whether the guards took one
        # finding or the lot, so the verdict cannot decide this on its own. It
        # writes `complete-without-findings` for a review with nothing in it
        # whether the reviewers raised nothing or the guards took everything, so
        # the status cannot either. What separates them is the held-back count,
        # and the engine is what reads it. These two runs differ in that count
        # and in nothing else that matters, and they come out on opposite sides.
        assert set(local_review.GUARD_VERDICTS) == {"clean", "quarantined"}, (
            f"the engine writes two guard verdicts and no more: {local_review.GUARD_VERDICTS}"
        )
        for index, held in enumerate((0, 3)):
            run_dir = _run_directory(
                Path(tmp) / f"emptied-{index}",
                **{
                    "progress.json": {
                        "status": local_review.WITHOUT_FINDINGS_STATUS,
                        "review_guard_status": "clean" if not held else "quarantined",
                        "stages": _stages(TRACKS),
                        "findings_delivered": 0,
                        "quarantined_findings_count": held,
                    },
                    "issues.json": dict(sound_package, stages=_stages(TRACKS)),
                    # Neither run has a ledger row left: one raised nothing and
                    # the other had everything held back before the editor saw
                    # it. A ledger with rows in it under an issues document that
                    # holds no issue over them is the engine's own
                    # not-publishable case, which would decide these two runs on
                    # the wrong fact.
                    "findings.jsonl": None,
                },
            )
            if held:
                _quarantine(
                    run_dir,
                    *(
                        {"finding_uid": f"f-05{n}", "severity": "major", "title": "Unquotable"}
                        for n in range(held)
                    ),
                )
            run = local_review.read_run(run_dir)
            if not held:
                local_review.require_complete_run(run_dir, run)
                continue
            try:
                local_review.require_complete_run(run_dir, run)
            except local_review.CommandError as error:
                assert str(held) in str(error), (
                    f"the refusal has to say how many the guards took: {error}"
                )
            else:
                raise AssertionError(
                    f"a review the guards emptied of {held} findings published"
                )

        # A run that kept some findings and lost others does publish, and the
        # count of what was held back travels with it. A guard that cannot
        # anchor a finding and drops it is the guard working, so the review that
        # survives it is still a review. Refusing it would have thrown away a
        # finished panel over one unquotable row. What a reader needs is the
        # number, which the record carries and the page prints. The fixture
        # writes what the engine writes, `quarantined`, in both places the
        # reading looks.
        partial = _run_directory(
            Path(tmp) / "partial",
            **{
                "progress.json": {
                    "status": "complete",
                    "review_guard_status": local_review.QUARANTINED_GUARD,
                    "stages": _stages(TRACKS),
                    "quarantined_findings_count": 1,
                },
                "issues.json": dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    review_guard_status=local_review.QUARANTINED_GUARD,
                ),
            },
        )
        _quarantine(
            partial, {"finding_uid": "f-040", "severity": "moderate", "title": "Unquotable"}
        )
        partial_record = local_review.read_run(partial)
        assert partial_record["publishable"] is True, (
            f"a run that kept findings is publishable: {partial_record}"
        )
        local_review.require_complete_run(partial, partial_record)
        assert local_review.run_errors(partial_record) == [], (
            f"a guard catch is not a run error: {local_review.run_errors(partial_record)}"
        )
        assert partial_record["review_guard_status"] == local_review.QUARANTINED_GUARD, (
            f"the guard verdict has to travel with the record: {partial_record}"
        )
        assert partial_record["quarantined_findings_count"] == 1, (
            f"the held-back count has to travel with the record: {partial_record}"
        )

        # The whole way through, because the gate is only half the job. A partly
        # quarantined run has to publish, the written provenance has to validate
        # against the schema the site checks, and the held-back count has to be
        # in the record the page reads, since that is the field the provenance
        # component prints the sentence from.
        with _stub_engine(), _published_tree(Path(tmp) / "reviews-partial") as reviews:
            destination = reviews / "2026" / "fixture-partial-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-partial", destination),
                    partial,
                    _workspace(Path(tmp) / "workspace-partial"),
                    "--publish",
                    "--decision", "major",
                )
            assert code == 0, (
                f"a partly quarantined run has to publish, got exit {code}: {out.getvalue()}"
            )
            assert (destination / "provenance.json").exists(), (
                f"no bundle was written to {destination}"
            )
            published = json.loads((destination / "provenance.json").read_text(encoding="utf-8"))
            run_record = published["generator"]["run"]
            assert run_record["review_guard_status"] == local_review.QUARANTINED_GUARD, (
                f"the published record lost the guard verdict: {run_record}"
            )
            assert run_record["review_guard_status"] in _schema_guard_verdicts(), (
                "the published guard verdict has to be one the schema accepts: "
                f"{run_record['review_guard_status']} not in {_schema_guard_verdicts()}"
            )
            # The page reads this field and no other to say how many findings
            # the guards held back, so a bundle that drops it publishes a review
            # that quietly understates itself.
            assert run_record["quarantined_findings_count"] == 1, (
                f"the page gets the held-back count from the record: {run_record}"
            )
            assert "quarantined_findings_count" in _provenance_component_fields(), (
                "the provenance page has to read the held-back count it is given"
            )


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

    The probe itself comes from the engine's reading, as `startup`, and the one
    thing that reading does not carry is when the probe ran. That is read out
    of `startup.json` by hand, by `startup_stamp`, and handed in as
    `verified_at`, so a record cannot claim a stamp the run never wrote. Both
    halves are checked below: the function with the stamp passed to it, and
    `startup_stamp` against a real run folder.
    """
    assert local_review.VERIFIED_BY == _schema_verified_by(), (
        f"the schema accepts {_schema_verified_by()!r} and this path writes "
        f"{local_review.VERIFIED_BY!r}"
    )

    restore = os.environ.get("PATH", "")
    os.environ["PATH"] = ""
    try:
        record = local_review.transport_record(
            provider="claude-code",
            runtime=_runtime(TRACKS),
            startup=_startup(),
            verified_at=STARTED_AT,
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
        # A folder with no `startup.json`, and a `startup.json` holding anything
        # other than a probe, both reach this as a reading with a null probe.
        # The engine always returns the block, so an empty one is not what is
        # refused: the absent probe inside it is.
        "nothing in the start-up block": {"provider": "claude-code", "startup": {}},
        "a reading with no probe in it": {
            "provider": "claude-code",
            "startup": {"probe": None, "problems": []},
        },
        "a probe that reported a problem": {
            "provider": "claude-code",
            "startup": _startup(problems=["the pra plugin failed to load"]),
        },
        "no MCP server": {
            "provider": "claude-code",
            "startup": _startup(
                probe={
                    "plugins": [{"name": "pra", "path": "/plugins/pra"}],
                    "mcp_servers": [],
                }
            ),
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
        # And the stamp the reading does not carry is read off the folder, so a
        # published record says when the session started rather than nothing.
        whole = _run_directory(Path(tmp) / "whole")
        assert local_review.startup_stamp(local_review.engine_reading(whole)) == STARTED_AT, (
            "the probe's own stamp has to be read from the run folder: "
            f"{local_review.startup_stamp(local_review.engine_reading(whole))}"
        )
        unproved = _run_directory(Path(tmp) / "unproved", **{"startup.json": None})
        assert local_review.startup_stamp(local_review.engine_reading(unproved)) is None, (
            "a run with no startup.json has no stamp to publish"
        )
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

    0.9 merges every task row into one row per slot and drops the label-only
    ones itself, so nothing here filters them any more. The fixture still
    carries them, because what has to stay true is the published panel, and the
    run folder a real review writes is where they come from.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        rows = local_review.agent_rows(local_review.engine_reading(run))

        slots = [row["slot"] for row in rows]
        assert not [slot for slot in slots if slot.startswith("agent-")], (
            f"a placeholder row was published as an agent that ran: {slots}"
        )
        assert len(rows) == 13, (
            "expected three core reviewers, six specialists, an editor, a "
            f"recorder and two citation workers, one row each: {slots}"
        )
        assert all("slot" in row for row in rows), f"a row with no slot: {rows}"

        # The citation workers are agents of the run and the identity names
        # them, and they wrote no part of the review. So they are here, and
        # every count and map below is taken over the agents that reviewed.
        reviewers = local_review.reviewing_agents(rows)
        assert [row["slot"] for row in reviewers] == [
            slot for slot in slots if slot not in CITATION_WORKERS
        ], f"the panel is the agents that reviewed: {[r['slot'] for r in reviewers]}"
        assert len(reviewers) == 11, (
            f"a citation worker was counted as a reviewer: {[r['slot'] for r in reviewers]}"
        )

        by_slot = {row["slot"]: row for row in rows}
        for slot in CITATION_WORKERS:
            assert by_slot[slot]["role"] == "citation-worker", (
                f"a worker's own role was lost: {by_slot[slot]}"
            )
            assert by_slot[slot]["findings"] == 0, (
                f"a citation worker delivered a finding: {by_slot[slot]}"
            )
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
        assert by_slot["editor"]["model"] == EDITOR_MODEL, (
            f"the editor's model was lost: {by_slot['editor']}"
        )
        # The three core reviewers are three different models, which is the
        # reason 0.9 records a model per slot at all. A row that lost its own
        # model and took a neighbour's would read as a panel that did not sit.
        for index, slot in enumerate(CORE_SLOTS):
            assert by_slot[slot]["model"] == REVIEWER_MODELS[index], (
                f"a core reviewer's own model was lost: {by_slot[slot]}"
            )
        # The harness ran the recorder under the label `ingest`, and 0.9 merges
        # that work into the protocol's own `recorder` slot rather than
        # publishing a twelfth agent beside it. So the one model protocol.json
        # carries for nobody reaches the record through the slot that ran it,
        # which is the row a reader can match to a report.
        assert by_slot["recorder"]["model"] == RECORDER_MODEL, (
            "the recorder's work was observed under another label and belongs to "
            f"its slot: {by_slot['recorder']}"
        )
        assert "ingest" not in by_slot, (
            f"a label the harness used was published as an agent of its own: {slots}"
        )

        # Every row carries the plan beside the observation, and the two are
        # kept apart: the plan says what the slot was asked for and the
        # observation says what was seen.
        assert local_review.assigned_map(reviewers) == _expected_assigned(), (
            f"the plan was lost: {local_review.assigned_map(reviewers)}"
        )
        # The run assigned the workers a model too, and that is the plan rather
        # than the panel. A published map that grew by two would say the review
        # was written by thirteen agents.
        assert local_review.assigned_map(rows) == _planned_models(), (
            f"a worker's assignment was lost from the run's own plan: {rows}"
        )

        models = local_review.model_map(reviewers)
        assert models == _expected_models(), f"the model map is wrong: {models}"
        assert local_review.model_phrase(models) == EXPECTED_MODEL_PHRASE, (
            f"the model counts are wrong: {local_review.model_phrase(models)}"
        )
        assert local_review.model_phrase({}) == "models the run did not record", (
            "a run with no model map must say so rather than name one"
        )

        # A run whose harness record is nothing but placeholders still has the
        # protocol's own slots, and the one model only the harness knew is gone
        # from the map, so a record built from it says nothing about the slot
        # that never reported one. The plan for that slot survives, because the
        # plan was written before anything ran, and it is never promoted into
        # the observed map to fill the hole.
        unnamed = _run_directory(
            Path(tmp) / "unnamed",
            **{
                "runtime.json": _runtime(
                    TRACKS, agents=[{"label": f"agent-{index}"} for index in range(5)]
                )
            },
        )
        placeholders = local_review.agent_rows(local_review.engine_reading(unnamed))
        assert len(placeholders) == 13, (
            f"the protocol's own slots are still agents: {placeholders}"
        )
        observed = local_review.model_map(local_review.reviewing_agents(placeholders))
        assert "recorder" not in observed, (
            f"the recorder's model is only known from the harness: {observed}"
        )
        assert local_review.assigned_map(placeholders)["recorder"] == RECORDER_MODEL, (
            "the plan is written before the run and survives a harness record "
            f"that observed nothing: {local_review.assigned_map(placeholders)}"
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
                "issues.json": dict(PACKAGE),
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

        # A file under the same prefix that is not one of the six tracks stays
        # in the run folder. The reports were globbed, so anything an operator
        # or a later engine left beside them was copied into a public bundle
        # and shown on the page as a report with no track.
        for name in ("audit_notes.md", "audit_scratch-for-me.md", "audit_.md"):
            (run / name).write_text(f"# {name}\n\nNot a track report.\n", encoding="utf-8")
        published = local_review.track_reports(run)
        assert sorted(published) == sorted(f"audit_{track}.md" for track in TRACKS), (
            f"a file that is not a track report was published: {sorted(published)}"
        )

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
            assert "manifest.json" in str(error) and MAIN_DOCUMENT in str(error), (
                f"the refusal has to say what it wanted: {error}"
            )
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
    summary = local_review.render_summary(PAPER, READING, prov)
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

    def fields(value: object) -> list[str]:
        """The field trails only, so the assertions read as the shapes they test."""
        return [leak.where for leak in local_review.local_reference_fields(value)]

    assert fields({"a": {"b": "/home/someone/run"}}) == ["a.b"]
    assert fields({"u": "file:///home/someone"}) == ["u"]
    assert fields({"runs": [{"directory": "/tmp/x"}]}) == ["runs[0].directory"], (
        "a leak inside a list has to be named"
    )

    # Every shape a published record has leaked, each one in a field no list
    # here names, because the field name is what the scrubber works from and
    # this is the guard for the field it does not know.
    leaks = {
        "a mounted drive": "/mnt/data1/papers/draft.pdf",
        "a temporary directory": "/tmp/claude-1000/session/run",
        "a home-relative path": "~/papers/x.pdf",
        "a Windows path": r"C:\Users\someone\papers\x.pdf",
        "a Windows path with forward slashes": "D:/papers/x.pdf",
        "an email address": "someone@example.org",
    }
    for why, value in leaks.items():
        assert fields({"generator": {"note_the_engine_just_added": value}}) == [
            "generator.note_the_engine_just_added"
        ], f"{why} reached a published record: {value}"

    # And the shapes that are not leaks. A DOI link and an archive URL are the
    # record's own content, a relative path names something a reader has, and a
    # reviewer's arithmetic is a sentence rather than a path.
    kept = {
        "a relative path": "docs/reviews/2026/p/v1/r1",
        "an archive URL": "https://arxiv.org/abs/2501.01234",
        "a DOI URL": "https://www.biorxiv.org/content/10.1101/2026.03.12.711120v1.full.pdf",
        "a DOI": "10.1101/2026.03.12.711120",
        "arithmetic": "the denominator should be n/2 and/or the paired count",
        "a version range": "0.9.0/0.9.1",
    }
    for why, value in kept.items():
        assert fields({"field": value}) == [], f"{why} was refused as a local path: {value}"

    # The whole record, built from a run whose manifest carries the absolute
    # manuscript path and plugin root the plugin server writes into it.
    with _stub_engine():
        record = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=True)
        )
    assert local_review.local_reference_fields(record) == [], (
        f"the record names the machine that wrote it: "
        f"{local_review.local_reference_fields(record)}"
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
    unread = provenance_fixture()
    unread["generator"]["attestation"]["human_reviewed_before_merge"] = False
    unread["generator"]["attestation"]["rehearsal"] = True
    unread["generator"]["attestation"]["statement"] = local_review.UNREAD_STATEMENT

    summary = local_review.render_summary(PAPER, READING, unread)
    letter = local_review.render_decision_letter(PAPER, READING, unread)
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
    attested = local_review.render_summary(PAPER, READING, provenance_fixture())
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

    issues.json is copied out of the run as it stands, and a run folder records
    absolute paths in several places: the plugin server writes the manuscript's
    path as `pdf` and the loaded plugin's as `plugin_root`, each evidence memo
    at `memo_path`, and a figure map is keyed by the absolute path of every
    figure. Those are the leaks. `source_review_path` is in the list and in
    this fixture although 0.10 writes no such field, because the list is what
    the publish path refuses to carry and a field that stops being written is
    not a field that stops being a path.

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
            {"slot": "core-1", "source_review_path": f"{home}/runs/out/core-1/report.json"},
            {"slot": "core-2", "source_review_path": f"{home}/runs/out/core-2/report.json"},
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

    # The figure map is keyed by the absolute path of every figure, and that key
    # is refused rather than dropped: publishing an artifact missing an entry the
    # engine wrote is not this script's call to make. The refusal names the key,
    # and check_a_path_shaped_key_is_refused_rather_than_published_without_it
    # covers the flag that publishes such a key deliberately.
    figure_key = f"{home}/runs/fig1.png"
    try:
        local_review.without_local_paths(leaky)
    except local_review.CommandError as refusal:
        assert figure_key in str(refusal), f"the refusal did not name the key: {refusal}"
    else:
        raise AssertionError("a path used as a field name was dropped with its value")

    scrubbed = local_review.without_local_paths(
        {name: value for name, value in leaky.items() if name != "synthesis_provenance"}
    )

    # The review's own words, first. Scrubbing by value rather than by field
    # deleted a finding whose comment opened with a slash, and aborted the
    # publish on the one that only mentioned a path.
    assert scrubbed["findings"] == leaky["findings"], (
        f"a reviewer's own comments were rewritten: {scrubbed['findings']}"
    )
    assert scrubbed["summary"] == leaky["summary"], "the review's own words were altered"
    assert scrubbed["reference"] == leaky["reference"], "a URL is not a local path"
    assert scrubbed["notes"] == leaky["notes"], "ordinary prose was altered"

    # Then the fields the engine really fills with a path.
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

    # A path inside this repository is still a path, but it names something a
    # reader has, so it is rewritten rather than dropped.
    inside = local_review.without_local_paths(
        {"source_review_path": str(local_review.REPO / "runs" / "local")}
    )
    assert inside == {"source_review_path": "runs/local"}, (
        f"a repository path should be made relative: {inside}"
    )

    # And the bundle is scanned as a bundle, in every text file, for anything
    # that names the machine rather than the review. This machine's own two
    # directories are named exactly, on top of the shapes.
    facts = local_review.machine_facts(run_dir=Path(home) / "runs" / "local" / "review")
    for why, value in (
        ("the checkout", str(local_review.REPO.resolve())),
        ("the home directory", home),
        ("the run folder", f"{home}/runs/local/review"),
    ):
        assert any(fact.pattern.search(value) for fact in facts), (
            f"{why} has to be one of the facts this machine is known by: {value}"
        )

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        (dest / "provenance.json").write_text(json.dumps({"review": {"id": "p/v1/r1"}}), encoding="utf-8")
        (dest / "summary.md").write_text(
            "# Review Summary\n\nThe denominator should be n/2, and the DOI is "
            "https://doi.org/10.1101/2026.03.12.711120.\n",
            encoding="utf-8",
        )
        assert local_review.bundle_local_path_leaks(dest) == [], (
            "a clean bundle must not be reported as leaking"
        )

        # Each shape on its own, in a file of its own, because the scan knowing
        # this machine's home directory is not the same as the scan knowing
        # what a path looks like. All of these published in a reviewer's probe.
        shapes = {
            "letter_mount.md": "The figures are in /mnt/data1/papers/draft.pdf.\n",
            "letter_tmp.md": "Run written to /tmp/claude-1000/session/run.\n",
            "letter_home.md": "The manuscript is ~/papers/x.pdf.\n",
            "letter_windows.md": "Copied from C:\\Users\\someone\\papers.\n",
            "letter_email.md": "Correspondence to someone@example.org.\n",
        }
        for name, text in shapes.items():
            (dest / name).write_text(text, encoding="utf-8")
        shaped = local_review.bundle_local_path_leaks(dest)
        for name in shapes:
            assert any(leak.where.startswith(name) for leak in shaped), (
                f"{name} published something that names the machine: "
                f"{[leak.line for leak in shaped]}"
            )
        for name in shapes:
            (dest / name).unlink()

        # The forms the old scan could not see: a path inside a sentence in the
        # Markdown, a path used as a key, a path in a specialist report copied
        # out of the run, and a path in a nested receipt file.
        (dest / "decision_letter.md").write_text(
            f"The reviewer read {home}/runs/out/core-1.\n", encoding="utf-8"
        )
        (dest / "issues.json").write_text(
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
        lines = [leak.line for leak in found]
        assert len(found) == 4, f"every text file in the bundle has to be read: {lines}"
        for name, why in (
            ("decision_letter.md", "the rendered Markdown was not scanned"),
            ("issues.json", "a path used as a key was not seen"),
            ("audit_stats.md", "a specialist report copied out of the run was not scanned"),
            ("attachments/runtime.json", "a nested receipt was not scanned"),
        ):
            assert any(leak.where.startswith(name) for leak in found), f"{why}: {lines}"


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
            (run / "issues.json").write_text(
                json.dumps(
                    {
                        "schema_version": ISSUES_SCHEMA,
                        "issues_source": "editor",
                        "summary": "A reading.",
                        "issues": [],
                    }
                ),
                encoding="utf-8",
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
    dropped from issues.json was printed in decision_letter.md, where nothing
    was looking. This publishes for real, with the field names engine 0.10
    writes, and reads every file of the finished bundle, including the
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
            run = _run_directory(Path(tmp) / "run", **{"issues.json":package})
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
            published = json.loads(
                (destination / local_review.REVIEW_ISSUES).read_text(encoding="utf-8")
            )
            assert [i["id"] for i in published["issues"]] == [i["id"] for i in ISSUES], (
                f"an issue was dropped or reordered on the way out: {published['issues']}"
            )
            assert sorted(f["comment"] for f in published["findings"]) == sorted(
                row["comment"] for row in LEDGER
            ), f"a finding was rewritten or dropped on the way out: {published['findings']}"
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
            assert round_record["required_revisions"][0]["finding_uids"] == ["f-001"], (
                f"the round record lost the finding: {round_record['required_revisions']}"
            )

            # And a path in a field nothing here knows about refuses, leaving
            # the published tree as it found it. The field is inside an issue,
            # because an issue is published whole: a stray key beside the
            # document is dropped with everything else the engine's reading does
            # not carry, and would prove nothing about the guard.
            unknown = reviews / "2026" / "fixture-paper" / "v1" / "r2"
            second_run = _run_directory(
                Path(tmp) / "run-2",
                **{
                    "issues.json": dict(
                        package,
                        issues=[
                            dict(ISSUES[0], evidence_log=f"{home}/runs/out/log.txt"),
                            *ISSUES[1:],
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


# The account of the Read stage this suite publishes against, written into the
# manifest by hand. No model ran: engine 0.10's reader looks at the page images
# of a real paper, and nothing in this repository calls a model. What is being
# checked is what a bundle says about a manuscript a model read, which is a
# property of the publish path and not of the reader.
READER_ACCOUNT = {
    "read": True,
    "reader_model": OPUS,
    "reader_slot": "reader",
    "attempt": 1,
    "pages": 4,
    "pages_viewed": 4,
    "actions": {"repaired": 1, "confirmed": 6, "merged": 0, "described": 1, "added": 2},
    "tool_calls": 11,
    "lost_pages": [{"page": 4, "words": 0, "rotation": 0, "added": ["p-21", "p-23"]}],
}

# The same account in the shape a published record carries it, for the checks
# that build a record with no workspace behind them. `ingest_record` reads this
# off the folder the engine wrote, and `check_a_bundle_says_which_lines_a_model
# _wrote` publishes for real and compares the two, so what is typed here cannot
# quietly become a shape the publish path does not produce. The one value with
# nothing behind it is the base schema name, which that same check reads off
# the installed engine instead.
INGEST_READ = {
    "base_schema_version": "paper-base-v2",
    "ai_read": {
        **{name: value for name, value in READER_ACCOUNT.items() if name != "lost_pages"},
        "lost_pages": [
            {"page": page["page"], "pieces": len(page["added"]), "words": page["words"]}
            for page in READER_ACCOUNT["lost_pages"]
        ],
    },
    "pieces_per_source": {
        "text": len(PAPER_PIECES) - len(PIECE_SOURCE),
        **{
            source: sum(1 for row in PIECE_SOURCE.values() if row["source"] == source)
            for source in sorted({row["source"] for row in PIECE_SOURCE.values()})
        },
    },
    "source_values": {
        "text": "the converter's own text layer",
        "ai": "written by a model reading the page image",
        "ai-reconstructed": "a model's repair of a line the converter misread",
    },
    "model_written": [
        {
            "document": MAIN_DOCUMENT,
            "lines": [line, line],
            "kind": row["kind"],
            "source": row["source"],
            "page": row["page"],
        }
        for line, row in sorted(PIECE_SOURCE.items())
    ],
}


def check_a_bundle_says_which_lines_a_model_wrote() -> None:
    """A review of a read manuscript has to say what the model wrote into it.

    Engine 0.10 puts a model between the converter and the panel. It rewrites
    an equation the converter mangled, writes a description under every figure
    and transcribes a page the converter returned nothing from, and only then is
    the manuscript sealed. Every one of those lines is quotable, cited by line
    number like any other and printed in the letter in the same type.

    So a bundle that published only the character count and a digest would be
    publishing a review of a text it did not describe. Two facts are owed to
    anyone reading it: which lines of the manuscript a model wrote, which is
    what makes a quotation checkable against the list, and which pages of the
    paper exist in the review only because a model read them off an image.
    Both are published here from the import's own files.

    The account of the stage is a whitelist of the engine's fields rather than
    a copy of its object. A release that put a path in it would otherwise
    publish this machine's directories, which is the one thing a bundle may
    never carry, so the fixture puts a path there and the bundle is read back.
    """
    leaky = dict(READER_ACCOUNT, reader_log=f"{Path.home().resolve()}/runs/read.json")
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run")
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            prepared = _prepared(Path(tmp) / "prepared", destination)
            workspace = _workspace(Path(tmp) / "workspace", read=leaky)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(prepared, run, workspace, "--publish")
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"

            record = json.loads((destination / "provenance.json").read_text(encoding="utf-8"))
            ingest = record["ingest"]
            assert ingest["base_schema_version"] == local_review.engine_public(
                "BASE_SCHEMA_VERSION", "the base schema version cannot be read"
            ), f"the shape of the imported manuscript was not published: {ingest}"

            read = ingest["ai_read"]
            assert read["read"] is True and read["reader_model"] == OPUS, (
                f"the model that read the pages was not published: {read}"
            )
            assert read["pages_viewed"] == 4, f"what the reader looked at was dropped: {read}"
            assert [row["page"] for row in read["lost_pages"]] == [4], (
                f"a page the converter returned nothing from was not published: {read}"
            )
            assert "reader_log" not in read, (
                f"a field this release does not publish by name reached a bundle: {read}"
            )

            # The per-line facts, which are what a quotation can be checked
            # against. The counts come from the import and the lines from the
            # map it wrote over the file, and the two are published separately
            # because a tally cannot say which line to look at.
            assert ingest["pieces_per_source"]["ai"] == 1, (
                f"the pieces a model wrote were not counted: {ingest['pieces_per_source']}"
            )
            assert ingest["pieces_per_source"]["ai-reconstructed"] == 1, (
                f"a repaired piece was counted as the converter's: {ingest['pieces_per_source']}"
            )
            written = {row["lines"][0]: row for row in ingest["model_written"]}
            assert sorted(written) == [DESCRIPTION_LINE, EQUATION_LINE], (
                f"the lines a model wrote were not published: {ingest['model_written']}"
            )
            assert written[DESCRIPTION_LINE]["source"] == "ai", (
                f"a description written from an image is not the converter's: {written}"
            )
            assert written[EQUATION_LINE]["source"] == "ai-reconstructed", (
                f"a repaired equation is not reported as repaired: {written}"
            )
            assert written[EQUATION_LINE]["kind"] == "equation", (
                f"what kind of piece a model wrote was dropped: {written}"
            )

            # And the same facts in the document a person reads, because a
            # reader of the review is owed them in words rather than in a field
            # of a JSON file nobody opens.
            stats = (destination / "manuscript_stats.md").read_text(encoding="utf-8")
            assert OPUS in stats, f"the statistics page does not name the reader: {stats}"
            assert f"line {DESCRIPTION_LINE}" in stats and f"line {EQUATION_LINE}" in stats, (
                f"the statistics page does not say which lines a model wrote: {stats}"
            )
            assert "Pages the converter returned no text from at all: 4" in stats, (
                f"a page that reached the review only through a model is unnamed: {stats}"
            )
            assert local_review.bundle_local_path_leaks(destination) == [], (
                "the account of the Read stage carried a path into the bundle"
            )

    # A manuscript nothing read says so as plainly, which is the shape every
    # other check in this suite publishes: the equations in it are a converter's
    # reading of a picture and no figure has a description behind it.
    with tempfile.TemporaryDirectory() as tmp:
        unread = _workspace(Path(tmp) / "workspace")
        ingest = local_review.ingest_record(unread)
        assert ingest["ai_read"]["read"] is False, (
            f"a manuscript no model read was published as read: {ingest['ai_read']}"
        )
        assert ingest["ai_read"]["lost_pages"] == [], (
            f"a workspace with no reader cannot name a lost page: {ingest['ai_read']}"
        )
        said = local_review.render_read_stage(ingest)
        assert any("No model read the pages" in row for row in said), (
            f"the statistics page is silent about a manuscript nothing read: {said}"
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
    assert version >= (0, 10), (
        f"the lock pins peerreviewagents {locked}. The plugin, the commands and the "
        "run folder this repository reads are the 0.10 ones, and an issues document "
        "is not a file an earlier release writes"
    )


def _engine_imports(path: Path) -> list[tuple[str, tuple[str, ...]]]:
    """Every engine module a script imports, with the names it takes from each.

    Read from the syntax rather than from the text, so a module named in a
    docstring or in a refusal message is not mistaken for an import of it. A
    dynamic `importlib.import_module("...")` counts, because that is how this
    repository imports the engine at all.
    """
    taken: list[tuple[str, tuple[str, ...]]] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            taken += [(alias.name, ()) for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            taken.append((node.module, tuple(alias.name for alias in node.names)))
        elif isinstance(node, ast.Call):
            called = node.func
            name = called.attr if isinstance(called, ast.Attribute) else getattr(called, "id", "")
            if name in ("import_module", "__import__"):
                taken += [
                    (argument.value, ())
                    for argument in node.args
                    if isinstance(argument, ast.Constant) and isinstance(argument.value, str)
                ]
    package = local_review.ENGINE_PACKAGE
    return [pair for pair in taken if pair[0].split(".")[0] == package]


def _engine_public_names(path: Path) -> set[str]:
    """The names a script asks `engine_public` for, which are engine names too.

    The publish path takes nothing from the engine at import time, because the
    engine is optional on a laptop and a missing one has to be a refusal with a
    sentence in it rather than an ImportError at startup. So it resolves each
    name it needs through `engine_public`, and the name is the string argument.
    """
    asked: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Call):
            continue
        called = node.func
        name = called.attr if isinstance(called, ast.Attribute) else getattr(called, "id", "")
        if name != "engine_public" or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            asked.add(first.value)
    return asked


def check_nothing_reaches_into_the_engines_internals() -> None:
    """Every engine name these scripts use comes off the package's own surface.

    The publish path and the two static checks used to import
    `peerreviewagents.plugin.starter` and `peerreviewagents.cli.main` for the
    plugin directory, the Claude Code version and the two argument parsers.
    Those are the engine's internals, free to move between releases, so an
    upgrade that renamed a private module broke a check here rather than
    telling us the engine's supported surface had changed. 0.10 exports all of
    them, so there is nothing left to reach for: `plugin_directory`,
    `claude_code_version`, `review_parser`, `report_parser` and `CLI_COMMANDS`
    are on `peerreviewagents.__all__` beside `read_run`.

    What this proves is that no script went back. Imports are read from the
    syntax of every file under scripts/, the module has to be the package
    itself, and each name taken from it has to be one the installed engine
    exports, which is checked against the real `__all__` when the engine is
    importable here.

    One allowance, for one file and one module. `fixtures/make_engine_rounds.py`
    builds its two run folders by calling `peerreviewagents.plugin.server`,
    which is the plugin an agent session calls and not a supported surface. The
    public way to produce a run folder is `review`, which starts a Claude Code
    session and spends a subscription on a model, so it is not something a check
    can run. The alternative is not a public API, it is a run folder typed out
    by hand, which is the thing that generator exists to replace: a fixture
    written here can only ever agree with what this repository believes the
    engine writes. So the private import buys a fixture the engine wrote, the
    allowance names the one file and the one module, and the check below fails
    if the allowance ever stops being used, so it cannot quietly cover a file
    that no longer needs it.
    """
    root = Path(local_review.__file__).resolve().parent
    package = local_review.ENGINE_PACKAGE
    sources = (
        sorted(root.glob("*.py"))
        + sorted((root / "smoke_checks").glob("*.py"))
        + sorted((root / "fixtures").glob("*.py"))
    )
    assert len(sources) > 10, f"the scripts were not found under {root}"
    assert root / "fixtures" / "make_citation_ledger.py" in sources, (
        "the fixture generators are scripts too, and the generator that used to "
        "hold the one allowance is a file this scan has to be reading"
    )

    # The one allowance: this file, this module, this name, and nothing else.
    allowed_private = {"make_engine_rounds.py": (f"{package}.plugin", ("server",))}
    used = set()

    private = {}
    names: set[str] = set()
    for path in sources:
        for module, taken in _engine_imports(path):
            if module == package:
                names.update(taken)
            elif allowed_private.get(path.name) == (module, taken):
                # `server` is a module inside the plugin and not a public name,
                # so it is not one of the names checked against `__all__` below.
                used.add(path.name)
            else:
                private.setdefault(path.name, []).append(module)
        names.update(_engine_public_names(path))
    assert used == set(allowed_private), (
        "the allowance to import the engine's plugin covers "
        f"{sorted(set(allowed_private) - used)}, which no longer imports it. An "
        "allowance nobody uses is one the next file inherits by accident: take it out."
    )
    assert not private, (
        "these scripts import the engine's internals rather than its public "
        f"surface: {private}. Every name 0.10 supports is on {package}.__all__."
    )
    expected = {
        "CLI_COMMANDS",
        "claude_code_version",
        "plugin_directory",
        "read_citation_ledger",
        "read_run",
        "report_parser",
        "review_parser",
    }
    assert expected <= names, (
        "the public names this repository runs on are no longer taken from the "
        f"engine: {sorted(expected - names)} missing from {sorted(names)}"
    )
    if not engine_is_importable():
        print(f"    (the {package}.__all__ half needs the engine and was not run)")
        return
    exported = set(getattr(__import__(package), "__all__", ()))
    assert exported, f"{package} exports no public surface at all"
    missing = sorted(names - exported)
    assert not missing, (
        f"these scripts import {missing} from {package}, which the installed "
        "release does not export. Either the name moved or the lock is wrong."
    )


def check_a_review_of_a_detection_paper_publishes() -> None:
    """The same two guards, through publish, on a run that reads like a real one.

    The findings talk about `mAP@0.5`, dose per kilogram per day, a matrix entry
    and a map in set notation, and quote the author address printed in the
    manuscript. All of it published before the scan was narrowed only because no
    reviewer had written it yet, and all of it has to publish now.

    Then the leak, in the one place the old scan could not see it: a Windows
    path inside a list inside the evidence under an issue, where JSON doubles
    the backslash. That bundle is refused and nothing is written.
    """
    home = str(Path.home().resolve())
    notation = dict(
        PACKAGE,
        stages=_stages(TRACKS),
        summary=(
            "Detection improves to mAP@0.5 of 0.71, and IoU@0.75 is the wrong "
            "operating point for the claim in the abstract."
        ),
        limitations=[
            "The dose is reported as 5 mg /kg/day, and the incidence as 3.1 "
            "(events)/person/year, so the two tables cannot both be right.",
            r"The map $f:\mathbb{R}$ is assumed continuous, and E:/Z is undefined.",
        ],
        issues=[
            dict(
                ISSUES[0],
                statement=(
                    "The interval cannot be read off mAP@0.5 and the per-class "
                    "counts. Correspondence to a.author@univ.example.edu asks "
                    "for the alignment files, and /etc/hosts is the convention "
                    "they cite."
                ),
            ),
            *ISSUES[1:],
        ],
    )
    # A paper of its own for this check, because the address the review quotes
    # has to be in the manuscript for the scan to read it as the paper's.
    pieces = [
        {"kind": "title", "section": "Front matter", "text": "A detection paper"},
        {
            "kind": "paragraph",
            "section": "Methods",
            "text": "Correspondence to a.author@univ.example.edu.",
        },
    ]

    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run", **{"issues.json":notation})
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            workspace = _workspace(Path(tmp) / "workspace", pieces=pieces)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    workspace,
                    "--publish",
                )
            assert code == 0, (
                f"a review that discusses a detection metric has to publish, got exit {code}: "
                f"{out.getvalue()}"
            )
            letter = (destination / "decision_letter.md").read_text(encoding="utf-8")
            assert "mAP@0.5" in letter, "the reviewer's own metric did not reach the letter"

            # And the leak, nested where a text scan of the file cannot see it.
            nested = reviews / "2026" / "fixture-paper" / "v1" / "r2"
            leaking = dict(
                notation,
                issues=[
                    dict(
                        ISSUES[0],
                        members=[
                            dict(
                                ISSUES[0]["members"][0],
                                where=["ok", "C:\\Users\\someone\\runs\\out\\core-1.json"],
                            ),
                            *ISSUES[0]["members"][1:],
                        ],
                    ),
                    *ISSUES[1:],
                ],
            )
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                refused = _publish(
                    _prepared(Path(tmp) / "prepared-2", nested, attempt=2),
                    _run_directory(Path(tmp) / "run-2", **{"issues.json":leaking}),
                    workspace,
                    "--publish",
                )
            message = stderr.getvalue()
            assert refused == 2, f"a path nested under an issue should refuse, got {refused}"
            assert not nested.exists(), f"a refused publish left a bundle at {nested}"
            assert "Nothing was written" in message, (
                f"the refusal has to say the tree was left alone: {message!r}"
            )


def _corpus_gate_leaks(record: object, waived: tuple[str, ...], trail: str = "") -> list[str]:
    """The rule scripts/check_local_provenance.mjs applies to docs/reviews.

    That gate walks every published provenance.json and refuses a string value
    that begins with a slash or with `file://`, whatever key it sits under. A
    recorded allowance is such a string by definition, so a publish with
    `--allow-text` wrote a bundle the repository's own gate rejected. The gate
    now takes the allowances out of each string before it looks, and this is the
    same rule in Python, applied to the record a publish just wrote, so the two
    cannot drift apart without one of them failing.
    """
    if isinstance(record, str):
        rest = record
        for text in waived:
            rest = rest.replace(text, "")
        return [f"{trail} = {record}"] if rest.startswith(("/", "file://")) else []
    if isinstance(record, list):
        return [
            leak
            for index, item in enumerate(record)
            for leak in _corpus_gate_leaks(item, waived, f"{trail}[{index}]")
        ]
    if isinstance(record, dict):
        return [
            leak
            for key, item in record.items()
            for leak in _corpus_gate_leaks(item, waived, f"{trail}.{key}" if trail else str(key))
        ]
    return []


def check_an_editor_can_publish_a_hit_the_review_meant_and_never_a_fact() -> None:
    """Round after round, a reviewer's own words were refused as a path.

    `R:/G/B channel order` and `E:/I/G ratio` are a drive letter followed by
    path segments and there is no rule that tells them from one. Every earlier
    answer was a narrower regular expression, and the next review found another
    sentence it refused. So tier 2 has a valve: the editor reads the refusal,
    sees the matched text and the flag to copy, and publishes it deliberately.
    The allowance is recorded in the provenance record, where a reader of the
    page can see what was allowed and decide what to make of it.

    The valve never reaches tier 1. A fact about this machine is looked up
    rather than recognised, so there is nothing for an editor to judge: it is
    the operator's home directory either way.
    """
    home = str(Path.home().resolve())
    package = dict(
        PACKAGE,
        stages=_stages(TRACKS),
        issues=[
            dict(
                ISSUES[0],
                statement="The R:/G/B channel order is never stated, so panel c cannot be read.",
            ),
            *ISSUES[1:],
        ],
    )

    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run", **{"issues.json":package})
            workspace = _workspace(Path(tmp) / "workspace")
            refused_at = reviews / "2026" / "fixture-paper" / "v1" / "r1"

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", refused_at), run, workspace, "--publish"
                )
            message = stderr.getvalue()
            assert code == 2, f"a path-shaped phrase is refused first, got exit {code}"
            assert not refused_at.exists(), f"a refused publish left a bundle at {refused_at}"
            assert "--allow-text=R:/G/B" in message, (
                f"the refusal has to print the flag to copy: {message!r}"
            )
            assert "recorded in the provenance record" in message, (
                f"the refusal has to say the allowance is published: {message!r}"
            )

            # The same run, published with the allowance. The text reaches the
            # bundle as the reviewer wrote it and the record says it was allowed.
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r2"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-2", destination, attempt=2),
                    run,
                    workspace,
                    "--publish",
                    "--allow-text",
                    "R:/G/B",
                )
            assert code == 0, (
                f"an allowed hit has to publish, got exit {code}: {out.getvalue()}"
            )
            letter = (destination / "decision_letter.md").read_text(encoding="utf-8")
            assert "R:/G/B channel order" in letter, (
                "the allowed text has to reach the letter as the reviewer wrote it"
            )
            record = json.loads((destination / "provenance.json").read_text(encoding="utf-8"))
            assert record["review"].get("allowed_text") == ["R:/G/B"], (
                f"the allowance is not in the record: {record['review'].get('allowed_text')!r}"
            )
            review_schema.assert_valid_provenance(record, source="allowed")
            # A record this path writes has to survive the gate that reads the
            # published corpus, allowance and all.
            allowance = tuple(record["review"]["allowed_text"])
            assert not _corpus_gate_leaks(record, allowance), (
                "a published record carrying an allowance must pass "
                "scripts/check_local_provenance.mjs: "
                f"{_corpus_gate_leaks(record, allowance)}"
            )
            assert _corpus_gate_leaks({"deposited": "/srv/public/set"}, allowance), (
                "the mirrored rule has to see a path the allowance does not name, "
                "or it is asserting nothing"
            )

            # And the fact, with the flag that names it exactly. The flag is
            # read before the scan runs, so what is refused is the allowance,
            # and the reason names the allowance rather than the finding.
            leaking = dict(
                package,
                issues=[
                    dict(
                        ISSUES[0],
                        statement=f"The reviewer read the draft at {home}/papers/draft.pdf.",
                    ),
                    *ISSUES[1:],
                ],
            )
            nested = reviews / "2026" / "fixture-paper" / "v1" / "r3"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-3", nested, attempt=3),
                    _run_directory(Path(tmp) / "run-3", **{"issues.json":leaking}),
                    workspace,
                    "--publish",
                    "--allow-text",
                    f"{home}/papers/draft.pdf",
                )
            message = stderr.getvalue()
            assert code == 2, f"no flag waives this machine's own home directory, got {code}"
            assert not nested.exists(), f"a refused publish left a bundle at {nested}"
            assert "An allowance may not contain anything that names this machine" in message, (
                f"the refusal has to say why the flag did not apply: {message!r}"
            )
            assert f"{home}/papers/draft.pdf" in message, (
                f"the refusal has to quote the allowance it rejected: {message!r}"
            )

            # An allowance that wraps a fact in something else is rejected on
            # the same terms: `file:///` in front of a checkout path was what
            # got one past the flag check, because the check matched the whole
            # allowance against a fact rather than looking inside it.
            wrapped = reviews / "2026" / "fixture-paper" / "v1" / "r4"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = _publish(
                    _prepared(Path(tmp) / "prepared-4", wrapped, attempt=4),
                    run,
                    workspace,
                    "--publish",
                    f"--allow-text=file:///{local_review.REPO}/scripts/local_review.py",
                )
            assert code == 2, f"a wrapped fact waived through the flag, got {code}"
            assert not wrapped.exists(), f"a refused publish left a bundle at {wrapped}"
            assert "An allowance may not contain anything that names this machine" in (
                stderr.getvalue()
            ), f"the refusal has to name the allowance: {stderr.getvalue()!r}"


def check_a_draft_check_run_is_refused_as_the_arm_it_is() -> None:
    """A draft check published as a peer review, and nothing said otherwise.

    `draft-check` is what the engine runs on a draft of your own: chosen
    specialists, no core track, no editor, and nobody outside the authorship
    reads the paper. The engine does not call it unpublishable, because it is a
    perfectly good run of that arm, so the only thing standing between it and
    docs/reviews was the reviewer count, which refused it as a thin review
    rather than as the wrong kind of run. A reader of that refusal would have
    gone looking for a missing reviewer.
    """
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(
                Path(tmp) / "run",
                **{
                    "protocol.json": _protocol(
                        mode="draft-check", arm="draft-check", reviewers=0
                    ),
                    "progress.json": _progress(arm="draft-check", reviewers=0),
                },
            )
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            message = stderr.getvalue()
            assert code == 2, f"a draft check must not publish as a review, got exit {code}"
            assert not destination.exists(), f"a refused publish left a bundle at {destination}"
            assert "draft-check" in message, (
                f"the refusal has to name the arm that ran: {message!r}"
            )
            assert "reviewers" not in message.split("draft-check")[0], (
                f"the arm is refused before the reviewer count, not through it: {message!r}"
            )


def check_a_record_the_schema_refuses_is_never_written() -> None:
    """A guard value the engine cannot write published with exit 0.

    `npm run check:schema` is the gate on the repository and it runs after the
    fact, so a record carrying a word the schema does not list was written into
    the published tree and caught later, leaving a bundle to delete by hand.
    `review_guard_status` is the case in hand: `read_run` reports whatever the
    run recorded, publish copies it into the record, and the schema allows only
    `clean` and `quarantined`.

    Publish validates the record against that schema before it writes anything.
    """
    with _stub_engine():
        record = local_review.build_provenance(
            **_build_arguments(editor="fixture-editor", human_reviewed=True, publishing=True)
        )
    review_schema.assert_valid_provenance(record, source="fixture")

    broken = json.loads(json.dumps(record))
    broken["generator"]["run"]["review_guard_status"] = "partially-quarantined"
    try:
        review_schema.assert_valid_provenance(broken, source="fixture")
    except review_schema.InvalidProvenance as refusal:
        assert "review_guard_status" in str(refusal), f"the refusal has to name the field: {refusal}"
    else:
        raise AssertionError("a guard status the schema does not list was accepted")

    # A keyword the validator does not implement stops it rather than passing
    # quietly, because a validator that ignores what it cannot read reports a
    # record sound that nobody checked.
    try:
        review_schema.provenance_problems(
            {"schema_version": 4}, {"type": "object", "dependentRequired": {"a": ["b"]}}
        )
    except review_schema.UnsupportedSchema as stopped:
        assert "dependentRequired" in str(stopped), f"it has to name the keyword: {stopped}"
    else:
        raise AssertionError("an unsupported schema keyword was quietly ignored")

    # And through publish, with the word in the run rather than in the record:
    # nothing is written, and the refusal says so.
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            run = _run_directory(
                Path(tmp) / "run",
                **{
                    "progress.json": {
                        "status": "complete",
                        "error": "",
                        "reviewers": 3,
                        "arm": "full-two-track",
                        "stages": _stages(TRACKS),
                        "findings_delivered": 6,
                        "quarantined_findings_count": 0,
                        "review_guard_status": "partially-quarantined",
                        "tool_calls": _tool_calls(TRACKS),
                        "tool_calls_total": sum(_tool_calls(TRACKS).values()),
                        "started": STARTED_AT,
                        "updated": "2026-11-11T12:31:00+00:00",
                    },
                    "issues.json": dict(
                        PACKAGE,
                        stages=_stages(TRACKS),
                        review_guard_status="partially-quarantined",
                    ),
                },
            )
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            message = stderr.getvalue()
            assert code == 2, f"a record the schema refuses must not publish, got exit {code}"
            assert not destination.exists(), f"a refused publish left a bundle at {destination}"
            assert "review_guard_status" in message, (
                f"the refusal has to name the field that failed: {message!r}"
            )
            assert "Nothing was written" in message, (
                f"the refusal has to say the tree was left alone: {message!r}"
            )


# Ordinary review text, every line of it refused by the first version of the
# leak scan. A specialist reader writes like this, so each one has to publish.
REVIEW_TEXT = (
    "detection improves to mAP@0.5 of 0.71, which the abstract rounds up",
    "IoU@0.75 is the wrong operating point for this claim",
    "the incidence is 3.1 (events)/person/year, not per month",
    "the dose is reported as 5 mg /kg/day for six weeks",
    r"the map $f:\mathbb{R}$ is assumed continuous and never shown to be",
    "the matrix entry E:/Z is left undefined in equation 4",
    "the hosts convention is the one /etc/hosts uses",
    "the earlier round is linked as [x](/reviews/2026/foo/v1)",
    "https://home/x resolves, so that URL is not a path",
    "docs/reviews/2026/paper/v1/r1 is where the last attempt sits",
    "the denominator should be n/2 and/or the paired count",
    # Round 3: each of these was refused by the boundaries the round-2 scan
    # used. A fraction after a tilde read as a home path, LaTeX environment
    # delimiters read as a Windows share, and a word ending in a letter before
    # `/tmp`, `/data` or a user name read as this machine's own directories.
    "~1/3 of the cohort responded to the second dose",
    r"the matrix \begin{pmatrix}1\\0\end{pmatrix} is never defined",
    r"\begin{matrix}a\\b\end{matrix} appears twice in section 3",
    "the temperature/tmp ratio in figure 2 is unlabelled",
    "the training/data/test split is never stated",
    r"the rotation is $2\pi$ radians rather than degrees",
    "the dataset they cite is https://doi.org/10.1000/tmp/abc",
)

# And the strings that are a leak whatever file they sit in.
LEAKING_TEXT = (
    "/mnt/data1/papers/draft.pdf",
    "/tmp/claude-1000/session/run",
    "~/papers/x.pdf",
    "~someone/papers/x.pdf",
    "$HOME/papers/x.pdf",
    "${HOME}/papers/x.pdf",
    "file:///var/tmp/draft.pdf",
    r"\\fileserver\share\papers",
    r"C:\Users\someone\papers\x.pdf",
    "D:/papers/drafts/x.pdf",
    "//home/someone/papers/x.pdf",
    "someone@example.org",
    # Round 3: each of these published. A lower-case drive letter, a drive
    # letter with forward slashes, the doubled backslashes a JSON file holds, a
    # path after a colon rather than at the start of the value, three roots the
    # list did not have, and an address with no domain name to look up.
    r"c:\Users\bob\x.pdf",
    "c:/Users/bob/x.pdf",
    r"C:\\Users\\bob\\x.pdf",
    "PATH=/usr/bin:/home/bob/bin",
    "host:/home/bob/x",
    "file:/home/bob/x.pdf",
    "/Volumes/Data/bob/x.pdf",
    "/scratch/bob/run1/x",
    "/users/bob/x",
    "/workspace/bob/x",
    "/nfs/bob/x",
    "bob@localhost",
    "bob@192.168.1.4",
    # And the two ways of writing a path that no longer look like one: percent
    # encoding, which a URL in a record carries, and the full-width slash,
    # which a copy through a document can leave behind.
    "%2Fhome%2Fbob%2Fx.pdf",
    "\uff0fhome\uff0fbob\uff0fx.pdf",
)

# The two tier-2 hits the editor is expected to allow rather than reword: a
# channel order and a ratio of two one-letter variables, which are a path shape
# and cannot be told apart from one by any rule.
OVERRIDDEN_TEXT = ("R:/G/B channel order", "E:/I/G ratio")


def check_ordinary_review_text_publishes_and_a_local_path_does_not() -> None:
    """The scan refused the review it was guarding.

    `mAP@0.5` and `IoU@0.75` read as mail addresses, `(events)/person/year` and
    `5 mg /kg/day` read as absolute paths, `E:/Z` and the `$f:\\mathbb{R}$` of a
    specialist's notation read as Windows paths, and an author address quoted
    from the paper read as a leak. Each of them made publish exit 2, so a review
    that discussed a detection metric could not be published at all, which is as
    broken as one that leaks a path.

    What is refused now is either an exact fact about this machine, looked up
    rather than recognised, or one of a few shapes that cannot be anything but a
    local path. A hit that appears verbatim in the manuscript is the paper's own
    text and is allowed, except for the facts, which no paper can waive.
    """
    # The manuscript as the scan is given it: the text of `paper.md`, which is
    # what `local_references` takes. Nothing is read out of it but the words.
    manuscript = (
        "# A short fixture manuscript\n"
        "\n"
        "Correspondence to a.author@univ.example.edu, data at /srv/public/set.\n"
    )
    facts = local_review.machine_facts(run_dir="/tmp/fixture-run/review")

    for text in REVIEW_TEXT:
        hits = local_review.local_references(text, facts=facts, manuscript=manuscript)
        assert hits == [], (
            f"ordinary review text was refused as a leak: {text!r} -> "
            f"{[leak.line for leak in hits]}"
        )

    for text in LEAKING_TEXT:
        hits = local_review.local_references(text, facts=facts, manuscript=manuscript)
        assert hits, f"a local path published: {text!r}"

    # The two hits an editor is meant to allow rather than reword. They are
    # refused by default and `--allow-text` is what lets them through, which is
    # the whole reason tier 2 only has to be sensible.
    for text in OVERRIDDEN_TEXT:
        assert local_review.local_references(text, facts=facts, manuscript=manuscript), (
            f"a path-shaped phrase has to be refused before it can be allowed: {text!r}"
        )
        hits = local_review.local_references(
            text, facts=facts, manuscript=manuscript, allowed=(text.split(" ")[0],)
        )
        assert hits == [], (
            f"--allow-text did not allow the text it names: {text!r} -> "
            f"{[leak.line for leak in hits]}"
        )

    # The refusal says the flag to copy, with the matched text quoted for a
    # shell, and says how many hits no flag can waive.
    refusal = local_review.leak_refusal(
        local_review.local_references("R:/G/B channel order", facts=facts)
        + local_review.local_references(f"{Path.home().resolve()}/x.pdf", facts=facts)
    )
    assert "--allow-text=R:/G/B" in refusal, (
        f"the refusal has to print the flag an editor can copy: {refusal!r}"
    )
    assert f"--allow-text={Path.home().resolve()}/x.pdf" not in refusal, (
        f"the refusal must not offer a flag for a fact about this machine: {refusal!r}"
    )
    # The `=` form rather than two arguments, because a hit can begin with a
    # hyphen and as a separate argument that reads as another option.
    hyphen = local_review.leak_refusal(
        local_review.local_references("write to -bob@example.org", facts=facts)
    )
    assert "--allow-text=-bob@example.org" in hyphen, (
        f"a hit that starts with a hyphen needs the = form: {hyphen!r}"
    )
    assert "1 of these name this machine itself" in refusal, (
        f"the refusal has to say how many hits nothing waives: {refusal!r}"
    )

    # The manuscript's own words, both ways round. The address printed in the
    # paper is allowed, the same shape that is not in the paper is not, and
    # `/srv/public/set` is a path the paper gives rather than one from here.
    for allowed in (
        "write to a.author@univ.example.edu for the alignment files",
        "the data they cite at /srv/public/set is not the set in table 2",
    ):
        hits = local_review.local_references(allowed, facts=facts, manuscript=manuscript)
        assert hits == [], f"the paper's own text was refused: {allowed!r} -> {hits}"
    assert local_review.local_references(
        "write to someone@example.org instead", facts=facts, manuscript=manuscript
    ), "an address the paper does not print is still a leak"

    # And the facts, refused even when the manuscript prints them, because a
    # paper that happens to name this operator's home directory does not make
    # it publishable from here.
    for why, value in (
        ("the home directory", f"{Path.home().resolve()}/papers/x.pdf"),
        ("the run folder", "/tmp/fixture-run/review/progress.json"),
    ):
        assert local_review.local_references(value, facts=facts, manuscript=value), (
            f"{why} is a fact about this machine and the paper cannot allow it: {value}"
        )

    # Every refusal names the file, the field and the text, which is what an
    # editor reading one needs in order to find it.
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        (dest / "summary.md").write_text(
            "\n\n".join(REVIEW_TEXT) + "\n", encoding="utf-8"
        )
        (dest / "provenance.json").write_text(
            json.dumps({"review": {"id": "p/v1/r1"}, "notes": list(REVIEW_TEXT)}),
            encoding="utf-8",
        )
        assert local_review.bundle_local_path_leaks(
            dest, facts=facts, manuscript=manuscript
        ) == [], "a bundle of ordinary review text must publish"

        # A Windows path inside a JSON value, at depth, in a list. JSON doubles
        # a backslash, so the text scan this replaced saw nothing here and a
        # published bundle carried the path.
        (dest / "issues.json").write_text(
            json.dumps({"extra": {"deep": [{"where": ["ok", "C:\\Users\\reviewer\\x.pdf"]}]}}),
            encoding="utf-8",
        )
        # A path keyed by itself, and a path in one row of a JSONL file.
        (dest / "findings.jsonl").write_text(
            json.dumps({"uid": "f-1", "comment": "mAP@0.5 is fine"}) + "\n"
            + json.dumps({"uid": "f-2", "memo": "/mnt/data1/papers/draft.pdf"}) + "\n",
            encoding="utf-8",
        )
        found = local_review.bundle_local_path_leaks(dest, facts=facts, manuscript=manuscript)
        lines = [leak.line for leak in found]
        windows = [leak.line for leak in found if leak.where.startswith("issues.json:")]
        assert windows == [
            "issues.json: extra.deep[0].where[1] names a path in a Windows user "
            "profile, 'C:\\\\Users\\\\reviewer\\\\x.pdf'"
        ], f"a Windows path inside a JSON value was not seen as a value: {lines}"
        rows = [leak.line for leak in found if leak.where.startswith("findings.jsonl:")]
        assert rows == [
            "findings.jsonl: line 2.memo names an absolute path, "
            "'/mnt/data1/papers/draft.pdf'"
        ], f"a leak in one row of a JSONL file has to name the row: {lines}"
        assert len(found) == 2, f"nothing else in this bundle is a leak: {lines}"

        # A JSON file that will not parse is read as text rather than skipped,
        # because a half-written record is exactly when a scan matters.
        (dest / "issues.json").write_text(
            '{"memo": "/mnt/data1/papers/draft.pdf", ', encoding="utf-8"
        )
        damaged = local_review.file_local_references(
            dest / "issues.json", facts=facts, manuscript=manuscript
        )
        assert damaged and "unparsed JSON" in damaged[0].line, (
            f"a damaged JSON file has to be scanned as text: "
            f"{[leak.line for leak in damaged]}"
        )


def _detected_facts(
    *,
    home: str = "/export/people/pretend",
    host: str = "lab-WS-01",
    user: str = "pretend",
    tmp: str = "/tmp",
    cwd: str = "/data",
    checkout: str = "/export/people/pretend/insilico",
    run_dir: str | None = None,
    typed_run: str | None = None,
) -> tuple:
    """The facts `machine_facts` detects on a machine described here.

    A fact is looked up rather than recognised, so the only way to check how it
    is matched is to say what was looked up. Each of these is a real machine
    someone publishes from: a home outside `/home` entirely, a host called
    `media` or `editor`, a user called `pi` or `test`, a working directory of
    `/data`. The patching lasts exactly one call and the sources are put back,
    because a fact detected from the wrong machine would be wrong for every
    other check in this file.

    The environment is patched along with the callables. `machine_facts` reads
    HOME, PWD and TMPDIR as well, because a shell that exports a home directory
    the resolved one does not match is the ordinary case on a machine reached
    through a symbolic link. Leaving the real environment in place meant the
    facts of the machine running the suite were mixed into every described
    machine, and a case written about `/home/opal` passed here for the wrong
    reason on this machine and failed on anybody else's.
    """
    saved = {name: Path.__dict__.get(name) for name in ("home", "cwd")}
    saved_host = local_review.socket.gethostname
    saved_user = local_review.getpass.getuser
    saved_tmp = local_review.tempfile.gettempdir
    saved_repo = local_review.REPO
    named = ("HOME", "USERPROFILE", "PWD", "TMPDIR", "TMP", "TEMP")
    saved_env = {name: os.environ.get(name) for name in named}
    Path.home = classmethod(lambda cls: Path(home))  # type: ignore[method-assign]
    Path.cwd = classmethod(lambda cls: Path(cwd))  # type: ignore[method-assign]
    local_review.socket.gethostname = lambda: host
    local_review.getpass.getuser = lambda: user
    local_review.tempfile.gettempdir = lambda: tmp
    local_review.REPO = Path(checkout)
    for name in named:
        os.environ.pop(name, None)
    os.environ["HOME"] = home
    os.environ["PWD"] = cwd
    os.environ["TMPDIR"] = tmp
    try:
        return local_review.machine_facts(run_dir=run_dir, typed_run=typed_run)
    finally:
        for name, value in saved.items():
            if value is None:
                delattr(Path, name)
            else:
                setattr(Path, name, value)
        local_review.socket.gethostname = saved_host
        local_review.getpass.getuser = saved_user
        local_review.tempfile.gettempdir = saved_tmp
        local_review.REPO = saved_repo
        for name, value in saved_env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


# A generic fact is a word that happens to be this machine's: a one-segment
# directory, a one-word host name, a bare account name. A word is not a leak, so
# each of these ordinary sentences has to publish with no flag and no hit at all.
# Every one of them was refused by some version of this scan.
MUST_PUBLISH = (
    ("the temperature/tmp ratio is unlabelled", {}),
    ("the dataset is at https://doi.org/10.1000/tmp/abc", {}),
    ("the training/data/test split is never stated", {"cwd": "/data"}),
    (r"the rotation is $2\pi$ radians", {"user": "pi"}),
    ("the train/test split is stratified", {"user": "test"}),
    ("reported as and/or", {"user": "or"}),
    ("the dose was 5 mg/kg/day", {}),
    ("the dose was 5 mg /kg/day", {}),
    ("mAP@0.5 and IoU@0.75 are reported", {}),
    ("the rate is 3 (events)/person/year", {}),
    ("~1/3 of the cohort responded", {}),
    ("claude-code ran the panel", {"host": "claude"}),
    ("the media files are not deposited", {"host": "media"}),
    ("a review of the core claim", {"host": "core"}),
    ("the editor agent wrote the letter", {"host": "editor"}),
    ("the stats reader found nothing", {"host": "stats"}),
    ("consistency across the field is the claim", {"host": "consistency"}),
    ("the preprint is on biorxiv", {"host": "biorxiv"}),
    ("localhosting the server is enough to reproduce it", {"host": "localhost"}),
    ("/tmp alone names no run", {"tmp": "/tmp"}),
    ("/data alone names no run", {"cwd": "/data"}),
)

# A generic fact is still found in the shapes where a bare word can only be a
# machine, and there it is tier 2: refused by default, and waivable, because
# being wrong about a word has to be survivable.
GENERIC_HOSTS = ("media", "editor", "stats", "core", "claude", "biorxiv")

# A one-segment directory is a shape too. `/tmp` and `/data` are on every
# machine, so what is refused is something written under them. A path under a
# temporary directory is not in this list any more: whoever's machine it is on,
# it is one of the shapes nothing waives, and it is checked as such below.
GENERIC_PATHS = (
    ("/data/sets/x is where it ran", {"cwd": "/data"}),
    ("/export/sets/x is where it ran", {"tmp": "/export"}),
    (r"copied from \\media\share\x.pdf", {"host": "media"}),
    (r"copied from \\fileserver\share\draft.pdf", {}),
)


def _specific_forms(home: str, checkout: str, host: str) -> tuple[str, ...]:
    """Every place a specific fact was published by a boundary that had a hole.

    A boundary on the left let any character that is not a word character
    through: a scheme, a doubled slash, a tilde, a port, a quote. A boundary on
    the right did the same. A specific fact is a plain substring now, in either
    case, so there is no left or right for a hole to be in.
    """
    return (
        f"http://localhost:8000{checkout}/x",
        f"file:{home}/x.pdf",
        f"file:///{checkout}/scripts/local_review.py",
        f"box:{home}/x",
        f"//{home}/x",
        f"a~{home}/x",
        f"{home}/papers/draft.pdf",
        f"the run wrote {home}",
        f"{home.upper()}/x",
        f'"{home}/x"',
        f"[{home}/x]",
        f"{home}/x,{home}/y",
        f"{checkout}/scripts/local_review.py",
        host,
        host.lower(),
        host.upper(),
        f"node.{host.lower()}",
        f"run_{host.lower()}_1",
        f"{host}:/srv/x",
        f"bob@{host}",
        f"//{host}/share",
        f"the panel ran on {host} overnight",
    )


def _path_spellings(path: str) -> tuple[tuple[str, str], ...]:
    """Every way one absolute path has been written past a scan.

    Each entry is one encoding, named, so a failure says which spelling got
    through rather than printing a string whose characters are invisible. The
    list is not a list of patterns the scan carries: one canonical function runs
    these in reverse until the text stops changing, and this says what that
    function has to cover.
    """
    inner = [segment for segment in path.split("/") if segment]
    return (
        ("a decimal HTML entity", path.replace("/", "&#47;")),
        ("a hexadecimal HTML entity", path.replace("/", "&#x2F;")),
        ("the named solidus entity", path.replace("/", "&sol;")),
        ("a percent sign written as an entity", path.replace("/", "&#37;2F")),
        ("percent-encoding", path.replace("/", "%2F")),
        ("percent-encoding twice over", path.replace("/", "%252F")),
        ("percent-encoding three times over", path.replace("/", "%25252F")),
        ("a zero-width space", path.replace("/", "/​")),
        ("a zero-width non-joiner", path.replace("/", "/‌")),
        ("a zero-width joiner", path.replace("/", "/‍")),
        ("a word joiner", path.replace("/", "/⁠")),
        ("a byte order mark", path.replace("/", "/﻿")),
        ("a soft hyphen", path.replace("/", "/­")),
        ("a division slash", path.replace("/", "∕")),
        ("a fraction slash", path.replace("/", "⁄")),
        ("a big solidus", path.replace("/", "⧸")),
        ("a full-width solidus", path.replace("/", "／")),
        ("a mathematical rising diagonal", path.replace("/", "⟋")),
        ("a box drawing diagonal", path.replace("/", "╱")),
        ("a kana vertical repeat mark", path.replace("/", "〳")),
        ("a backslash", path.replace("/", "\\")),
        ("a set minus", path.replace("/", "∖")),
        ("a full-width backslash", path.replace("/", "＼")),
        ("a backslash escaping each slash", path.replace("/", "\\/")),
        ("a doubled slash", path.replace("/", "//")),
        ("a tripled slash", path.replace("/", "///")),
        ("a dot segment between each pair", "/" + "/./".join(inner)),
        ("a dot segment and a doubled slash", "//" + "/./".join(inner)),
    )


def _name_spellings(name: str) -> tuple[tuple[str, str], ...]:
    """Every way one hyphenated host name has been written past a scan."""
    return (
        ("a hyphen", name),
        ("a hyphen in the other case", name.swapcase()),
        ("a hyphen written as a decimal entity", name.replace("-", "&#45;")),
        ("a hyphen written as a hex entity", name.replace("-", "&#x2D;")),
        ("a percent-encoded hyphen", name.replace("-", "%2D")),
        ("a percent-encoded hyphen twice over", name.replace("-", "%252D")),
        ("a hyphen escaped with a backslash", name.replace("-", "\\-")),
        ("a hyphen followed by a zero-width space", name.replace("-", "-​")),
        ("a non-breaking hyphen", name.replace("-", "‑")),
        ("a figure dash", name.replace("-", "‒")),
        ("an en dash", name.replace("-", "–")),
        ("an em dash", name.replace("-", "—")),
        ("a horizontal bar", name.replace("-", "―")),
        ("a hyphen from the general punctuation block", name.replace("-", "‐")),
        ("a minus sign", name.replace("-", "−")),
        ("a small em dash", name.replace("-", "﹘")),
        ("a small hyphen-minus", name.replace("-", "﹣")),
        ("a full-width hyphen-minus", name.replace("-", "－")),
    )


# The machines the matrix is run on: this one, a home under `/home`, and a home
# outside every root `LOCAL_ROOTS` knows, which is the case a scan that works
# from path shapes alone cannot see at all.
SPECIFIC_MACHINES = (
    {},
    {"home": "/home/opal", "user": "opal", "checkout": "/home/opal/Repos/insilico"},
    {"host": "node1.lab"},
)


def check_only_this_machines_own_names_are_refused_as_this_machine() -> None:
    """Every boundary on a specific fact was a hole, and a word was never a leak.

    The version before this one asked for a boundary on each side of each fact,
    so that a fact could not misfire on ordinary text. Six separate holes came
    out of that one decision. A left boundary of `(?<![\\w.:/~-])` let through
    every character that is not a word character: `file:` was excluded by hand
    and `box:` was not, `//` and `a~` and `http://localhost:8000` all published
    the home directory that followed them. A whole-field host rule published
    `node.lab-ws-01`, `run_lab-ws-01_1` and the host as a JSON key. And the
    same caution made a word-shaped host name unwaivable, so a machine called
    `editor` could not publish its own provenance record.

    The rule now splits by what the fact is rather than by where it sits. A path
    of two or more segments and a host name carrying a digit, a hyphen or a dot
    are specific: matched as a plain case-insensitive substring, everywhere, in
    every string and every key at any depth, and nothing waives one. Nothing has
    to be protected from that test, because `/home/opal` and `lab-ws-01` do not
    occur in a review of a paper or in this repository's own vocabulary. A
    one-segment directory, a one-word host and the bare account name are generic:
    tier 2 shapes, waivable, because a word is not a leak.
    """
    for text, machine in MUST_PUBLISH:
        facts = _detected_facts(**machine)
        hits = local_review.local_references(text, facts=facts)
        assert hits == [], (
            f"a machine described by {machine} cannot publish {text!r}: "
            f"{[leak.line for leak in hits]}"
        )
        # And in a record, where the same string is a value and a field name.
        record = {text: "a value", "note": {"deep": [text]}}
        found = local_review.local_reference_fields(record, facts=facts)
        assert found == [], (
            f"a machine described by {machine} cannot publish a record saying "
            f"{text!r}: {[leak.line for leak in found]}"
        )

    for machine in SPECIFIC_MACHINES:
        facts = _detected_facts(**machine)
        home = machine.get("home", "/export/people/pretend")
        checkout = machine.get("checkout", "/export/people/pretend/insilico")
        host = machine.get("host", "lab-WS-01")
        for text in _specific_forms(home, checkout, host):
            hits = local_review.local_references(text, facts=facts)
            assert any(leak.machine_fact for leak in hits), (
                f"a machine described by {machine} published its own name in "
                f"{text!r}: {[leak.line for leak in hits]}"
            )
            # Neither the manuscript nor the flag reaches one, and an allowance
            # that merely contains one is refused before it allows anything.
            for waiver in ({"manuscript": f"{text}\n"}, {"allowed": (text,)}):
                again = local_review.local_references(text, facts=facts, **waiver)
                assert any(leak.machine_fact for leak in again), (
                    f"{list(waiver)[0]} waived a fact about this machine: {text!r}"
                )
            assert local_review.names_a_specific_fact(text, facts), (
                f"an allowance naming {text!r} has to be refused as a flag too"
            )
            # Through a record: as a value at depth, and as a field name, which
            # is where the host name reached a published page.
            record = {"generator": {"id": text, "status": "ok"}, text: "a value"}
            found = local_review.local_reference_fields(record, facts=facts)
            assert len([leak for leak in found if leak.machine_fact]) >= 2, (
                f"a record naming {text!r} in a value and in a key published: "
                f"{[leak.line for leak in found]}"
            )
        # An ordinary allowance is not refused by that same test.
        assert not local_review.names_a_specific_fact("R:/G/B", facts), (
            "an allowance that names nothing about this machine has to be taken"
        )

    # A word-shaped host is a shape and not a fact: a clean record publishes
    # from it, and the shapes still catch it where a word can only be a machine.
    for host in GENERIC_HOSTS:
        facts = _detected_facts(host=host)
        clean = {"generator": {"kind": host}, "panel": [{"slot": host, "status": "ok"}]}
        found = local_review.local_reference_fields(clean, facts=facts)
        assert found == [], (
            f"a clean record was refused on a host called {host!r}: "
            f"{[leak.line for leak in found]}"
        )
        for text in (f"{host}:/srv/x", f"bob@{host}", f"//{host}/share/x"):
            hits = local_review.local_references(text, facts=facts)
            assert hits, f"a host called {host!r} published {text!r}"
            assert not any(leak.machine_fact for leak in hits), (
                f"a one-word host name is not unwaivable: {[leak.line for leak in hits]}"
            )
            waived = local_review.local_references(
                text, facts=facts, allowed=tuple(leak.text for leak in hits)
            )
            assert waived == [], (
                f"--allow-text did not waive {text!r}: {[leak.line for leak in waived]}"
            )

    for text, machine in GENERIC_PATHS:
        facts = _detected_facts(**machine)
        hits = local_review.local_references(text, facts=facts)
        assert hits, f"a machine described by {machine} published {text!r}"
        assert not any(leak.machine_fact for leak in hits), (
            f"one directory on this machine is not unwaivable: "
            f"{[leak.line for leak in hits]}"
        )
        waived = local_review.local_references(
            text, facts=facts, allowed=tuple(leak.text for leak in hits)
        )
        assert waived == [], (
            f"--allow-text did not waive {text!r}: {[leak.line for leak in waived]}"
        )

    # A fact inside a longer path is reported at the length of the path, and the
    # shape that found that length must not demote it into something a flag
    # could waive. The promotion runs before the allowances are read, which is
    # what stops `--allow-text` on the whole path from waiving the home
    # directory inside it.
    facts = _detected_facts(
        home="/home/opal", user="opal", checkout="/home/opal/Repos/insilico"
    )
    hits = local_review.local_references(
        "the run wrote /home/opal/papers/draft.pdf", facts=facts
    )
    assert [leak.text for leak in hits] == ["/home/opal/papers/draft.pdf"], (
        f"the leak has to be reported whole: {[leak.line for leak in hits]}"
    )
    assert hits[0].machine_fact, (
        f"a path that contains a fact is still a fact: {hits[0].line}"
    )

    # A home outside every root the shapes know has no shape to be reported at,
    # so the fact itself is the hit. It is still tier 1, which is the point: a
    # scan that worked from path shapes alone could not see this home at all.
    outside = local_review.local_references(
        "the run wrote /export/people/pretend/papers/draft.pdf", facts=_detected_facts()
    )
    assert [leak.text for leak in outside] == ["/export/people/pretend"], (
        f"a fact outside every known root is reported as itself: "
        f"{[leak.line for leak in outside]}"
    )
    assert outside[0].machine_fact, f"and it is still a fact: {outside[0].line}"

    # A slash that is not a slash. NFKC folds the full-width pair and leaves the
    # division slash, the fraction slash and the big solidus alone, and
    # `∕home∕pretend∕x` published because of it.
    for separator in ("\u2215", "\u2044", "\u29f8", "\uff0f"):
        text = f"{separator}home{separator}pretend{separator}x"
        hits = local_review.local_references(
            text, facts=_detected_facts(home="/home/pretend", user="pretend",
                                        checkout="/home/pretend/insilico")
        )
        assert any(leak.machine_fact for leak in hits), (
            f"{separator!r} written for a slash published a home directory: "
            f"{[leak.line for leak in hits]}"
        )
    # A backslash and its look-alikes fold to a plain slash rather than to a
    # backslash, because one canonical form cannot hold both and the slash is
    # the form a path fact is written in. `C:\Users\bob` and `C:/Users/bob` are
    # the same path to Windows and the drive-letter shape reads either, so the
    # pair is still refused with one spelling between them.
    for separator in ("\\", "\uff3c", "\u2216"):
        folded = f"C:{separator}Users{separator}bob{separator}x.pdf"
        assert local_review.canonical_text(folded) == "C:/Users/bob/x.pdf", (
            f"{separator!r} did not fold to a slash: "
            f"{local_review.canonical_text(folded)!r}"
        )
        assert local_review.local_references(folded, facts=()), (
            f"a Windows path written with {separator!r} published"
        )


def check_a_home_or_temporary_path_is_refused_on_anybodys_machine() -> None:
    """A path in a home or a temporary directory is tier 1, whoever owns it.

    This machine's own home and temporary directories are looked up at publish
    time and were already unwaivable. Everybody else's were tier 2: `/home/
    runner` out of a CI log, `/Users/someone` from a collaborator's laptop,
    `/tmp/pdf-cache` from a container the run passed through. Tier 2 means the
    refusal prints the flag that publishes it, so any of them could be published
    by passing the refusal's own text back, and a bundle then carried a machine
    path that happened not to be this machine's.

    A path in a home or a temporary directory is never a review's own words, so
    the shape itself is the fact now. Nothing waives one: not `--allow-text`,
    not the manuscript printing it, and the allowance is refused as a flag
    rather than quietly ignored. What is left waivable is a directory that is
    not one of those, because being wrong about `/data` has to be survivable.
    """
    # A machine that shares none of these: its home is elsewhere, and its
    # temporary directory is not /tmp.
    facts = _detected_facts(
        home="/export/people/pretend",
        user="pretend",
        checkout="/export/people/pretend/insilico",
        tmp="/export/scratch",
    )
    somebody_elses = (
        ("a CI runner's home", "/home/runner/work/insilico/draft.pdf"),
        ("a macOS home", "/Users/someone/Desktop/draft.pdf"),
        ("a container's temporary directory", "/tmp/pdf-cache/draft.pdf"),
        ("a macOS temporary directory", "/var/folders/ab/cd/T/review.json"),
        ("a tilde home", "~/papers/draft.pdf"),
        ("a home spelled as a variable", "$HOME/papers/draft.pdf"),
        ("a Windows user profile", "C:\\Users\\someone\\papers\\draft.pdf"),
    )
    for why, text in somebody_elses:
        hits = local_review.local_references(text, facts=facts)
        assert any(leak.machine_fact for leak in hits), (
            f"{why} is not tier 1: {text!r} -> {[leak.line for leak in hits]}"
        )
        for waiver in ({"manuscript": f"{text}\n"}, {"allowed": (text,)}):
            again = local_review.local_references(text, facts=facts, **waiver)
            assert any(leak.machine_fact for leak in again), (
                f"{list(waiver)[0]} waived {why}: {text!r}"
            )
        assert local_review.names_a_specific_fact(text, facts), (
            f"an allowance naming {why} has to be refused as a flag: {text!r}"
        )

    # A directory that is nobody's home and nobody's scratch space is still
    # refused and still waivable, because that is the judgement a flag is for.
    for text in ("/data/sets/x", "/srv/public/deposit/x.csv"):
        hits = local_review.local_references(text, facts=facts)
        assert hits, f"an absolute path has to be refused: {text!r}"
        assert not any(leak.machine_fact for leak in hits), (
            f"an ordinary directory is not tier 1: {[leak.line for leak in hits]}"
        )
        waived = local_review.local_references(
            text, facts=facts, allowed=tuple(leak.text for leak in hits)
        )
        assert waived == [], (
            f"--allow-text did not waive {text!r}: {[leak.line for leak in waived]}"
        )

    # And a word that merely starts the same way is not a path at all.
    for text in ("homeostasis was restored", "the temperature was held at 37 C"):
        assert local_review.local_references(text, facts=facts) == [], (
            f"ordinary prose was refused as a path: {text!r}"
        )

    # Through a written bundle, which is the guard that actually runs on
    # publish: one file naming somebody else's home, and the flag that names it
    # does not publish it.
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        (dest / "summary.md").write_text(
            "The run wrote /home/runner/work/out/report.json\n", encoding="utf-8"
        )
        leaks = local_review.bundle_local_path_leaks(
            dest, facts=facts, manuscript="", allowed=("/home/runner/work/out/report.json",)
        )
        assert len(leaks) == 1 and leaks[0].where.startswith("summary.md"), (
            f"a bundle file naming a home directory published: "
            f"{[leak.line for leak in leaks]}"
        )
        assert leaks[0].machine_fact, f"and the flag did not waive it: {leaks[0].line}"


def check_every_spelling_of_a_machine_fact_is_the_same_fact() -> None:
    """The scan read four look-alike slashes, and the next round found a fifth.

    Each round of review found another encoding that published a path: a
    division slash, then a full-width solidus, then `&#47;`, then `%252F`, then
    a zero-width space inside the path. Every answer was another entry in a list
    inside the scan, which is a race nobody wins, because the list only ever
    holds the spellings somebody has already thought of.

    There is one canonical function now, applied to the scanned text and to the
    facts alike and run until the string stops changing: NFKC, HTML entities,
    percent-decoding, format characters removed, slash and hyphen look-alikes
    folded, a backslash in front of punctuation dropped, repeated slashes and
    `/./` collapsed. The loop is the part that matters. One pass turns `%252F`
    into `%2F` and stops, and an entity can hide a percent sign from the
    decoder that ran before it. The raw text is still scanned beside the
    canonical form, so folding never loses a hit it would have found as
    written.

    Both readings of a backslash are canonicalised, because a quoted separator
    and a quoted punctuation mark are written the same way: a path segment that
    starts with `.`, `-` or `_` is lost by one reading and a quoted host name by
    the other. The run folder is a fact in the spelling the editor typed as well
    as the one the engine resolved it to.

    Every case here is a tier 1 refusal: unwaivable by the flag and by the
    manuscript, refused as an allowance, and through a real publish it leaves
    nothing on disk.
    """
    described = (
        {"home": "/home/pretend", "user": "pretend",
         "checkout": "/home/pretend/insilico", "host": "box-7.lab"},
        {"home": "/export/people/pretend", "user": "pretend",
         "checkout": "/export/people/pretend/insilico", "host": "lab-WS-01"},
    )
    for machine in described:
        facts = _detected_facts(**machine)
        cases = (
            *_path_spellings(machine["home"]),
            *_path_spellings(machine["checkout"]),
            *_name_spellings(machine["host"]),
        )
        for why, text in cases:
            hits = local_review.local_references(text, facts=facts)
            assert any(leak.machine_fact for leak in hits), (
                f"a machine described by {machine} published its own name "
                f"written with {why}: {text!r} -> {[leak.line for leak in hits]}"
            )
            for waiver in ({"manuscript": f"{text}\n"}, {"allowed": (text,)}):
                again = local_review.local_references(text, facts=facts, **waiver)
                assert any(leak.machine_fact for leak in again), (
                    f"{list(waiver)[0]} waived a fact written with {why}: {text!r}"
                )
            assert local_review.names_a_specific_fact(text, facts), (
                f"an allowance written with {why} has to be refused as a flag: {text!r}"
            )
            # The canonical form has to be a fixed point, or the loop that
            # produced it stopped early and a longer chain would still get past.
            once = local_review.canonical_text(text)
            assert local_review.canonical_text(once) == once, (
                f"the canonical form of {why} keeps changing: {once!r} then "
                f"{local_review.canonical_text(once)!r}"
            )
            # And through a record, as a value at depth and as a field name.
            record = {text: "a value", "generator": {"id": text, "status": "ok"}}
            found = local_review.local_reference_fields(record, facts=facts)
            assert len([leak for leak in found if leak.machine_fact]) >= 2, (
                f"a record naming this machine with {why} published: {text!r} -> "
                f"{[leak.line for leak in found]}"
            )

    # A machine reached through a symbolic link, which is the ordinary case for
    # a home on a network mount or a run folder under a linked scratch
    # directory. The shell's HOME, PWD and TMPDIR hold the link and the resolved
    # path is what every file operation reports, so a fact registered in one
    # spelling published the other.
    with tempfile.TemporaryDirectory() as tmp:
        real = Path(tmp) / "real-place"
        link = Path(tmp) / "linked-place"
        real.mkdir()
        link.symlink_to(real, target_is_directory=True)
        for role in ("home", "cwd", "tmp", "run"):
            machine = {"home": "/export/people/pretend", "user": "pretend",
                       "checkout": "/export/people/pretend/insilico"}
            if role == "run":
                facts = _detected_facts(**machine, run_dir=str(link / "runs" / "one"))
                spellings = (str(link / "runs" / "one"), str(real / "runs" / "one"))
            else:
                machine[role] = str(link)
                facts = _detected_facts(**machine)
                spellings = (str(link), str(real))
            for spelling in spellings:
                text = f"the run wrote {spelling}/x"
                hits = local_review.local_references(text, facts=facts)
                assert any(leak.machine_fact for leak in hits), (
                    f"a symbolically linked {role} published as {spelling}: "
                    f"{[leak.line for leak in hits]}"
                )

    # A path segment that begins with punctuation, which is the case that
    # decides how a backslash has to be read. Read as a quoted punctuation mark
    # first, `\opt\.cache\insilico` becomes `/opt.cache/insilico`, which is a
    # path on no machine, and the fact is gone with no hit at all. Read as a
    # separator first it is the path it was. Neither reading is right on its
    # own, `lab\-WS\-01` needing the other one, so both are canonicalised and
    # a hit is taken from whichever found it. These four are a cache directory,
    # a scratch disk, a runs folder and the macOS temporary directory.
    for checkout in (
        "/opt/.cache/insilico",
        "/data/-scratch/run",
        "/mnt/data1/.runs/p1",
        "/var/folders/_k/abc/T",
    ):
        facts = _detected_facts(
            home="/home/pretend", user="pretend", checkout=checkout
        )
        for separator, label in (("\\", "a backslash"), ("＼", "U+FF3C")):
            quoted = checkout.replace("/", separator)
            for text in (quoted, f"the run wrote {quoted}/x.pdf"):
                hits = local_review.local_references(text, facts=facts)
                assert any(leak.machine_fact for leak in hits), (
                    f"a checkout at {checkout} published as {label}: {text!r} -> "
                    f"{[leak.line for leak in hits]}"
                )
                for waiver in ({"manuscript": f"{text}\n"}, {"allowed": (text,)}):
                    again = local_review.local_references(text, facts=facts, **waiver)
                    assert any(leak.machine_fact for leak in again), (
                        f"{list(waiver)[0]} waived {checkout} written as {label}: "
                        f"{text!r}"
                    )

    # And the reading the other order is there for still holds: a quoted slash
    # and a quoted hyphen are the separator and the hyphen they stand for.
    facts = _detected_facts(
        home="/home/pretend", user="pretend", checkout="/home/pretend/insilico",
        host="lab-WS-01",
    )
    for text in ("\\/home\\/pretend\\/x", "lab\\-WS\\-01", "lab＼-WS＼-01"):
        hits = local_review.local_references(text, facts=facts)
        assert any(leak.machine_fact for leak in hits), (
            f"a quoted separator stopped being this machine: {text!r} -> "
            f"{[leak.line for leak in hits]}"
        )

    # The run folder in the spelling the editor typed. The engine resolves the
    # path it is given before it records it, so a run reached through a link was
    # a fact only as the target, and the path the editor typed, which is the one
    # in every log line they can see, was tier 2 and published with the flag the
    # refusal printed.
    with tempfile.TemporaryDirectory() as tmp:
        real = Path(tmp) / "real-runs"
        link = Path(tmp) / "linked-runs"
        real.mkdir()
        link.symlink_to(real, target_is_directory=True)
        (real / "one").mkdir()
        typed = link / "one"
        facts = _detected_facts(
            home="/home/pretend",
            user="pretend",
            checkout="/home/pretend/insilico",
            run_dir=str(real / "one"),
            typed_run=str(typed),
        )
        cases = (
            ("the typed run folder", f"{typed}/audit.md"),
            ("the typed run's parent", f"{link}/notes.txt"),
            ("the bare typed parent", str(link)),
            ("the typed run as entities", f"{typed}/audit.md".replace("/", "&sol;")),
            (
                "the typed run with a zero-width space",
                f"{typed}/audit.md".replace("/", "/​"),
            ),
        )
        for why, text in cases:
            hits = local_review.local_references(text, facts=facts)
            assert any(leak.machine_fact for leak in hits), (
                f"{why} published: {text!r} -> {[leak.line for leak in hits]}"
            )
            for waiver in ({"manuscript": f"{text}\n"}, {"allowed": (text,)}):
                again = local_review.local_references(text, facts=facts, **waiver)
                assert any(leak.machine_fact for leak in again), (
                    f"{list(waiver)[0]} waived {why}: {text!r}"
                )
            assert local_review.names_a_specific_fact(text, facts), (
                f"{why} has to be refused as an allowance: {text!r}"
            )


def check_a_machine_fact_in_any_spelling_leaves_no_bundle_behind() -> None:
    """The same spellings through a real publish, which has to write nothing.

    A scan that finds the hit is half the claim. The other half is that the
    publish stops before anything reaches the published tree, because a bundle
    half written and then refused is worse than either outcome. The fact used
    here is this checkout, which is two segments or more on any machine that can
    run this suite, and the refusal has to say the hit is one no flag waives.

    Then the same publish from two checkouts whose paths hold a segment starting
    with punctuation, because the backslash spellings used to pass in a clone at
    `/opt/.cache/insilico` and this check would have said so only on a machine
    whose checkout happened to be spelled that way. Then a run reached through a
    symbolic link and published by the path the editor typed, which the engine
    resolves before it records it.
    """
    checkout = str(local_review.REPO)
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            workspace = _workspace(Path(tmp) / "workspace")
            for index, (why, text) in enumerate(_path_spellings(checkout), start=1):
                package = dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    issues=[
                        dict(
                            ISSUES[0],
                            statement=f"The reviewer read the draft at {text}/x.pdf.",
                        ),
                        *ISSUES[1:],
                    ],
                )
                run = _run_directory(
                    Path(tmp) / f"run-{index}", **{"issues.json": package}
                )
                destination = reviews / "2026" / "fixture-paper" / "v1" / f"r{index}"
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                    code = _publish(
                        _prepared(
                            Path(tmp) / f"prepared-{index}", destination, attempt=index
                        ),
                        run,
                        workspace,
                        "--publish",
                    )
                message = stderr.getvalue()
                assert code == 2, (
                    f"this checkout written with {why} published, exit {code}: {text!r}"
                )
                assert not destination.exists(), (
                    f"a refused publish left a bundle at {destination}"
                )
                assert "name this machine itself" in message, (
                    f"{why} was refused as something a flag could waive: {message!r}"
                )
                assert "Nothing was written" in message, (
                    f"the refusal has to say the tree was left alone: {message!r}"
                )

    # The same publish from a checkout whose path holds a segment starting with
    # punctuation, which no longer depends on the shape of the checkout this
    # suite happens to be run from. In a clone at `/opt/.cache/insilico` the
    # backslash spellings used to pass the scan and publish, because one reading
    # of a backslash turns `\opt\.cache\insilico` into `/opt.cache/insilico`.
    # `REPO` names only how a path inside the repository is written down, so
    # standing it somewhere else for the length of a publish into a temporary
    # tree changes which strings are this machine and nothing else.
    quoted = [
        spelling
        for spelling in _path_spellings("/placeholder")
        if "backslash" in spelling[0]
    ]
    assert len(quoted) == 3, f"the backslash spellings went missing: {quoted}"
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            workspace = _workspace(Path(tmp) / "workspace")
            standing = local_review.REPO
            cases = [
                (checkout, why, text)
                for checkout in ("/opt/.cache/insilico", "/opt/-x/insilico")
                for why, text in _path_spellings(checkout)
                if "backslash" in why
            ]
            try:
                for index, (checkout, why, text) in enumerate(cases, start=1):
                    local_review.REPO = Path(checkout)
                    package = dict(
                        PACKAGE,
                        stages=_stages(TRACKS),
                        issues=[
                            dict(
                                ISSUES[0],
                                statement=f"The reviewer read the draft at {text}/x.pdf.",
                            ),
                            *ISSUES[1:],
                        ],
                    )
                    run = _run_directory(
                        Path(tmp) / f"run-{index}", **{"issues.json": package}
                    )
                    destination = reviews / "2026" / "fixture-paper" / "v1" / f"r{index}"
                    stderr = io.StringIO()
                    with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(
                        io.StringIO()
                    ):
                        code = _publish(
                            _prepared(
                                Path(tmp) / f"prepared-{index}", destination, attempt=index
                            ),
                            run,
                            workspace,
                            "--publish",
                        )
                    message = stderr.getvalue()
                    assert code == 2, (
                        f"a checkout at {checkout} written with {why} published, "
                        f"exit {code}: {text!r}"
                    )
                    assert not destination.exists(), (
                        f"a refused publish left a bundle at {destination}"
                    )
                    assert "name this machine itself" in message, (
                        f"{why} of {checkout} was refused as something a flag could "
                        f"waive: {message!r}"
                    )
            finally:
                local_review.REPO = standing

    # A run reached through a symbolic link, published by the path the editor
    # typed. The engine resolves what it is given before it records it, so the
    # typed spelling reached the scan only as the target it pointed at, and a
    # review quoting the path the editor had just typed published it with the
    # flag the refusal offered.
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            workspace = _workspace(Path(tmp) / "workspace")
            real = Path(tmp) / "real-runs"
            real.mkdir()
            link = Path(tmp) / "linked-runs"
            link.symlink_to(real, target_is_directory=True)
            typed = link / "one"
            for index, (why, text) in enumerate(
                (
                    ("the run folder as it was typed", f"{typed}/audit_statistics.md"),
                    ("the folder the typed run sits in", f"{link}/notes.txt"),
                ),
                start=1,
            ):
                package = dict(
                    PACKAGE,
                    stages=_stages(TRACKS),
                    issues=[
                        dict(
                            ISSUES[0],
                            statement=f"The reviewer read the audit at {text}.",
                        ),
                        *ISSUES[1:],
                    ],
                )
                _run_directory(real / "one", **{"issues.json": package})
                destination = reviews / "2026" / "fixture-paper" / "v1" / f"r{index}"
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(
                    io.StringIO()
                ):
                    code = _publish(
                        _prepared(
                            Path(tmp) / f"prepared-{index}", destination, attempt=index
                        ),
                        typed,
                        workspace,
                        "--publish",
                    )
                message = stderr.getvalue()
                assert code == 2, f"{why} published, exit {code}: {text!r}"
                assert not destination.exists(), (
                    f"a refused publish left a bundle at {destination}"
                )
                assert "name this machine itself" in message, (
                    f"{why} was refused as something a flag could waive: {message!r}"
                )


def check_a_path_shaped_key_is_refused_rather_than_published_without_it() -> None:
    """A published artifact was quietly missing an entry, or quietly holding one.

    `issues.json` is the engine's own output, copied into the bundle. A
    mapping keyed by a path leaks through the key, and a key outside this
    repository used to be dropped with its value: the bundle then carried a
    hash map one entry short, with nothing in the bundle or the record to say
    so. A key inside the repository was quietly rewritten, which is the same
    silent edit with a kinder result.

    Engine 0.10 writes no mapping keyed by a path, so there is nothing for
    that rewrite to be faithful to. Every path-shaped key is refused now, inside
    this repository or outside it, and `--allow-text` publishes one as it
    stands unless the key names this machine, which no flag publishes and which
    the refusal therefore does not offer the flag for. What is still projected
    is a value in one of the engine's own path
    fields, and each projection is printed on publish, so a dropped `pdf` is
    never silent either. A value in such a field that is not a path at all is
    left alone, because `/ 2 is the wrong denominator` is a sentence.
    """
    home = str(Path.home().resolve())
    # Which way out the refusal offers follows the tier of the key. A key that
    # names this machine is tier 1 wherever it sits, and the version that
    # offered the flag for one sent the editor to an allowance that was then
    # refused for naming a specific fact, which reads as the script changing
    # its mind between one command and the next.
    for key, waivable in (
        (f"{home}/fig1.png", False),
        (str(local_review.REPO / "docs" / "figs" / "a.png"), False),
        ("/export/people/pretend/fig1.png", True),
    ):
        package = {"summary": "One reading.", "shared_images": {key: "a" * 64}}
        try:
            local_review.without_local_paths(package)
        except local_review.CommandError as exc:
            message = str(exc)
        else:
            raise AssertionError(f"a path used as a field name published: {key}")
        assert key in message, f"the refusal has to name the key: {message!r}"
        assert ("--allow-text=" in message) is waivable, (
            f"the refusal for {key!r} offered the wrong way out: {message!r}"
        )
        if not waivable:
            assert "no flag publishes it" in message, (
                f"a key naming this machine has to say no flag waives it: {message!r}"
            )
            # And the flag does not publish it when it is passed anyway.
            try:
                local_review.without_local_paths(package, allowed=(key,))
            except local_review.CommandError:
                pass
            else:
                raise AssertionError(
                    f"an allowance published a field name that is this machine: {key}"
                )
            continue

        # Named back on the command line, it is published as it stands, value
        # and all, rather than edited on the way out.
        allowed = local_review.without_local_paths(package, allowed=(key,))
        assert allowed == package, f"an allowed key has to be published verbatim: {allowed}"

    # A key that is not shaped like a path is nobody's business.
    plain = {"files": {"docs/x.md": "b" * 64, "a reading of the figure": "c" * 64}}
    assert local_review.without_local_paths(plain) == plain, (
        "a relative key is published as it was written"
    )

    # The engine's own path fields are still projected, and the projection is
    # reported rather than done quietly.
    projected: list[str] = []
    kept = local_review.without_local_paths(
        {
            "pdf": f"{home}/runs/x/review.pdf",
            "source_review_path": str(local_review.REPO / "runs" / "local"),
            "memo_path": "/ 2 is the wrong denominator",
        },
        projected=projected,
    )
    assert "pdf" not in kept, f"an absolute path outside this repository published: {kept}"
    assert kept["source_review_path"] == "runs/local", (
        f"a path inside this repository is named relative to it: {kept}"
    )
    assert kept["memo_path"] == "/ 2 is the wrong denominator", (
        f"a reviewer's sentence was dropped from a path field: {kept}"
    )
    assert projected == ["pdf dropped", "source_review_path rewritten to runs/local"], (
        f"every projection has to be reported: {projected}"
    )


def check_a_schema_pattern_means_what_the_repositorys_own_gate_means() -> None:
    """A sha256 with a newline on the end passed here and failed the gate.

    JSON Schema patterns are ECMAScript, and Ajv runs them that way. Python's
    `$` also matches just before a trailing newline, so `^[0-9a-f]{64}$`
    accepted `"<sha>\\n"`, the record was written, and `npm run check:schema`
    refused it afterwards: a bundle in docs/reviews to delete by hand, holding a
    hash nothing will ever match.
    """
    pattern = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    clean = "a" * 64
    assert review_schema.provenance_problems(clean, pattern) == [], (
        "a clean sha256 still has to validate"
    )
    assert review_schema.provenance_problems(clean + "\n", pattern), (
        "a sha256 with a trailing newline is not a sha256"
    )
    for value in (f"{clean}\n ", f" {clean}", f"{clean}\r\n"):
        assert review_schema.provenance_problems(value, pattern), (
            f"{value!r} must not validate as a sha256"
        )

    # The translation is of the anchor only: a `$` inside a character class or
    # escaped is the character itself and still matches it.
    assert review_schema.provenance_problems("a$b", {"type": "string", "pattern": "^a[$]b$"}) == []
    assert review_schema.provenance_problems("a$b", {"type": "string", "pattern": r"^a\$b$"}) == []
    assert review_schema.provenance_problems(
        "a$b\n", {"type": "string", "pattern": r"^a\$b$"}
    ), "an escaped dollar does not make the anchor loose again"

    # And the schema this repository publishes is read the same way, through
    # its own hash fields rather than a pattern written here.
    schema = review_schema.provenance_schema()["properties"]
    for trail in (
        ("environment", "lock_sha256"),
        ("generator", "engine_fingerprint", "sha256"),
        ("generator", "input", "sha256"),
    ):
        field = schema
        for name in trail:
            field = field["properties"][name] if "properties" in field else field[name]
        assert review_schema.provenance_problems(clean, field) == [], (
            f"{'.'.join(trail)} has to accept a clean hash: {field}"
        )
        assert review_schema.provenance_problems(clean + "\n", field), (
            f"{'.'.join(trail)} accepted a hash with a newline on the end"
        )


def check_the_run_fixture_is_a_run_the_engine_could_have_written() -> None:
    """The fixtures drifted into shapes no engine writes.

    `synthesis_policy` said `editor-pooled` where the engine writes `editor` or
    `none`, `protocol.json` said `mode: plugin` where the engine writes the arm,
    and `progress.json` carried `tool_calls: 64` where the engine writes one
    count per agent slot. A check that reads a shape the publish path never
    meets proves nothing about publishing.

    Generating these from the plugin server would be better, and it is closed:
    the writers live on `peerreviewagents.plugin.server`, a private submodule,
    and `check_nothing_reaches_into_the_engines_internals` refuses an import of
    one. So the shapes are asserted instead, against the vocabulary the schema
    and the protocol state, and the two numbers have to agree.
    """
    # The arms 0.9 defines, as the schema's own note on `generator.run.arm`
    # lists them.
    arms = {
        "full-two-track",
        "reviewers-only",
        "single",
        "single-revision",
        "manuscript-only",
        "draft-check",
    }
    assert PACKAGE["synthesis_policy"] in ("editor", "none"), (
        f"the engine writes `editor` or `none`: {PACKAGE['synthesis_policy']!r}"
    )
    assert PACKAGE["arm"] in arms, f"the package's arm is not one the engine runs: {PACKAGE['arm']}"

    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        protocol = json.loads((run / "protocol.json").read_text(encoding="utf-8"))
        progress = json.loads((run / "progress.json").read_text(encoding="utf-8"))

        assert protocol["mode"] == protocol["arm"], (
            f"the engine writes the arm as `mode` as well: {protocol['mode']!r}"
        )
        assert protocol["arm"] in arms, f"the protocol's arm is not one the engine runs: {protocol}"

        calls = progress["tool_calls"]
        assert isinstance(calls, dict), f"tool calls are counted per agent slot: {calls!r}"
        assert set(calls) == set(protocol["agents"]), (
            "the slots that made tool calls are the slots the protocol declares: "
            f"{sorted(set(calls) ^ set(protocol['agents']))}"
        )
        assert all(isinstance(count, int) for count in calls.values()), (
            f"each slot's tool calls are a count: {calls}"
        )
        assert progress["tool_calls_total"] == sum(calls.values()), (
            "the run total has to be the sum of the slots: "
            f"{progress['tool_calls_total']} against {sum(calls.values())}"
        )


def check_a_version_is_only_recorded_when_it_looks_like_one() -> None:
    """The fingerprint recorded a broken harness's complaint as its version.

    The engine's resolver returns the first line of `claude --version`, standard
    error included, and does not look at the exit status. A CLI that is on PATH
    and will not run answers with its error, and `transport.version` carried
    that sentence. Only something shaped like a version is kept now, so a broken
    harness reports none, and the line under the record already says what that
    means.
    """
    original = local_review.engine_public
    answers = {
        "2.0.14 (Claude Code)": "2.0.14 (Claude Code)",
        "v1.2.3": "v1.2.3",
        "claude: error while loading shared libraries: libffi.so.8": None,
        "/usr/bin/claude: not found": None,
        "Error: not logged in": None,
        "": None,
        None: None,
    }
    try:
        for reported, expected in answers.items():
            local_review.engine_public = lambda *a, reported=reported, **k: (
                lambda: reported
            )
            assert local_review.claude_version() == expected, (
                f"{reported!r} should be recorded as {expected!r}, got "
                f"{local_review.claude_version()!r}"
            )
    finally:
        local_review.engine_public = original

    # The page is told the finding schema version by the record, and the value
    # already carries its own `v`. The component printed another one in front of
    # it, so every published page read `findings vreview-finding-v3`.
    component = (
        Path(local_review.__file__).resolve().parents[1] / "src" / "components" / "Provenance.astro"
    ).read_text(encoding="utf-8")
    assert "findings v${" not in component, (
        "the finding schema version carries its own `v`, so the page must not add one"
    )


def check_the_page_keeps_the_model_asked_apart_from_the_model_that_ran() -> None:
    """The page named one model for the whole panel, and 0.9 gives each slot one.

    A reader who sees a single model under a panel of eleven agents reads it as
    the model that wrote every report. Worse is a page that fills the column for
    what ran out of the plan: that tells the reader a slot was seen running what
    it was told to run, which is a claim nobody made. The component has to carry
    both facts per row, each from its own field, and it has to say in a sentence
    when the run recorded no model for a slot.

    The page is Astro and is rendered by the site build rather than here, so
    what this proves offline is that the component reads the two published
    fields and never writes one in the other's place.
    """
    component = _provenance_component_fields()

    for heading in ("<th>Model asked</th>", "<th>Model ran</th>"):
        assert heading in component, f"the per-agent table needs the column {heading}"
    assert 'String(row.assigned_model || "")' in component, (
        "the asked column has to be read from the run's own assigned_model field"
    )
    assert 'String(row.model || "")' in component, (
        "the ran column has to be read from the run's own model field"
    )
    assert '{row.model || "unrecorded"}' in component, (
        "a slot nobody observed reads unrecorded rather than borrowing the plan"
    )
    # Neither field may ever stand in for the other. A fallback from one to the
    # next publishes the plan as an observation, and a substituted model is
    # exactly what that would hide.
    for fallback in (
        "row.model || row.assignedModel",
        "row.assignedModel || row.model",
        "row.model || row.assigned_model",
        "row.assigned_model || row.model",
    ):
        assert fallback not in component, (
            f"the page must not fill one model fact out of the other: {fallback}"
        )

    assert "runRecord.models_unverified" in component, (
        "the page has to read the slots whose assigned model nothing observed"
    )
    assert "unverifiedModels.length > 0" in component, (
        "reading the unverified slots is only worth doing if the page says when "
        "there are any"
    )
    assert 'unverifiedModels.join(", ")' in component, (
        "the sentence has to name the slots, so a reader can see which reports it is about"
    )
    assert "the plan is all this record has" in component, (
        "a slot whose model went unrecorded gets one sentence saying so"
    )


def check_a_slot_that_ran_another_model_family_cannot_be_published() -> None:
    """A substituted model would attribute a report to a model that never wrote it.

    Claude Code answers a model it may not run with a different one rather than
    refusing, and it does that inside the session, after every check that can be
    made before a run starts. The engine is what notices, by reading each slot's
    plan against what was observed in it, and it holds the run back. There is no
    second copy of that rule here: what this path has to do is refuse, and print
    the engine's own sentence naming the slot, what it was asked for and what
    ran.

    A different version of the same family is not a substitution. It is which
    version that family resolved to on this login, so such a run publishes, and
    the record still keeps the version observed apart from the one assigned.
    """
    with tempfile.TemporaryDirectory() as tmp:
        clean = _run_directory(Path(tmp) / "clean")
        clean_reading = local_review.engine_reading(clean)
        assert clean_reading["publishable"], (
            "the fixture run has to be publishable before a swap is read into it: "
            f"{clean_reading['not_publishable_reasons']}"
        )

        def _one_slot_ran(observed: str, where: Path) -> Path:
            """The same run, with core-1 observed running `observed` instead."""
            protocol = _protocol()
            protocol["agents"]["core-1"]["model"] = observed
            runtime = _runtime(TRACKS)
            for row in runtime["agents"]:
                if row.get("label") == "core-1":
                    row["model"] = observed
            return _run_directory(
                where, **{"protocol.json": protocol, "runtime.json": runtime}
            )

        assert _assigned_model("core-1") == SONNET, (
            "this check reads core-1's plan, so the plan has to be the one it names"
        )
        swapped = _one_slot_ran(OPUS, Path(tmp) / "swapped")
        reading = local_review.engine_reading(swapped)
        assert not reading["publishable"], (
            "the engine has to hold back a run whose slot ran another model family"
        )
        reasons = [str(reason).strip() for reason in reading["not_publishable_reasons"]]
        named = [reason for reason in reasons if "core-1" in reason]
        assert named, f"the engine's reasons have to name the slot: {reasons}"
        assert SONNET in named[0] and OPUS in named[0], (
            f"the reason has to say what was asked for and what ran: {named[0]}"
        )

        try:
            local_review.require_complete_run(swapped, local_review.read_run(swapped))
        except local_review.CommandError as error:
            for reason in reasons:
                assert reason.rstrip(".") in str(error), (
                    f"the refusal has to print the engine's own reason: {error}"
                )
        else:
            raise AssertionError(
                "a run whose slot ran a different model family was published"
            )

        # The same family at another version, which the engine does not call a
        # substitution. It publishes, and the two fields stay apart in the
        # record: what ran is the id that was observed, never the planned one.
        resolved = _one_slot_ran("claude-sonnet-4-5", Path(tmp) / "resolved")
        resolved_reading = local_review.engine_reading(resolved)
        assert resolved_reading["publishable"], (
            "another version of the family a slot was assigned is the version that "
            f"family resolved to: {resolved_reading['not_publishable_reasons']}"
        )
        local_review.require_complete_run(resolved, local_review.read_run(resolved))
        rows = {row["slot"]: row for row in local_review.agent_rows(resolved_reading)}
        assert rows["core-1"]["assigned_model"] == SONNET, (
            f"the plan for core-1 was lost: {rows['core-1']}"
        )
        assert rows["core-1"]["model"] == "claude-sonnet-4-5", (
            f"what core-1 was observed running was replaced by its plan: {rows['core-1']}"
        )


def check_the_citation_section_prints_no_charge_nobody_made() -> None:
    """The citations section of a public page about named authors' own papers.

    A reference the lookups could not reach, and a reference two indexes do not
    list, are both states of a lookup rather than facts about a work. Printed
    without their own caption, or added into one total, they read as a count of
    references that do not exist, which is a charge no part of this run made.

    So the page builds its own labelled rows out of the counts: how many works
    the reference list holds, and each state with its own number and its own
    sentence saying what it does and does not mean. The three states that are
    not a clean resolution are never summed.

    What stays out of the page is the engine's one-sentence summary and the
    per-use verdict tallies inside it. Those count in-text uses a citation
    worker judged as not supported, a worker writes no part of the review, and
    an aggregate of unconfirmed verdicts is a numeric accusation against
    references nobody names. They are published in provenance.json, beside the
    counts that qualify them.

    The page is Astro and the site build renders it, so what this proves
    offline is which fields the component reads and which wordings it carries.
    """
    component = _provenance_component_fields()
    # Every sentence here is asserted against the source with its runs of
    # whitespace collapsed, because the component is wrapped prose: a phrase
    # this check cares about can sit across two lines today and on one line
    # after an editor reflows the paragraph, and a check that passed only on
    # the line breaks would stop guarding the wording the day someone tidied
    # it. Field names and expressions are matched against the source itself.
    prose = " ".join(component.split())

    assert "runRecord.citations" in component, (
        "the page has to read the citation lane from the record's own field"
    )
    for key in ("references", "resolved", "not_found", "not_located", "could_not_check"):
        assert f'citeCount("{key}")' in component, (
            f"the lane's {key} count has to be read by name and printed on its own"
        )
    # Each of the three states that is not a clean resolution carries the
    # sentence that stops it being read as a missing work.
    for caveat in (
        "usually a typo in the reference rather than anything about the work",
        "while being perfectly real",
        "no evidence at all that the work does not exist",
        "says nothing whatever about the reference",
    ):
        assert caveat in prose, f"a state of a lookup needs its own caption: {caveat}"

    # The engine's summary sentence is not printed. It bundles the three states
    # in with the one clean one and carries the verdict tallies besides.
    for printed in ("citations.summary", "citations?.summary", "citeSummary"):
        assert printed not in component, (
            f"the engine's own summary sentence must not reach the page: {printed}"
        )
    # Nor is any use-level verdict tally read at all, so none of them can be
    # printed by a later edit without this check noticing.
    for verdict in ("supported", "partly_supported", "not_supported", "cannot_tell"):
        assert f'citeCount("{verdict}")' not in component, (
            f"a use-level verdict tally belongs in the record and not on the page: {verdict}"
        )
    # And nothing adds the states together. Any arithmetic over two counts is
    # the aggregate this section exists to avoid.
    for summed in (
        'citeCount("not_found") +',
        'citeCount("not_located") +',
        'citeCount("could_not_check") +',
        '+ citeCount(',
    ):
        assert summed not in component, (
            f"the states are never added into one figure: {summed}"
        )

    # The lane's own account of what it did not finish is carried word for
    # word, under a sentence saying none of it is a finding.
    assert "citeProblems.map" in component, (
        "the engine's lines about what the lane did not settle have to be printed"
    )
    assert "Nothing in this section is a finding" in prose, (
        "a reader has to be told that a row no specialist wrote up is not a finding"
    )
    assert "the citations specialist read the row, judged it and" in prose, (
        "the page has to say what turns a row into a finding"
    )
    # A lane that was planned and left no table, and an arm that convened no
    # lane at all, each say so rather than reading as a clean result.
    assert "citeEnabled && !citeTable" in component, (
        "a planned lane with no ledger behind it needs its own wording"
    )
    assert "convened no citation lane" in prose, (
        "an arm with no lane has to say so, because absent is not zero"
    )
    assert "so the absence is not read as a clean result" in prose, (
        "the no-lane wording has to say what it is not"
    )

    # Neither empty branch may say more than the run folder knows.
    #
    # `citations.enabled` is true exactly when the plan holds the citations
    # specialist, so false means there was no such specialist. A sentence
    # promising the reader that the specialist read the works cited anyway is
    # false every time that branch prints, and it is the more damaging
    # direction of the two: it tells a reader the references were examined by
    # someone when nobody was asked to.
    assert "ran no citations specialist and convened no citation lane" in prose, (
        "the no-lane wording has to say there was no citations specialist either"
    )
    for claimed in (
        "read the works cited either way",
        "its report is beside",
    ):
        assert claimed not in prose, (
            "a run with no citations specialist must not be described as having "
            f"one that read anything: {claimed}"
        )

    # The other branch prints for three different runs: a lane that wrote no
    # ledger, a record written before the ledger existed, and a ledger file
    # that is there and could not be read. Only the first of those three is a
    # lane that looked nothing up, and the page cannot tell them apart, so it
    # reports the absence of counts and lets the engine's own line below give
    # the reason.
    assert "this record carries no counts from it" in prose, (
        "an empty lane section reports what the record lacks, not what the lane did"
    )
    assert "this page cannot say what that lane looked up or checked" in prose, (
        "the page has to admit it does not know, since an unreadable ledger lands here too"
    )
    for overclaimed in (
        "that lane looked up no reference",
        "left no table behind it",
    ):
        assert overclaimed not in prose, (
            "a record with no counts is not a lane that checked nothing: "
            f"{overclaimed}"
        )


def check_the_citation_lane_is_read_from_the_runs_own_ledger() -> None:
    """The lane's numbers come off the ledger the run wrote, through the engine.

    `read_run` fills `citations` by reading `citations/ledger.jsonl` itself, so
    the fixture here is a run folder with a real ledger in it, written row by
    row in the shape `docs/INTEGRATIONS.md` documents.

    Three things have to hold. The counts in the record are the engine's own
    counts, so the constants this suite compares pages against cannot drift
    from what 0.9 reports. The ledger path is gone, both the absolute one and
    the relative one, because the bundle carries no ledger file and a path in a
    published record points at nothing a reader can open. And a lane with rows
    still owed does not hold the review back: the engine appends its lines
    after it has decided the run publishable, and this path keeps them out of
    what went wrong.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run = _run_directory(Path(tmp) / "run")
        assert (run / CITATION_LEDGER_PATH).exists(), (
            "the fixture run has to carry a ledger for this to be reading one"
        )
        reading = local_review.engine_reading(run)
        citations = reading["citations"]

        assert citations["enabled"] is True, f"the lane was planned: {citations}"
        assert citations["complete"] is False, (
            f"a ledger with a use still owed is not complete: {citations}"
        )
        counts = {
            key: value
            for key, value in citations["counts"].items()
            if isinstance(value, int) and not isinstance(value, bool)
        }
        assert counts == CITATION_COUNTS, (
            "the engine counts this ledger differently from the constants this "
            f"suite checks pages against: {counts}"
        )
        assert citations["summary"] == CITATION_SUMMARY, (
            f"the engine's summary sentence changed: {citations['summary']}"
        )
        assert [str(line) for line in citations["problems"]] == CITATION_PROBLEMS, (
            f"the engine's own lines changed: {citations['problems']}"
        )

        # A lane with work still owed is published work rather than harm.
        assert reading["publishable"] is True, (
            f"an unfinished citation lane held the review back: {reading}"
        )
        assert reading["problems"], (
            "this run is the case where a publishable run carries problems, and a "
            "reading with none of them proves nothing"
        )
        record = local_review.read_run(run)
        assert record["errors"] == [], (
            f"the lane's unfinished work was filed as something that went wrong: {record}"
        )
        assert record["citations"] == _citation_record(), (
            f"the published lane is not the one the engine read: {record['citations']}"
        )
        published = record["citations"]
        assert "ledger" not in published and "ledger" not in published["counts"], (
            f"the bundle carries no ledger file, so no record may name one: {published}"
        )
        assert "stages" not in published["counts"], (
            f"the lane's stage record is not a tally: {published['counts']}"
        )
        assert str(run) not in json.dumps(record), (
            "the absolute ledger path reached the record"
        )

        # A planned lane that wrote no ledger says that, and still publishes.
        none = _run_directory(Path(tmp) / "none", citations=False)
        assert not (none / CITATION_LEDGER_PATH).exists(), "this run has no ledger"
        empty = local_review.read_run(none)["citations"]
        assert empty["enabled"] is True and empty["counts"] == {}, (
            f"a planned lane with no table is enabled and holds no counts: {empty}"
        )
        assert len(empty["problems"]) == 1 and "no citation ledger" in empty["problems"][0], (
            f"the engine's one line about an empty lane was lost: {empty}"
        )
        assert local_review.read_run(none)["errors"] == [], (
            "a lane that checked nothing is work the lane did not get to"
        )
        assert local_review.read_run(none)["publishable"] is True, (
            "an empty citation lane cannot hold a finished review back"
        )


def check_a_citation_worker_on_another_model_is_not_an_error() -> None:
    """A worker that ran another family is a line beside the review, not a gate.

    A reviewer slot observed running a model family other than the one it was
    assigned makes the run unpublishable, because a report would be attributed
    to a model that did not write it. A citation worker writes no report: it
    looks a reference up and answers one question about one sentence, and the
    engine's own answer is to publish the run and say so in `problems`.

    So this path has to carry that line and must not file it under what went
    wrong, and the run has to publish.
    """
    with tempfile.TemporaryDirectory() as tmp:
        protocol = _protocol()
        protocol["agents"]["cite-1"]["model"] = OPUS
        runtime = _runtime(TRACKS)
        for row in runtime["agents"]:
            if row.get("label") == "cite-1":
                row["model"] = OPUS
        assert _assigned_model("cite-1") == HAIKU, (
            "this check reads cite-1's plan, so the plan has to be the one it names"
        )
        swapped = _run_directory(
            Path(tmp) / "swapped",
            **{"protocol.json": protocol, "runtime.json": runtime},
        )
        reading = local_review.engine_reading(swapped)
        assert reading["publishable"] is True, (
            f"a worker on another model family held the review back: {reading}"
        )
        assert reading["not_publishable_reasons"] == [], (
            f"the engine gated on a slot that wrote nothing: {reading}"
        )
        named = [
            str(line) for line in reading["problems"] if str(line).split(" ", 1)[0] == "cite-1"
        ]
        assert named, f"the engine's line about the worker was lost: {reading['problems']}"
        assert HAIKU in named[0] and OPUS in named[0], (
            f"the line has to say what was asked for and what ran: {named[0]}"
        )

        record = local_review.read_run(swapped)
        assert record["errors"] == [], (
            f"a worker's substitution was published as an error: {record['errors']}"
        )
        # And the publish path agrees: the run goes out.
        local_review.require_complete_run(swapped, record)
        # The same swap in a reviewer slot still refuses, which is what keeps
        # this allowance about the slots that write nothing.
        protocol = _protocol()
        protocol["agents"]["core-1"]["model"] = OPUS
        runtime = _runtime(TRACKS)
        for row in runtime["agents"]:
            if row.get("label") == "core-1":
                row["model"] = OPUS
        reviewer = _run_directory(
            Path(tmp) / "reviewer",
            **{"protocol.json": protocol, "runtime.json": runtime},
        )
        assert not local_review.engine_reading(reviewer)["publishable"], (
            "a reviewer slot that ran another model family is still refused"
        )


def check_the_published_issues_file_is_a_later_rounds_prior_input() -> None:
    """Publish a bundle, then read its issues file the way the next round does.

    This is the other half of a persistent id. Publishing the engine's ids is no
    use if the file they are published in is one the next round refuses, and
    that refusal would arrive a round later, in front of the authors, with the
    ids already printed in a decision letter. So the file is read back off disk
    and put through the rules the engine's own prior-round loader applies: a
    known schema stamp, every row an object with a string id of the engine's
    form, no id twice across open and closed rows alike, every `members` and
    `surviving_quotes` a list, and `issue_ids_used` present and accounting for
    every id in the file.

    `prior_issues_file` is the function `prepare` uses to find this file for the
    next round, so it is asked for the same answer here rather than the path
    being rebuilt by hand.
    """
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    _run_directory(Path(tmp) / "run"),
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"

            # The next round finds the file through this function, not by a path
            # built here, and a bundle with nothing open in it answers None.
            found = local_review.prior_issues_file(destination)
            assert found == destination / local_review.REVIEW_ISSUES, (
                f"the next round would not find this round's issues: {found}"
            )
            document = json.loads(found.read_text())

    assert document["schema_version"] == ISSUES_SCHEMA, (
        f"the published file carries no readable schema stamp: {document.get('schema_version')}"
    )
    rows = document["issues"]
    assert rows and all(isinstance(row, dict) for row in rows), (
        "every row of a prior-round file has to be an object"
    )
    identifiers = [row.get("id") for row in rows]
    assert all(isinstance(name, str) and name for name in identifiers), (
        f"an id that is not a string is not an id the engine can match: {identifiers}"
    )
    assert all(local_review.ISSUE_ID_PATTERN.match(name) for name in identifiers), (
        f"an id is not of the engine's own form: {identifiers}"
    )
    assert len(set(identifiers)) == len(identifiers), (
        f"an id appears twice across the open and closed rows: {identifiers}"
    )
    for row in rows:
        assert isinstance(row.get("members"), list), f"members is not a list: {row['id']}"
        assert isinstance(row.get("surviving_quotes"), list), (
            f"surviving_quotes is not a list: {row['id']}"
        )
    spent = document["issue_ids_used"]
    assert isinstance(spent, list) and spent, "the spent ids were not carried into the bundle"
    assert all(local_review.ISSUE_ID_PATTERN.match(str(name)) for name in spent), (
        f"a spent id is not of the engine's own form: {spent}"
    )
    assert not set(identifiers) - set(spent), (
        f"an id in the file is missing from issue_ids_used: {set(identifiers) - set(spent)}"
    )
    # The prior round's own ids are in that list although this round carries
    # only one of them as a row, which is what stops a later round handing a
    # retired id to a different problem.
    assert "i05" in spent, f"a resolved id was dropped from the spent list: {spent}"


def check_the_run_manifests_manuscript_path_never_reaches_a_bundle() -> None:
    """The run's manifest names the manuscript on the operator's disk.

    The plugin server writes the absolute path of the PDF it was handed into the
    run's `manifest.json`, along with the absolute path of the plugin it loaded.
    Neither is a fact about the review, both are facts about one machine, and
    the bundle is a public artifact. The manifest is therefore never published
    as it stands: what travels is the fingerprint computed from it, which is a
    hash and a file count.

    The fixture run carries both paths, so this check reads every file of a
    published bundle back off disk and looks for them. It is deliberately a
    check on the bytes that were written rather than on the code that wrote
    them, because the engine is free to start recording a path in a field
    nothing here knows about.
    """
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run")
            manifest = json.loads((run / "manifest.json").read_text())
            pdf = str(manifest["pdf"])
            plugin_root = str(manifest["plugin_root"])
            assert pdf.startswith("/") and plugin_root.startswith("/"), (
                f"the fixture manifest has to hold absolute paths: {pdf}, {plugin_root}"
            )

            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"

            published = sorted(path for path in destination.rglob("*") if path.is_file())
            assert published, "nothing was published, so this check proved nothing"
            for path in published:
                text = path.read_text(encoding="utf-8", errors="replace")
                assert pdf not in text, f"{path.name} names the manuscript on the operator's disk"
                assert plugin_root not in text, f"{path.name} names the plugin on the operator's disk"
                assert Path(pdf).name not in text, (
                    f"{path.name} names the file the operator's copy of the manuscript sat in"
                )

            # What does travel is the fingerprint taken from that manifest: a
            # hash and a count of the files it listed.
            record = json.loads((destination / "provenance.json").read_text())
            fingerprint = record["generator"]["engine_fingerprint"]
            assert fingerprint["source"] == "run_manifest", (
                f"the fingerprint was not taken from the run's own manifest: {fingerprint}"
            )
            assert fingerprint["file_count"] > 0 and len(fingerprint["sha256"]) == 64, (
                f"the fingerprint is not a hash over the files the run loaded: {fingerprint}"
            )


def check_a_published_bundle_carries_no_ledger_and_no_fetched_text() -> None:
    """Publish a run with a citation lane, and read the whole bundle back.

    Two things must not travel. The ledger rows are not published, because a
    row the citations specialist did not read and write up is not a finding and
    printing one would make it look like one. The lookups cache is not
    published either: it holds abstracts and passages fetched from publishers,
    the review rests on that text only through the short passage quoted inside
    a confirmed verdict, and republishing the rest would make this site a
    mirror of other people's copy.

    The counts and the engine's own lines about what the lane did not settle do
    travel, in provenance.json, which is what a reader can act on.
    """
    from fixtures import make_citation_ledger

    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        with _published_tree(Path(tmp) / "reviews") as reviews:
            run = _run_directory(Path(tmp) / "run")
            cache = run / "citations" / "lookups"
            assert any(cache.iterdir()), "the fixture run has to have fetched something"
            assert make_citation_ledger.FETCHED_PHRASE in "".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in sorted(cache.iterdir())
                if path.is_file()
            ), "the phrase this check looks for has to be in the run's own cache"

            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = _publish(
                    _prepared(Path(tmp) / "prepared", destination),
                    run,
                    _workspace(Path(tmp) / "workspace"),
                    "--publish",
                )
            assert code == 0, f"this bundle should publish, got exit {code}: {out.getvalue()}"

            written = sorted(
                str(path.relative_to(destination))
                for path in destination.rglob("*")
                if path.is_file()
            )
            assert "manifest.json" in written, f"the bundle was not finished: {written}"
            # The citations specialist's own report is published like every
            # other track report. What may not travel is the run's
            # `citations/` folder, which is the rows and the fetched text.
            assert "audit_citations.md" in written, (
                f"the citations specialist's report belongs in the bundle: {written}"
            )
            assert not [name for name in written if name.startswith("citations/")], (
                f"the citation lane's own folder reached the bundle: {written}"
            )
            assert not [name for name in written if "ledger" in name], (
                f"a ledger was published: {written}"
            )
            assert not [name for name in written if name.endswith(".jsonl")], (
                f"a row file was published: {written}"
            )
            for path in sorted(destination.rglob("*")):
                if path.is_file():
                    text = path.read_text(encoding="utf-8", errors="replace")
                    assert make_citation_ledger.FETCHED_PHRASE not in text, (
                        f"{path.name} carries text fetched from a publisher"
                    )
                    assert "ledger.jsonl" not in text, (
                        f"{path.name} names a ledger the bundle does not carry"
                    )

            # What does travel is the lane's state, where a reader can use it.
            record = json.loads((destination / "provenance.json").read_text())
            published = record["generator"]["run"]["citations"]
            assert published == _citation_record(), (
                f"the lane's own state did not reach the record: {published}"
            )


def _engine_round(out: Path, number: int, prior: str) -> dict:
    """Drive one round of the fixture generator and return what it wrote.

    `scripts/fixtures/make_engine_rounds.py` runs the engine's own plugin over a
    PDF it builds, with no model and no network, and prints a JSON line
    describing the run folder. One round per call, because the engine serves one
    paper per process and because a later round has to be given the file the
    round before it published.
    """
    generator = Path(local_review.__file__).resolve().parent / "fixtures" / "make_engine_rounds.py"
    done = subprocess.run(
        [sys.executable, str(generator), "--out", str(out), "--round", str(number),
         "--prior", prior],
        capture_output=True,
        text=True,
        check=False,
        timeout=900,
    )
    assert done.returncode == 0, (
        f"round {number} of the fixture generator failed with exit "
        f"{done.returncode}: {done.stdout[-1500:]}{done.stderr[-1500:]}"
    )
    return json.loads(done.stdout.strip().splitlines()[-1])


def _plugin_tree(run: Path) -> None:
    """Record the plugin files a session would have loaded, hashed for real.

    The plugin server hashes the engine's modules and its own, and the starter
    hashes the Claude Code plugin tree it hands the session. Nothing handed this
    run a plugin tree, because nothing started a session, so the folder carries
    two thirds of the manifest and the publish path refuses it. The hashes put
    here are the installed plugin's own bytes, read through the engine's
    `plugin_directory`, which is what a run started in this environment would
    have recorded.
    """
    path = run / "review" / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    installed = local_review.installed_code_manifest()
    manifest["code"].update(
        {
            name: value
            for name, value in installed.items()
            if name.startswith(local_review.PLUGIN_PREFIX)
        }
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _session_evidence(run: Path) -> None:
    """Write the start-up probe and the harness record, which are this suite's.

    Those two files are the evidence that a Claude Code session started, loaded
    the plugin and ran the agents, and no session did: this fixture is the
    agents. So they are written here, out of the suite's own `_startup` and
    `_runtime`, into a temporary folder, and the check below first proves the
    publish path refuses the run without them. The slots and the models in the
    harness record are read out of the run's own `protocol.json`, so the record
    says what this run asked for rather than what another fixture asked for.
    """
    review = run / "review"
    protocol = json.loads((review / "protocol.json").read_text(encoding="utf-8"))
    rows = [
        {
            "label": slot,
            "state": "complete",
            "attempt": 1,
            "agentType": f"pra:{slot}",
            "model": model,
            "tokens": 24000,
            "toolCalls": 6,
            "durationMs": 120000,
        }
        for slot, model in sorted(protocol["models"].items())
    ]
    (review / "runtime.json").write_text(
        json.dumps(_runtime((), agents=rows), indent=2) + "\n", encoding="utf-8"
    )
    (review / "startup.json").write_text(
        json.dumps(_startup(), indent=2) + "\n", encoding="utf-8"
    )


def _engine_prepared(root: Path, destination: Path, run: Path, pdf: Path, **overrides) -> Path:
    """What prepare would have written for the paper this run really imported.

    The publish path refuses a run of one paper published under another paper's
    identity, by comparing the hash prepare took of the fetched bytes against
    the hash the importer recorded. So the hash here is read out of the run's
    own import manifest rather than made up, and the rest of the record is the
    suite's preprint fixture.
    """
    manifest = json.loads(
        (run / "manuscript" / "manifest.json").read_text(encoding="utf-8")
    )
    return _prepared(
        root,
        destination,
        input={
            "kind": "doi",
            "identifier": PAPER.doi,
            "sha256": manifest["source"]["sha256"],
            "bytes": pdf.stat().st_size,
            "local_file": False,
        },
        **overrides,
    )


def _publish_refusal(prepared: Path, run: Path, workspace: Path) -> str:
    """Publish, expect a refusal, and hand back the sentence it refused with."""
    out = io.StringIO()
    errors = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(errors):
        code = _publish(prepared, run, workspace, "--publish")
    assert code != 0, f"this publish should have been refused: {out.getvalue()}"
    return errors.getvalue() + out.getvalue()


def check_two_rounds_the_engine_itself_wrote_publish() -> None:
    """Publish a run folder the engine wrote, and a second round that reads it back.

    Every other check here publishes a fixture: a run folder typed out in this
    file from the engine's documents. That is a copy of what this repository
    believes the engine writes, and a field the engine starts writing
    differently stays as it was typed until somebody notices. This check
    publishes what the engine produces. `scripts/fixtures/make_engine_rounds.py`
    drives the plugin over a PDF it builds, filing the findings, pooling them
    into issues and ruling on the round before, and the publish path then reads
    that folder.

    Two of the files a published bundle rests on cannot come from that
    generator, and the check proves it before it supplies them. The plugin tree
    is hashed by the starter out of the directory it hands a session, and the
    start-up probe is the engine's evidence that the session connected the
    plugin's MCP server. Nothing started a session here, because this fixture is
    the reviewers, so the folder as the generator leaves it is refused twice
    over, once for the manifest and once for the probe. Only then are the two
    supplied, from the installed plugin's real bytes and from this suite's own
    probe, and what publishes is a bundle whose every review document is the
    engine's.

    Then the round the two blockers were about. The second round is given the
    file the first round published, which is what `prepare` hands the engine, so
    the digest the run records of its prior input is a digest of the published
    bytes. It carries one prior item forward as persisting, rules one resolved
    with a sentence that still reads the same in the revision, and leaves one
    unverified. The letter has to print those surviving sentences as the
    authors' words and the record has to carry the reasons, both of which were
    wrong against a hand written fixture until this round.

    The field names are checked in both directions too, because that is the
    drift this generator exists to catch: nothing the hand written package
    declares may be missing from the engine's own `issues.json`, and nothing the
    engine writes there may be missing from the fixture, but for `stages`, which
    the fixture carries in `progress.json` instead.
    """
    with _stub_engine(), tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "rounds"
        first = _engine_round(out, 1, "")
        run = Path(first["run"])
        assert first["publishable"], f"the engine called its own run unpublishable: {first}"

        # What the engine wrote, before anything of this suite's is added to it.
        document = json.loads((run / "review" / "issues.json").read_text(encoding="utf-8"))
        absent = sorted(set(PACKAGE) - set(document))
        assert not absent, (
            f"the hand written package declares fields the engine does not write: {absent}"
        )
        extra = sorted(set(document) - set(PACKAGE) - {"stages"})
        assert not extra, (
            f"the engine writes fields the hand written package has never heard of: {extra}"
        )
        rows = document["issues"]
        assert rows, "the engine wrote no issues at all"
        drifted = sorted(set(rows[0]) ^ set(PACKAGE["issues"][0]))
        assert not drifted, f"an issue row has drifted from the fixture's: {drifted}"

        # And the members inside a row, which is where a finding says what it
        # cites: the document, the line, the end line and the quoted words. That
        # is the shape this round moved to, so it is the shape most likely to
        # drift, and a member key the fixture invented or missed would be a
        # fixture testing a review nobody writes.
        engine_member_keys = {key for row in rows for member in row["members"] for key in member}
        fixture_member_keys = {
            key for row in PACKAGE["issues"] for member in row["members"] for key in member
        }
        drifted = sorted(engine_member_keys ^ fixture_member_keys)
        assert not drifted, f"an issue member has drifted from the fixture's: {drifted}"
        for name in ("document", "line", "end_line", "quote", "start", "end", "anchor_text"):
            assert name in engine_member_keys, (
                f"the engine's own members carry no {name}, so a finding does not say "
                f"where it reads: {sorted(engine_member_keys)}"
            )

        # The manuscript folder the engine imported, in the shape every line
        # number in the review is a line of.
        workspace = json.loads(
            (run / "manuscript" / "manifest.json").read_text(encoding="utf-8")
        )
        # Read off the engine rather than typed, because the publish path reads
        # it off the engine too: a release that stamped a new shape would
        # otherwise be caught here by a name while the pipeline went on
        # publishing against whatever the new shape turned out to be.
        base_schema = local_review.engine_public(
            "BASE_SCHEMA_VERSION", "the base schema version cannot be read"
        )
        assert workspace["schema_version"] == base_schema, (
            f"the imported manuscript is not the shape this release reads: {workspace}"
        )
        assert base_schema != "paper-base-v1", (
            "paper-base-v1 carries no source on a map row and no account of the "
            "Read stage, so a review published over it could not say which of "
            "its lines a model wrote"
        )
        for name in (MAIN_DOCUMENT, "map.json"):
            assert (run / "manuscript" / name).is_file(), (
                f"the engine's own import holds no {name}"
            )
            assert name in workspace["files"], (
                f"{name} is not digested by the import manifest, so an edit to it "
                "would go unnoticed"
            )
        assert not (run / "manuscript" / "paper.json").exists(), (
            "the engine still writes the block shape this pipeline stopped reading"
        )

        with _published_tree(Path(tmp) / "reviews") as reviews:
            destination = reviews / "2026" / "fixture-paper" / "v1" / "r1"
            prepared = _engine_prepared(
                Path(tmp) / "prepared-1",
                destination,
                run,
                out / "manuscript.pdf",
                round=1,
                prior_issues="",
                plan_kind="first round",
            )

            # The folder as the generator leaves it, refused for the plugin tree
            # nothing handed it.
            refusal = _publish_refusal(prepared, run, run / "manuscript")
            assert "plugin/" in refusal, (
                f"a run with no plugin tree in its manifest has to be refused for it: {refusal}"
            )
            assert not destination.exists(), "a refused publish wrote a bundle anyway"

            # And then for the session that never started.
            _plugin_tree(run)
            refusal = _publish_refusal(prepared, run, run / "manuscript")
            assert "start-up probe" in refusal, (
                f"a run with no start-up probe has to be refused for it: {refusal}"
            )
            assert not destination.exists(), "a refused publish wrote a bundle anyway"

            _session_evidence(run)
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                code = _publish(prepared, run, run / "manuscript", "--publish")
            assert code == 0, (
                f"a run the engine wrote should publish, got exit {code}: {printed.getvalue()}"
            )
            published = local_review.prior_issues_file(destination)
            assert published == destination / local_review.REVIEW_ISSUES, (
                f"the next round would not find this round's issues: {published}"
            )

            # The second round reads the file the first round published, which is
            # the file `prepare` hands the engine, and records a digest of those
            # bytes.
            second = _engine_round(out, 2, str(published))
            later = Path(second["run"])
            reading = json.loads((later / "review" / "issues.json").read_text(encoding="utf-8"))
            recorded = (reading.get("prior_round") or {}).get("digest")
            expected = local_review.digest(published.read_bytes())[:16]
            assert recorded == expected, (
                "the engine's record of its prior input is not a digest of the published "
                f"bytes: {recorded} against {expected}"
            )

            _plugin_tree(later)
            _session_evidence(later)
            next_destination = reviews / "2026" / "fixture-paper" / "v2" / "r1"
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                code = _publish(
                    _engine_prepared(
                        Path(tmp) / "prepared-2",
                        next_destination,
                        later,
                        out / "revision.pdf",
                        round=2,
                        draft=2,
                        prior_issues=str(published),
                    ),
                    later,
                    later / "manuscript",
                    "--publish",
                )
            assert code == 0, (
                f"the second round should publish, got exit {code}: {printed.getvalue()}"
            )
            record = json.loads((next_destination / "round.json").read_text(encoding="utf-8"))
            letter = (next_destination / "decision_letter.md").read_text(encoding="utf-8")

    closed = record["closed_issues"]
    resolved = closed["resolved"]
    unverified = closed["unverified"]
    assert len(resolved) == 1 and len(unverified) == 1, (
        f"the second round ruled on something other than one of each: {closed}"
    )
    for row in resolved + unverified:
        assert row["status_reason"].strip(), f"a ruling carries no reason: {row['id']}"
        quotes = row["surviving_quotes"]
        assert quotes and all(isinstance(quote, dict) for quote in quotes), (
            f"the engine's surviving quotes did not reach the record: {row['id']}"
        )
        for quote in quotes:
            assert {"finding_uid", "document", "line", "quote"} <= set(quote), (
                f"a surviving quote is missing a field the engine writes: {quote}"
            )
            # And the field set the fixture's own surviving quotes carry, so a
            # row the engine starts writing differently fails here rather than
            # being rendered from a fixture nobody wrote.
            drifted = sorted(set(quote) ^ set(ISSUES[4]["surviving_quotes"][0]))
            assert not drifted, (
                f"a surviving quote has drifted from the fixture's: {drifted}"
            )
            # The authors read their own sentence, not a mapping of it.
            assert f"> {quote['quote']}" in letter, (
                f"the letter does not print the surviving sentence as a quotation: {quote}"
            )
    assert resolved[0]["text_unchanged_reason"].strip(), (
        "a resolved item whose quoted sentence still reads the same has to say why"
    )
    assert "finding_uid" not in letter and "'quote'" not in letter, (
        "the letter prints a mapping where the authors should read a sentence"
    )

    # The quote marked in the line it reads on, which is what the engine's
    # offsets are for. The marks are counted in the characters of the converted
    # line, so the row above a row of carets has to hold the words the member
    # anchored: a letter that marked anything else would be pointing the authors
    # at the wrong part of their own sentence.
    rendered = letter.splitlines()
    anchored = {
        str(member.get("anchor_text") or "")
        for issue in reading["issues"]
        for member in issue["members"]
    }
    marked = []
    for index, row in enumerate(rendered):
        stripped = row.strip()
        if index and stripped and set(stripped) == {"^"}:
            column = row.index("^")
            marked.append(rendered[index - 1][column:column + len(stripped)])
    assert marked, (
        "the letter marks no quote in the line it reads on, so the offsets the "
        "engine recorded reach no reader"
    )
    stray = sorted(set(marked) - anchored)
    assert not stray, f"the letter marks characters no member anchored: {stray}"
    standing = {row["id"]: row["status"] for row in record["required_revisions"]}
    assert standing.get("i01") == "persisting", (
        f"the item both rounds raised is not marked persisting: {standing}"
    )
    assert unverified[0]["id"] in record["carried_forward"], (
        "an item nobody verified has to be carried into the next round"
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
    (
        check_a_bundle_says_which_lines_a_model_wrote,
        "a bundle says which lines a model wrote and which pages only it read",
    ),
    (
        check_a_review_of_a_detection_paper_publishes,
        "a review full of @-notation publishes, and one naming a Windows path does not",
    ),
    (
        check_a_record_the_schema_refuses_is_never_written,
        "a record the provenance schema refuses is never written",
    ),
    (
        check_an_editor_can_publish_a_hit_the_review_meant_and_never_a_fact,
        "the editor can allow a hit the review meant, and never one about this machine",
    ),
    (
        check_a_draft_check_run_is_refused_as_the_arm_it_is,
        "a draft check is refused as the arm it is, not as a thin review",
    ),
    (
        check_a_machine_fact_in_any_spelling_leaves_no_bundle_behind,
        "a fact in any spelling refuses the publish and leaves nothing on disk",
    ),
    (
        check_a_slot_that_ran_another_model_family_cannot_be_published,
        "a slot that ran another model family is refused in the engine's own words",
    ),
    (
        check_the_citation_lane_is_read_from_the_runs_own_ledger,
        "the citation lane is counted off the ledger the run wrote",
    ),
    (
        check_a_citation_worker_on_another_model_is_not_an_error,
        "a citation worker on another model is a line beside the review, not a gate",
    ),
    (
        check_a_published_bundle_carries_no_ledger_and_no_fetched_text,
        "a published bundle carries no ledger row and no fetched publisher text",
    ),
    (
        check_the_published_issues_file_is_a_later_rounds_prior_input,
        "the published issues file is one the next round accepts as its prior input",
    ),
    (
        check_the_run_manifests_manuscript_path_never_reaches_a_bundle,
        "the manuscript path in the run's manifest never reaches a published file",
    ),
    (
        check_two_rounds_the_engine_itself_wrote_publish,
        "two rounds the engine itself wrote publish, the second reading the first",
    ),
    (
        check_a_run_of_one_paper_cannot_be_published_as_another,
        "a run is bound to the paper that was prepared, through the engine's own reader",
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
