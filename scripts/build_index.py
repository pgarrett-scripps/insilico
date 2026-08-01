"""Regenerate ``docs/reviews/index.md`` from the frontmatter of each review.

Run after adding or removing a review bundle. Idempotent; safe to run in CI on
every build.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"

BADGE = {
    "accept": "✅ Accept",
    "minor": "🟢 Minor revision",
    "major": "🟡 Major revision",
    "reject": "🔴 Reject",
}


def read_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    _, _, rest = text.partition("---")
    raw, sep, _ = rest.partition("\n---")
    if not sep:
        return None
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def collect() -> list[dict]:
    entries = []
    for landing in sorted(REVIEWS.glob("*/*/index.md")):
        meta = read_frontmatter(landing)
        if not meta:
            print(f"skipping {landing.relative_to(REPO)}: no usable frontmatter")
            continue
        meta["path"] = landing.parent.relative_to(REVIEWS).as_posix()
        meta["year"] = landing.parent.parent.name
        entries.append(meta)
    entries.sort(key=lambda e: (e.get("reviewed", ""), e.get("title", "")), reverse=True)
    return entries


def render(entries: list[dict]) -> str:
    lines = [
        "# Published reviews",
        "",
        f"{len(entries)} review{'' if len(entries) == 1 else 's'} published.",
        "",
        "Each entry links to a preprint hosted elsewhere and to the full referee",
        "bundle produced for it. Recommendations are advisory — see the",
        "[editorial policy](../policy.md).",
        "",
    ]

    if not entries:
        lines += [
            "!!! note \"Nothing published yet\"",
            "    Reviews appear here once an editor merges a review PR.",
            "",
        ]
        return "\n".join(lines)

    by_year: dict[str, list[dict]] = {}
    for entry in entries:
        by_year.setdefault(entry["year"], []).append(entry)

    for year in sorted(by_year, reverse=True):
        lines += [f"## {year}", "", "| Paper | Recommendation | Source | Reviewed |", "|---|---|---|---|"]
        for entry in by_year[year]:
            title = str(entry.get("title", "Untitled")).replace("|", "\\|")
            decision = str(entry.get("decision", ""))
            lines.append(
                f"| [{title}]({entry['path']}/index.md) "
                f"| {BADGE.get(decision, decision)} "
                f"| {entry.get('source', '—')} "
                f"| {entry.get('reviewed', '—')} |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    REVIEWS.mkdir(parents=True, exist_ok=True)
    entries = collect()
    (REVIEWS / "index.md").write_text(render(entries), encoding="utf-8")

    # Machine-readable mirror, for anyone who wants to consume the corpus.
    (REVIEWS / "index.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"indexed {len(entries)} review(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
