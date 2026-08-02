"""Render a synthetic review bundle and assert it comes out well-formed.

Hermetic: no network, no API key, no model call. Guards the failure mode that
matters most here — a review bundle whose generated frontmatter is malformed
(an unescaped quote in a title, a missing field) breaks the site build *after*
the review PR is merged, when it's least convenient.

    python scripts/smoke_test.py
"""

from __future__ import annotations

import hashlib
import json
import os
import re
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

        # A citation is only useful if it compiles and points somewhere real.
        assert "## Cite this review" in landing, "no citation block"
        assert "@misc{insilico-" in landing, "no BibTeX entry"
        assert "author       = {{In Silico}}," in landing, "corporate author not braced"
        bib = landing.split("```bibtex", 1)[1].split("```", 1)[0]
        assert bib.count("{") == bib.count("}"), f"unbalanced braces in BibTeX:\n{bib}"
        for raw in ("&", "%", "$", "#", "_"):
            # Every LaTeX special in the entry must be backslash-escaped.
            for i, ch in enumerate(bib):
                if ch == raw:
                    assert i and bib[i - 1] == "\\", f"unescaped {raw!r} in BibTeX"


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


def check_baseline_restoration() -> None:
    """A revision round must never present a missing diff as a real one.

    Restoration runs on a CI runner whose ingest cache is empty, so the
    failure path is the *common* path, not the edge case. Each way it can
    fail has to come back as restored=False with a reason — a silent no-diff
    round is indistinguishable on the page from one that actually compared
    the drafts.
    """
    import run_review

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        work.mkdir()
        prior = Path(tmp) / "v1"
        prior.mkdir()

        # No provenance at all.
        st = run_review.restore_prior_draft(prior, work, {})
        assert not st["restored"] and "provenance" in st["reason"], st

        # Provenance with no PDF URL — reviews from before fingerprinting.
        (prior / "provenance.json").write_text(json.dumps({"preprint": {}}))
        st = run_review.restore_prior_draft(prior, work, {})
        assert not st["restored"] and "no PDF URL" in st["reason"], st

        # The file at the recorded URL no longer hashes to what we reviewed.
        # This one matters most: diffing against it would produce a confident
        # delta over the wrong baseline, which is worse than no delta at all.
        payload = b"%PDF-1.4 not the reviewed bytes"
        (prior / "provenance.json").write_text(json.dumps({
            "round": 1,
            "preprint": {
                "pdf_url": "https://example.org/v1.pdf",
                "pdf_sha256": "0" * 64,
            },
        }))
        original_get = run_review._get
        run_review._get = lambda url: payload
        try:
            st = run_review.restore_prior_draft(prior, work, {})
        finally:
            run_review._get = original_get
        assert not st["restored"], "a hash mismatch must not be a usable baseline"
        assert "no longer matches" in st["reason"], st["reason"]
        assert hashlib.sha256(payload).hexdigest()[:12] in st["reason"], \
            "the reason should name the hash actually fetched"

        # A fetch failure degrades, it does not raise.
        def boom(url):
            raise OSError("network is unreachable")

        run_review._get = boom
        try:
            st = run_review.restore_prior_draft(prior, work, {})
        finally:
            run_review._get = original_get
        assert not st["restored"] and "re-fetch" in st["reason"], st


