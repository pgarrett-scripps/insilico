#!/usr/bin/env python3
"""Build two run folders by driving the engine, not by writing what one looks like.

The hand written fixtures in the smoke suite are copies of a run folder: every
field was typed out here from the engine's documents, and a field the engine
starts writing differently stays as it was typed until somebody notices. That is
the wrong way round for the files the publish path reads. This script produces
the same thing the engine does, because it is the engine that produces it. One
server process per round, the plugin's own calls in the order a session makes
them, and `issues.json`, `findings.jsonl`, `progress.json`, `manifest.json`,
`REVIEW.md` and the rest written by the engine's own writers.

Two rounds, because a paper can be reviewed twice and the second bundle is
published at `r2` on the paper's page. Each round is a review of the draft in
front of it and nothing else: the second reads the revised manuscript, raises
what it finds there, and is given no part of the first round, because no review
on this path reads an earlier one.

No model and no network. The reader, the reviewers, the editor and the recorder
here are all this script: it drives the Read stage through the engine's public
`scripted_read`, views every page and seals the manuscript, then claims each
slot with the claim code the run minted, reads the whole paper, files findings
quoted verbatim out of it, groups them into issues and asks the recorder to
write the review. The
manuscript is a PDF built here out of the sentences below, so there is no paper
to fetch and nothing to look up. The `reviewers-only` arm is the smallest arm
whose issues an editor writes, which is what `publishable` asks about.

One process per round is the engine's rule rather than a convenience: a server
serves one paper, and a second `ingest` in the same process is refused. So each
round runs as a subprocess of this script.

Running it:

    python3 scripts/fixtures/make_engine_rounds.py --out /tmp/engine-rounds

writes `round-1/` and `round-2/` run folders under `--out` with the two
manuscripts beside them, and prints what each review holds. The interpreter has
to be one the engine is installed in.

Nothing here is pinned and nothing pretends to be. A run folder carries the time
it ran and the digests of its own files, so two runs of this script differ in
those fields. This is a fixture builder for a check that reads the folder, not a
golden file to diff.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# The smallest arm an editor writes the issues in, with two core reviewers,
# which is enough for an issue raised by two of them.
ARM = "reviewers-only"
REVIEWERS = 2
TITLE = "A Held Out Split, Reported Throughout: A Fixture Manuscript"

# The manuscript, sentence by sentence, because the review quotes it. A quote is
# one of these strings: the converter joins the wrapped lines back together with
# single spaces, so the sentence that goes into the PDF is the sentence the
# engine finds in a line of `paper.md`.
ABSTRACT = (
    "The measured improvement of eleven percent was recorded on a single held "
    "out split and the paper reports it as the headline result throughout.",
    "The interval around that improvement is quoted to three decimal places "
    "and no seed is recorded for the resampling that produced it.",
    "The approach is described as generalising to other instruments although "
    "every experiment reported here was run on one instrument.",
)
METHODS = (
    "The normalisation step is described in one sentence and the paper does "
    "not say which of the two candidate scalers was fitted before the split.",
    "The comparison against the earlier method reuses the numbers that method "
    "published rather than running it again on this corpus.",
    "Counts per class for the held out split are available on request.",
)
RESULTS = (
    "The table reports the headline figure to two decimal places while the "
    "text rounds it to a whole number in three places.",
    "No measure of spread is given for the second dataset and the row for it "
    "is marked as a single run.",
)

PAGES = (("Abstract", ABSTRACT), ("Methods", METHODS), ("Results", RESULTS))

# The revision. One sentence is rewritten and everything else is left as it was,
# so the second draft is a draft the panel can raise fewer items against without
# the two manuscripts being the same bytes.
REWRITTEN = {
    METHODS[1]: (
        "The comparison against the earlier method was rerun on this corpus "
        "under the conditions this paper reports, and both numbers are given."
    ),
}

HEADLINE = "The headline improvement rests on one held out split"
INTERVAL = "The interval is quoted more precisely than its procedure supports"
NORMALISATION = "The normalisation step cannot be reproduced as written"
COMPARISON = "The comparison reuses published numbers"
COUNTS = "Per class counts are withheld"
ROUNDING = "The table and the text round the headline figure differently"

ONE_MEASUREMENT = "The headline result is one measurement"
CANNOT_RERUN = "The method as written cannot be run again"
PRINT_THE_COUNTS = "Per class counts belong in the paper"
ROUNDS_DIFFER = "The table and the text do not agree on the headline figure"

# Each round: the manuscript it reads, what each reviewer files, how the editor
# groups it, and the verdict it closes on. `sentence` is the quote, and the
# engine places it: it finds the words in `paper.md` and records the line, so a
# sentence that moves to another page needs no change here. `members` names
# findings by their title, because a finding uid is minted by the engine and
# cannot be written down in advance.
ROUNDS = (
    {
        "revision": False,
        "findings": {
            "core-1": (
                {
                    "title": HEADLINE,
                    "sentence": ABSTRACT[0],
                    "severity": "major",
                    "kind": "question",
                    "comment": "One split cannot carry a number the abstract, the results and "
                               "the discussion all repeat. Report the improvement over "
                               "repeated splits, or report it as a single measurement.",
                    "escalate": True,
                },
                {
                    "title": INTERVAL,
                    "sentence": ABSTRACT[1],
                    "severity": "moderate",
                    "kind": "question",
                    "comment": "Three decimal places with no seed is a precision the "
                               "resampling cannot be checked at. Record the seed and how "
                               "many resamples were drawn.",
                    "escalate": False,
                },
            ),
            "core-2": (
                {
                    "title": NORMALISATION,
                    "sentence": METHODS[0],
                    "severity": "major",
                    "kind": "question",
                    "comment": "Which scaler was fitted, and whether it was fitted before the "
                               "split was drawn, decides whether the held out split is held "
                               "out at all.",
                    "escalate": False,
                },
                {
                    "title": COMPARISON,
                    "sentence": METHODS[1],
                    "severity": "moderate",
                    "kind": "question",
                    "comment": "Numbers from another corpus under other conditions are not a "
                               "comparison. Run the earlier method here, or say that it was "
                               "not run.",
                    "escalate": False,
                },
                {
                    "title": COUNTS,
                    "sentence": METHODS[2],
                    "severity": "minor",
                    "kind": "question",
                    "comment": "Counts per class are a table, not a request. Print them.",
                    "escalate": False,
                },
            ),
        },
        "issues": (
            {
                "name": ONE_MEASUREMENT,
                "severity": "major",
                "category": "statistics-and-inference",
                "rank": 1,
                "statement": "The improvement the paper is built on was measured once, on one "
                             "held out split, and its interval is quoted to three decimals "
                             "with no seed. Report it over repeated splits, or report it as a "
                             "single measurement.",
                "members": (HEADLINE, INTERVAL),
            },
            {
                "name": CANNOT_RERUN,
                "severity": "major",
                "category": "reproducibility",
                "rank": 2,
                "statement": "The normalisation is one sentence that does not say which scaler "
                             "was fitted or when, and the comparison against the earlier "
                             "method reuses numbers from elsewhere. Neither can be rerun from "
                             "the paper.",
                "members": (NORMALISATION, COMPARISON),
            },
            {
                "name": PRINT_THE_COUNTS,
                "severity": "minor",
                "category": "methods-and-reporting",
                "rank": 3,
                "statement": "The held out split's counts per class are offered on request. "
                             "Print them in the paper.",
                "members": (COUNTS,),
            },
        ),
        "summary": "The work is clearly written and the question is worth asking. What this "
                   "review turns on is that the number the paper is built on was measured "
                   "once and is reported everywhere as though it had been measured "
                   "repeatedly, and that the method as written cannot be run again to check "
                   "it.",
        "significance": "If the improvement holds over repeated splits it is a result worth "
                        "having, and nothing in the paper yet shows that it does.",
        "evidence": "One measurement, an interval whose procedure is not recorded, and a "
                    "comparison against numbers from another corpus.",
        "reasoning": "Both required changes are answerable with what the authors already "
                     "have: rerun the split, and write down what was done.",
        "limitations": ("No reviewer here ran the authors' code, so nothing in this review is "
                        "a replication of their result.",),
    },
    {
        "revision": True,
        "findings": {
            "core-1": (
                {
                    "title": HEADLINE,
                    "sentence": ABSTRACT[0],
                    "severity": "major",
                    "kind": "question",
                    "comment": "The design this draft reports is one split, and the number "
                               "measured on it is repeated throughout as the result.",
                    "escalate": True,
                },
                {
                    "title": INTERVAL,
                    "sentence": ABSTRACT[1],
                    "severity": "moderate",
                    "kind": "question",
                    "comment": "No seed is recorded for the resampling, so the interval is "
                               "quoted more precisely than it can be checked at.",
                    "escalate": False,
                },
            ),
            "core-2": (
                {
                    "title": ROUNDING,
                    "sentence": RESULTS[0],
                    "severity": "moderate",
                    "kind": "question",
                    "comment": "Two decimal places in the table and a whole number in the "
                               "text are two different claims about the same figure. Round "
                               "once and say where.",
                    "escalate": False,
                },
            ),
        },
        "issues": (
            {
                "name": ONE_MEASUREMENT,
                "severity": "major",
                "category": "statistics-and-inference",
                "rank": 1,
                "statement": "The improvement this draft is built on was measured once, on one "
                             "held out split, and the interval around it carries no seed. "
                             "Report it over repeated splits, or report it as a single "
                             "measurement.",
                "members": (HEADLINE, INTERVAL),
            },
            {
                "name": ROUNDS_DIFFER,
                "severity": "moderate",
                "category": "results-and-numbers",
                "rank": 2,
                "statement": "The table gives the headline figure to two decimals and the "
                             "text rounds it to a whole number in three places. Round it once "
                             "and say which places are rounded.",
                "members": (ROUNDING,),
            },
        ),
        "summary": "What this review turns on is that the headline improvement is a single "
                   "measurement reported as the result. The table and the text also round "
                   "that figure differently, which is a second thing the reader cannot settle "
                   "from the paper.",
        "significance": "The result would matter if it held over repeated splits, and this "
                        "draft shows one measurement.",
        "evidence": "One measurement and no seed, against a method section that can be rerun "
                    "as written.",
        "reasoning": "Both items are answerable with what the authors already have: rerun the "
                     "split, and round the figure once.",
        "limitations": ("No reviewer here ran the authors' code, so nothing in this review is "
                        "a replication of their result.",),
    },
)


def pdf_bytes(pages: list[list[str]]) -> bytes:
    """A PDF of one text page per list of lines, written out by hand.

    Small enough to read and to build with nothing installed, which is the
    point: a fixture manuscript that needs a library to make is a fixture nobody
    regenerates.
    """
    objects: list[bytes] = []
    # Object 1 is the catalogue, 2 the page tree, 3 the font. Each page and its
    # content stream follow in pairs, so the page tree can name them up front.
    first_page = 4
    kids = " ".join(f"{first_page + 2 * index} 0 R" for index in range(len(pages)))
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for index, lines in enumerate(pages):
        stream_lines = ["BT", "/F1 11 Tf", "15 TL", "54 740 Td"]
        for line in lines:
            safe = line.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
            stream_lines.append(f"({safe}) Tj")
            stream_lines.append("T*")
        stream_lines.append("ET")
        stream = "\n".join(stream_lines).encode("latin-1")
        content = first_page + 2 * index + 1
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources "
            f"<< /Font << /F1 3 0 R >> >> /Contents {content} 0 R >>".encode()
        )
        objects.append(
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream
            + b"\nendstream"
        )
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    start = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{start}\n".encode()
        + b"%%EOF\n"
    )
    return bytes(out)


def sentence_in(sentence: str, revision: bool) -> str:
    """The sentence as this draft prints it, rewritten or as it was."""
    return REWRITTEN.get(sentence, sentence) if revision else sentence


def manuscript(revision: bool) -> bytes:
    """The fixture manuscript as a PDF, in its first or its revised form."""
    pages = []
    heading_block = [TITLE + (" (revised)" if revision else ""), ""]
    for heading, sentences in PAGES:
        lines = list(heading_block) + [heading, ""]
        heading_block = []
        for sentence in sentences:
            lines += textwrap.wrap(sentence_in(sentence, revision), width=78)
            lines.append("")
        pages.append(lines)
    return pdf_bytes(pages)


def whole_paper(server, token: str, slot: str) -> str:
    """Every part of the manuscript, read as a reviewer reads it.

    A slot that has not been served the whole paper has its findings refused, and
    the paper is served in parts, so the part count is read off the first part's
    own heading, which is `paper.md - part 1 of N - lines a-b`. Reading costs
    nothing from the allowance, so there is nothing to spend by reading it all.
    """
    first = server.read_paper(token)
    refused(first, f"read_paper {slot}")
    if not isinstance(first, str):
        raise SystemExit(f"read_paper {slot} answered {type(first).__name__}, not the paper")
    found = re.search(r"part 1 of (\d+)", first.splitlines()[0])
    if not found:
        raise SystemExit(f"read_paper {slot} did not say which part it served: "
                         f"{first.splitlines()[0][:120]}")
    served = [first]
    for part in range(2, int(found.group(1)) + 1):
        more = server.read_paper(token, part=part)
        refused(more, f"read_paper {slot} part {part}")
        served.append(more)
    return "\n".join(served)


def quoted_once(paper: str, sentence: str) -> None:
    """Fail now if the sentence is not one passage of the paper the slot was served.

    The engine quarantines a quote it cannot place, or places twice, and finds
    the line itself. The fixture does not name a line, so this is the only check
    worth making here: a manuscript that drifts fails with the sentence, rather
    than one call later as a quarantine.
    """
    if paper.count(sentence) != 1:
        raise SystemExit(
            f"the sentence reads in {paper.count(sentence)} passage(s) of the paper and has to "
            f"read in one: {sentence[:70]}"
        )


def refused(answer: dict, what: str) -> None:
    """Stop on the engine's own refusal, with the refusal in the message.

    A refused call answers `request_rejected` rather than raising, because the
    caller it was written for is an agent that keeps its turn. This script is
    not one: a refusal here means the fixture asked for something the engine
    does not do, and the message is the thing worth reading.
    """
    if isinstance(answer, dict) and answer.get("request_rejected"):
        raise SystemExit(f"{what} was refused: {json.dumps(answer, indent=2)[:2000]}")


def issue_batch(plan: dict, uids: dict) -> list:
    """The issues this round's editor submits, with its findings named by uid.

    The plan names a member by the finding's title, because a uid is minted by
    the engine and cannot be written down in advance, so the uids the slots were
    given back are read in here.
    """
    return [
        {
            "name": issue["name"],
            "severity": issue["severity"],
            "category": issue["category"],
            "rank": issue["rank"],
            "statement": issue["statement"],
            "members": [uids[title] for title in issue["members"]],
        }
        for issue in plan["issues"]
    ]


def one_round(out: Path, run_dir: Path, plan: dict) -> dict:
    """Drive one whole round in this process and return what it wrote.

    Called as a subprocess by :func:`main`, once per round, because a server
    process serves one paper.
    """
    import peerreviewagents as engine
    from peerreviewagents.plugin import server

    revision = plan["revision"]
    pdf = out / ("revision.pdf" if revision else "manuscript.pdf")
    pdf.write_bytes(manuscript(revision))

    # Every PDF review reads the pages, and there is no setting that turns the
    # stage off: the import holds the paper in a draft until the reader slot has
    # looked at the page images and sealed it, and no other slot may claim
    # before the seal. No model runs here, so the reader is this script, through
    # the engine's own `scripted_read`: it views every page of the fixture and
    # seals. What the panel below reads is therefore a manuscript the engine's
    # reader wrote, and the bundle says a reader sealed it.
    #
    # The handle is deliberately left open. Closing it puts back the run that
    # was attached before, and the slots below claim against the codes this
    # import minted, so the round goes on in the run the read opened.
    read = engine.scripted_read(pdf, run_dir, title=TITLE, reviewers=REVIEWERS,
                                arm=ARM)
    # The pages of this fixture are the ones it wrote the PDF from, and a seal
    # is refused while any page is unopened, because a piece the converter
    # dropped is only visible on its page.
    for page in range(1, len(PAGES) + 1):
        read.view_page(page)
    # No note. A note is the reader's own account of the document, and the
    # reader here is a script with nothing to report that the page images told
    # it.
    read.seal()
    opened = read.opened
    codes = {row["slot"]: row["claim_code"] for row in opened["claim_codes"]}

    uids: dict[str, str] = {}
    escalated: list[str] = []
    for slot, filings in plan["findings"].items():
        claim = server.claim_agent(slot, codes[slot])
        refused(claim, f"claim {slot}")
        token = claim["agent_token"]
        paper = whole_paper(server, token, slot)
        for filing in filings:
            quote = sentence_in(filing["sentence"], revision)
            quoted_once(paper, quote)
            stored = server.submit_finding(
                token, title=filing["title"], quote=quote,
                comment=filing["comment"], severity=filing["severity"],
                kind=filing["kind"], escalate=filing["escalate"],
            )
            refused(stored, f"submit_finding {filing['title'][:40]}")
            uids[filing["title"]] = stored["finding_uid"]
            if filing["escalate"]:
                escalated.append(stored["finding_uid"])
        closed = server.submit_report(
            token,
            summary=f"{slot} read the manuscript and filed {len(filings)} finding(s).",
            limitations=["No code was run and no data was obtained."],
        )
        refused(closed, f"submit_report {slot}")

    editor = server.claim_agent("editor", codes["editor"])
    refused(editor, "claim editor")
    token = editor["agent_token"]
    whole_paper(server, token, "editor")
    submitted = server.submit_issues(token, issues=issue_batch(plan, uids))
    refused(submitted, "submit_issues")
    closed = server.submit_editor(
        token, summary=plan["summary"], significance=plan["significance"],
        strength_of_evidence=plan["evidence"], verdict_reasoning=plan["reasoning"],
        limitations=list(plan["limitations"]),
        escalation_rulings=[
            {"finding_uid": uid,
             "ruling": "Upheld. The number is reported as though it had been measured "
                       "repeatedly and it was measured once, which is this review's first "
                       "item."}
            for uid in escalated
        ],
    )
    refused(closed, "submit_editor")
    report = server.submit_report(
        token,
        summary="The editor pooled the findings of this review into issues.",
        limitations=["The verdict is a judgement in words and not a score."],
    )
    refused(report, "submit_report editor")

    recorder = server.claim_agent("recorder", codes["recorder"])
    refused(recorder, "claim recorder")
    written = server.write_review(recorder["agent_token"])
    refused(written, "write_review")

    # Where the files are and what the folder reads as, from the engine's own
    # reader rather than from the paths this script would guess. `read_run` is
    # what the publish path reads a run with, so a fixture that reader refuses
    # fails here instead of in a check.
    reading = engine.read_run(str(run_dir))
    return {
        "run": str(run_dir),
        "issues_path": reading["reports"]["issues"],
        "status": reading["status"],
        "publishable": reading["publishable"],
        "reasons": reading["not_publishable_reasons"],
        "issues": closed["issues"],
        "required": closed["required_changes"],
        "suggestions": closed["suggestions"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="where to write the rounds")
    parser.add_argument("--round", type=int, choices=range(1, len(ROUNDS) + 1), default=None,
                        help="internal: drive this one round in this process")
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if args.round:
        wrote = one_round(out, out / f"round-{args.round}", ROUNDS[args.round - 1])
        print(json.dumps(wrote))
        return 0

    # One process per round, which is the engine's rule about a server and a
    # paper, so the rounds are subprocesses of this script rather than two
    # ingests in one interpreter.
    rounds = []
    for number in range(1, len(ROUNDS) + 1):
        done = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--out", str(out),
             "--round", str(number)],
            capture_output=True, text=True, check=False,
        )
        if done.returncode != 0:
            sys.stderr.write(done.stdout + done.stderr)
            return done.returncode
        rounds.append(json.loads(done.stdout.strip().splitlines()[-1]))
    for wrote in rounds:
        print(f"{wrote['run']}: {wrote['status']}, "
              f"{'publishable' if wrote['publishable'] else '; '.join(wrote['reasons'])}, "
              f"{wrote['issues']} issue(s), {wrote['required']} required, "
              f"{wrote['suggestions']} suggestion(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
