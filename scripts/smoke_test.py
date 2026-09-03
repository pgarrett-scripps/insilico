"""Write a synthetic review bundle and assert it comes out well-formed.

Hermetic: no network, no API key, no model call.

What this guards is the *data contract* between the pipeline and the site.
run_review.py writes documents and provenance.json; the site reads them and
renders every page. So the failure that matters is a bundle the site cannot
read — a missing field, a score that never reaches provenance, reports that
bleed between versions — not the shape of any particular page. Page rendering
is checked by the site's own build, which CI runs on every PR and which fails
if any published bundle goes unrendered.

    python scripts/smoke_test.py
"""

from __future__ import annotations

import contextlib
import datetime as dt
import email.utils
import hashlib
import json
import os
import sys
import tempfile
import tomllib
import urllib.error
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))

REPO = Path(__file__).resolve().parent.parent

from fetch_preprint import Preprint, resolve  # noqa: E402
from manuscript_source import (  # noqa: E402
    html_to_markdown,
    jats_to_markdown,
    select_manuscript_source,
    validate_text,
)
from preview_submission import COMMENT_MARKER, build_preview  # noqa: E402
from run_review import (  # noqa: E402
    BUNDLE_FILES,
    CommandError,
    configuration_record,
    draft_number,
    paper_slug,
    plan_review,
    slugify,
    write_bundle,
)


def provenance_of(bundle: Path) -> dict:
    return json.loads((bundle / "provenance.json").read_text(encoding="utf-8"))


# Titles that have historically broken naive metadata handling.
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
    for name in BUNDLE_FILES:
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

        prov = provenance_of(dest)

        # Metadata has to survive verbatim. Every one of these titles broke a
        # previous encoding of this record at some point.
        assert prov["preprint"]["title"] == title, (
            f"title mangled: {prov['preprint']['title']!r} != {title!r}"
        )
        assert prov["decision"] == "major", f"decision lost: {prov.get('decision')!r}"
        assert prov["preprint"]["authors"] == ["Ada Lovelace", "Alan Turing"], "authors mangled"
        # The index puts a score on every card and the panel readout needs the
        # per-referee detail; both come from here and nowhere else.
        assert prov["mean_score"] == 3.0, f"mean_score missing: {prov.get('mean_score')!r}"
        assert len(prov["panel"]) == 4, "per-referee scores not recorded"
        assert {p["reviewer"] for p in prov["panel"]} == {
            "methodology", "novelty", "clarity", "rigor",
        }, "panel roster wrong"

        # Which model wrote which report is a disclosure, not a nicety.
        assert prov["models"]["reviewer"]["model"] == "claude-haiku-4-5"
        assert prov["models"]["synthesis"]["model"] == "claude-opus-5"
        assert prov["schema_version"] == 2
        assert prov["insilico"]["sha"]
        assert len(prov["configuration"]["sha256"]) == 64

        manifest = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["schema_version"] == 1
        assert manifest["files"]["provenance.json"] == hashlib.sha256(
            (dest / "provenance.json").read_bytes()
        ).hexdigest()

        for name in BUNDLE_FILES:
            assert (dest / name).exists(), f"missing bundle file {name}"
        assert len(list(dest.glob("review_*.md"))) == 4, "specialist reports not copied"
        assert len(list(dest.glob("audit_*.md"))) == 2, "audit reports not copied"

        assert slugify(title), f"title produced an empty slug: {title!r}"