def check_round_is_not_version() -> None:
    """The bundle's vN and the review round are different numbers.

    Re-running a review of the same manuscript under changed criteria makes a
    new bundle at round 1. Only a review of a revised draft advances the
    round. Reading one off the other would mislabel both.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name, _ in BUNDLE_ORDER:
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
        # Second bundle, still round 1 — a re-review, not a revision.
        write_bundle(preprint, state, run_dir, paper / "v1", "1", "me")
        write_bundle(preprint, state, run_dir, paper / "v2", "1", "me")
        v2 = json.loads((paper / "v2" / "provenance.json").read_text())
        assert v2["round"] == 1, f"v2 must not imply round 2: {v2['round']}"

        # Now a genuine round 2.
        write_bundle(
            preprint, state, run_dir, paper / "v3", "1", "me", None,
            {"round": 2, "prior_decision": "major",
             "baseline": {"restored": False, "reason": "cache was empty"}},
        )
        v3 = json.loads((paper / "v3" / "provenance.json").read_text())
        assert v3["round"] == 2, "explicit round not recorded"
        landing = (paper / "v3" / "index.md").read_text()
        assert "Revision round 2" in landing, "round not stated on the page"
        assert "No draft comparison" in landing, \
            "an unverified baseline must be disclosed on the page"
        assert "cache was empty" in landing, "the reason should be given"

        write_paper_page(paper)
        history = (paper / "index.md").read_text()
        assert "How it moved" in history, "no revision arc on the paper page"
        assert "2 ⚠" in history, "unverified round not flagged in the history"


def check_correction() -> None:
    """A correction is not a revision, and the pages must not conflate them.

    It leaves the round number alone (rounds count manuscript revisions), says
    plainly that the manuscript is unchanged, and publishes the authors'
    response verbatim — GitHub comments are editable, so a link would let the
    record drift out from under the review that answered it.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name, _ in BUNDLE_ORDER:
            (run_dir / name).write_text("x")
        statement = Path(tmp) / "response.md"
        statement.write_text("Effect sizes are in Table 2, not omitted.\n")

        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"
        preprint = Preprint(
            url="https://arxiv.org/abs/1706.03762", source="arxiv",
            pdf_url="p", identifier="1706.03762", title="A paper", version="1",
        )
        state = {"decision": "minor", "manuscript_title": "A paper",
                 "total_cost": 0.3, "errors": [], "reports": []}

        paper = Path(tmp) / "2026" / "a-paper"
        write_bundle(preprint, state, run_dir, paper / "v1", "1", "me")
        write_bundle(
            preprint, state, run_dir, paper / "v2", "1", "me", None,
            {"round": 1, "kind": "correction", "prior_decision": "major",
             "only_reviewers": ["methodology"],
             "statement_path": str(statement),
             "statement_source": "https://github.com/x/y/issues/3#issuecomment-1",
             "baseline": {"restored": False, "reason": "", "n/a": True}},
        )

        prov = json.loads((paper / "v2" / "provenance.json").read_text())
        assert prov["round"] == 1, "a correction must not advance the round"
        assert prov["revision"]["kind"] == "correction"

        landing = (paper / "v2" / "index.md").read_text()
        assert "manuscript is\n    unchanged" in landing or \
               "manuscript is" in landing, "must say the manuscript is unchanged"
        assert "does not advance the" in landing, "must say the round is unchanged"
        assert "methodology" in landing, "must name which reviewers re-ran"
        assert "No draft comparison" not in landing, \
            "a correction has nothing to compare; absence is not a defect"

        # The response must be published, not linked.
        assert (paper / "v2" / "author_response.md").exists(), \
            "the authors' response was not snapshotted into the bundle"
        assert "Table 2" in (paper / "v2" / "author_response.md").read_text()

        write_paper_page(paper)
        history = (paper / "index.md").read_text()
        assert "1 (corrected)" in history, "history must distinguish a correction"


def check_metadata_is_escaped() -> None:
    """Author-written metadata must not become HTML on the published page.

    Title, abstract and author names come from the preprint server, so the
    authors wrote them — and markdown renders inline HTML. Before this was
    escaped, a preprint posted with `<script>` in its abstract was stored XSS
    on every reader's browser, needing no model to be fooled and no editor to
    be careless.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name, _ in BUNDLE_ORDER:
            (run_dir / name).write_text("x")
        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"

        preprint = Preprint(
            url="https://arxiv.org/abs/1706.03762", source="arxiv",
            pdf_url="p", identifier="1706.03762",
            title="Title with <script>alert(1)</script>",
            authors=["A <img src=x onerror=alert(1)>", "B | Pipe"],
            abstract="Abstract <script>fetch('https://evil.example')</script> end.",
            doi="10.0/<b>x</b>",
        )
        dest = Path(tmp) / "v1"
        write_bundle(
            preprint,
            {"decision": "minor", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": []},
            run_dir, dest, "1", "octocat",
        )
        page = (dest / "index.md").read_text()

        # Layer 2: the rendered body. Frontmatter and fenced code are excluded
        # because neither becomes HTML — the body is what markdown renders.
        body = page.split("---", 2)[2]
        outside_fences = "".join(body.split("```")[::2])
        for payload in ("<script>", "<img src=x", "<b>"):
            assert payload not in outside_fences, \
                f"unescaped {payload!r} would render as HTML"
        assert "&lt;script&gt;" in outside_fences, "escaping should preserve the text"

        # A pipe in an author name must not break the metadata table: it has
        # to be backslash-escaped, leaving only the three structural pipes.
        author_row = [ln for ln in page.splitlines() if ln.startswith("| Authors")][0]
        structural = len(re.findall(r"(?<!\\)\|", author_row))
        assert structural == 3, f"pipe broke the table ({structural}): {author_row}"
        assert r"\|" in author_row, "the author's pipe was not escaped"

        meta = read_frontmatter(dest / "index.md")
        assert meta is not None, "frontmatter must still parse"


def check_metadata_is_sanitised_at_ingestion() -> None:
    """Layer 1, and the one that actually closes the hole.

    MkDocs Material writes the frontmatter title into <title> and the header
    bar without escaping it, so escaping only at our own render sites leaves
    the title exploitable. Metadata is therefore stripped of tags where it
    enters — one place, rather than every place it is later printed.
    """
    from fetch_preprint import _clean

    assert _clean("Cool paper <script>alert(1)</script>") == "Cool paper alert(1)"
    assert _clean("A <img src=x onerror=alert(1)>") == "A"
    assert _clean("</title><script>x</script>") == "x"
    # Legitimate text survives, including a lone comparison operator.
    assert _clean("Growth  when  x < y") == "Growth when x < y"
    assert _clean("Effects of TNF-α on  cells") == "Effects of TNF-α on cells"


def check_url_is_canonical() -> None:
    """The stored URL is rebuilt from the match, never echoed from input.

    The source patterns are searched rather than anchored, so a string like
    `javascript:alert(1)#arxiv.org/abs/1706.03762` matches on its tail — and
    echoing the input back would publish it as a clickable link.
    """
    hostile = "javascript:alert(document.domain)#arxiv.org/abs/1706.03762"
    p = resolve(hostile)
    assert p.url == "https://arxiv.org/abs/1706.03762", p.url
    assert "javascript:" not in p.url
    assert not p.pdf_url.startswith("javascript:")


def check_download_is_bounded() -> None:
    """An unbounded read is a memory bomb; a runner has a couple of GB."""
    import fetch_preprint

    assert fetch_preprint.MAX_DOWNLOAD_BYTES <= 100 * 1024 * 1024

    class _Resp:
        """Endless stream, as a hostile server would send."""
        def read(self, n=-1):
            return b"\x00" * (n if n and n > 0 else 65536)
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False

    real = fetch_preprint.urllib.request.urlopen
    fetch_preprint.urllib.request.urlopen = lambda *a, **k: _Resp()
    try:
        fetch_preprint._get("https://example.org/huge.pdf", max_bytes=1024)
    except ValueError as exc:
        assert "larger than" in str(exc), exc
    else:
        raise AssertionError("an endless response was read without limit")
    finally:
        fetch_preprint.urllib.request.urlopen = real


def check_statement_url_is_external() -> None:
    """A response-letter URL must not reach the runner's own network."""
    import run_review

    for bad, why in (
        ("http://example.org/x.md", "plain http"),
        ("https://127.0.0.1/x.md", "loopback"),
        ("https://169.254.169.254/latest/meta-data/", "cloud metadata"),
        ("https://10.0.0.5/x.md", "private range"),
    ):
        try:
            run_review._reject_internal_url(bad)
        except SystemExit:
            continue
        raise AssertionError(f"{why} was not rejected: {bad}")


