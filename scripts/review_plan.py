"""Locate manuscript versions and plan immutable review attempts."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from fetch_preprint import Preprint
from review_commands import CommandError
from review_paths import REPO, REVIEWS, ROUND_RECORD


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


def _read_provenance(bundle: Path) -> dict:
    try:
        return json.loads((bundle / "provenance.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def baseline_eligible(bundle: Path) -> bool:
    """Whether a review may define status and anchor the next revision.

    New records state this directly. Legacy records use the existing policy:
    a configured role split is an editorial panel, while a single-model run is
    an experiment. Withdrawn and superseded records never become baselines.
    """
    provenance = _read_provenance(bundle)
    review = provenance.get("review") or {}
    lifecycle = str(review.get("lifecycle") or "active")
    if lifecycle in {"withdrawn", "superseded"}:
        return False
    explicit = review.get("baseline_eligible")
    if isinstance(explicit, bool):
        return explicit
    models = provenance.get("models")
    return isinstance(models, dict) and bool(models)


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


def _same_draft(manuscript: Path, prior: dict, config: dict) -> bool:
    """Whether the manuscript just fetched is the one the prior round read.

    A rerun exists to hold the manuscript fixed and vary the pipeline, so this
    guard is the whole feature: without it a comparison silently measures a
    manuscript change and a pipeline change at once, and produces a bundle
    that looks exactly like evidence about the pipeline.

    It compares the *converted text*, not the PDF. Those are different
    questions and the file hash answers the wrong one. Measured on this very
    paper: three downloads of the same pinned bioRxiv URL over ten hours gave
    three different file checksums at an identical 1,689,095 bytes, the
    server stamps something fixed-width into the container, while the
    converted text came back byte-identical all three times. Checking the file
    hash refuses every bioRxiv rerun, including the correct ones.

    Older bundles predate the text fingerprint. Those fall back to the
    character count, which is weak but real, and say so, refusing to rerun
    the oldest reviews would defeat the purpose, since they are the ones most
    likely to predate a pipeline worth re-running.
    """
    from peerreviewagents.ingest.loader import load_manuscript_record

    ok, message = draft_matches(
        prior.get("ingest") or {}, load_manuscript_record(str(manuscript), config).ingest
    )
    print(message if ok else f"{message}\n{_REVISE_HINT}", file=sys.stderr)
    return ok


_REVISE_HINT = (
    "A rerun holds the manuscript fixed and varies the pipeline, so a "
    "comparison here would measure both at once. If the authors posted a new "
    "version, that is a revision. Use --revise."
)


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
                "matching the prior round. That bundle predates the text "
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


def latest_baseline(
    published: dict[int, list[Path]], *, before_draft: int
) -> Path | None:
    """Newest eligible review of the newest earlier manuscript version."""
    for draft in sorted((n for n in published if n < before_draft), reverse=True):
        for bundle in reversed(published[draft]):
            if (bundle / ROUND_RECORD).is_file() and baseline_eligible(bundle):
                return bundle
    return None


@dataclass
class Plan:
    """Where this review goes, and what kind of run it therefore is."""

    dest: Path
    draft: int
    attempt: int = 1
    # The bundle this round rules against, or None for a first look. Set only
    # when an earlier draft was reviewed AND left a round record.
    prior: Path | None = None
    # The previous attempt when this is a fresh review of identical text.
    previous_attempt: Path | None = None

    @property
    def kind(self) -> str:
        if self.previous_attempt:
            return "same-draft re-review"
        return "revision round" if self.prior else "first review"


def plan_review(
    paper_dir: Path, draft: int, replace: bool, *, publishing: bool = True
) -> Plan:
    """Decide where a review of ``draft`` belongs, or refuse.

    Three cases, and the caller declares none of them:

    - no review of this draft, none of any earlier draft  -> first look
    - no review of this draft, an earlier one exists      -> revision round
    - a review of this draft already exists              -> needs ``replace``

    The last case creates another immutable attempt for the same manuscript
    version. Despite the legacy command name, it never replaces or edits the
    prior attempt. If the authors have posted a new version, the draft number
    differs and the run becomes a revision round instead.

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

    # A revision round rules against the newest earlier draft that left a
    # round record. Reviews published before round records existed cannot be
    # ruled against, there is nothing in them for a referee to check off, so
    # those fall through to a fresh look rather than a broken second round.
    prior = latest_baseline(published, before_draft=draft)
    return Plan(dest=dest, draft=draft, attempt=attempt, prior=prior)