def check_provenance_is_portable_and_secret_free() -> None:
    """Configuration hashes describe the run without leaking its machine."""
    record = configuration_record({
        "revision_of": str(REPO / "docs" / "reviews" / "paper" / "v1" / "r2"),
        "journals_dir": str(REPO / "journals"),
        "api_key": "do-not-publish",
        "models": {"reviewer": {"model": "safe", "token": "also-secret"}},
        "openai_base_url": "https://user:password@example.test/v1?api_key=secret",
        "output_dir": "/tmp/runtime-only",
    })
    resolved = record["resolved"]
    assert "revision_of" not in resolved
    assert "journals_dir" not in resolved
    assert "api_key" not in resolved
    assert "token" not in resolved["models"]["reviewer"]
    assert "output_dir" not in resolved
    assert resolved["openai_base_url"] == "https://example.test/v1"
    canonical = json.dumps(
        resolved,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    assert record["sha256"] == hashlib.sha256(canonical).hexdigest()


def check_published_artifacts_are_preserved() -> None:
    """Reviewer prose and metadata must survive publication byte for byte."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        exact = f"finding {chr(0x2014)} evidence{chr(59)} citation"
        for name in BUNDLE_FILES:
            (run_dir / name).write_text(exact, encoding="utf-8")
        preprint = Preprint(
            url="https://arxiv.org/abs/0000.00000",
            source="arxiv",
            pdf_url="https://arxiv.org/pdf/0000.00000",
            title=exact,
        )
        dest = Path(tmp) / "bundle"
        write_bundle(preprint, {"decision": "major"}, run_dir, dest, "1", "octocat")
        assert (dest / BUNDLE_FILES[0]).read_text(encoding="utf-8") == exact
        assert provenance_of(dest)["preprint"]["title"] == exact


def check_published_bundle_cannot_be_overwritten() -> None:
    """A second write to one record must fail before changing any artifact."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "v1" / "r1"
        build_fixture("First review", dest)
        before = (dest / "provenance.json").read_bytes()
        try:
            build_fixture("Second review", dest)
        except FileExistsError:
            pass
        else:
            raise AssertionError("an existing review bundle was overwritten")
        assert (dest / "provenance.json").read_bytes() == before


def check_unscorable_dimension_is_not_a_good_score() -> None:
    """A dimension that does not apply must leave the mean, not inflate it.

    A reviewer with nothing in its remit to judge used to be forced to invent
    a number, and reliably invented a generous one: on a qualitative interview
    study the data-analysis reviewer wrote that there were "no p-values,
    confidence intervals, effect sizes, sample-size calculations, or
    statistical claims to evaluate" and scored the paper 5/5 — the highest
    data-analysis score in the corpus. The pipeline now returns null there,
    and this asserts the record keeps it null and averages without it. Filling
    the gap in — with a zero, a midpoint, anything — reintroduces the bug in
    the other direction, so the null has to survive all the way to the page.
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
            pdf_url="p", identifier="1706.03762", title="A qualitative study",
        )
        reports = [
            {"reviewer": "methodology", "score": 3.0, "confidence": 4},
            {"reviewer": "clarity", "score": 4.0, "confidence": 5},
            {"reviewer": "data_analysis", "score": None, "confidence": 5,
             "not_applicable_reason": "No quantitative analysis in this manuscript."},
        ]
        dest = Path(tmp) / "v1"
        write_bundle(
            preprint,
            {"decision": "minor", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": reports},
            run_dir, dest, "1", "octocat",
        )
        prov = provenance_of(dest)

        by = {e["reviewer"]: e for e in prov["panel"]}
        assert by["data_analysis"]["score"] is None, \
            "an unscorable dimension must stay null in the record"
        assert by["data_analysis"]["not_applicable_reason"], \
            "the reason must travel with it, or the page cannot say why"

        # 3.0 and 4.0 average to 3.5. Counting the null as anything at all
        # moves this: as a 5 it would read 4.0, as a 0 it would read 2.33.
        assert prov["mean_score"] == 3.5, \
            f"the mean must be over scored referees only, got {prov['mean_score']}"
        assert prov["scored_count"] == 2, prov["scored_count"]
        assert prov["panel_size"] == 3, prov["panel_size"]
        assert prov["scored_count"] != prov["panel_size"], \
            "the page needs both numbers to say 'mean over 2 of 3'"

        # A panel where nobody could score has no mean — not a zero.
        allna = [dict(r, score=None) for r in reports]
        dest2 = Path(tmp) / "v2"
        write_bundle(
            preprint,
            {"decision": "reject", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": allna},
            run_dir, dest2, "1", "octocat",
        )
        prov2 = provenance_of(dest2)
        assert prov2["mean_score"] is None, "no scores means no mean, not zero"
        assert prov2["scored_count"] == 0


def check_manuscript_ingest_is_recorded() -> None:
    """However the manuscript was read, the record has to say so.

    The panel is handed a markdown rendering of the PDF, not the PDF, and
    under compression a quoted sentence is missing its articles and copulas.
    A reader checking a referee's quotation against the paper will not find it
    verbatim — so the record must name the tool and the compression level, or
    the mismatch reads as the referee having misquoted.

    The pipeline builds that record now; this script's job is to check it
    survives into provenance.json unaltered, and that the pages still render
    when it is absent — every review published before the record existed has
    no ingest field at all.
    """
    with tempfile.TemporaryDirectory() as tmp:
        preprint = Preprint(
            url="https://arxiv.org/abs/2401.00001", source="arxiv",
            pdf_url="https://arxiv.org/pdf/2401.00001v1",
            identifier="2401.00001", version="1", title="Ingest Fixture",
            authors=["A. Author"], abstract="x", published="2026-01-02",
        )
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        (run_dir / "summary.md").write_text("# Summary\n")
        (run_dir / "decision_letter.md").write_text("# Decision\n")

        record = {
            "format": "markdown",
            "tool": "rustypaper 9.9.9",
            "caveman": "light",
            "chars": 41234,
        }
        dest = Path(tmp) / "v1"
        write_bundle(
            preprint,
            {"decision": "minor", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": [], "ingest": record},
            run_dir, dest, "1", "octocat", ingest=record,
        )
        got = provenance_of(dest)["ingest"]
        assert got == record, f"the ingest record must travel verbatim, got {got}"
        assert got["caveman"] == "light", "the compression level must be on the record"
        assert "9.9.9" in got["tool"], "the converter version must be on the record"

        # "off" reaches the record as null rather than as the string "off",
        # so a page can test the field instead of parsing it.
        plain = dict(record, caveman=None)
        dest2 = Path(tmp) / "v2"
        write_bundle(
            preprint,
            {"decision": "minor", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": [], "ingest": plain},
            run_dir, dest2, "1", "octocat", ingest=plain,
        )
        assert provenance_of(dest2)["ingest"]["caveman"] is None

        # A review published before the record existed. The page has to say
        # "not recorded" rather than invent a tool it never used.
        dest3 = Path(tmp) / "v3"
        write_bundle(
            preprint,
            {"decision": "minor", "manuscript_title": preprint.title,
             "total_cost": 1.0, "errors": [], "reports": []},
            run_dir, dest3, "1", "octocat",
        )
        assert provenance_of(dest3)["ingest"] == {}, \
            "an unrecorded ingest must be empty, not a guess at what was used"


def check_desk_reject() -> None:
    """A desk reject produces almost none of the usual bundle. Render anyway.

    This is the shape that breaks a bundler written against the happy path:
    no reports, no mean score, and decision_letter / desk_screen both set to
    the same body by the pipeline.
    """
    body = "# Desk screen\n\n**Outcome:** out of scope for the venue.\n"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir()
        for name in ("decision_letter.md", "desk_screen.md"):
            (run_dir / name).write_text(body)
        (run_dir / "summary.md").write_text("# Summary\n\nDesk rejected.\n")

        os.environ["REVIEW_MODELS"] = "{}"
        os.environ["REVIEW_AGENT_MODELS"] = "{}"
        os.environ["REVIEW_SCREENS"] = json.dumps({"desk_screen_mode": "gate"})
        preprint = Preprint(
            url="https://arxiv.org/abs/0000.00001",
            source="arxiv",
            pdf_url="https://arxiv.org/pdf/0000.00001",
            identifier="0000.00001",
            title="A manuscript stopped at the desk",
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

        prov = provenance_of(dest)
        # A desk reject and a panel reject are both `decision: reject` but are
        # not the same editorial act. This flag is the only thing that tells
        # them apart, and every page keys off it.
        assert prov["desk_rejected"] is True, "desk_rejected not recorded in provenance"
        assert prov["decision"] == "reject"
        assert prov["mean_score"] is None, "a desk reject has no panel to score"
        assert prov["panel"] == [], "a desk reject convened no panel"
        assert prov["screens"]["desk_screen_mode"] == "gate", "screen config not recorded"

        # Both identical bodies are copied so a direct link resolves; the
        # site is what collapses them to one entry.
        for name in ("decision_letter.md", "desk_screen.md"):
            assert (dest / name).exists(), f"{name} not copied into the bundle"


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
        assert review("2", "accept", ("methodology",)) == 2, \
            "the folder must be named after the draft the archive served"

        # A draft we have not seen lands beside the others; one we have needs
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
        assert again.dest == paper / "v1" / "r2", \
            "--replace must create a second immutable review attempt"
        assert again.prior is None, \
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
        # has — and the page can only state it because these fields survive
        # into the record.
        assert v3["revision"]["prior_decision"] == "major"
        assert v3["revision"]["prior_required_revisions"] == 7, \
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


def check_site_never_injects_raw_html() -> None:
    """Layer 2: nothing in the site may hand untrusted metadata to the parser.

    Titles, abstracts and author names are written by the *authors*, and they
    reach every page. Astro escapes the value of a `{...}` expression, so the
    default is safe — but `set:html` opts out of exactly that, and one use of
    it on a title would put stored XSS on every reader's browser. It is easier
    to forbid the escape hatch outright than to audit each use of it, because
    the components that render author-supplied text are most of them.

    The one place raw markup is legitimately rendered is a bundle document,
    and that goes through Astro's markdown pipeline via <Content />, which is
    a different mechanism with its own sanitisation posture.
    """
    src = REPO / "src"
    offenders = []
    for path in sorted(src.rglob("*.astro")):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if "set:html" in line:
                offenders.append(f"{path.relative_to(REPO)}:{lineno}")
    assert not offenders, (
        "set:html bypasses Astro's escaping, and author-supplied metadata "
        "reaches these components: " + ", ".join(offenders)
    )


def check_metadata_is_sanitised_at_ingestion() -> None:
    """Layer 1, and the one that actually closes the hole.

    The title reaches many places — <title>, og:description, a card, a
    heading — and an escape that has to be remembered at each of them is one
    that will be forgotten at the eleventh. Metadata is therefore stripped of
    tags where it enters, which is one place.
    """
    from fetch_preprint import _clean

    assert _clean("Cool paper <script>alert(1)</script>") == "Cool paper alert(1)"
    assert _clean("A <img src=x onerror=alert(1)>") == "A"
    assert _clean("</title><script>x</script>") == "x"
    # Legitimate text survives, including a lone comparison operator.
    assert _clean("Growth  when  x < y") == "Growth when x < y"
    assert _clean("Effects of TNF-α on  cells") == "Effects of TNF-α on cells"


@contextlib.contextmanager
def offline():
    """Run a block with metadata lookups failing, as if there were no network.

    What the URL checks below actually assert is how a string is classified
    and canonicalised, which is pure parsing — but ``resolve`` also calls the
    arXiv and bioRxiv APIs to enrich the result. Letting those run would put a
    live dependency on someone else's uptime into a test suite whose whole
    claim is that it is hermetic, and CI would fail for reasons having nothing
    to do with the commit under test.

    Both resolvers already treat a metadata failure as a nicety they can do
    without, so failing the fetch exercises the real code path rather than
    stubbing it out.
    """
    import fetch_preprint

    def no_network(*a, **k):
        raise urllib.error.URLError("offline (smoke test)")

    original = fetch_preprint._get
    fetch_preprint._get = no_network
    try:
        yield
    finally:
        fetch_preprint._get = original


def check_url_is_canonical() -> None:
    """The stored URL is rebuilt from the match, never echoed from input.

    The source patterns are searched rather than anchored, so a string like
    `javascript:alert(1)#arxiv.org/abs/1706.03762` matches on its tail — and
    echoing the input back would publish it as a clickable link.
    """
    hostile = "javascript:alert(document.domain)#arxiv.org/abs/1706.03762"
    with offline():
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




def check_solicitation_is_labelled() -> None:
    """Whether the authors asked for the review has to be on the page.

    Anyone may submit any public preprint, which makes In Silico usable for
    scrutinising unexamined work and equally usable for attaching a permanent
    public criticism to a rival's paper. Publishing both identically would let
    the second hide inside the first.
    """
    from fetch_preprint import extract_authorship

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

        # All three answers must be distinguishable in the record, including
        # the empty one. The site renders a different notice for each, and
        # collapsing "not an author" into "unrecorded" would let an
        # unsolicited review pass for a requested one.
        for claim in ("yes", "no", ""):
            dest = Path(tmp) / f"v-{claim or 'unset'}"
            write_bundle(preprint, state, run_dir, dest, "1", "someone",
                         submitter_is_author=claim)
            prov = provenance_of(dest)
            assert prov["submitter_is_author"] == claim, \
                f"claim {claim!r} not recorded, got {prov['submitter_is_author']!r}"
            assert prov["submitter"] == "someone", "submitter not recorded"


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
    assert r["status"] == "bytes-differ", \
        "arXiv is byte-stable; a hash change there is not a re-stamp"

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


def check_rejected_sources() -> None:
    """Only the three preprint servers are reviewable."""
    with offline():
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


def check_link_forms_a_browser_produces() -> None:
    """The identifier must survive whatever the address bar hands over.

    Submitters paste what their browser shows, and bioRxiv's own page links
    end in `.full-text` and `.supplementary-material`. Matching the DOI by
    shape rather than by "everything up to the end of the string" is what
    makes these equivalent; anchoring to the end made a trailing slash fatal
    and quietly swallowed `.full-text` into the DOI itself — which then became
    the API query, the PDF URL and the published directory name.
    """
    doi = "10.1101/2020.03.24.20042937"
    forms = [
        f"https://www.medrxiv.org/content/{doi}v1",
        f"https://www.medrxiv.org/content/{doi}v1/",
        f"https://www.medrxiv.org/content/{doi}v1.full",
        f"https://www.medrxiv.org/content/{doi}v1.full.pdf",
        f"https://www.medrxiv.org/content/{doi}v1.full-text",
        f"https://www.medrxiv.org/content/{doi}v1.supplementary-material",
    ]
    with offline():
        for form in forms:
            p = resolve(form)
            assert p.identifier == doi, f"{form} -> {p.identifier!r}"
            assert p.source == "medrxiv", f"{form} -> {p.source}"
            assert p.version == "1", f"{form} -> version {p.version!r}"
            assert p.pdf_url == (
                f"https://www.medrxiv.org/content/{doi}v1.full.pdf"
            ), f"{form} -> {p.pdf_url}"

        # The legacy bare-serial DOI form still resolves.
        assert resolve("https://doi.org/10.1101/001834").identifier == "10.1101/001834"

        # A DOI from another registrar is still not a preprint — and neither
        # is a *journal* article sharing bioRxiv's prefix. 10.1101 belongs to
        # Cold Spring Harbor Press, who use it for Genome Research and
        # Learning & Memory as well as for bioRxiv, so the prefix alone does
        # not identify a preprint. Matching the DOI's shape is what separates
        # them; the previous open-ended pattern accepted `10.1101/gr.123456`
        # and would have published a review of a peer-reviewed paper as though
        # it were a preprint, pointing at a bioRxiv URL that does not exist.
        for bad in (
            "https://doi.org/10.1038/s41586-020-2649-2",
            "https://doi.org/10.5555/12345678",
            "https://doi.org/10.1101/gr.123456.111",
            "https://doi.org/10.1101/lm.049890.119",
        ):
            try:
                resolve(bad)
            except ValueError:
                continue
            raise AssertionError(f"not a preprint DOI, should be rejected: {bad}")


def check_metadata_fetch_retries_throttling() -> None:
    """A throttled metadata lookup must be retried, not silently swallowed.

    Both resolvers treat a metadata failure as survivable, on the reasoning
    that the PDF is what gets reviewed. That reasoning is wrong at the point
    it matters: arXiv answers 429 when called too quickly, the exception is
    caught, and the run continues to spend a full panel on a manuscript whose
    published review then carries no title, no authors and no DOI — a record
    that cannot be cited and cannot be found. Observed live, twice.

    So transient failures are retried, and permanent ones are not: asking
    again for something that 404s just wastes the backoff.
    """
    import fetch_preprint as fp

    calls = {"n": 0}
    sleeps = []
    real_once, real_sleep = fp._get_once, fp.time.sleep
    fp.time.sleep = lambda s: sleeps.append(s)

    def throttled_twice(url, max_bytes=None, opener=None):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)
        return b"<ok/>"

    fp._get_once = throttled_twice
    try:
        assert fp._get("https://example.org/api", retries=3) == b"<ok/>", \
            "a throttled lookup should succeed once the throttle lifts"
        assert calls["n"] == 3, f"expected 3 attempts, got {calls['n']}"
        assert sleeps and sleeps == sorted(sleeps), \
            f"backoff should grow between attempts, got {sleeps}"

        # A 404 is permanent. Retrying it only delays the error.
        calls["n"] = 0

        def missing(url, max_bytes=None, opener=None):
            calls["n"] += 1
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)

        fp._get_once = missing
        try:
            fp._get("https://example.org/gone", retries=3)
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
        else:
            raise AssertionError("a 404 should propagate")
        assert calls["n"] == 1, f"a 404 must not be retried, tried {calls['n']} times"
    finally:
        fp._get_once, fp.time.sleep = real_once, real_sleep


def check_a_rate_limit_is_waited_out_in_minutes() -> None:
    """A 429 and a 500 are both "later", on timescales two orders apart.

    The schedule used to be one exponential curve for both, topping out at 16
    seconds. bioRxiv throttled a repeated `.full.pdf` fetch and the run died on
    the download — before any model call, so nothing was billed, but also
    before any review existed. No rate limit lifts inside 28 seconds.

    So: a hiccup is still answered in seconds, a throttle in minutes, a server
    that names its own interval is taken at its word, and the total is bounded
    so a host refusing us all afternoon fails the run instead of eating the
    workflow's whole time budget to arrive at the same place.
    """
    import fetch_preprint as fp

    def err(code, headers=None):
        return urllib.error.HTTPError("https://x/y", code, "no", headers or {}, None)

    # A hiccup keeps the seconds-scale curve.
    assert [fp._retry_delay(err(500), n, 0) for n in (1, 2, 3)] == [4, 8, 16], \
        "a 5xx should still be retried in seconds"

    # A throttle does not.
    throttle = [fp._retry_delay(err(429), n, 0) for n in (1, 2, 3)]
    assert throttle == [30.0, 120.0, 300.0], f"429 backoff should be minutes, got {throttle}"

    # Retry-After wins over the schedule, in either legal form.
    assert fp._retry_delay(err(429, {"Retry-After": "45"}), 1, 0) == 45.0
    when = email.utils.format_datetime(
        dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=90)
    )
    dated = fp._retry_delay(err(429, {"Retry-After": when}), 1, 0)
    assert 80 <= dated <= 95, f"an HTTP-date Retry-After should resolve to ~90s, got {dated}"

    # ... but is not trusted past the budget, and nonsense falls back.
    assert fp._retry_delay(err(429, {"Retry-After": "9999"}), 1, 0) == fp.MAX_THROTTLE_WAIT_SECONDS
    assert fp._retry_delay(err(429, {"Retry-After": "soon"}), 1, 0) == 30.0

    # `Retry-After: 0` is what bioRxiv answers a second 429 with. Taken at its
    # word that is no backoff at all, which is what earned the throttle.
    assert fp._retry_delay(err(429, {"Retry-After": "0"}), 1, 0) == fp.MIN_THROTTLE_WAIT_SECONDS

    # Spent budget stops the retrying rather than extending it.
    assert fp._retry_delay(err(429), 2, fp.MAX_THROTTLE_WAIT_SECONDS) is None

    # End to end: a host that never relents costs exactly the budget.
    slept: list[float] = []
    real_once, real_sleep = fp._get_once, fp.time.sleep
    fp.time.sleep = lambda s: slept.append(s)

    def always_throttled(url, max_bytes=None, opener=None):
        raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)

    fp._get_once = always_throttled
    try:
        try:
            fp._get("https://www.biorxiv.org/x.pdf", retries=fp.METADATA_RETRIES)
        except urllib.error.HTTPError as exc:
            assert exc.code == 429
        else:
            raise AssertionError("a permanent throttle should surface, not hang")
        assert sum(slept) == fp.MAX_THROTTLE_WAIT_SECONDS, \
            f"should spend exactly the budget, spent {sum(slept)}"
    finally:
        fp._get_once, fp.time.sleep = real_once, real_sleep


def check_pdf_download_retries_a_flaky_server() -> None:
    """The PDF fetch is retried on the same terms as the metadata lookup.

    bioRxiv intermittently answers 500 on `.full.pdf` for a posting it served
    a minute earlier. Observed live: a dry run resolved and downloaded the same
    DOI that 500ed on the real run seconds later. Without a retry the whole
    review stops on a hiccup that clears by itself, and an editor re-runs the
    command by hand for no reason.

    The 500 case is what this pins. A 404 still fails on the first attempt,
    because bioRxiv answers 404 for a posting that is not yet indexed and no
    amount of asking again will index it.
    """
    import fetch_preprint as fp

    calls = {"n": 0}
    real_once, real_sleep = fp._get_once, fp.time.sleep
    fp.time.sleep = lambda s: None
    pdf = b"%PDF-1.7\n" + b"x" * 4096

    def flaky(url, max_bytes=None, opener=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise urllib.error.HTTPError(url, 500, "Internal Server Error", {}, None)
        return pdf

    fp._get_once = flaky
    try:
        pre = fp.Preprint(
            source="biorxiv", identifier="10.64898/2026.07.24.740542",
            url="https://www.biorxiv.org/content/10.64898/2026.07.24.740542v1",
            pdf_url="https://www.biorxiv.org/content/10.64898/2026.07.24.740542v1.full.pdf",
        )
        with tempfile.TemporaryDirectory() as tmp:
            dest = fp.download(pre, Path(tmp))
            assert dest.read_bytes().startswith(b"%PDF"), "should have written the PDF"
        assert calls["n"] == 2, f"expected one retry, made {calls['n']} attempts"
    finally:
        fp._get_once, fp.time.sleep = real_once, real_sleep


def check_command_parsing_is_strict() -> None:
    """`/review openrouter <model>` is parsed here, from untrusted text.

    An issue comment is the least trustworthy input this repo takes, and the
    model name it can carry ends up in a config value and in a published
    record. So the parser accepts known provider names and slugs matching a
    strict pattern, and refuses everything else with a message written for the
    editor who typed it. Nothing is sanitised into working.
    """
    from run_review import CommandError, parse_command

    ok = parse_command("/review openrouter nvidia/nemotron-3-ultra:free")
    assert ok == {"replace": False, "provider": "openrouter",
                  "model": "nvidia/nemotron-3-ultra:free"}, ok
    assert parse_command("/review")["provider"] is None, \
        "a bare /review must leave peerreview.toml in charge"
    assert parse_command("/review anthropic")["model"] is None

    # There is one verb. Whether a run is a first look or a new round is read
    # off which draft the archive serves, not declared by the editor, so
    # /revise survives only as muscle memory and does nothing extra.
    assert parse_command("/revise") == parse_command("/review")

    # A same-draft re-review must be requested explicitly. It creates a new
    # immutable attempt and is never inferred from a bare command.
    assert parse_command("/review replace")["replace"] is True
    assert parse_command("/review")["replace"] is False
    assert parse_command("/review replace openrouter x/y:free") == {
        "replace": True, "provider": "openrouter", "model": "x/y:free"}

    # Only the first line is a command; a comment may say more below it.
    assert parse_command("/review\nplease be thorough")["provider"] is None
    assert parse_command("just chatting")["replace"] is False

    for bad in (
        "/review openrouter",                    # free tier has no stable alias
        "/review groq foo/bar",                  # unknown provider
        "/review anthropic claude-opus-5",       # the split is the point
        "/review openrouter ../../etc/passwd",   # path
        "/review openrouter $(rm -rf /)",        # shell
        "/review openrouter no-vendor",          # not vendor/model
        "/review openrouter x/y:free extra",     # trailing input
    ):
        try:
            parse_command(bad)
        except CommandError:
            pass
        else:
            raise AssertionError(f"{bad!r} should have been refused")


def check_one_model_means_one_model() -> None:
    """Naming a model must clear the per-stage tables.

    resolve_model reads `raw.get("model") or config.get("reasoning_model")`, so
    the tag tables in peerreview.toml BEAT the global model. Setting only
    reasoning_model leaves every agent pointed at claude-haiku-4-5 and
    claude-opus-5 while claiming to run on the named model: it would review
    nothing, those slugs are not valid on OpenRouter, and the run bills someone
    for Claude or fails oddly. Verified against resolve_model directly before
    this was written.
    """
    import inspect

    import run_review

    src = inspect.getsource(run_review._run)
    block = src[src.index("if args.model:"):]
    block = block[: block.index("if args.debate_rounds")]
    code = "\n".join(
        line for line in block.splitlines() if not line.lstrip().startswith("#")
    )
    assert 'overrides["models"] = {}' in code, \
        "a named model must clear the tag table, or it reviews nothing"
    assert 'overrides["agent_models"] = {}' in code, \
        "a named model must clear the per-agent overrides too"


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
    assert ok and "cannot show" in msg, \
        "a bundle recording nothing must rerun, and must say it cannot check"


def check_rerun_does_not_inherit_the_prior_round() -> None:
    """A same-draft re-review must not be wired as a revision.

    Two properties, both load-bearing. It stays round 1, because nothing was
    revised. And `revision_of` never reaches the pipeline config, because that
    is what hands the editor the earlier round's decision, score and numbered
    required revisions as its reference point — a re-review that inherits the
    verdict it exists to test is not a test.

    `plan_review` enforces the second structurally: a re-review carries no
    prior, and only a prior sets `revision_of`. Asserted there as well as
    here, because the two could drift apart.
    """
    import inspect

    import run_review

    src = inspect.getsource(run_review._run)
    block = src[src.index("if plan.previous_attempt is not None:"):]
    block = block[: block.index("if prior_bundle is not None:")]
    # Comments stripped, or this matches the comment explaining the absence
    # rather than the absence. It did, the first time it ran.
    code = "\n".join(
        line for line in block.splitlines()
        if not line.lstrip().startswith("#")
    )
    assert '"round": 1' in code, "a same-draft re-review is round 1"
    assert '"kind": "rerun"' in code, "the page needs to know what this is"
    assert "revision_of" not in code, \
        "a same-draft re-review must not inherit the verdict it is testing"


def check_bare_doi_picks_the_right_server() -> None:
    """bioRxiv and medRxiv share both DOI prefixes, so a bare DOI names neither.

    Defaulting to bioRxiv publishes a medRxiv preprint labelled `source:
    biorxiv`, with every link and the PDF fetch pointed at a bioRxiv URL that
    does not exist. The servers are asked instead of guessed.
    """
    import fetch_preprint

    doi = "10.1101/2020.03.24.20042937"
    asked = []

    def fake_records(server: str, wanted: str) -> list[dict]:
        asked.append(server)
        # Only medRxiv holds it, which is the case the guess gets wrong.
        return [{"title": "T", "version": "2", "date": "2020-03-30",
                 "authors": "A" + chr(59) + " B", "abstract": "x",
                 "jatsxml": "/content/10.1101/example.source.xml"}] \
            if server == "medrxiv" else []

    original = fetch_preprint._rxiv_records
    fetch_preprint._rxiv_records = fake_records
    try:
        p = fetch_preprint.resolve(f"https://doi.org/{doi}")
    finally:
        fetch_preprint._rxiv_records = original

    assert asked == ["biorxiv", "medrxiv"], f"both servers should be tried: {asked}"
    assert p.source == "medrxiv", f"resolved to the wrong server: {p.source}"
    assert "medrxiv.org" in p.url, p.url
    assert "medrxiv.org" in p.pdf_url, p.pdf_url
    assert "medrxiv.org" in p.jats_url, p.jats_url
    assert "medrxiv.org" in p.html_url, p.html_url

    # A URL that *does* name its server is authoritative and must not be
    # second-guessed with an extra request.
    asked.clear()
    fetch_preprint._rxiv_records = fake_records
    try:
        p = fetch_preprint.resolve(f"https://www.biorxiv.org/content/{doi}v1")
    finally:
        fetch_preprint._rxiv_records = original
    assert asked == ["biorxiv"], f"a named server should not be probed twice: {asked}"
    assert p.source == "biorxiv"


def check_submission_preview() -> None:
    """Submission comments resolve metadata and recommend the safe command."""
    preprint = Preprint(
        url="https://arxiv.org/abs/2608.12345",
        source="arxiv",
        pdf_url="https://arxiv.org/pdf/2608.12345v2",
        identifier="2608.12345",
        doi="10.48550/arXiv.2608.12345",
        title="A [linked] title with a | table character by @reviewer",
        authors=["Ada Lovelace", "Alan Turing"],
        published="2026-08-30",
        version="2",
    )
    seen: list[str] = []

    def fake_resolve(url: str) -> Preprint:
        seen.append(url)
        return preprint

    with tempfile.TemporaryDirectory() as raw:
        reviews = Path(raw)
        body = """### Preprint link

https://arxiv.org/abs/2608.12345

### Are you an author of, or affiliated with, this paper?

Yes
"""
        preview = build_preview(body, resolver=fake_resolve, reviews_root=reviews)
        assert seen == ["https://arxiv.org/abs/2608.12345"]
        assert preview.startswith(COMMENT_MARKER)
        assert "A \\[linked\\] title with a \\| table character" in preview
        assert "@\u200breviewer" in preview
        assert "Ada Lovelace, Alan Turing" in preview
        assert "| Current draft | v2 |" in preview
        assert "Use `/review` to run the configured referee panel" in preview
        assert "`/review replace`" not in preview

        bundle = reviews / "2026" / "paper" / "v2"
        bundle.mkdir(parents=True)
        (bundle / "provenance.json").write_text(
            json.dumps({"preprint": preprint.to_dict()}), encoding="utf-8"
        )
        preview = build_preview(body, resolver=fake_resolve, reviews_root=reviews)
        assert "| Published In Silico reviews | v2 |" in preview
        assert "Use `/review replace` only" in preview

        preprint.version = "3"
        preview = build_preview(body, resolver=fake_resolve, reviews_root=reviews)
        assert "Earlier draft v2 has been reviewed" in preview
        assert "revision round for v3" in preview

    bad = build_preview("No link here", resolver=fake_resolve)
    assert "metadata could not be resolved" in bad
    assert "no URL found" in bad


def _full_text_fixture(preprint: Preprint) -> str:
    body = " ".join(
        [
            "Fibroblast cultures showed reproducible neurotrophin signaling "
            "after controlled treatment with matched controls and quantified "
            "replicates."
        ]
        * 90
    )
    return f"{preprint.title}\n\n{preprint.abstract}\n\n{body}"


def check_full_text_source_hierarchy() -> None:
    """Official structured text wins and damaged PDF text reaches OCR."""
    preprint = Preprint(
        url="https://www.biorxiv.org/content/10.1101/2026.01.01.123456v1",
        source="biorxiv",
        pdf_url="https://www.biorxiv.org/content/10.1101/2026.01.01.123456v1.full.pdf",
        identifier="10.1101/2026.01.01.123456",
        title="Fibroblast neurotrophin signaling after controlled treatment",
        abstract=(
            "We measure fibroblast neurotrophin signaling after controlled "
            "treatment using matched controls, quantified replicates, and "
            "independent validation across multiple biological conditions."
        ),
        jats_url="https://www.biorxiv.org/content/10.1101/2026.01.01.123456v1.full.xml",
        html_url="https://www.biorxiv.org/content/10.1101/2026.01.01.123456v1.full",
    )
    full_text = _full_text_fixture(preprint)
    body = full_text.split("\n\n", 2)[2]
    jats = (
        "<article><front><article-meta><title-group><article-title>"
        f"{preprint.title}</article-title></title-group><abstract><p>"
        f"{preprint.abstract}</p></abstract></article-meta></front><body>"
        f"<sec><title>Results</title><p>{body}</p></sec></body></article>"
    ).encode()
    rendered = jats_to_markdown(jats)
    assert f"# {preprint.title}\n\n## Abstract\n\n{preprint.abstract}" in rendered
    assert f"## Results\n\n{body}" in rendered
    assert "arthritis.## Abstract" not in rendered
    assert validate_text(rendered, preprint)["passed"]

    html = (
        "<html><body><nav>Skip this menu</nav><article>"
        f"<h1>{preprint.title}</h1><h2>Abstract</h2><p>{preprint.abstract}</p>"
        f"<h2>Results</h2><p>{body}</p></article></body></html>"
    ).encode()
    html_rendered = html_to_markdown(html)
    assert "Skip this menu" not in html_rendered
    assert validate_text(html_rendered, preprint)["passed"]

    broken_pdf = SimpleNamespace(
        text="7UHDWPHQW QHXURWURSKLQ VLJQDOLQJ" * 500,
        ingest={"tool": "test PDF converter"},
    )
    with tempfile.TemporaryDirectory() as raw:
        workdir = Path(raw)
        pdf = workdir / "paper.pdf"
        pdf.write_bytes(b"%PDF fixture")

        source = select_manuscript_source(
            preprint,
            pdf,
            workdir,
            {},
            fetcher=lambda url, **kwargs: jats,
            loader=lambda path, config: broken_pdf,
            ocr=lambda path, dest: full_text,
        )
        assert source.kind == "jats"

        def unavailable(url: str, **kwargs) -> bytes:
            raise urllib.error.URLError("not available")

        source = select_manuscript_source(
            preprint,
            pdf,
            workdir,
            {},
            fetcher=unavailable,
            loader=lambda path, config: broken_pdf,
            ocr=lambda path, dest: full_text,
        )
        assert source.kind == "ocr"
        assert [attempt["kind"] for attempt in source.attempts] == [
            "jats", "html", "pdf", "ocr",
        ]


def check_desk_screen_is_non_enforcing() -> None:
    config = tomllib.loads((REPO / "peerreview.toml").read_text(encoding="utf-8"))
    assert config["desk_screen_mode"] == "warm"


def main() -> int:
    for title in NASTY_TITLES:
        check(title)
        print(f"ok  {title}")

    check_unscorable_dimension_is_not_a_good_score()
    print("ok  a dimension that does not apply leaves the mean")
    check_manuscript_ingest_is_recorded()
    print("ok  how the manuscript was read is always recorded")
    check_desk_reject()
    print("ok  desk reject records no panel and keeps every body")
    check_provenance_is_portable_and_secret_free()
    print("ok  provenance is portable and excludes secrets")
    check_published_artifacts_are_preserved()
    print("ok  published reviewer output and metadata are preserved")
    check_published_bundle_cannot_be_overwritten()
    print("ok  published review bundles cannot be overwritten")
    check_versioning()
    print("ok  manuscript versions and immutable review attempts stay separate")
    check_slug_uniqueness()
    print("ok  distinct papers get distinct directories")
    check_staleness_scan_finds_bundles()
    print("ok  the staleness scan finds the layout we write")
    check_restamping_is_not_staleness()
    print("ok  a re-stamped bioRxiv PDF is not reported as stale")
    check_round_is_not_version()
    print("ok  bundle version and review round stay distinct")
    check_latest_editorial_attempt_is_the_revision_baseline()
    print("ok  a revision follows the latest eligible editorial review")
    check_solicitation_is_labelled()
    print("ok  the solicitation claim is recorded, all three ways")
    check_metadata_is_sanitised_at_ingestion()
    print("ok  metadata is stripped of tags where it enters")
    check_site_never_injects_raw_html()
    print("ok  the site never opts out of escaping")
    check_url_is_canonical()
    print("ok  stored URLs are rebuilt, not echoed")
    check_download_is_bounded()
    print("ok  downloads are size-capped")
    check_rejected_sources()
    print("ok  only arXiv / bioRxiv / medRxiv accepted")
    check_link_forms_a_browser_produces()
    print("ok  every browser link form yields the same identifier")
    check_bare_doi_picks_the_right_server()
    print("ok  a bare DOI resolves to the server that actually holds it")
    check_submission_preview()
    print("ok  submission issues get one safe editor command preview")
    check_full_text_source_hierarchy()
    print("ok  official full text is preferred and damaged PDF text falls back to OCR")
    check_desk_screen_is_non_enforcing()
    print("ok  desk screening is temporarily non-enforcing")
    check_metadata_fetch_retries_throttling()
    print("ok  a throttled metadata lookup is retried, a missing one is not")
    check_pdf_download_retries_a_flaky_server()
    print("ok  a flaky PDF download is retried too")
    check_a_rate_limit_is_waited_out_in_minutes()
    print("ok  a rate limit is waited out in minutes, within a budget")
    check_command_parsing_is_strict()
    print("ok  editor commands are parsed strictly")
    check_one_model_means_one_model()
    print("ok  one named model means one model")
    check_rerun_refuses_a_moved_draft()
    print("ok  a rerun refuses a draft that moved")
    check_rerun_does_not_inherit_the_prior_round()
    print("ok  a rerun does not inherit the round it tests")

    assert slugify("") == "", "empty title should yield an empty slug"
    assert slugify("!!!") == "", "punctuation-only title should yield an empty slug"
    print(f"\n{len(NASTY_TITLES)} fixture bundle(s) written cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
