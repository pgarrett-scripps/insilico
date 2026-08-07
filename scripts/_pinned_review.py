"""Review a specific preprint version rather than the current one. Testing only.

`resolve()` deliberately always returns the *latest* version of a preprint,
because a review has to describe what is actually posted now. That is correct
in production and makes the revision pipeline impossible to exercise: to test
a v1 -> v2 round you have to first hold a review of v1, and by the time v2
exists the resolver will only ever hand you v2.

This pins the version for the first leg of that test. It changes nothing about
how a review is produced — the pinned Preprint goes through the ordinary
run_review path — so what it exercises is the real bundle writer, the real
round record, and afterwards the real `--revise` flow resolving forward to v2
and diffing against the recorded v1 bytes.

The other reason to pin is a benchmark against human referees: a journal's
peer review file describes the manuscript as *submitted*, which is whichever
preprint version predates the journal's received date, not the revised draft
the resolver serves today. Comparing a review of v4 against referee reports
written on v2 measures nothing.

Not wired into the CLI on purpose. Reviewing a stale revision is a thing to do
deliberately in a test, not an option an editor should find sitting on the
production command.

    python scripts/_pinned_review.py 2607.24356 1
    python scripts/_pinned_review.py 10.1101/2024.08.26.609665 2
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import run_review  # noqa: E402
from fetch_preprint import _clean, _rxiv_records  # noqa: E402
from fetch_preprint import resolve as _real_resolve  # noqa: E402


def _is_doi(ident: str) -> bool:
    return ident.startswith("10.")


def _landing(ident: str, want: str) -> str:
    """The URL to hand the real resolver, so it identifies the server itself.

    bioRxiv and medRxiv share both DOI prefixes, so which one holds a DOI is
    a question only the servers can answer. Guess bioRxiv here and let
    `resolve` correct it — it already asks both.
    """
    if _is_doi(ident):
        return f"https://www.biorxiv.org/content/{ident}v{want}"
    return f"https://arxiv.org/abs/{ident}"


def _repin_rxiv(pp, ident: str, want: str) -> None:
    """Point a resolved bioRxiv/medRxiv preprint at the version we asked for.

    Metadata as well as the PDF: the record the resolver kept describes the
    newest version, and versions differ in the things a review records. This
    preprint gained an author between v2 and v4, so taking the latest record
    would credit the v2 manuscript with someone who had not joined it yet.
    """
    doi = pp.doi or ident
    base = f"https://www.{pp.source}.org/content/{doi}v{want}"
    pp.pdf_url = f"{base}.full.pdf"
    pp.url = base
    for rec in _rxiv_records(pp.source, doi):
        if str(rec.get("version")) != str(want):
            continue
        pp.title = _clean(rec.get("title", "")) or pp.title
        pp.abstract = _clean(rec.get("abstract", "")) or pp.abstract
        pp.published = rec.get("date", "") or pp.published
        authors = [_clean(a) for a in rec.get("authors", "").split(";") if a.strip()]
        if authors:
            pp.authors = authors
        break


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    ident, want = sys.argv[1], sys.argv[2]

    def pinned(url: str):
        pp = _real_resolve(url)
        latest = pp.version
        pp.version = want
        if pp.source == "arxiv":
            pp.pdf_url = f"https://arxiv.org/pdf/{ident}v{want}"
            pp.url = f"https://arxiv.org/abs/{ident}"
        else:
            _repin_rxiv(pp, ident, want)
        print(
            f"pinned    v{want} (latest is v{latest or '?'}) — {pp.pdf_url}",
            file=sys.stderr,
        )
        return pp

    run_review.resolve = pinned
    sys.argv = [
        "run_review.py",
        "--url", _landing(ident, want),
        "--submitter", "insilico-test",
        "--submitter-is-author", "no",
    ] + sys.argv[3:]
    return run_review.main()


if __name__ == "__main__":
    raise SystemExit(main())
