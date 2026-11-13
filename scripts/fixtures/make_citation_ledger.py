#!/usr/bin/env python3
"""Write the citation ledger fixture as hand written JSON lines.

The smoke suite needs a `citations/ledger.jsonl` that looks exactly like one a
run produces, because the record builder and the published page read it. The
engine documents that table as a consumer surface: `docs/INTEGRATIONS.md` gives
both row shapes, the stage file beside them and the one rule the file has, that
the last row written for a `row_id` is that row. So the rows below are written
out here, field for field, rather than driven out of the engine's own writer.

Nothing in this file imports the engine. The numbers it claims are not typed in
either: `counts` reads the table back through `read_citation_ledger`, the public
reader, so the tallies every check compares against are the engine's reading of
these rows and not this repository's idea of them.

The table carries one reference of each existence state it can hold:

* a reference whose printed DOI Crossref holds, with an abstract, which is the
  one reference a worker can judge a sentence against
* a reference whose printed DOI no agency holds and whose handle the DOI
  resolver does not know, which is the only state in the table that says a
  printed identifier does not exist
* a book that neither index lists, which is weak evidence about a reference and
  no evidence at all about the work
* a reference whose lookups never answered, which says nothing whatever

Four in-text uses come out of two prose blocks. Three are judged and one is left
unjudged on purpose, so the fixture carries an unfinished stage: an unfinished
ledger is reported beside the findings and never as a reason to withhold the
review, and a fixture where every stage finished could not test that.

The lookups cache is written too, because it is the one place in a run folder
that holds text fetched from a publisher, and a check publishes this run and
proves none of that text reached the bundle.

Every timestamp is pinned, so running this twice writes the same bytes and a
regenerated fixture is an empty diff rather than a timestamp diff.

Running it:

    python3 scripts/fixtures/make_citation_ledger.py --out /tmp/ledger

The engine is needed only to print the tallies at the end.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

# Where a run keeps the lane, from `docs/INTEGRATIONS.md`.
LEDGER_PATH = "citations/ledger.jsonl"
STATE_PATH = "citations/stages.json"
CACHE_PATH = "citations/lookups"

# The two sentinels the engine locks the table and the stage record on. They are
# opened and never written, so they are empty here as they are in a run. They
# are in the fixture because they are files a real lane leaves in `citations/`,
# and the check that publishes this run and proves the lane's folder never
# travels should be reading every file the folder holds and not only the ones
# this repository knows how to read.
LOCK_PATHS = ("citations/rows.lock", "citations/stages.lock")

# The one timestamp every row in the fixture carries. A run stamps each row as
# it writes it, and a fixture regenerated an hour later would differ in every
# line while saying the same thing.
FIXED_TIME = "2026-11-12T00:00:00+00:00"

# The worker slot that claimed and judged the uses. `fill` takes the slot it is
# given and writes it into the rows, so a caller that runs the lane under a
# different slot name gets a table that says so.
WORKER = "cite-1"

RESOLVED_DOI = "10.1234/jcb.2024.0001"
UNREGISTERED_DOI = "10.5555/nucleolar-phase-2023-0002"

# The abstract Crossref holds for the one resolved reference, as the ledger
# stores it: the markup of the fetched body stripped off.
ABSTRACT = (
    "We measured uniporter flux in isolated cardiac myocytes across a range of "
    "cytosolic calcium concentrations. Flux saturated above two micromolar in "
    "every preparation, and the saturating concentration did not shift with "
    "pacing rate."
)

# A phrase out of that abstract. It is here so a check can prove no published
# bundle carries it: the lookups cache is third party publisher text, the review
# rests on it only through the short passage quoted in a verdict, and
# republishing the rest would make this a mirror of it.
FETCHED_PHRASE = "Flux saturated above two micromolar"

# The passage the worker quoted when it judged the first use. It is a window cut
# out of the abstract above, which is what the engine requires of a passage: a
# verdict that quotes something the source does not say is refused.
PASSAGE = ABSTRACT[ABSTRACT.index(FETCHED_PHRASE):][:96]

# Every lookup URL the lane made, written out rather than rebuilt, because this
# is a record of what a run did and not a second copy of the engine's query
# builder.
_SELECT = (
    "&rows=3&select=DOI%2Ctitle%2Cauthor%2Cissued%2Cpublished%2Ccontainer-title"
    "%2Ctype%2Crelation%2Cupdated-by%2Cabstract%2Csubtitle"
)
CROSSREF_DOI_URL = "https://api.crossref.org/works/" + RESOLVED_DOI
EUROPEPMC_DOI_URL = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    "query=DOI%3A%2210.1234%2Fjcb.2024.0001%22&format=json&resultType=core&pageSize=1"
)
UNREGISTERED_WORK_URL = "https://api.crossref.org/works/" + UNREGISTERED_DOI
UNREGISTERED_AGENCY_URL = UNREGISTERED_WORK_URL + "/agency"
UNREGISTERED_HANDLE_URL = "https://doi.org/api/handles/" + UNREGISTERED_DOI
CROSSREF_NUCLEOLAR_URL = (
    "https://api.crossref.org/works?query.bibliographic="
    "A+phase+separation+model+of+nucleolar+assembly" + _SELECT
    + "&query.author=lindqvist"
    + "&filter=from-pub-date%3A2022-01-01%2Cuntil-pub-date%3A2024-12-31"
)
EUROPEPMC_NUCLEOLAR_URL = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    "query=A+phase+separation+model+of+nucleolar+assembly"
    "&format=json&resultType=core&pageSize=3"
)
CROSSREF_HANDBOOK_URL = (
    "https://api.crossref.org/works?query.bibliographic="
    "Handbook+of+quantitative+cell+physiology%2C+third+edition" + _SELECT
    + "&query.author=marchetti"
    + "&filter=from-pub-date%3A2018-01-01%2Cuntil-pub-date%3A2020-12-31"
)
EUROPEPMC_HANDBOOK_URL = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    "query=Handbook+of+quantitative+cell+physiology%2C+third+edition"
    "&format=json&resultType=core&pageSize=3"
)
CROSSREF_CRYOSTASIS_URL = (
    "https://api.crossref.org/works?query.bibliographic="
    "Cryostasis+artefacts+in+cryo-electron+tomography+of+mitochondria" + _SELECT
    + "&query.author=sorensen"
    + "&filter=from-pub-date%3A2021-01-01%2Cuntil-pub-date%3A2023-12-31"
)
EUROPEPMC_CRYOSTASIS_URL = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    "query=Cryostasis+artefacts+in+cryo-electron+tomography+of+mitochondria"
    "&format=json&resultType=core&pageSize=3"
)

# What came back, in the order it was asked for. The cryostasis pair is here
# three times because a reference whose lookups did not answer is owed another
# attempt, and the lane made all three before giving up on it.
REQUESTS = (
    (CROSSREF_DOI_URL, "ok"),
    (EUROPEPMC_DOI_URL, "ok"),
    (UNREGISTERED_WORK_URL, "not_found"),
    (UNREGISTERED_AGENCY_URL, "not_found"),
    (UNREGISTERED_HANDLE_URL, "not_found"),
    (CROSSREF_NUCLEOLAR_URL, "ok"),
    (EUROPEPMC_NUCLEOLAR_URL, "ok"),
    (CROSSREF_HANDBOOK_URL, "ok"),
    (EUROPEPMC_HANDBOOK_URL, "ok"),
    (CROSSREF_CRYOSTASIS_URL, "unavailable"),
    (EUROPEPMC_CRYOSTASIS_URL, "unavailable"),
    (CROSSREF_CRYOSTASIS_URL, "unavailable"),
    (EUROPEPMC_CRYOSTASIS_URL, "unavailable"),
    (CROSSREF_CRYOSTASIS_URL, "unavailable"),
    (EUROPEPMC_CRYOSTASIS_URL, "unavailable"),
)

# The body each answered lookup returned. A lookup that failed cached nothing,
# which is why the three not_found and the six unavailable URLs are absent here.
EMPTY_CROSSREF_SEARCH = {"status": "ok", "message": {"items": []}}
EMPTY_EUROPEPMC = {"resultList": {"result": []}}
CROSSREF_WORK = {
    "status": "ok",
    "message": {
        "DOI": RESOLVED_DOI,
        "title": ["Mitochondrial calcium uniporter kinetics in cardiac myocytes"],
        "author": [{"given": "Adaeze", "family": "Okafor"},
                   {"given": "Marc", "family": "Beaulieu"}],
        "issued": {"date-parts": [[2024, 3, 14]]},
        "container-title": ["Journal of Cell Biology"],
        "type": "journal-article",
        "abstract": (
            "<jats:p>We measured uniporter flux in isolated cardiac myocytes across a "
            "range of cytosolic calcium concentrations. Flux saturated above two "
            "micromolar in every preparation, and the saturating concentration did not "
            "shift with pacing rate.</jats:p>"
        ),
    },
}
BODIES = {
    CROSSREF_DOI_URL: CROSSREF_WORK,
    EUROPEPMC_DOI_URL: EMPTY_EUROPEPMC,
    CROSSREF_NUCLEOLAR_URL: EMPTY_CROSSREF_SEARCH,
    EUROPEPMC_NUCLEOLAR_URL: EMPTY_EUROPEPMC,
    CROSSREF_HANDBOOK_URL: EMPTY_CROSSREF_SEARCH,
    EUROPEPMC_HANDBOOK_URL: EMPTY_EUROPEPMC,
}

# Where every field in `printed` was read out of. The fixture's manuscript has a
# reference list and nothing else, so every field came from the reference entry.
_FROM_REFERENCE = {
    "doi": "reference",
    "first_author": "reference",
    "title": "reference",
    "venue": "reference",
    "year": "reference",
}
_NO_DOI = dict(_FROM_REFERENCE, doi=None)

# No field was compared for a reference that never resolved to a record, which
# is not the same as a field that was compared and disagreed.
_NOT_COMPARED = {"first_author": None, "title": None, "venue": None, "year": None}

REFERENCES = (
    {
        "kind": "reference",
        "row_id": "ref:ref-1",
        "reference_id": "ref-1",
        "label": "1",
        "stage": "resolve",
        "filled_at": FIXED_TIME,
        "raw": (
            "Okafor A, Beaulieu M. Mitochondrial calcium uniporter kinetics in cardiac "
            "myocytes. Journal of Cell Biology 2024. doi:" + RESOLVED_DOI
        ),
        "printed": {
            "doi": RESOLVED_DOI,
            "first_author": "okafor",
            "title": "Mitochondrial calcium uniporter kinetics in cardiac myocytes",
            "venue": "Journal of Cell Biology",
            "year": "2024",
            "year_suffix": None,
            "extracted": dict(_FROM_REFERENCE),
        },
        # Crossref holds the printed DOI and every compared field agrees, which
        # is what a reference in good order looks like in this table.
        "resolution": {
            "exists": "yes",
            "method": "doi",
            "attempts": 1,
            "checked_at": FIXED_TIME,
            "confident": True,
            "registered_with": "crossref",
            "printed_doi": RESOLVED_DOI,
            "printed_doi_registered": True,
            "printed_doi_source": "reference",
            "resolved_doi": RESOLVED_DOI,
            "record": {
                "doi": RESOLVED_DOI,
                "first_author": "okafor",
                "pmcid": None,
                "registered_with": "crossref",
                "title": "Mitochondrial calcium uniporter kinetics in cardiac myocytes",
                "type": "journal-article",
                "venue": "Journal of Cell Biology",
                "year": "2024",
            },
            "matches": {"first_author": True, "title": True, "venue": True, "year": True},
            "mismatched": [],
            "abstract": ABSTRACT,
            "abstract_url": CROSSREF_DOI_URL,
            "full_text": None,
            "full_text_url": None,
            "source_url": CROSSREF_DOI_URL,
            "candidate": None,
            "is_retraction_notice": False,
            "retracted": False,
            "retraction_notice": None,
            "note": None,
            "requests": [
                {"url": CROSSREF_DOI_URL, "status": "ok"},
                {"url": EUROPEPMC_DOI_URL, "status": "ok"},
            ],
        },
    },
    {
        "kind": "reference",
        "row_id": "ref:ref-2",
        "reference_id": "ref-2",
        "label": "2",
        "stage": "resolve",
        "filled_at": FIXED_TIME,
        "raw": (
            "Lindqvist H. A phase separation model of nucleolar assembly. Cell Reports "
            "2023. doi:" + UNREGISTERED_DOI
        ),
        "printed": {
            "doi": UNREGISTERED_DOI,
            "first_author": "lindqvist",
            "title": "A phase separation model of nucleolar assembly",
            "venue": "Cell Reports",
            "year": "2023",
            "year_suffix": None,
            "extracted": dict(_FROM_REFERENCE),
        },
        # The one state in the table that says a printed identifier does not
        # exist: no agency registered it and no index lists the title either.
        "resolution": {
            "exists": "no",
            "method": "doi-unregistered",
            "attempts": 1,
            "checked_at": FIXED_TIME,
            "registered_with": None,
            "printed_doi": UNREGISTERED_DOI,
            "printed_doi_registered": False,
            "printed_doi_source": "reference",
            "matches": dict(_NOT_COMPARED),
            "mismatched": [],
            "candidate": None,
            "retracted": None,
            "retraction_notice": None,
            "note": (
                "The DOI resolver has no handle for the DOI the reference list gives "
                "and no registration agency holds it, and no work with this title is "
                "indexed at Crossref or Europe PMC."
            ),
            "requests": [
                {"url": UNREGISTERED_WORK_URL, "status": "not_found"},
                {"url": UNREGISTERED_AGENCY_URL, "status": "not_found"},
                {"url": UNREGISTERED_HANDLE_URL, "status": "not_found"},
                {"url": CROSSREF_NUCLEOLAR_URL, "status": "ok"},
                {"url": EUROPEPMC_NUCLEOLAR_URL, "status": "ok"},
            ],
        },
    },
    {
        "kind": "reference",
        "row_id": "ref:ref-3",
        "reference_id": "ref-3",
        "label": "3",
        "stage": "resolve",
        "filled_at": FIXED_TIME,
        "raw": (
            "Marchetti L. Handbook of quantitative cell physiology, third edition. "
            "Universitat Press 2019."
        ),
        "printed": {
            "doi": None,
            "first_author": "marchetti",
            "title": "Handbook of quantitative cell physiology, third edition",
            "venue": "Universitat Press",
            "year": "2019",
            "year_suffix": None,
            "extracted": dict(_NO_DOI),
        },
        # Weak evidence about the reference and none at all about the work: both
        # indexes are journal indexes and this is a textbook.
        "resolution": {
            "exists": "not located",
            "method": "title-search",
            "attempts": 1,
            "checked_at": FIXED_TIME,
            "registered_with": None,
            "printed_doi": None,
            "printed_doi_registered": None,
            "printed_doi_source": None,
            "matches": dict(_NOT_COMPARED),
            "mismatched": [],
            "candidate": None,
            "retracted": None,
            "retraction_notice": None,
            "note": (
                "Neither Crossref nor Europe PMC lists a work with this title. Much of "
                "the literature is in neither index, so this is not evidence that the "
                "work does not exist."
            ),
            "requests": [
                {"url": CROSSREF_HANDBOOK_URL, "status": "ok"},
                {"url": EUROPEPMC_HANDBOOK_URL, "status": "ok"},
            ],
        },
    },
    {
        "kind": "reference",
        "row_id": "ref:ref-4",
        "reference_id": "ref-4",
        "label": "4",
        "stage": "resolve",
        "filled_at": FIXED_TIME,
        "raw": (
            "Sorensen K. Cryostasis artefacts in cryo-electron tomography of "
            "mitochondria. Ultramicroscopy 2022."
        ),
        "printed": {
            "doi": None,
            "first_author": "sorensen",
            "title": "Cryostasis artefacts in cryo-electron tomography of mitochondria",
            "venue": "Ultramicroscopy",
            "year": "2022",
            "year_suffix": None,
            "extracted": dict(_NO_DOI),
        },
        # Three attempts, no answer. This row says nothing whatever about the
        # reference, which is the state this fixture exists to carry.
        "resolution": {
            "exists": "could not check",
            "method": None,
            "attempts": 3,
            "checked_at": FIXED_TIME,
            "registered_with": None,
            "printed_doi": None,
            "printed_doi_registered": None,
            "printed_doi_source": None,
            "matches": dict(_NOT_COMPARED),
            "mismatched": [],
            "candidate": None,
            "retracted": None,
            "retraction_notice": None,
            "note": (
                "The lookups did not answer, so whether this reference exists could "
                "not be checked."
            ),
            "requests": [
                {"url": CROSSREF_CRYOSTASIS_URL, "status": "unavailable"},
                {"url": EUROPEPMC_CRYOSTASIS_URL, "status": "unavailable"},
            ],
        },
    },
)


def _use(
    row_id: str,
    block_id: str,
    section: str,
    sentence_index: int,
    marker: str,
    reference_id: str,
    sentence: str,
    slot: str,
    verdict: str | None = None,
    passage: str | None = None,
    source_kind: str | None = None,
    source_url: str | None = None,
) -> dict:
    """One in-text use, claimed by a worker slot and judged or left owed.

    A row with no verdict is the shape the lane leaves behind when a worker
    claimed a use and the stage ran out before it answered.
    """
    row = {
        "kind": "use",
        "row_id": row_id,
        "reference_id": reference_id,
        "block_id": block_id,
        "section": section,
        "sentence_index": sentence_index,
        "sentence": sentence,
        "marker": marker,
        "derivation": "marker-numeric",
        "stage": "fill",
        "filled_at": FIXED_TIME,
        "claimed_at": FIXED_TIME,
        "claimed_by": slot,
    }
    if verdict is None:
        return row
    row.update({
        "stage": "judge",
        "verdict": verdict,
        "judged_at": FIXED_TIME,
        "judged_by": slot,
        "passage": passage,
        "note": None,
        # A verdict given with no source text in front of the worker names no
        # source, and null is that: the string "none" would read as a kind.
        "source_kind": source_kind,
        "source_url": source_url,
    })
    return row


def uses(slot: str = WORKER) -> tuple[dict, ...]:
    """The four in-text uses, three judged and the fourth left unjudged."""
    return (
        _use(
            "use:block-results-1:1:ref-1", "block-results-1", "Results", 1, "[1]", "ref-1",
            "Calcium entry through the uniporter saturates above two micromolar in "
            "isolated myocytes [1].",
            slot,
            verdict="supports", passage=PASSAGE,
            source_kind="abstract", source_url=CROSSREF_DOI_URL,
        ),
        _use(
            "use:block-results-1:2:ref-2", "block-results-1", "Results", 2, "[2]", "ref-2",
            "The nucleolus has been modelled as a phase separated compartment [2].",
            slot,
            # No source text was fetched for this reference, so cannot tell is
            # the only answer the engine allows here.
            verdict="cannot tell",
        ),
        _use(
            "use:block-methods-1:1:ref-3", "block-methods-1", "Methods", 1, "[3]", "ref-3",
            "Physiological constants were taken from the standard handbook [3].",
            slot,
            verdict="cannot tell",
        ),
        # The fourth use is claimed and unjudged: one stage short of done.
        _use(
            "use:block-methods-1:2:ref-4", "block-methods-1", "Methods", 2, "[4]", "ref-4",
            "Tomography of mitochondria is prone to freezing artefacts [4].",
            slot,
        ),
    )


def stages(slot: str = WORKER) -> dict:
    """The stage record beside the rows, as `docs/INTEGRATIONS.md` describes it.

    Fill and resolve are done. Judge is not, because one use is still owed, and
    that is what makes this fixture an unfinished lane rather than a finished
    one with nothing to report.
    """
    return {
        "fill": {
            "done": True, "at": FIXED_TIME,
            "added": len(REFERENCES) + len(uses(slot)),
            "references": len(REFERENCES), "uses": len(uses(slot)),
        },
        "resolve": {
            "done": True, "at": FIXED_TIME,
            "references": len(REFERENCES), "resolved": 1, "remaining": 0,
            "lookups": len(REQUESTS),
        },
        "judge": {
            "done": False, "at": FIXED_TIME,
            "uses": len(uses(slot)), "verdicts": 3, "workers": [slot],
        },
    }


def _digest(url: str) -> str:
    """The cache key for a lookup, which is the digest of the URL asked for."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _write_cache(review: Path) -> None:
    """The lookups cache: one body per answered lookup, and the receipts.

    This is written because it is the one place in a run folder that holds text
    fetched from a publisher. A check publishes this run and proves that none of
    it travelled, and a fixture without a cache would let that check pass on a
    run that had nothing to leak.
    """
    cache = review / CACHE_PATH
    cache.mkdir(parents=True, exist_ok=True)
    for url, payload in BODIES.items():
        raw = json.dumps(payload).encode("utf-8")
        key = _digest(url)
        (cache / f"{key}.raw").write_bytes(raw)
        (cache / f"{key}.json").write_text(
            json.dumps({
                "status": "ok",
                "source_url": url,
                "retrieved_at": FIXED_TIME,
                "raw_sha256": hashlib.sha256(raw).hexdigest(),
            }, indent=2) + "\n",
            encoding="utf-8",
        )
    (cache / "requests.json").write_text(
        json.dumps({
            "limit": 600,
            "requests": [
                {"source_url": url, "status": status, "at": FIXED_TIME}
                for url, status in REQUESTS
            ],
        }, indent=2) + "\n",
        encoding="utf-8",
    )


