"""Planning regression checks."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[2]

from fetch_preprint import Preprint  # noqa: E402
from run_review import (  # noqa: E402
    BUNDLE_FILES,
    CommandError,
    draft_number,
    paper_slug,
    plan_review,
    slugify,
    write_bundle,
)

from .support import provenance_of  # noqa: E402


def check_versioning() -> None:
    """The bundle directory is named after the draft, and a new draft never
    overwrites the review of the old one.

    `v2` means "our review of the authors' second draft", not "our second
    review". The number is a fact the archive gives us rather than a count of
    our own activity, which is what lets a paper's history be read off the
    directory listing.

    The flat layout it replaced silently overwrote the earlier bundle *and*
    left its specialist reports behind, so a reader saw v1 reports filed under
    v2's verdict. Both halves are still asserted.
    """
    with tempfile.TemporaryDirectory() as tmp:
        paper = Path(tmp) / "2026" / "a-paper"

        def review(mver: str, decision: str, reviewers: tuple[str, ...]) -> int:
            run_dir = Path(tempfile.mkdtemp())
            for name in BUNDLE_FILES:
                (run_dir / name).write_text(f"# {name}\n")
            for r in reviewers:
                (run_dir / f"review_{r}.md").write_text(f"# {r} m{mver}\n")
            os.environ["REVIEW_MODELS"] = "{}"
            os.environ["REVIEW_AGENT_MODELS"] = "{}"
            preprint = Preprint(
                url="https://arxiv.org/abs/1706.03762", source="arxiv",
                pdf_url="p", identifier="1706.03762", title="A paper",
                version=mver, pdf_sha256=mver * 64,
            )
            v = draft_number(preprint)
            write_bundle(
                preprint,
                {"decision": decision, "manuscript_title": "A paper",
                 "total_cost": 1.0, "errors": [], "reports": []},
                run_dir, paper / f"v{v}" / "r1", "1", "octocat",
            )
            return v

        assert review("1", "reject", ("methodology", "novelty", "ethics")) == 1
        assert review("2", "accept", ("methodology",)) == 2,\
            "the folder must be named after the draft the archive served"

        # A draft we have not seen lands beside the others. one we have needs
        # asking for. v1 and v2 both exist by now.
        planned = plan_review(paper, 3, replace=False)
        assert planned.dest.parent.name == "v3" and planned.dest.name == "r1"
        for seen in (1, 2):
            try:
                plan_review(paper, seen, replace=False)
                raise AssertionError(
                    f"re-reviewing reviewed draft v{seen} must refuse"
                )
            except CommandError:
                pass
        again = plan_review(paper, 1, replace=True)
        assert again.previous_attempt == paper / "v1" / "r1"
        assert again.dest == paper / "v1" / "r2",\
            "--replace must create a second immutable review attempt"
        assert again.prior is None,\
            "a same-draft re-review is round 1 and inherits no prior verdict"

        v1 = provenance_of(paper / "v1" / "r1")
        v2 = provenance_of(paper / "v2" / "r1")
        assert v1["decision"] == "reject", "v1 verdict was overwritten by the re-review"
        assert v2["decision"] == "accept", "v2 verdict not recorded"
        assert v1["preprint"]["version"] == "1"
        assert v2["preprint"]["version"] == "2"

        bled = sorted(p.name for p in (paper / "v2" / "r1").glob("review_*.md"))
        assert bled == ["review_methodology.md"], f"v1 reports bled into v2: {bled}"

        # Both bundles sit side by side under the paper, which is what the site
        # walks to build the review history.
        versions = sorted(p.name for p in paper.glob("v*") if p.is_dir())
        assert versions == ["v1", "v2"], f"unexpected bundle layout: {versions}"


def check_round_is_not_version() -> None:
    """The bundle's vN and the review round are different numbers.

    Re-running a review of the same manuscript under changed criteria makes a
    new bundle at round 1. Only a review of a revised draft advances the
    round. Reading one off the other would mislabel both.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name in BUNDLE_FILES:
            (run_dir / name).write_text("x")
        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"
        preprint = Preprint(
            url="https://arxiv.org/abs/1706.03762", source="arxiv",
            pdf_url="p", identifier="1706.03762", title="A paper",
        )
        state = {"decision": "major", "manuscript_title": "A paper",
                 "total_cost": 1.0, "errors": [], "reports": []}

        paper = Path(tmp) / "2026" / "a-paper"
        # Second attempt, still round 1, a re-review, not a revision.
        write_bundle(preprint, state, run_dir, paper / "v1" / "r1", "1", "me")
        write_bundle(preprint, state, run_dir, paper / "v1" / "r2", "1", "me")
        v2 = json.loads((paper / "v1" / "r2" / "provenance.json").read_text())
        assert v2["round"] == 1, f"v2 must not imply round 2: {v2['round']}"

        # Now a genuine round 2.
        write_bundle(
            preprint, state, run_dir, paper / "v2" / "r1", "1", "me", None,
            {"round": 2, "prior_decision": "major", "kind": "revision",
             "prior_required_revisions": 7},
        )
        v3 = provenance_of(paper / "v2" / "r1")
        assert v3["round"] == 2, "explicit round not recorded"
        # The panel reads every round cold, so what the previous round decided
        # and how many revisions it required is the only continuity a reader
        # has, and the page can only state it because these fields survive
        # into the record.
        assert v3["revision"]["prior_decision"] == "major"
        assert v3["revision"]["prior_required_revisions"] == 7,\
            "the previous round's asks must reach the record"


