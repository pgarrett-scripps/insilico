#!/usr/bin/env python3
"""Write the citation ledger fixture with the engine's own ledger writer.

The smoke suite needs a `citations/ledger.jsonl` that looks exactly like one a
run produces, because the record builder and the published page read it and a
hand typed table would only ever agree with what this repository believed the
engine writes. So the fixture is generated: this script fills, resolves and
judges a tiny synthetic manuscript through
`peerreviewagents.engine.citation_ledger` itself, and the rows it commits are
the engine's rows, field for field, at the release the fixture was cut from.

Nothing here reaches the network. Every lookup goes through an opener handed to
the engine's own fetcher, which answers four canned bodies and two failures, so
the four existence states the table can hold are all produced by the resolver
rather than written down:

* a reference whose printed DOI Crossref holds, with an abstract, which is the
  one reference a worker can judge a sentence against
* a reference whose printed DOI no agency holds and whose handle the DOI
  resolver does not know, which is the only state in the table that says a
  printed identifier does not exist
* a book that neither index lists, which is weak evidence about a reference and
  no evidence at all about the work
* a reference whose lookups never answered, which says nothing whatever

Four in-text uses come out of the two prose blocks. Three are judged and one is
left unjudged on purpose, so the fixture carries an unfinished stage: an
unfinished ledger is reported beside the findings and never as a reason to
withhold the review, and a fixture where every stage finished could not test
that.

The clock is pinned, so running this twice writes the same bytes and a
regenerated fixture is an empty diff rather than a timestamp diff.

Running it:

    PYTHONPATH=/path/to/peerreviewagents python3 scripts/fixtures/make_citation_ledger.py \
        --out /tmp/ledger

The engine has to be importable, and this is the one file in the repository
that imports a module inside `peerreviewagents.engine`: 0.9.0 publishes no
reader or writer for the ledger, and `read_run` hands a consumer the counts
without handing it the rows. `scripts/smoke_checks/local.py` names this file
and that module in the one allowance its import check holds, and the allowance
goes away the day the engine exports a ledger writer.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
from pathlib import Path

from peerreviewagents.engine import citation_ledger

# The one timestamp every row in the fixture carries. The engine stamps each
# row as it writes it, and a fixture regenerated an hour later would differ in
# every line while saying the same thing.
FIXED_TIME = "2026-11-12T00:00:00+00:00"

RESOLVED_DOI = "10.1234/jcb.2024.0001"
UNREGISTERED_DOI = "10.5555/nucleolar-phase-2023-0002"

# The paper. A plain dict with a reference list and two prose blocks is all the
# ledger's fill stage reads, so the fixture needs no PDF and no ingest.
PAPER = {
    "id": "fixture-citations",
    "title": "A manuscript with findings at every severity",
    "references": [
        {
            "id": "ref-1",
            "label": "1",
            "title": "Mitochondrial calcium uniporter kinetics in cardiac myocytes",
            "first_author": "Okafor",
            "year": "2024",
            "venue": "Journal of Cell Biology",
            "doi": RESOLVED_DOI,
            "raw": (
                "Okafor A, Beaulieu M. Mitochondrial calcium uniporter kinetics in cardiac "
                "myocytes. Journal of Cell Biology 2024. doi:" + RESOLVED_DOI
            ),
        },
        {
            "id": "ref-2",
            "label": "2",
            "title": "A phase separation model of nucleolar assembly",
            "first_author": "Lindqvist",
            "year": "2023",
            "venue": "Cell Reports",
            "doi": UNREGISTERED_DOI,
            "raw": (
                "Lindqvist H. A phase separation model of nucleolar assembly. Cell Reports "
                "2023. doi:" + UNREGISTERED_DOI
            ),
        },
        {
            "id": "ref-3",
            "label": "3",
            "title": "Handbook of quantitative cell physiology, third edition",
            "first_author": "Marchetti",
            "year": "2019",
            "venue": "Universitat Press",
            "raw": (
                "Marchetti L. Handbook of quantitative cell physiology, third edition. "
                "Universitat Press 2019."
            ),
        },
        {
            "id": "ref-4",
            "label": "4",
            "title": "Cryostasis artefacts in cryo-electron tomography of mitochondria",
            "first_author": "Sorensen",
            "year": "2022",
            "venue": "Ultramicroscopy",
            "raw": (
                "Sorensen K. Cryostasis artefacts in cryo-electron tomography of "
                "mitochondria. Ultramicroscopy 2022."
            ),
        },
    ],
    "blocks": [
        {
            "id": "block-results-1",
            "kind": "paragraph",
            "section": "Results",
            "text": (
                "Calcium entry through the uniporter saturates above two micromolar in "
                "isolated myocytes [1]. The nucleolus has been modelled as a phase "
                "separated compartment [2]."
            ),
        },
        {
            "id": "block-methods-1",
            "kind": "paragraph",
            "section": "Methods",
            "text": (
                "Physiological constants were taken from the standard handbook [3]. "
                "Tomography of mitochondria is prone to freezing artefacts [4]."
            ),
        },
    ],
}

# What Crossref answers for the one DOI it holds. The compared fields are the
# ones the reference list prints, so the row resolves with nothing mismatched,
# which is what a reference in good order looks like in this table.
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

EMPTY_CROSSREF_SEARCH = {"status": "ok", "message": {"items": []}}
EMPTY_EUROPEPMC = {"resultList": {"result": []}}
HANDLE_NOT_FOUND_BODY = {"responseCode": 100, "handle": UNREGISTERED_DOI}

# The one word in a title search URL that says which reference is being looked
# up. Routing on the title keeps the opener readable: a reference that is not
# located and a reference whose lookups failed differ only in what answered.
UNREACHABLE_TOKEN = "cryostasis"
NOT_LOCATED_TOKEN = "handbook"

# A phrase out of the fetched abstract above, which the resolver stores in the
# lookups cache and in the ledger's own source window. It is here so a check
# can prove no published bundle carries it: the lookups cache is third party
# publisher text, the review rests on it only through the short passage quoted
# in a verdict, and republishing the rest would make this a mirror of it.
FETCHED_PHRASE = "Flux saturated above two micromolar"


class _Response:
    """What `urllib`'s opener hands back: a context manager that reads bytes."""

    def __init__(self, body: bytes) -> None:
        self._body = body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_exc: object) -> bool:
        return False

    def read(self, _limit: int | None = None) -> bytes:
        return self._body