def fill(review: Path, slot: str = WORKER) -> tuple[dict, ...]:
    """Write one fixture ledger inside a review directory, and hand back the rows.

    Everything lands where a run puts it: `citations/ledger.jsonl`,
    `citations/stages.json`, the lookups cache beside them and the two empty
    lock sentinels the engine holds the table and the stage record on. A caller
    that wants a run folder with a citation lane in it points this at the
    folder, and a caller that wants the two files on their own goes through
    `build`.

    The rows go in the order a run wrote them, references before uses, because
    the file is append only and reading it back has to be reading a table a run
    could have left.

    Nothing is counted here. `read_citation_ledger` reads a run folder, and a
    folder with only a ledger in it is not one yet: a caller writes the run's own
    files and then asks `counts`.
    """
    review = Path(review)
    (review / CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)
    rows = tuple(REFERENCES) + uses(slot)
    (review / LEDGER_PATH).write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )
    (review / STATE_PATH).write_text(
        json.dumps(stages(slot), indent=2) + "\n", encoding="utf-8"
    )
    for lock in LOCK_PATHS:
        (review / lock).touch()
    _write_cache(review)
    return rows


def counts(review: Path) -> dict:
    """The tallies the engine reads off the ledger written under this run folder.

    Through `read_citation_ledger`, the public reader, rather than off the rows
    above: a fixture that counted itself would agree with itself no matter what
    the engine does with these rows, and agreeing with the engine is the whole
    point of the fixture.
    """
    return reading(review)["counts"]


