#!/usr/bin/env python3
"""Build one run folder whose review read the code behind the paper, not just the paper.

The other fixture generators here produce a review of a manuscript alone. This
one produces the review this release added a lane for: a run given the code the
paper was computed with, a specialist that reads that code against the methods
section, and a finding whose evidence is a passage of a file the server checked
against its own snapshot rather than a passage the agent said was there.

There is no model and no network in it. The paper is a PDF written here out of
the sentences below. The code is a folder written here too, committed as a real
git checkout so that the commit, the branch and the clean state the run records
are read off git rather than invented, and holding three files a snapshot has no
business copying so that what the snapshot left out is a number the publish path
has something to say about. The reader, the reviewers, the editor and the
recorder are all this script, driving the engine's own plugin in the order a
session calls it.

What the publish path gets out of this that it cannot get anywhere else:

* a run whose `code` block says code was reviewed, at a commit, with counts of
  what was held and what a reviewer opened;
* one finding carrying `code_evidence`, which the engine stored only because the
  quoted lines are the lines the snapshot holds;
* a data file fetched whole and a second one too large to be served whole, so
  the counts the page states about data are counts of something that happened;
* a code check that answered three findings three different ways, one of them
  contradicted, which is the finding the publish path has to keep out of every
  issue and still account for;
* a snapshot folder inside the run, whose absolute path the record must never
  publish.

Running it:

    python3 scripts/fixtures/make_code_round.py --out /tmp/code-round

writes `run/` under `--out` with the manuscript and the code folder beside it,
and prints one JSON line naming them. The interpreter has to be one the engine
is installed in.

Nothing here is pinned. A run folder carries the time it ran, the digests of its
own files and a commit this script makes, so two runs of it differ in those
fields: it is a fixture builder for a check that reads the folder, not a golden
file to diff.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from make_engine_rounds import pdf_bytes, quoted_once, refused, whole_paper  # noqa: E402

# The arm that plans specialists, which is the only kind of arm the code lane is
# planned in, with one core reviewer and one specialist track beside the code
# one so the run is the smallest one that has a code lane at all.
ARM = "full-two-track"
# The slot this engine plans on a run with code beside the paper. It reads the
# code behind every finding that rests on how something was computed and files
# no finding of its own.
CHECK_SLOT = "code-check"
REVIEWERS = 1
TRACKS = ["stats"]
TITLE = "Features Accepted At One Percent: A Fixture Manuscript"
BRANCH = "trunk"

# The manuscript, sentence by sentence, because the review quotes it and the
# engine places the quote itself. The methods sentence is the one the code
# contradicts: the paper says one percent and the code says five.
ABSTRACT = (
    "Every count reported in this paper is a count of features that passed the "
    "acceptance threshold the pipeline applies.",
    "The threshold is stated once, in the methods section, and the counts are "
    "reported under it throughout.",
)
METHODS = (
    "Features were accepted at a false discovery rate of one percent before any "
    "count reported here was taken.",
    "The pipeline that applied the threshold is the version archived with this "
    "submission and no parameter of it was changed between the runs.",
)
RESULTS = (
    "The retained feature count is given for each of the three instruments and "
    "no instrument was left out of the totals.",
)

PAGES = (("Abstract", ABSTRACT), ("Methods", METHODS), ("Results", RESULTS))

# The data behind the counts, which this engine lists rather than copies: a data
# file reaches a reviewer only when the reviewer asks for that one file. Two of
# them, because the fact the page has to state about data is how much of what
# was listed came back whole. The small table is served as it stands. The wide
# one is larger than the lane serves in one answer, so it comes back as a head
# of itself, and a finding about it may quote only the lines that were served.
SMALL_DATA = "measurements.csv"
WIDE_DATA = "instrument-counts.csv"
# Enough rows to put the file over the per-file cap the lane serves whole,
# which is what makes the fetch of it a partial one. The number is here rather
# than inline because the fact the fixture needs is the size and not the rows.
WIDE_DATA_ROWS = 9000


def wide_table() -> str:
    """A data file too large to be served whole, built rather than pasted."""
    rows = ["instrument,feature,fdr,retained"]
    for number in range(1, WIDE_DATA_ROWS + 1):
        rows.append(f"inst-{number % 3 + 1},feature-{number},0.0{number % 9 + 1},1")
    return "\n".join(rows) + "\n"


# The code behind the paper, as a folder a run can be given. Four files are text
# source and are copied into the snapshot. Two data tables are listed beside
# them and fetched only if asked for. Two files are neither: a binary note and a
# file whose name says it may hold a secret, which the snapshot leaves out by
# name before it looks at the contents.
THRESHOLD_LINE = "FDR_THRESHOLD = 0.05"
CODE_FILES = {
    "analysis/pipeline.py": (
        '"""The pipeline behind the paper."""\n'
        "\n"
        f"{THRESHOLD_LINE}\n"
        "MIN_FEATURES = 3\n"
        "\n"
        "\n"
        "def keep(rows):\n"
        '    """Every row at or under the accepted false discovery rate."""\n'
        "    return [row for row in rows if row['fdr'] <= FDR_THRESHOLD]\n"
    ),
    "analysis/plot.R": 'counts <- read.csv("counts.csv")\nplot(counts$retained)\n',
    "requirements.txt": "numpy==1.26.4\nscipy==1.13.0\n",
    "README.md": (
        "# The analysis\n"
        "\n"
        "Run `python -m analysis.pipeline` to reproduce every count in the paper.\n"
    ),
    SMALL_DATA: "feature,fdr\n1,0.004\n2,0.031\n",
    WIDE_DATA: wide_table(),
    "notes.dat": "not text source either\n",
    "prod.env": "TOKEN=not-a-real-token\n",
}

# What each slot files. The code lane's finding is the one with evidence in it:
# the quoted line is the line the snapshot holds, which is why the engine stores
# it as code-checked, and the quote is built from the fixture above rather than
# typed twice.
CORE_FINDING = {
    "title": "The threshold the counts rest on is stated once",
    "sentence": ABSTRACT[1],
    "severity": "minor",
    "comment": "A number every count in the paper depends on is worth stating "
               "where the counts are reported as well as in the methods.",
}
STATS_FINDING = {
    "title": "No spread is given for the per instrument counts",
    "sentence": RESULTS[0],
    "severity": "moderate",
    "comment": "Three counts with no spread around them cannot be compared. "
               "Report the counts with their uncertainty, or say that each is a "
               "single measurement.",
    # The step this finding takes for granted, which is what sends it to the
    # code check: a reviewer saying the paper reports no spread is reading the
    # paper, and a reviewer saying the pipeline computes none is reading code it
    # has not opened.
    "assumed_method": "The pipeline computes no spread around the per "
                      "instrument counts anywhere in it.",
}
CODE_FINDING = {
    "title": "The code accepts five percent where the paper says one",
    "sentence": METHODS[0],
    "severity": "major",
    "comment": "The methods section says features were accepted at a false "
               "discovery rate of one percent. The archived pipeline accepts "
               "them at five, and every count in the paper was taken through "
               "that filter. Either the threshold in the paper is wrong or the "
               "counts were taken with the wrong one.",
    "code_path": "analysis/pipeline.py",
    "code_quote": THRESHOLD_LINE,
    "assumed_method": "The threshold the pipeline applies is the one the "
                      "counts in the paper were taken under.",
}
# The finding the code throws out. It is filed like any other, by a reviewer
# reading the manuscript, and the step it assumes is one the pipeline does not
# take: nothing in the code drops an instrument. A fixture needs it because a
# contradicted finding is the one case the publish path has to get right
# without the engine's help, being in no issue and so in nothing the letter
# prints as an ask.
DROPPED_FINDING = {
    "title": "The totals leave out the instrument with the fewest features",
    "sentence": RESULTS[0],
    "severity": "moderate",
    "comment": "If the lowest instrument is dropped before the totals are "
               "taken, the totals are of two instruments and the paper reports "
               "them as three. Say which instruments each total covers.",
    "assumed_method": "The pipeline drops the instrument with the fewest "
                      "retained features before the totals are taken.",
}

ISSUES = (
    {
        "name": "The reported threshold is not the threshold the code applied",
        "severity": "major",
        "category": "reproducibility",
        "rank": 1,
        "statement": "The paper reports a false discovery rate of one percent and "
                     "the archived pipeline applies five. Say which threshold the "
                     "reported counts were taken at, and report the counts at it.",
        "members": (CODE_FINDING["title"],),
    },
    {
        "name": "The per instrument counts carry no spread",
        "severity": "moderate",
        "category": "results-and-numbers",
        "rank": 2,
        "statement": "The three instrument counts are given as single numbers. "
                     "Report the spread around each, or say that each is one "
                     "measurement.",
        "members": (STATS_FINDING["title"],),
    },
    {
        "name": "The threshold is stated in one place only",
        "severity": "minor",
        "category": "presentation",
        "rank": 3,
        "statement": "State the acceptance threshold where the counts are "
                     "reported as well as in the methods section.",
        "members": (CORE_FINDING["title"],),
    },
)


# What the code check answers, one row per finding it is handed. The three
# verdicts are all exercised on purpose: a confirmed finding stays in the
# letter with the code printed beside it, a contradicted one is thrown out of
# every issue and published only as a thrown-out finding, and a not-shown one
# stands on its reviewer's reading of the manuscript with the searches printed
# so the code's silence is not read as a verdict. `code_lines` is a line range
# of the fixture file above, so the quote is the snapshot's own text rather than
# text typed twice, which is the only kind of quote the engine stores.
CHECKS = (
    {
        "finding": CODE_FINDING,
        "verdict": "confirmed",
        "code_path": "analysis/pipeline.py",
        "code_lines": (THRESHOLD_LINE, THRESHOLD_LINE),
        "note": "The pipeline sets the accepted false discovery rate to five "
                "percent at the line quoted here, and every count in the paper "
                "was taken through that filter.",
    },
    {
        "finding": DROPPED_FINDING,
        "verdict": "contradicted",
        "code_path": "analysis/pipeline.py",
        "code_lines": ("def keep(rows):", "return [row for row"),
        "note": "The only filter the pipeline applies is on the false "
                "discovery rate of a row. Nothing in it drops an instrument, "
                "ranks the instruments or counts features per instrument, so "
                "the totals are not of two instruments out of three.",
    },
    {
        "finding": STATS_FINDING,
        "verdict": "not-shown",
        "searches": ("std", "stderr", "confidence", "analysis/pipeline.py"),
        "note": "Nothing in the copy computes a spread, and the copy holds four "
                "source files out of a repository that may hold more. The "
                "finding stands on the paper reporting none, which is what its "
                "reviewer read.",
    },
)

SUMMARY = ("The question is worth asking and the paper is clearly written. What this "
           "review turns on is that the threshold the paper reports is not the "
           "threshold the archived code applies, so every count in the paper was "
           "taken through a filter the methods section does not describe.")
SIGNIFICANCE = ("If the counts hold at the threshold the paper reports, the result "
                "stands as written. Nothing here yet shows that they do.")
EVIDENCE = ("One threshold in the methods section, another in the code that produced "
            "the counts, and no spread around the counts themselves.")
REASONING = ("The first item is answerable with what the authors already have: run the "
             "pipeline at the threshold the paper reports, or report the threshold it "
             "was run at.")
LIMITATIONS = ("The code was read and never run, so nothing in this review is a "
               "replication of the authors' counts.",)


def manuscript() -> bytes:
    """The fixture manuscript as a PDF, built out of the sentences above."""
    pages = []
    heading_block = [TITLE, ""]
    for heading, sentences in PAGES:
        lines = list(heading_block) + [heading, ""]
        heading_block = []
        for sentence in sentences:
            lines += textwrap.wrap(sentence, width=78)
            lines.append("")
        pages.append(lines)
    return pdf_bytes(pages)


def git(folder: Path, *arguments: str) -> None:
    done = subprocess.run(["git", "-C", str(folder), *arguments], capture_output=True,
                          text=True, check=False)
    if done.returncode != 0:
        raise SystemExit(f"git {' '.join(arguments)} failed: {done.stdout}{done.stderr}")


def code_checkout(folder: Path) -> Path:
    """The fixture code on disk, as one commit on a branch.

    A checkout rather than a plain folder, because the commit and the branch are
    what the published record names as the code that was reviewed, and a fixture
    that typed them in would be publishing a commit nothing made. The author is
    fixed here so the commit does not depend on whoever runs this.
    """
    for name, text in CODE_FILES.items():
        path = folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    git(folder, "init", "--quiet", "-b", BRANCH)
    git(folder, "add", "-A")
    git(folder, "-c", "user.email=fixture@example.invalid", "-c", "user.name=Fixture",
        "commit", "--quiet", "-m", "the analysis behind the fixture paper")
    return folder


def line_of(path: str, needle: str) -> int:
    """The line *needle* is on in the fixture file at *path*.

    The evidence a code finding carries is a line range, and a number typed here
    would pass or fail on how the fixture above is laid out rather than on what
    the server checked against its snapshot.
    """
    for number, line in enumerate(CODE_FILES[path].splitlines(), start=1):
        if needle in line:
            return number
    raise SystemExit(f"{needle} is not in the fixture {path}")


def code_slice(path: str, first: str, last: str) -> tuple[int, int, str]:
    """The lines of the fixture file at *path* from *first* through *last*.

    A verdict carries the passage of the snapshot that decides it, quoted
    exactly as the snapshot holds it, and the engine stores the verdict only if
    the text is what stands at those lines. So the range is found by its own
    content and the text is cut out of the fixture, which is the same file the
    snapshot was taken from.
    """
    start, end = line_of(path, first), line_of(path, last)
    rows = CODE_FILES[path].splitlines()[start - 1:end]
    return start, end, "\n".join(rows)


def file_a_finding(server, token: str, slot: str, paper: str, filing: dict) -> str:
    """One finding, with its code evidence where the filing carries some."""
    quoted_once(paper, filing["sentence"])
    extra = {}
    if filing.get("code_path"):
        line = line_of(filing["code_path"], filing["code_quote"])
        extra = {"code_path": filing["code_path"], "code_start_line": line,
                 "code_end_line": line, "code_quote": filing["code_quote"]}
    if filing.get("assumed_method"):
        extra["assumed_method"] = filing["assumed_method"]
    stored = server.submit_finding(
        token, title=filing["title"], quote=filing["sentence"],
        comment=filing["comment"], severity=filing["severity"], kind="question",
        **extra,
    )
    refused(stored, f"submit_finding {slot} {filing['title'][:40]}")
    return stored["finding_uid"]


def one_run(out: Path, run_dir: Path) -> dict:
    """Drive the whole run in this process and return what it wrote."""
    import peerreviewagents as engine
    from peerreviewagents.plugin import server

    pdf = out / "manuscript.pdf"
    pdf.write_bytes(manuscript())
    code = code_checkout(out / "analysis-code")

    # The run is opened with the code beside the paper. The engine takes its own
    # snapshot of the folder into the run, and nothing in the folder is ever
    # executed or imported: the lane reads it as text.
    read = engine.scripted_read(pdf, run_dir, title=TITLE, reviewers=REVIEWERS,
                                arm=ARM, tracks=list(TRACKS), code=str(code))
    for page in range(1, len(PAGES) + 1):
        read.view_page(page)
    read.seal()
    codes = {row["slot"]: row["claim_code"] for row in read.opened["claim_codes"]}
    planned = sorted(codes)
    for slot in ("core-1", "spec-stats", "spec-code", CHECK_SLOT, "editor", "recorder"):
        if slot not in codes:
            raise SystemExit(f"the run planned {planned}, which has no {slot} to claim")

    uids: dict[str, str] = {}
    for slot, filings in (("core-1", (CORE_FINDING, DROPPED_FINDING)),
                          ("spec-stats", (STATS_FINDING,)),
                          ("spec-code", (CODE_FINDING,))):
        claim = server.claim_agent(slot, codes[slot])
        refused(claim, f"claim {slot}")
        token = claim["agent_token"]
        paper = whole_paper(server, token, slot)
        if slot == "spec-code":
            # What the lane does before it concludes anything: find the number
            # the methods section names, then read the file around the hit. Both
            # are recorded with the review as what this reviewer opened.
            found = server.search_code(token, query="FDR_THRESHOLD")
            refused(found, "search_code")
            served = server.read_code(token, path=CODE_FINDING["code_path"])
            refused(served, "read_code")
            # The data the counts were taken from, which the snapshot lists and
            # does not copy. Reading one is what fetches it: the small table
            # comes back whole and the wide one comes back as a head of itself,
            # which is the pair of facts the published page has to state.
            for name in (SMALL_DATA, WIDE_DATA):
                fetched = server.read_code(token, path=name)
                refused(fetched, f"read_code {name}")
                if name == WIDE_DATA and not fetched.get("partial"):
                    raise SystemExit(
                        f"{name} is meant to be larger than the lane serves "
                        f"whole, and it came back entire: {sorted(fetched)}"
                    )
        for filing in filings:
            uids[filing["title"]] = file_a_finding(server, token, slot, paper, filing)
        closed = server.submit_report(
            token,
            summary=f"{slot} read the manuscript and filed {len(filings)} finding(s).",
            limitations=["No code was run."],
        )
        refused(closed, f"submit_report {slot}")

    # The code check, which runs before the editor because its verdicts decide
    # what the editor may group: a finding the code contradicts is out of the
    # issues, and the engine refuses an editor that puts one in.
    checker = server.claim_agent(CHECK_SLOT, codes[CHECK_SLOT])
    refused(checker, f"claim {CHECK_SLOT}")
    token = checker["agent_token"]
    queue = server.method_claims(token)
    refused(queue, "method_claims")
    queued = {str(row["finding_uid"]) for row in queue["claims"]}
    for check in CHECKS:
        title = check["finding"]["title"]
        uid = uids[title]
        if uid not in queued:
            raise SystemExit(
                f"{title!r} was meant to reach the code check and the queue "
                f"holds {len(queued)} other finding(s): {queue['claims']}"
            )
        if check["verdict"] == "not-shown":
            extra = {"searches": list(check["searches"])}
        else:
            start, end, text = code_slice(check["code_path"], *check["code_lines"])
            extra = {"code_path": check["code_path"], "code_start_line": start,
                     "code_end_line": end, "code_quote": text}
        answered = server.submit_code_check(
            token, finding_uid=uid, verdict=check["verdict"], note=check["note"], **extra,
        )
        refused(answered, f"submit_code_check {check['verdict']}")
    closed = server.submit_report(
        token,
        summary=f"{CHECK_SLOT} read the code behind three findings and answered each one.",
        limitations=["The code was read and never run."],
    )
    refused(closed, f"submit_report {CHECK_SLOT}")

    editor = server.claim_agent("editor", codes["editor"])
    refused(editor, "claim editor")
    token = editor["agent_token"]
    whole_paper(server, token, "editor")
    batch = [
        {
            "name": issue["name"],
            "severity": issue["severity"],
            "category": issue["category"],
            "rank": issue["rank"],
            "statement": issue["statement"],
            "members": [uids[title] for title in issue["members"]],
        }
        for issue in ISSUES
    ]
    submitted = server.submit_issues(token, issues=batch)
    refused(submitted, "submit_issues")
    closed = server.submit_editor(
        token, summary=SUMMARY, significance=SIGNIFICANCE,
        strength_of_evidence=EVIDENCE, verdict_reasoning=REASONING,
        limitations=list(LIMITATIONS),
    )
    refused(closed, "submit_editor")
    report = server.submit_report(
        token,
        summary="The editor pooled the findings into issues, the first of them the "
                "one the code lane checked against the archived pipeline.",
        limitations=["The verdict is a judgement in words and not a score."],
    )
    refused(report, "submit_report editor")

    recorder = server.claim_agent("recorder", codes["recorder"])
    refused(recorder, "claim recorder")
    written = server.write_review(recorder["agent_token"])
    refused(written, "write_review")

    # What the folder reads as, from the engine's own reader rather than from the
    # paths this script would guess. `read_run` is what the publish path reads a
    # run with, so a fixture that reader refuses fails here instead of in a check.
    reading = engine.read_run(str(run_dir))
    block = reading.get("code") or {}
    if not block.get("reviewed"):
        raise SystemExit(f"the run does not say it reviewed any code: {block}")
    return {
        "run": str(run_dir),
        "pdf": str(pdf),
        "code": str(code),
        "slots": planned,
        "status": reading["status"],
        "publishable": reading["publishable"],
        "reasons": reading["not_publishable_reasons"],
        "issues": closed["issues"],
        "required": closed["required_changes"],
        "suggestions": closed["suggestions"],
        "code_commit": block.get("commit", ""),
        "code_branch": block.get("branch", ""),
        "code_files": block.get("files_in_snapshot", 0),
        "code_skipped": block.get("files_skipped", 0),
        "code_opened": sorted(block.get("files_opened") or []),
        "code_evidence_finding": CODE_FINDING["title"],
        # What the data side of the lane did, which the engine counts and the
        # published page states: how much was listed, how much of it was
        # fetched, and how much of that came back as a head of the file only.
        "data_listed": block.get("data_listed", 0),
        "data_fetched": block.get("data_fetched", 0),
        "data_partial": block.get("data_partial", 0),
        "data_refused": block.get("data_refused", 0),
        # The findings the code check answered, by verdict, so a check reading
        # this run knows which uid is meant to be thrown out of the issues and
        # which is meant to survive them.
        "checked": {
            check["verdict"]: {
                "title": check["finding"]["title"],
                "finding_uid": uids[check["finding"]["title"]],
            }
            for check in CHECKS
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="where to write the run")
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    wrote = one_run(out, out / "run")
    print(json.dumps(wrote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