def check_solicitation_is_labelled() -> None:
    """Whether the authors asked for the review has to be on the page.

    Anyone may submit any public preprint, which makes In Silico usable for
    scrutinising unexamined work and equally usable for attaching a permanent
    public criticism to a rival's paper. Publishing both identically would let
    the second hide inside the first.
    """
    from fetch_preprint import extract_authorship
    import run_review

    # Parsed from the submission form, which asks outright.
    assert extract_authorship(
        "### Are you an author of this paper?\n\nYes — I am an author\n"
    ) == "yes"
    assert extract_authorship(
        "### Are you an author of this paper?\n\nNo — I am not an author\n"
    ) == "no"
    assert extract_authorship("### Preprint URL\n\nhttps://x\n") == "", \
        "an absent field must not be read as either answer"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name, _ in BUNDLE_ORDER:
            (run_dir / name).write_text("x")
        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"
        preprint = Preprint(
            url="https://arxiv.org/abs/1706.03762", source="arxiv",
            pdf_url="p", identifier="1706.03762", title="A paper",
        )
        state = {"decision": "major", "manuscript_title": "A paper",
                 "total_cost": 1.0, "errors": [], "reports": []}

        pages = {}
        for claim in ("yes", "no", ""):
            dest = Path(tmp) / f"v-{claim or 'unset'}"
            write_bundle(preprint, state, run_dir, dest, "1", "someone",
                         submitter_is_author=claim)
            pages[claim] = (dest / "index.md").read_text()
            prov = json.loads((dest / "provenance.json").read_text())
            assert prov["submitter_is_author"] == claim, "claim not recorded"

        assert "did not request this review" in pages["no"], \
            "an unsolicited review must say so"
        assert "states they are **not** an author" in pages["no"]
        assert "did not request" not in pages["yes"], \
            "an author-requested review must not carry the warning"
        assert "Requested by an author" in pages["yes"]
        assert "Solicitation unrecorded" in pages[""], \
            "an unknown claim must be stated as unknown, not assumed"
        # The claim is unverifiable and the page has to admit it.
        assert "do not verify" in pages["yes"] or "states" in pages["yes"]


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
    check_baseline_restoration()
    print("ok  a missing revision baseline is never silent")
    check_round_is_not_version()
    print("ok  bundle version and review round stay distinct")
    check_correction()
    print("ok  a correction is not a revision")
    check_solicitation_is_labelled()
    print("ok  unsolicited reviews say so on the page")
    check_metadata_is_sanitised_at_ingestion()
    print("ok  metadata is stripped of tags where it enters")
    check_metadata_is_escaped()
    print("ok  and escaped again where it renders")
    check_url_is_canonical()
    print("ok  stored URLs are rebuilt, not echoed")
    check_download_is_bounded()
    print("ok  downloads are size-capped")
    check_statement_url_is_external()
    print("ok  response URLs cannot reach the runner's network")
    check_rejected_sources()
    print("ok  only arXiv / bioRxiv / medRxiv accepted")

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture(s) rendered cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
