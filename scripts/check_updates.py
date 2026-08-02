"""Find published reviews whose preprint has changed since we reviewed it.

    python scripts/check_updates.py              # human-readable report
    python scripts/check_updates.py --json       # machine-readable
    python scripts/check_updates.py --only-stale # exit 1 if anything is stale

A review is a statement about a specific revision of a manuscript. Preprint
servers let authors replace that revision in place, so a published review can
silently come to sit next to a paper it never read. This walks the published
corpus, re-resolves each preprint, and reports what moved.

Two independent signals, deliberately not conflated:

``version``
    The server's own revision counter (arXiv v1 -> v2, bioRxiv v1 -> v2). A
    bump is authoritative: the authors posted a new revision, and the review
    is now stale. This is the signal to act on.

``pdf_sha256``
    The bytes we actually reviewed. A change here means *something* about the
    file differs, which is weaker evidence than it sounds. Treat it as a prompt
    to look, never as proof.

The converse is the case worth having both for: bytes changed with no version
bump means the file was replaced without the server recording a revision, and
nothing else would catch that.

How much a byte change is worth depends entirely on the server, which is why
they are not treated alike:

    arXiv       serves a fixed file per version. Two fetches of the same URL
                are byte-identical, so a hash change really does mean the file
                was replaced.
    bioRxiv     re-renders on request and stamps each PDF with a generation
    medRxiv     date. Two fetches seconds apart already differ, so a hash
                change on its own carries no information at all.

For the re-stamping servers the length is the usable signal: a date stamp
swaps bytes in place and leaves the size untouched, while edited content
essentially never does. So an unchanged length is reported as a re-stamp and
is *not* stale, and only a length change is worth an editor's attention.

Getting this wrong is not a small matter of tidiness. Treating every re-stamp
as staleness would file a report every month naming the same papers, none of
which had changed — and a monthly alarm that is always wrong is one an editor
correctly learns to ignore, which costs the real signal too.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fetch_preprint import fingerprint, resolve  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"

# Exit codes: 0 nothing to do, 1 something is stale (with --only-stale),
# 2 the check itself could not run. CI can branch on these.
EXIT_OK, EXIT_STALE, EXIT_ERROR = 0, 1, 2

# Servers that re-render the PDF per request and stamp it with a generation
# date, so its bytes differ every time it is fetched. Verified by fetching the
# same URL twice: bioRxiv returns two different hashes at identical length,
# arXiv returns the same hash.
RESTAMPING_SOURCES = {"biorxiv", "medrxiv"}


def published() -> list[tuple[Path, dict]]:
    """The most recent review of each published paper, where it can be re-checked.

    Bundles live at ``docs/reviews/<year>/<slug>/v<N>/``, so the glob has to
    reach the version directory. It matched only two levels until this was
    fixed, which meant it silently found nothing at all once reviews became
    versioned — the check reported "no published reviews" every month and the
    corpus went unwatched.

    One entry per *paper*, not per bundle. Older versions are by definition
    reviews of superseded drafts: re-checking them would report every paper
    that has ever been revised as stale forever, which is noise that would
    train an editor to ignore the report.
    """
    latest: dict[Path, tuple[int, Path, dict]] = {}
    for prov_path in sorted(REVIEWS.glob("*/*/v*/provenance.json")):
        bundle = prov_path.parent
        if not bundle.name[1:].isdigit():
            continue
        try:
            prov = json.loads(prov_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"skipping {prov_path.relative_to(REPO)}: {exc}", file=sys.stderr)
            continue
        if not prov.get("preprint", {}).get("url"):
            continue
        version = int(bundle.name[1:])
        paper = bundle.parent
        if paper not in latest or version > latest[paper][0]:
            latest[paper] = (version, bundle, prov)
    return [
        (bundle, prov)
        for bundle, prov in sorted(
            ((b, p) for _, b, p in latest.values()), key=lambda e: str(e[0])
        )
    ]


def check_one(bundle: Path, prov: dict) -> dict:
    """Re-resolve one published review's preprint and diff it against the record."""
    old = prov.get("preprint", {})
    result = {
        "review": bundle.relative_to(REVIEWS).as_posix(),
        "title": old.get("title") or "Untitled",
        "url": old.get("url", ""),
        "reviewed_version": old.get("version") or "",
        "reviewed_sha256": old.get("pdf_sha256") or "",
        "reviewed_bytes": old.get("pdf_bytes") or 0,
        "source": old.get("source") or "",
        "status": "unchanged",
        "detail": "",
    }

    # Reviews published before fingerprinting existed have nothing to compare
    # against. Say so rather than reporting them as unchanged, which would be
    # a claim the data does not support.
    if not result["reviewed_sha256"] and not result["reviewed_version"]:
        result["status"] = "unknown"
        result["detail"] = "reviewed before fingerprints were recorded; cannot compare"
        return result

    try:
        current = resolve(result["url"])
    except (ValueError, urllib.error.URLError) as exc:
        result["status"] = "unreachable"
        result["detail"] = f"could not re-resolve: {exc}"
        return result

    result["current_version"] = current.version or ""

    if result["reviewed_version"] and current.version:
        if str(current.version) != str(result["reviewed_version"]):
            result["status"] = "revised"
            result["detail"] = (
                f"version {result['reviewed_version']} -> {current.version}; "
                "the authors posted a new revision"
            )
            return result

    if not result["reviewed_sha256"]:
        result["detail"] = "version matches; no hash on record to compare"
        return result

    try:
        sha, size = fingerprint(current)
    except (ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        result["status"] = "unreachable"
        result["detail"] = f"could not fetch the PDF: {exc}"
        return result

    result["current_sha256"] = sha
    result["current_bytes"] = size
    if sha == result["reviewed_sha256"]:
        return result

    # A re-stamping server changes bytes on every fetch, so the hash alone
    # says nothing. The length is what carries information there: a date
    # stamp is written in place and leaves it identical, while edited content
    # essentially never does.
    if result["source"] in RESTAMPING_SOURCES:
        was = result["reviewed_bytes"]
        if was and size == was:
            result["status"] = "restamped"
            result["detail"] = (
                f"the PDF bytes differ but its length is unchanged ({size} bytes). "
                f"{result['source']} re-renders on request and stamps each copy "
                "with a generation date, so this is the expected result for an "
                "untouched manuscript, not evidence of a change."
            )
            return result
        result["status"] = "bytes-differ"
        result["detail"] = (
            f"the PDF length changed ({was or 'unrecorded'} -> {size} bytes) with "
            f"no version bump. {result['source']} re-stamps every copy, so the "
            "hash alone would prove nothing — but the length moving means the "
            "content was actually edited. Worth comparing."
        )
        return result

    result["status"] = "bytes-differ"
    result["detail"] = (
        "the PDF changed but the version did not. arXiv serves a fixed file per "
        "version, so the file was genuinely replaced without the server "
        "recording a revision. Compare before acting."
    )
    return result


# Ordered worst-first so a report reads top-down.
_ORDER = {
    "revised": 0,
    "bytes-differ": 1,
    "unreachable": 2,
    "unknown": 3,
    "restamped": 4,
    "unchanged": 5,
}
_LABEL = {
    "revised": "REVISED     ",
    "bytes-differ": "BYTES DIFFER",
    "unreachable": "UNREACHABLE ",
    "unknown": "NO BASELINE ",
    "restamped": "re-stamped  ",
    "unchanged": "unchanged   ",
}

# What actually warrants an editor's attention. `restamped` is deliberately
# absent: it is the documented, reproducible behaviour of two of the three
# supported servers, and reporting it would bury the two statuses that mean
# something.
STALE_STATUSES = ("revised", "bytes-differ")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    ap.add_argument(
        "--only-stale",
        action="store_true",
        help="exit 1 if any review is stale, for use as a CI gate",
    )
    args = ap.parse_args()

    entries = published()
    if not entries:
        # Still emit a well-formed empty document in --json mode. The monthly
        # workflow pipes this straight into json.load, so printing nothing
        # crashes the job — and a corpus checker that fails loudly when the
        # corpus is empty is a worse signal than one that says "nothing yet".
        print("no published reviews to check", file=sys.stderr)
        if args.json:
            print("[]")
        return EXIT_OK

    results = [check_one(bundle, prov) for bundle, prov in entries]
    results.sort(key=lambda r: (_ORDER.get(r["status"], 9), r["review"]))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{_LABEL.get(r['status'], r['status'])}  {r['review']}")
            if r["detail"]:
                print(f"                {r['detail']}")

    stale = [r for r in results if r["status"] in STALE_STATUSES]
    unreachable = [r for r in results if r["status"] == "unreachable"]
    if not args.json:
        print(
            f"\n{len(results)} review(s) checked, {len(stale)} stale",
            file=sys.stderr,
        )

    # Every source unreachable is a broken check, not a clean bill of health.
    # Reported as an error so a month of failed DNS can't read as "nothing
    # changed" — the whole point of this job is to notice change.
    if unreachable and len(unreachable) == len(results):
        print(
            "every preprint was unreachable; the check could not run",
            file=sys.stderr,
        )
        return EXIT_ERROR
    if args.only_stale and stale:
        return EXIT_STALE
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
