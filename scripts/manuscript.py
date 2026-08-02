"""Turn the downloaded PDF into the text the panel actually reads.

The pipeline's own ingest is pypdf, which is adequate on paper and poor in
practice: on a real submission it fused 2% of all words into runs like
``comparableefficacyatlowerdoseusingonlycausallyavailableinformation``, lost
about a sixth of the content outright, and flattened every heading, table and
equation into undifferentiated text. rustypdf reads the same file with 3 fused
tokens instead of 235, and emits structure — headings, tables, mathematics —
that the referees can actually navigate.

Compression is a second, smaller thing. ``caveman`` strips closed-class words
(articles, copulas, and at ``hard`` also prepositions and connectives) for
models billed by the token. It saves little here — the manuscript is a cached
prefix read only by the cheapest tier, so it is about 3% of a review's cost —
so treat it as a modest saving rather than the reason to convert.

**The PDF remains the citable artifact.** It is still downloaded and still
fingerprinted, and the review still names its SHA-256. What changes is only
what the panel was handed, which is why :func:`describe` records it: a reader
comparing a quoted sentence against the paper needs to know the referees read
a derived rendering, not the file itself.
"""

from __future__ import annotations

import os
from pathlib import Path

# What the referees are given by default: the text as written.
#
# `light` was the intended default and was measured instead. It drops articles
# and copulas, which leaves every content word standing but not every sentence
# grammatical — and the clarity reviewer read the result as the authors'
# writing. On the same paper it reported "grammatical errors that obscure the
# main claims" three times under `light` and not once uncompressed. That is a
# published criticism of real people for something the pipeline did to their
# text, which no token saving justifies: the manuscript is a cached prefix
# read only by the cheapest model tier, so compressing it saves under a cent a
# review.
#
# `light` and `hard` remain available for callers that never publish a
# referee's prose — indexing or retrieval, where nothing is quoted back to an
# author. Mathematics, tables and bibliography entries are exempt at every
# level.
DEFAULT_CAVEMAN = os.environ.get("INSILICO_CAVEMAN", "off")

# A conversion that returns almost nothing is a failure wearing a success's
# clothes — an empty or near-empty manuscript would run a full panel over
# nothing and publish whatever it invented. Real papers clear this by an order
# of magnitude; the shortest in the corpus so far is about 40 000 characters.
MIN_PLAUSIBLE_CHARS = 4000


def _import_rustypdf():
    """Import the converter, or return None with the reason.

    Not a hard dependency: it is a compiled extension, and a review that could
    otherwise run should not fail because a wheel is missing. The caller
    records which path was taken so the degradation is never silent.
    """
    try:
        import rustypdf  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001 - any import failure is the same outcome
        return None, f"rustypdf unavailable ({exc.__class__.__name__}: {exc})"
    return rustypdf, ""


def prepare(pdf: Path, caveman: str = DEFAULT_CAVEMAN) -> tuple[Path, dict]:
    """Convert ``pdf`` to markdown beside it, and describe what happened.

    Returns the path to hand the pipeline and a record for provenance. On any
    failure the PDF itself is returned, so the review still runs on the older
    ingest path rather than not at all — but the record says so, and the
    published page can then be honest about how the manuscript was read.
    """
    record = {
        "format": "pdf",
        "tool": "pypdf (pipeline default)",
        "caveman": None,
        "chars": None,
        "reason": "",
    }

    rustypdf, why = _import_rustypdf()
    if rustypdf is None:
        record["reason"] = why
        return pdf, record

    try:
        text = rustypdf.to_markdown(str(pdf), caveman)
    except Exception as exc:  # noqa: BLE001 - scanned, malformed, or pdfium missing
        record["reason"] = f"conversion failed ({exc.__class__.__name__}: {exc})"
        return pdf, record

    if len(text) < MIN_PLAUSIBLE_CHARS:
        # Almost certainly a scanned or image-only PDF. The pipeline's own
        # loader raises a clear error for that case, so hand it the PDF and
        # let it be the one to refuse.
        record["reason"] = (
            f"conversion produced only {len(text)} characters, which is not a "
            "readable manuscript — likely scanned or image-only"
        )
        return pdf, record

    dest = pdf.with_suffix(".md")
    dest.write_text(text, encoding="utf-8")
    record.update(
        format="markdown",
        tool=f"rustypdf {getattr(rustypdf, '__version__', 'unknown')}",
        caveman=caveman if caveman not in (None, "off", "none") else None,
        chars=len(text),
    )
    return dest, record


def describe(record: dict) -> str:
    """One line for the run log."""
    if record["format"] == "pdf":
        return f"ingest    pdf via pypdf — {record['reason']}"
    level = record["caveman"] or "no compression"
    return f"ingest    markdown via {record['tool']} ({level}), {record['chars']} chars"
