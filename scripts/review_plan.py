"""Locate manuscript versions and plan immutable review attempts."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from fetch_preprint import Preprint
from review_commands import CommandError
from review_paths import REPO, REVIEWS


def slugify(text: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if len(s) <= limit:
        return s
    return s[:limit].rsplit("-", 1)[0] or s[:limit]


def paper_slug(preprint: Preprint, title: str) -> str:
    """A directory name that is readable *and* unique to one preprint.

    Titles alone are neither. slugify truncates at 60 characters, so two
    genuinely different papers can collide:

        "Deep learning approaches for the prediction of protein structure..."
        "Deep learning approaches for the prediction of protein folding..."

    both reduce to `deep-learning-approaches-for-the-prediction-of-protein`,
    and the second review would land on top of the first. Appending the
    preprint's own identifier makes the name unique by construction, and
    since submissions are restricted to arXiv/bioRxiv/medRxiv, there is
    always one.
    """
    title_part = slugify(title, limit=50)
    id_part = slugify(preprint.identifier or preprint.doi or preprint.url, limit=40)
    slug = "-".join(p for p in (title_part, id_part) if p)
    return slug or "submission"


def _published_provenance_paths() -> list[Path]:
    """Every legacy and attempt-aware provenance record in the corpus."""
    return sorted(
        list(REVIEWS.glob("*/*/v*/provenance.json"))
        + list(REVIEWS.glob("*/*/v*/r*/provenance.json"))
    )


def _paper_dir_for_bundle(bundle: Path) -> Path:
    """Return the paper directory for either ``vN`` or ``vN/rN``."""
    version_dir = bundle.parent if re.fullmatch(r"r\d+", bundle.name) else bundle
    return version_dir.parent


def _bundle_coordinates(bundle: Path) -> tuple[int, int]:
    """Return manuscript version and review attempt for one bundle."""
    if re.fullmatch(r"r\d+", bundle.name):
        return int(bundle.parent.name[1:]), int(bundle.name[1:])
    return int(bundle.name[1:]), 1


def find_paper_dir(preprint: Preprint) -> Path | None:
    """The directory already holding this paper's reviews, if any.

    Matched on the preprint's identifier rather than the slug. The slug embeds
    the title, and authors retitle between drafts, so a slug lookup can miss
    the earlier reviews of the same paper.
    """
    wanted = (preprint.identifier or preprint.doi or "").strip().lower()
    if not wanted:
        return None
    for prov_path in _published_provenance_paths():
        try:
            prov = json.loads(prov_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pp = prov.get("preprint") or {}
        got = str(pp.get("identifier") or pp.get("doi") or "").strip().lower()
        if got and got == wanted:
            return _paper_dir_for_bundle(prov_path.parent)
    return None


def _rerun_provenance(bundle: str) -> dict | None:
    """The provenance of the bundle being re-reviewed, or None with a message.

    Only provenance is needed, not a round record: a rerun is a fresh round 1
    that rules on nothing from before, so reviews published before round
    records existed can still be rerun. That is deliberate, the oldest
    reviews are the ones most likely to predate a pipeline worth re-running.
    """
    path = Path(bundle).resolve()
    prov_path = path / "provenance.json"
    if not prov_path.is_file():
        print(
            f"--rerun-of {bundle}: no provenance.json there. Point this at a "
            "published bundle directory, e.g. docs/reviews/2026/<slug>/v1.",
            file=sys.stderr,
        )
        return None
    try:
        prov = json.loads(prov_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"--rerun-of {bundle}: unreadable provenance.json ({exc}).", file=sys.stderr)
        return None
    if not (prov.get("preprint") or {}).get("url"):
        print(
            f"--rerun-of {bundle}: provenance records no preprint URL, so the "
            "draft it reviewed cannot be fetched again.",
            file=sys.stderr,
        )
        return None
    prov["_bundle"] = path
    return prov


# The wrapper that fetched a manuscript, converted it through the old ingest
# loader and compared it to the earlier bundle lived here. Engine 0.8.0 deletes
# `peerreviewagents.ingest`, and the local lane reads its own ingest record off
# the engine run, so the comparison below is the whole surviving contract.
def draft_matches(prior: dict, current: dict) -> tuple[bool, str]:
    """Compare two ingest records. Pure, so it can be tested without a PDF.

    Three tiers, strongest first. The text fingerprint is proof. The character
    count is evidence, and is all that older bundles carry. A bundle recording
    neither cannot be checked, and says so rather than claiming a match.
    """
    want = str(prior.get("text_sha256") or "")
    if want:
        got = str(current.get("text_sha256") or "")
        if want == got:
            return True, f"rerun     same draft confirmed (text {got[:16]}…)"
        return False, (
            "This is not the manuscript that bundle reviewed.\n"
            f"  recorded text {want}\n"
            f"  converted     {got}"
        )

    want_chars, got_chars = prior.get("chars"), current.get("chars")
    if isinstance(want_chars, int) and isinstance(got_chars, int):
        if want_chars == got_chars:
            return True, (
                f"rerun     same draft, probably: {got_chars:,} characters, "
                "matching the earlier bundle. That bundle predates the text "
                "fingerprint, so this is a length match, not proof."
            )
        return False, (
            "This is not the manuscript that bundle reviewed.\n"
            f"  recorded  {want_chars:,} characters\n"
            f"  converted {got_chars:,}"
        )

    return True, (
        "warning: the prior bundle recorded nothing about the text it read, so "
        "this rerun cannot show it read the same draft."
    )


def draft_number(preprint: Preprint) -> int:
    """Which draft of the paper this is, per the archive.

    The bundle directory is named after this, not after how many times we have
    run. `v3` means "our review of the authors' third draft", a fact about
    the paper rather than a count of our activity.

    It is a fact we are given, not one we choose: `resolve()` always reports
    whatever the archive serves now, and refuses to go backwards. So the
    number only ever increases, and folder order can never disagree with the
    order the drafts were written in.
    """
    try:
        return max(1, int(str(preprint.version or "1").strip()))
    except (TypeError, ValueError):
        return 1


def existing_bundles(paper_dir: Path) -> dict[int, list[Path]]:
    """Draft number to immutable review attempts, oldest first."""
    out: dict[int, list[Path]] = {}
    for version_dir in sorted(paper_dir.glob("v*")):
        if not version_dir.is_dir() or not version_dir.name[1:].isdigit():
            continue
        draft = int(version_dir.name[1:])
        attempts: list[Path] = []
        if (version_dir / "provenance.json").is_file():
            attempts.append(version_dir)
        attempts.extend(
            sorted(
                (
                    p for p in version_dir.glob("r*")
                    if p.is_dir() and p.name[1:].isdigit()
                    and (p / "provenance.json").is_file()
                ),
                key=lambda p: int(p.name[1:]),
            )
        )
        if attempts:
            out[draft] = attempts
    return out


@dataclass
class Plan:
    """Where this review goes, and what kind of run it therefore is."""

    dest: Path
    draft: int
    attempt: int = 1
    # The previous attempt when this is a fresh review of identical text.
    previous_attempt: Path | None = None

    @property
    def kind(self) -> str:
        if self.previous_attempt:
            return "same-draft re-review"
        return "review of this draft"


def plan_review(
    paper_dir: Path, draft: int, replace: bool, *, publishing: bool = True
) -> Plan:
    """Decide where a review of ``draft`` belongs, or refuse.

    Two cases, and the caller declares neither:

    - no review of this draft yet             -> a review of this draft
    - a review of this draft already exists   -> needs ``replace``

    The second case creates another immutable attempt for the same manuscript
    version. Despite the legacy command name, it never replaces or edits the
    earlier attempt. If the authors have posted a new version, the draft number
    differs and the run lands in its own folder instead.

    Either way the run is one independent review. A review of a new draft reads
    that draft and no earlier review of the paper, so there is nothing here that
    locates an earlier bundle to be measured against.

    ``publishing`` is false for a run that lands in ``runs/``, and then that
    refusal does not apply: there is no bundle at stake, because the run
    cannot reach ``docs/reviews/`` at all. Enforcing it anyway made the
    already-reviewed papers the ones a pipeline change could never be tested
    against, which is backwards, since they are the ones with a published
    result to compare against.
    """
    published = existing_bundles(paper_dir)
    same_draft = published.get(draft, [])
    attempt = max(
        (_bundle_coordinates(bundle)[1] for bundle in same_draft),
        default=0,
    ) + 1
    dest = paper_dir / f"v{draft}" / f"r{attempt}"

    if same_draft and publishing:
        if not replace:
            latest = same_draft[-1]
            raise CommandError(
                f"Draft v{draft} of this paper has already been reviewed "
                f"({latest.relative_to(REPO) if latest.is_relative_to(REPO) else latest}). "
                "The archive still serves that draft, so there is nothing new "
                "to read. Pass --replace (or `/review replace`) to review it "
                "again as a new immutable attempt, or wait for the authors "
                "to post a new version."
            )
        return Plan(
            dest=dest,
            draft=draft,
            attempt=attempt,
            previous_attempt=same_draft[-1],
        )

    if same_draft and replace:
        return Plan(
            dest=dest,
            draft=draft,
            attempt=attempt,
            previous_attempt=same_draft[-1],
        )

    return Plan(dest=dest, draft=draft, attempt=attempt)
