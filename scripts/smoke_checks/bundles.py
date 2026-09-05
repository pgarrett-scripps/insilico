"""Bundles regression checks."""
from __future__ import annotations

import hashlib
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
    configuration_record,
    slugify,
    write_bundle,
)

from .support import build_fixture, provenance_of  # noqa: E402


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
        # per-referee detail. both come from here and nowhere else.
        assert prov["mean_score"] == 3.0, f"mean_score missing: {prov.get('mean_score')!r}"
        assert prov["readiness_score"] == 78
        assert sum(prov["readiness_breakdown"].values()) == 78
        assert prov["contribution_profile"]["usefulness"] == "high"
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
    statistical claims to evaluate" and scored the paper 5/5, the highest
    data-analysis score in the corpus. The pipeline now returns null there,
    and this asserts the record keeps it null and averages without it. Filling
    the gap in, with a zero, a midpoint, anything, reintroduces the bug in
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
        assert by["data_analysis"]["score"] is None,\
            "an unscorable dimension must stay null in the record"
        assert by["data_analysis"]["not_applicable_reason"],\
            "the reason must travel with it, or the page cannot say why"

        # 3.0 and 4.0 average to 3.5. Counting the null as anything at all
        # moves this: as a 5 it would read 4.0, as a 0 it would read 2.33.
        assert prov["mean_score"] == 3.5,\
            f"the mean must be over scored referees only, got {prov['mean_score']}"
        assert prov["scored_count"] == 2, prov["scored_count"]
        assert prov["panel_size"] == 3, prov["panel_size"]
        assert prov["scored_count"] != prov["panel_size"],\
            "the page needs both numbers to say 'mean over 2 of 3'"

        # A panel where nobody could score has no mean, not a zero.
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
    verbatim, so the record must name the tool and the compression level, or
    the mismatch reads as the referee having misquoted.

    The pipeline builds that record now. this script's job is to check it
    survives into provenance.json unaltered, and that the pages still render
    when it is absent, every review published before the record existed has
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
        assert provenance_of(dest3)["ingest"] == {},\
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

        # Both identical bodies are copied so a direct link resolves. the
        # site is what collapses them to one entry.
        for name in ("decision_letter.md", "desk_screen.md"):
            assert (dest / name).exists(), f"{name} not copied into the bundle"


def check_site_never_injects_raw_html() -> None:
    """Layer 2: nothing in the site may hand untrusted metadata to the parser.

    Titles, abstracts and author names are written by the *authors*, and they
    reach every page. Astro escapes the value of a `{...}` expression, so the
    default is safe, but `set:html` opts out of exactly that, and one use of
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
    assert extract_authorship("### Preprint URL\n\nhttps://x\n") == "",\
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
            assert prov["submitter_is_author"] == claim,\
                f"claim {claim!r} not recorded, got {prov['submitter_is_author']!r}"
            assert prov["submitter"] == "someone", "submitter not recorded"