def check_latest_editorial_attempt_is_the_revision_baseline() -> None:
    """A new manuscript draft follows the latest eligible editorial review."""
    with tempfile.TemporaryDirectory() as tmp:
        paper = Path(tmp) / "2026" / "a-paper"

        def attempt(number: int, eligible: bool) -> Path:
            bundle = paper / "v1" / f"r{number}"
            bundle.mkdir(parents=True)
            (bundle / "provenance.json").write_text(json.dumps({
                "models": {"reviewer": {"model": "graded"}} if eligible else {},
                "review": {
                    "baseline_eligible": eligible,
                    "lifecycle": "active",
                },
            }))
            (bundle / "round.json").write_text(json.dumps({"round": 1}))
            return bundle

        first = attempt(1, True)
        latest_editorial = attempt(2, True)
        experiment = attempt(3, False)

        plan = plan_review(paper, 2, replace=False)
        assert plan.prior == latest_editorial
        assert plan.prior != first
        assert plan.prior != experiment
        assert plan.dest == paper / "v2" / "r1"


def check_staleness_scan_finds_bundles() -> None:
    """The corpus scanner has to find the layout the bundler actually writes.

    It did not, for a while: the glob stopped one directory short of ``vN/``,
    so once reviews became versioned it matched nothing and reported "no
    published reviews to check" every month against a corpus that was growing.
    A checker that finds zero reviews looks exactly like a corpus with nothing
    wrong, which is why this is asserted rather than eyeballed.
    """
    import check_updates

    with tempfile.TemporaryDirectory() as tmp:
        reviews = Path(tmp) / "reviews"
        for slug, versions in (("paper-a", 2), ("paper-b", 1)):
            for v in range(1, versions + 1):
                bundle = reviews / "2026" / slug / f"v{v}"
                bundle.mkdir(parents=True)
                (bundle / "provenance.json").write_text(json.dumps({
                    "preprint": {
                        "url": f"https://arxiv.org/abs/{slug}",
                        "version": str(v),
                        "pdf_sha256": str(v) * 64,
                        "source": "arxiv",
                    }
                }))

        original = check_updates.REVIEWS
        check_updates.REVIEWS = reviews
        try:
            found = check_updates.published()
        finally:
            check_updates.REVIEWS = original

    names = sorted(b.relative_to(reviews).as_posix() for b, _ in found)
    assert names == ["2026/paper-a/v2", "2026/paper-b/v1"], names


