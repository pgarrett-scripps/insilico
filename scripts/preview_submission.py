"""Render the metadata preview posted on a new submission issue.

This is intentionally stdlib-only. It resolves archive metadata but never
downloads the PDF and never calls a model.

    python scripts/preview_submission.py --issue-body "$ISSUE_BODY"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from fetch_preprint import Preprint, extract_url, resolve

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"
COMMENT_MARKER = "<!-- insilico-submission-preview -->"


def _cell(value: object) -> str:
    """Make external metadata safe inside a Markdown table cell."""
    text = " ".join(str(value or "").split()).replace("\\", "\\\\")
    for character in ("`", "*", "_", "{", "}", "[", "]", "<", ">", "#", "|"):
        text = text.replace(character, f"\\{character}")
    return text.replace("@", "@\u200b")


def _authors(names: list[str], limit: int = 12) -> str:
    if not names:
        return "Unavailable"
    shown = ", ".join(names[:limit])
    remaining = len(names) - limit
    return f"{shown}, plus {remaining} more" if remaining > 0 else shown


def _draft(preprint: Preprint) -> int:
    try:
        return max(1, int(str(preprint.version or "1").strip()))
    except (TypeError, ValueError):
        return 1


def _reviewed_drafts(preprint: Preprint, reviews_root: Path) -> list[int]:
    """Return published draft numbers for this archive identifier."""
    wanted = {
        str(value or "").strip().lower()
        for value in (preprint.identifier, preprint.doi)
        if str(value or "").strip()
    }
    if not wanted:
        return []

    found: set[int] = set()
    for path in reviews_root.glob("*/*/v*/provenance.json"):
        try:
            provenance = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        recorded = provenance.get("preprint") or {}
        identifiers = {
            str(value or "").strip().lower()
            for value in (recorded.get("identifier"), recorded.get("doi"))
            if str(value or "").strip()
        }
        if wanted.isdisjoint(identifiers):
            continue
        version = str(recorded.get("version") or path.parent.name.removeprefix("v"))
        try:
            found.add(max(1, int(version)))
        except (TypeError, ValueError):
            continue
    return sorted(found)


def _commands(current_draft: int, reviewed: list[int]) -> str:
    if current_draft in reviewed:
        primary = (
            f"Draft v{current_draft} already has a published review. Use "
            "`/review replace` only if you intend to overwrite that review with "
            "a fresh panel run. If the authors have a newer draft, wait for the "
            "archive to serve it and use `/review`."
        )
    elif reviewed:
        previous = ", ".join(f"v{number}" for number in reviewed)
        primary = (
            f"Earlier draft {previous} has been reviewed. Use `/review` to open "
            f"a revision round for v{current_draft}."
        )
    else:
        primary = "Use `/review` to run the configured referee panel."

    return f"""### Editor commands

{primary}

| Command | Action |
|---|---|
| `/review` | Run the configured panel against the current archive draft. |
| `/review anthropic` | Explicitly run the configured Anthropic panel. |
| `/review openrouter vendor/model` | Run every role with one named OpenRouter model. |

Only repository owners, members, and collaborators can start a run.
"""


def _error_preview(reason: str) -> str:
    return f"""{COMMENT_MARKER}
## Submission preview

> [!WARNING]
> The preprint metadata could not be resolved, so no review should be started yet.

{_cell(reason)}

Edit the issue so its first link is an arXiv, bioRxiv, or medRxiv abstract page. Do not use a direct PDF link. Editing the issue refreshes this preview.
"""


def build_preview(
    issue_body: str,
    *,
    resolver: Callable[[str], Preprint] = resolve,
    reviews_root: Path = REVIEWS,
) -> str:
    """Resolve an issue body and return the complete bot comment."""
    try:
        url = extract_url(issue_body)
        preprint = resolver(url)
    except ValueError as exc:
        return _error_preview(str(exc))

    current_draft = _draft(preprint)
    reviewed = _reviewed_drafts(preprint, reviews_root)
    history = ", ".join(f"v{number}" for number in reviewed) if reviewed else "None"
    source = {
        "arxiv": "arXiv",
        "biorxiv": "bioRxiv",
        "medrxiv": "medRxiv",
    }.get(preprint.source.lower(), preprint.source)

    rows = [
        ("Title", preprint.title or "Unavailable"),
        ("Authors", _authors(preprint.authors)),
        ("Archive", source),
        ("Identifier", preprint.identifier or preprint.doi or "Unavailable"),
        ("Posted", preprint.published or "Unavailable"),
        ("Current draft", f"v{current_draft}"),
        ("Published In Silico reviews", history),
    ]
    table = "\n".join(f"| {label} | {_cell(value)} |" for label, value in rows)

    if not preprint.title:
        readiness = """
> [!WARNING]
> The archive returned no title or author metadata. Wait and edit the issue to retry before starting a review.
"""
        commands = ""
    else:
        readiness = ""
        commands = "\n" + _commands(current_draft, reviewed)

    return f"""{COMMENT_MARKER}
## Submission preview

| Field | Value |
|---|---|
{table}
{readiness}{commands}
This preview uses public archive metadata and makes no model calls. Editing the issue refreshes it.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-body", required=True)
    args = parser.parse_args()
    print(build_preview(args.issue_body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