def reading(review: Path) -> dict:
    """The public reader's whole reading of this run's citation ledger."""
    from peerreviewagents import read_citation_ledger

    return read_citation_ledger(Path(review))


def build(out: Path, slot: str = WORKER) -> dict:
    """Write one fixture ledger in a scratch run, and copy the two files out.

    The scratch folder gets a `progress.json` as well as the lane, because the
    public reader reads a run folder and a folder with nothing but a ledger in
    it is a directory. The copied files are the lane alone.
    """
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="citation-ledger-fixture-") as workspace:
        review = Path(workspace) / "review"
        review.mkdir()
        fill(review, slot)
        (review / "progress.json").write_text("{}\n", encoding="utf-8")
        whole = reading(review)
        shutil.copyfile(review / LEDGER_PATH, out / "citation-ledger.jsonl")
        shutil.copyfile(review / STATE_PATH, out / "citation-stages.json")
    return whole


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True,
                        help="Directory the two fixture files are written to")
    args = parser.parse_args(argv)
    whole = build(Path(args.out).resolve())
    totals = whole["counts"]
    for key in ("references", "resolved", "not_found", "not_located", "could_not_check",
                "uses", "uses_judged", "uses_unjudged", "supported", "cannot_tell",
                "with_source_text", "lookups", "complete", "stages_done"):
        print(f"{key:18} {totals[key]}")
    print("summary  " + whole["summary"])
    for line in whole["problems"]:
        print("problem  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
