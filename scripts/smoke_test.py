"""Render a synthetic review bundle and assert it comes out well-formed.

Hermetic: no network, no API key, no model call. Guards the failure mode that
matters most here — a review bundle whose generated frontmatter is malformed
(an unescaped quote in a title, a missing field) breaks the site build *after*
the review PR is merged, when it's least convenient.

    python scripts/smoke_test.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from build_index import read_frontmatter  # noqa: E402
from fetch_preprint import Preprint, resolve  # noqa: E402
from run_review import (  # noqa: E402
    BUNDLE_ORDER,
    next_version,
    paper_slug,
    slugify,
    write_bundle,
    write_paper_page,
)

# Titles that have historically broken naive frontmatter generation.
NASTY_TITLES = [
    'A Study of "Attention": Colons, Quotes & Ampersands',
    "Backslashes \\ and [brackets] in a title",
    "Ünïcödé, emoji 🧬, and a | pipe",
]


def build_fixture(title: str, dest: Path) -> None:
    preprint = Preprint(
        url="https://arxiv.org/abs/0000.00000",
        source="arxiv",
        pdf_url="https://arxiv.org/pdf/0000.00000",
        identifier="0000.00000",
        doi="10.48550/arXiv.0000.00000",
        title=title,
        authors=["Ada Lovelace", "Alan Turing"],
        abstract='An abstract with a colon: quotes "like this" and a | pipe.',
        published="2024-01-01",
    )
    run_dir = Path(tempfile.mkdtemp())
    for name, _ in BUNDLE_ORDER:
        (run_dir / name).write_text(f"# {name}\n\nfixture body\n")
    for reviewer in ("methodology", "novelty", "clarity", "rigor"):
        (run_dir / f"review_{reviewer}.md").write_text(f"# {reviewer}\n\nfixture\n")
    # The audit lane writes these; an earlier bundler dropped them silently.
    for auditor in ("methods_completeness", "citation_integrity"):
        (run_dir / f"audit_{auditor}.md").write_text(f"# {auditor}\n\nfixture\n")

    os.environ["REVIEW_MODELS"] = json.dumps(
        {"reviewer": {"model": "claude-haiku-4-5"}, "synthesis": {"model": "claude-opus-5"}}
    )
    os.environ["REVIEW_AGENT_MODELS"] = "{}"
    state = {
        "decision": "major",
        "manuscript_title": title,
        "total_cost": 1.23,
        "errors": [],
        "reports": [
            {"reviewer": r, "score": s, "confidence": 3}
            for r, s in [("methodology", 3), ("novelty", 4), ("clarity", 2), ("rigor", 3)]
        ],
    }
    write_bundle(preprint, state, run_dir, dest, "1", "octocat")


def check(title: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "bundle"
        build_fixture(title, dest)

        landing = dest / "index.md"
        assert landing.exists(), "no index.md written"

        meta = read_frontmatter(landing)
        assert meta is not None, f"frontmatter did not parse for title {title!r}"
        assert meta["title"] == title, f"title mangled: {meta['title']!r} != {title!r}"
        assert meta["decision"] == "major", f"decision lost: {meta.get('decision')!r}"
        assert meta["authors"] == ["Ada Lovelace", "Alan Turing"], "authors mangled"
        # The index puts a score on every card; it can only do that if the
        # landing page publishes one in its frontmatter.
        assert meta["mean_score"] == 3.0, f"mean_score missing: {meta.get('mean_score')!r}"

        for name, _ in BUNDLE_ORDER:
            assert (dest / name).exists(), f"missing bundle file {name}"
        assert (dest / "provenance.json").exists(), "missing provenance.json"
        assert len(list(dest.glob("review_*.md"))) == 4, "specialist reports not copied"
        assert len(list(dest.glob("audit_*.md"))) == 2, "audit reports not copied"

        landing = (dest / "index.md").read_text()
        assert "Editorial audits" in landing, "audits not linked from the landing page"
        assert "audit_citation_integrity.md" in landing
        # Model tags must be disclosed — the panel and the chair differ.
        assert "specialist reviewers" in landing, "model tags not rendered"
        assert "claude-haiku-4-5" in landing

        assert slugify(title), f"title produced an empty slug: {title!r}"


def check_desk_reject() -> None:
    """A desk reject produces almost none of the usual bundle. Render anyway.

    This is the shape that breaks a bundler written against the happy path:
    no reports, no mean score, and decision_letter / desk_screen / integrity
    all set to the same body by the pipeline.
    """
    body = "# Submission integrity\n\n**Outcome:** concealed instructions found.\n"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name in ("decision_letter.md", "desk_screen.md", "integrity.md"):
            (run_dir / name).write_text(body)
        (run_dir / "summary.md").write_text("# Summary\n\nDesk rejected.\n")

        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"
        os.environ["REVIEW_SCREENS"] = json.dumps(
            {"injection_screen": True, "injection_screen_action": "reject",
             "desk_screen_mode": "gate"}
        )
        preprint = Preprint(
            url="https://arxiv.org/abs/0000.00001",
            source="arxiv",
            pdf_url="https://arxiv.org/pdf/0000.00001",
            identifier="0000.00001",
            title="A manuscript with a concealed payload",
        )
        state = {
            "decision": "reject",
            "desk_rejected": True,
            "manuscript_title": preprint.title,
            "total_cost": 0.0,
            "errors": [],
            "reports": [],  # no panel ran
        }
        dest = Path(tmp) / "bundle"
        write_bundle(preprint, state, run_dir, dest, "7", "octocat", {"desk_screen": 0.0})

        meta = read_frontmatter(dest / "index.md")
        assert meta is not None, "desk-reject frontmatter did not parse"
        assert meta["decision"] == "reject"
        assert meta.get("desk_rejected") is True, "desk_rejected missing from frontmatter"

        prov = json.loads((dest / "provenance.json").read_text())
        assert prov["desk_rejected"] is True, "desk_rejected not recorded in provenance"
        assert prov["mean_score"] is None, "a desk reject has no panel to score"
        assert prov["screens"]["desk_screen_mode"] == "gate", "screen config not recorded"

        landing = (dest / "index.md").read_text()
        assert "ins-verdict--desk" in landing, "no desk-reject chip on the landing page"
        assert "Rejected at the desk" in landing, "landing page doesn't say what happened"
        assert "Panel recommendation" not in landing, "claims a panel that never convened"
        # The three identical documents must be listed once, not three times.
        assert landing.count("(integrity.md)") + landing.count(
            "(decision_letter.md)"
        ) + landing.count("(desk_screen.md)") == 1, "duplicate bodies listed separately"
        assert (dest / "integrity.md").exists(), "integrity.md not copied into the bundle"


def check_versioning() -> None:
    """A re-review must never overwrite the review it supersedes.

    The flat layout silently replaced the earlier bundle *and* left its
    specialist reports behind, so a reader saw v1 reports filed under v2's
    verdict. Both halves are asserted here.
    """
    with tempfile.TemporaryDirectory() as tmp:
        paper = Path(tmp) / "2026" / "a-paper"

        def review(mver: str, decision: str, reviewers: tuple[str, ...]) -> int:
            run_dir = Path(tempfile.mkdtemp())
            for name, _ in BUNDLE_ORDER:
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
            v = next_version(paper)
            write_bundle(
                preprint,
                {"decision": decision, "manuscript_title": "A paper",
                 "total_cost": 1.0, "errors": [], "reports": []},
                run_dir, paper / f"v{v}", "1", "octocat",
            )
            write_paper_page(paper)
            return v

        assert review("1", "reject", ("methodology", "novelty", "ethics")) == 1
        assert review("2", "accept", ("methodology",)) == 2, "re-review did not bump"

        v1 = json.loads((paper / "v1" / "provenance.json").read_text())
        v2 = json.loads((paper / "v2" / "provenance.json").read_text())
        assert v1["decision"] == "reject", "v1 verdict was overwritten by the re-review"
        assert v2["decision"] == "accept", "v2 verdict not recorded"
        assert v1["preprint"]["version"] == "1"
        assert v2["preprint"]["version"] == "2"

        bled = sorted(p.name for p in (paper / "v2").glob("review_*.md"))
        assert bled == ["review_methodology.md"], f"v1 reports bled into v2: {bled}"

        history = (paper / "index.md").read_text()
        assert "[v1](v1/index.md)" in history, "history missing v1"
        assert "[v2](v2/index.md)" in history, "history missing v2"
        meta = read_frontmatter(paper / "index.md")
        assert meta["review_count"] == 2, "paper page miscounts reviews"
        assert meta["decision"] == "accept", "paper page should show the latest verdict"


def check_slug_uniqueness() -> None:
    """Titles truncate at 60 chars, so they cannot be the whole directory name."""
    long_a = "Deep learning approaches for the prediction of protein structure from sequence"
    long_b = "Deep learning approaches for the prediction of protein folding kinetics"
    a = Preprint(url="", source="arxiv", pdf_url="", identifier="2401.00001")
    b = Preprint(url="", source="arxiv", pdf_url="", identifier="2401.00002")
    assert slugify(long_a) == slugify(long_b), "fixture no longer exercises truncation"
    assert paper_slug(a, long_a) != paper_slug(b, long_b), "distinct papers still collide"


def check_rejected_sources() -> None:
    """Only the three preprint servers are reviewable."""
    for ok in (
        "https://arxiv.org/abs/1706.03762",
        "https://www.biorxiv.org/content/10.64898/2026.04.28.721232v1",
        "https://www.medrxiv.org/content/10.1101/2020.03.24.20042937v1",
    ):
        assert resolve(ok).identifier, f"should resolve: {ok}"
    for bad in ("https://example.com/paper.pdf", "https://example.com/page"):
        try:
            resolve(bad)
        except ValueError:
            continue
        raise AssertionError(f"should have been rejected: {bad}")


def main() -> int:
    for title in NASTY_TITLES:
        check(title)
        print(f"ok  {title}")

    check_desk_reject()
    print("ok  desk reject (no panel, deduped bodies)")
    check_versioning()
    print("ok  re-review adds v2 without touching v1")
    check_slug_uniqueness()
    print("ok  distinct papers get distinct directories")
    check_rejected_sources()
    print("ok  only arXiv / bioRxiv / medRxiv accepted")

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture(s) rendered cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