def _body(payload: dict) -> bytes:
    return json.dumps(payload).encode("utf-8")


def _not_found(url: str, payload: dict | None = None) -> urllib.error.HTTPError:
    """An HTTP 404, with the DOI resolver's own body when there is one."""
    raw = _body(payload) if payload is not None else b""
    return urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(raw))


def opener(request, timeout: int | None = None):
    """Every lookup the resolver makes, answered from the canned bodies above.

    The engine builds the URLs, so this routes on them rather than on a call
    count: the resolver asks Crossref for the printed DOI, then the Crossref
    agency index, then the DOI resolver's handle route, then the two title
    searches, and finally Europe PMC for an abstract it already has.
    """
    url = request.full_url
    readable = urllib.parse.unquote_plus(url).casefold()
    if "api.crossref.org/works/" in url:
        if RESOLVED_DOI in url:
            return _Response(_body(CROSSREF_WORK))
        # Crossref has no record of it, and neither does its agency index.
        raise _not_found(url)
    if "doi.org/api/handles/" in url:
        raise _not_found(url, HANDLE_NOT_FOUND_BODY)
    if UNREACHABLE_TOKEN in readable:
        # Neither index answered. The row that comes out of this says nothing
        # about the reference, which is the state this fixture exists to carry.
        raise OSError("the fixture lookup host did not answer")
    if "api.crossref.org/works?" in url:
        return _Response(_body(EMPTY_CROSSREF_SEARCH))
    if "ebi.ac.uk/europepmc" in url:
        return _Response(_body(EMPTY_EUROPEPMC))
    raise OSError("no canned answer for " + url)


