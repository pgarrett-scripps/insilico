"""Regenerate ``docs/reviews/index.md`` from the frontmatter of each review.

Run after adding or removing a review bundle. Idempotent; safe to run in CI on
every build.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"

VERDICT = {
    "accept": "Accept",
    "minor": "Minor revision",
    "major": "Major revision",
    "reject": "Reject",
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
        # No markdown="1" here. The cards are complete HTML, and asking the
        # markdown processor to walk into them makes it insert paragraph tags
        # that close the <a> early and shred every card.
        lines += [f"## {year}", "", '<div class="ins-cards">', ""]
        lines += [render_card(entry) for entry in by_year[year]]
        lines += ["</div>", ""]

    return "\n".join(lines)


def render_card(entry: dict) -> str:
    """One review as a card.

    Hand-written HTML rather than a markdown table: a table forces every
    review onto one line and gives the verdict the same weight as the date,
    which is backwards for the thing a reader is scanning for.
    """
    title = esc(str(entry.get("title", "Untitled")))
    authors = entry.get("authors") or []
    if isinstance(authors, str):  # a single-author frontmatter scalar
        authors = [authors]
    # Three names then et al. — full author lists on a card crowd out the title.
    shown = ", ".join(esc(str(a)) for a in authors[:3])
    if len(authors) > 3:
        shown += ", et al."

    # A directory URL, not `<path>/index.md`. MkDocs rewrites .md links written
    # in markdown, but leaves raw HTML alone — a card linking to index.md would
    # 404 on the built site while looking correct in the source.
    parts = [
        f'<a class="ins-card" href="{esc(entry["path"])}/">',
        f"  {verdict_chip(entry)}",
        f'  <p class="ins-card__title">{title}</p>',
    ]
    if shown:
        parts.append(f'  <p class="ins-card__authors">{shown}</p>')
    foot = [
        f'<span>{esc(str(entry.get("source", "—")))}</span>',
        f'<span>{esc(str(entry.get("reviewed", "—")))}</span>',
    ]
    score = entry.get("mean_score")
    if isinstance(score, (int, float)):
        foot.append(f'<span class="ins-card__score">{score} / 5</span>')
    parts.append(f'  <span class="ins-card__foot">{"".join(foot)}</span>')
    parts.append("</a>")
    return "\n".join(parts)


def verdict_chip(entry: dict) -> str:
    """The decision as a coloured chip.

    A desk reject carries `decision: reject` too, but nothing read the
    manuscript — rendering both identically would claim a panel weighed the
    work and declined it.
    """
    if entry.get("desk_rejected"):
        return '<span class="ins-verdict ins-verdict--desk">Desk reject</span>'
    decision = str(entry.get("decision", ""))
    label = VERDICT.get(decision, decision or "Unknown")
    return f'<span class="ins-verdict ins-verdict--{esc(decision)}">{esc(label)}</span>'


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


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