def check_restamping_is_not_staleness() -> None:
    """bioRxiv re-stamps every PDF it serves, so its hash alone proves nothing.

    Verified against the live server: two fetches of one bioRxiv URL seconds
    apart return different hashes at identical length, while arXiv returns the
    same bytes. Counting that as staleness would file a report every month
    naming papers that had not changed, and a monthly alarm that is always
    wrong is one an editor correctly learns to ignore.
    """
    import check_updates
    from fetch_preprint import Preprint

    reviewed = "a" * 64
    base = {
        "url": "https://www.biorxiv.org/content/10.1101/2020.01.01.000001v1",
        "version": "1",
        "pdf_sha256": reviewed,
        "pdf_bytes": 1000,
        "source": "biorxiv",
    }

    def run(source: str, now_sha: str, now_bytes: int) -> dict:
        pre = dict(base, source=source)
        original_resolve = check_updates.resolve
        original_fp = check_updates.fingerprint
        check_updates.resolve = lambda url: Preprint(
            url=url, source=source, pdf_url="p", version="1"
        )
        check_updates.fingerprint = lambda pp: (now_sha, now_bytes)
        try:
            bundle = check_updates.REVIEWS / "2026" / "x" / "v1"
            return check_updates.check_one(bundle, {"preprint": pre})
        finally:
            check_updates.resolve = original_resolve
            check_updates.fingerprint = original_fp

    # Same length, different bytes: the date stamp. Not stale.
    r = run("biorxiv", "b" * 64, 1000)
    assert r["status"] == "restamped", r
    assert r["status"] not in check_updates.STALE_STATUSES, "a re-stamp is not staleness"

    # Length moved: the content was actually edited. Stale.
    r = run("biorxiv", "b" * 64, 1200)
    assert r["status"] == "bytes-differ", r
    assert r["status"] in check_updates.STALE_STATUSES

    # arXiv serves a fixed file, so any hash change is a real replacement.
    r = run("arxiv", "b" * 64, 1000)
    assert r["status"] == "bytes-differ",\
        "arXiv is byte-stable. A hash change there is not a re-stamp"

    # Unchanged bytes stay unchanged whatever the server.
    r = run("biorxiv", reviewed, 1000)
    assert r["status"] == "unchanged", r


def check_slug_uniqueness() -> None:
    """Titles truncate at 60 chars, so they cannot be the whole directory name."""
    long_a = "Deep learning approaches for the prediction of protein structure from sequence"
    long_b = "Deep learning approaches for the prediction of protein folding kinetics"
    a = Preprint(url="", source="arxiv", pdf_url="", identifier="2401.00001")
    b = Preprint(url="", source="arxiv", pdf_url="", identifier="2401.00002")
    assert slugify(long_a) == slugify(long_b), "fixture no longer exercises truncation"
    assert paper_slug(a, long_a) != paper_slug(b, long_b), "distinct papers still collide"


def check_rerun_refuses_a_moved_draft() -> None:
    """A rerun holds the manuscript fixed and varies the pipeline.

    So the guard is the whole feature. If the draft moved underneath, the
    comparison silently measures a manuscript change and a pipeline change at
    once, and produces a bundle that looks exactly like evidence about the
    pipeline. That is worse than failing, because someone would read it.

    It compares the converted TEXT, not the PDF. Measured on the first real
    rerun: three downloads of one pinned bioRxiv URL over ten hours gave three
    different file checksums at an identical 1,689,095 bytes, while the
    converted text was byte-identical every time. A file-hash guard refuses
    every bioRxiv rerun, including the correct ones. This one did.
    """
    from run_review import draft_matches

    same, other = "c" * 64, "d" * 64

    ok, _ = draft_matches({"text_sha256": same}, {"text_sha256": same})
    assert ok, "identical converted text must rerun"

    ok, msg = draft_matches({"text_sha256": same}, {"text_sha256": other})
    assert not ok, "changed text must stop the run"
    assert "not the manuscript" in msg

    # The case that matters: a repackaged PDF whose text is unchanged. This is
    # the common case for bioRxiv, not an edge case.
    ok, _ = draft_matches(
        {"text_sha256": same, "chars": 86988},
        {"text_sha256": same, "chars": 86988},
    )
    assert ok, "a restamped PDF with identical text must rerun"

    # Bundles predating the fingerprint fall back to length, and still run.
    ok, msg = draft_matches({"chars": 86988}, {"chars": 86988, "text_sha256": same})
    assert ok and "not proof" in msg, "a length match must not claim to be proof"
    ok, _ = draft_matches({"chars": 86988}, {"chars": 12, "text_sha256": same})
    assert not ok, "a different length must stop the run"

    ok, msg = draft_matches({}, {"text_sha256": same})
    assert ok and "cannot show" in msg,\
        "a bundle recording nothing must rerun, and must say it cannot check"
