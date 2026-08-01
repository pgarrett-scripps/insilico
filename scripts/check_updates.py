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
    file differs, which is weaker evidence than it sounds: bioRxiv and medRxiv
    stamp each PDF with a generation date, and re-rendering can change
    compression, so a byte difference is routine and does not by itself mean
    the science changed. Treat it as a prompt to look, never as proof.

The converse is the case worth having both for: bytes changed with no version
bump means the file was replaced without the server recording a revision, and
nothing else would catch that.
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


def published() -> list[tuple[Path, dict]]:
    """Every published review that recorded enough provenance to re-check."""
    out = []
    for prov_path in sorted(REVIEWS.glob("*/*/provenance.json")):
        try:
            prov = json.loads(prov_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"skipping {prov_path.relative_to(REPO)}: {exc}", file=sys.stderr)
            continue
        if prov.get("preprint", {}).get("url"):
            out.append((prov_path.parent, prov))
    return out


def check_one(bundle: Path, prov: dict) -> dict:
    """Re-resolve one published review's preprint and diff it against the record."""
    old = prov.get("preprint", {})
    result = {
        "review": bundle.relative_to(REVIEWS).as_posix(),
        "title": old.get("title") or "Untitled",
        "url": old.get("url", ""),
        "reviewed_version": old.get("version") or "",
        "reviewed_sha256": old.get("pdf_sha256") or "",
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
    if sha != result["reviewed_sha256"]:
        result["status"] = "bytes-differ"
        result["detail"] = (
            "the PDF changed but the version did not. Often a re-stamped or "
            "re-rendered file rather than new science — compare before acting."
        )
    return result


# Ordered worst-first so a report reads top-down.
_ORDER = {"revised": 0, "bytes-differ": 1, "unreachable": 2, "unknown": 3, "unchanged": 4}
_LABEL = {
    "revised": "REVISED     ",
    "bytes-differ": "BYTES DIFFER",
    "unreachable": "UNREACHABLE ",
    "unknown": "NO BASELINE ",
    "unchanged": "unchanged   ",
}


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
        print("no published reviews to check", file=sys.stderr)
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

    stale = [r for r in results if r["status"] in ("revised", "bytes-differ")]
    if not args.json:
        print(
            f"\n{len(results)} review(s) checked, {len(stale)} stale",
            file=sys.stderr,
        )
    if args.only_stale and stale:
        return EXIT_STALE
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
