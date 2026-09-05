"""Sources regression checks."""
from __future__ import annotations

import contextlib
import datetime as dt
import email.utils
import json
import sys
import tempfile
import urllib.error
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[2]

from fetch_preprint import Preprint, resolve  # noqa: E402
from manuscript_source import (  # noqa: E402
    html_to_markdown,
    jats_to_markdown,
    select_manuscript_source,
    validate_text,
)
from preview_submission import COMMENT_MARKER, build_preview  # noqa: E402


@contextlib.contextmanager
def offline():
    """Run a block with metadata lookups failing, as if there were no network.

    What the URL checks below actually assert is how a string is classified
    and canonicalised, which is pure parsing, but ``resolve`` also calls the
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

def check_metadata_is_sanitised_at_ingestion() -> None:
    """Layer 1, and the one that actually closes the hole.

    The title reaches many places, <title>, og:description, a card, a
    heading, and an escape that has to be remembered at each of them is one
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


def check_url_is_canonical() -> None:
    """The stored URL is rebuilt from the match, never echoed from input.

    The source patterns are searched rather than anchored, so a string like
    `javascript:alert(1)#arxiv.org/abs/1706.03762` matches on its tail, and
    echoing the input back would publish it as a clickable link.
    """
    hostile = "javascript:alert(document.domain)#arxiv.org/abs/1706.03762"
    with offline():
        p = resolve(hostile)
    assert p.url == "https://arxiv.org/abs/1706.03762", p.url
    assert "javascript:" not in p.url
    assert not p.pdf_url.startswith("javascript:")


def check_download_is_bounded() -> None:
    """An unbounded read is a memory bomb. a runner has a couple of GB."""
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
    makes these equivalent. anchoring to the end made a trailing slash fatal
    and quietly swallowed `.full-text` into the DOI itself, which then became
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

        # A DOI from another registrar is still not a preprint, and neither
        # is a *journal* article sharing bioRxiv's prefix. 10.1101 belongs to
        # Cold Spring Harbor Press, who use it for Genome Research and
        # Learning & Memory as well as for bioRxiv, so the prefix alone does
        # not identify a preprint. Matching the DOI's shape is what separates
        # them. the previous open-ended pattern accepted `10.1101/gr.123456`
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
    published review then carries no title, no authors and no DOI, a record
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
        assert fp._get("https://example.org/api", retries=3) == b"<ok/>",\
            "a throttled lookup should succeed once the throttle lifts"
        assert calls["n"] == 3, f"expected 3 attempts, got {calls['n']}"
        assert sleeps and sleeps == sorted(sleeps),\
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
    the download, before any model call, so nothing was billed, but also
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
    assert [fp._retry_delay(err(500), n, 0) for n in (1, 2, 3)] == [4, 8, 16],\
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
        assert sum(slept) == fp.MAX_THROTTLE_WAIT_SECONDS,\
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
                 "jatsxml": "/content/10.1101/example.source.xml"}]\
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
            None,
            workdir,
            {},
            fetcher=lambda url, **kwargs: jats,
            loader=lambda path, config: broken_pdf,
            ocr=lambda path, dest: full_text,
        )
        assert source.kind == "jats"

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