def _judge(ledger, slot: str, row_id: str, answer: str, passage: str = "") -> None:
    stored, refusal = citation_ledger.verdict(ledger, slot, row_id, answer, passage=passage)
    if stored is None:
        raise SystemExit("the engine refused a fixture verdict: " + str(refusal))


def _use_row(ledger, marker: str) -> dict:
    """The one use row whose marker is this one, by the ledger's own reading."""
    rows = [row for row in ledger.rows("use") if row.get("marker") == marker]
    if len(rows) != 1:
        raise SystemExit("expected one use row for " + marker + ", found " + str(len(rows)))
    return rows[0]


def _passage(ledger, reference_id: str) -> str:
    """A clause of the stored source text, taken from the stored source text.

    Quoted out of the ledger rather than out of the canned body above, because
    the engine refuses a passage that is not in the source text character for
    character, and the source text is the abstract after the engine has stripped
    its markup.
    """
    reference = next(row for row in ledger.rows("reference")
                     if row.get("reference_id") == reference_id)
    body = citation_ledger.source_body(citation_ledger.source_window(reference))
    start = body.index(FETCHED_PHRASE)
    return body[start:start + 96]


def fill(review: Path, slot: str = "cite-1") -> dict:
    """Fill, resolve and judge one fixture ledger inside a review directory.

    Everything lands where a run puts it: `citations/ledger.jsonl`,
    `citations/stages.json` and the lookups cache beside them. A caller that
    wants a run folder with a citation lane in it points this at the folder,
    and a caller that wants the two files on their own goes through `build`.
    """
    citation_ledger.now = lambda: FIXED_TIME
    ledger = citation_ledger.Ledger(Path(review))
    citation_ledger.build(ledger, PAPER)
    lookups = citation_ledger.Lookups(ledger.cache, opener=opener)
    # Three passes, because a reference whose lookups did not answer is owed
    # another attempt and the stage is not done while one is owed. `wait=0`
    # takes the row up again in the same second, which only a fixture may do:
    # a caller that shortens the gap in a real run is asking a host that has
    # not had time to recover.
    for _ in range(citation_ledger.RESOLVE_ATTEMPTS):
        citation_ledger.resolve(ledger, lookups, retry=True, wait=0)
    claimed = {row["row_id"] for row in citation_ledger.batch(ledger, slot, size=10)}
    supported = _use_row(ledger, "[1]")
    if supported["row_id"] not in claimed:
        raise SystemExit("the fixture batch did not include the judgeable row")
    _judge(ledger, slot, supported["row_id"], "supports",
           _passage(ledger, supported["reference_id"]))
    # Two rows the table holds no source text for. The engine allows one
    # answer there, and a worker that answered anything else is refused.
    for marker in ("[2]", "[3]"):
        _judge(ledger, slot, _use_row(ledger, marker)["row_id"], "cannot tell")
    # The fourth use is left claimed and unjudged: one stage short of done.
    return citation_ledger.counts(ledger)


def counts(review: Path) -> dict:
    """The tallies a ledger already written under this review holds.

    For a caller that wrote the lane earlier and wants the numbers again
    without appending a second copy of every row.
    """
    return citation_ledger.counts(citation_ledger.Ledger(Path(review)))


def build(out: Path) -> dict:
    """Fill one fixture ledger in a scratch review, and copy the two files out."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="citation-ledger-fixture-") as workspace:
        review = Path(workspace) / "review"
        totals = fill(review)
        ledger = citation_ledger.Ledger(review)
        shutil.copyfile(ledger.path, out / "citation-ledger.jsonl")
        shutil.copyfile(ledger.state_path, out / "citation-stages.json")
    return totals


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True,
                        help="Directory the two fixture files are written to")
    args = parser.parse_args(argv)
    totals = build(Path(args.out).resolve())
    for key in ("references", "resolved", "not_found", "not_located", "could_not_check",
                "uses", "uses_judged", "uses_unjudged", "supported", "cannot_tell",
                "with_source_text", "complete", "stages_done"):
        print(f"{key:18} {totals[key]}")
    for line in citation_ledger.problems(totals):
        print("problem  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
