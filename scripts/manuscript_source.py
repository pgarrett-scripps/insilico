"""Choose and verify the text representation sent to the referee panel."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import unicodedata
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

from fetch_preprint import METADATA_RETRIES, Preprint, _get


class ManuscriptSourceUnreadable(RuntimeError):
    """No available representation passed the identity and completeness checks."""


@dataclass
class ManuscriptSource:
    path: Path
    kind: str
    url: str
    tool: str
    validation: dict
    attempts: list[dict] = field(default_factory=list)

    def record(self) -> dict:
        return {
            "kind": self.kind,
            "url": self.url,
            "tool": self.tool,
            "sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(),
            "validation": self.validation,
            "attempts": self.attempts,
        }


_WORD_RE = re.compile(r"[^\W_]{3,}", re.UNICODE)
_SPACE_RE = re.compile(r"[ \t\r\f\v]+")
_STOPWORDS = {
    "and", "are", "but", "for", "from", "has", "have", "into", "not",
    "our", "that", "the", "their", "these", "this", "those", "was",
    "were", "which", "with",
}


def _tokens(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", text or "").casefold()
    return {word for word in _WORD_RE.findall(normalized) if word not in _STOPWORDS}


def _recall(expected: str, actual: str) -> float:
    wanted = _tokens(expected)
    if not wanted:
        return 1.0
    return len(wanted & _tokens(actual)) / len(wanted)


def validate_text(
    text: str,
    preprint: Preprint,
    *,
    relaxed: bool = False,
) -> dict:
    """Check that extracted text contains the archive title and abstract."""
    chars = len(text.strip())
    words = len(_WORD_RE.findall(text))
    title_recall = _recall(preprint.title, text)
    abstract_recall = _recall(preprint.abstract, text)
    title_floor = 0.55 if relaxed else 0.70
    abstract_floor = 0.42 if relaxed else 0.58
    reasons: list[str] = []
    if chars < 4000:
        reasons.append(f"only {chars:,} characters")
    if words < 700:
        reasons.append(f"only {words:,} words")
    if preprint.title and title_recall < title_floor:
        reasons.append(f"title match {title_recall:.0%}")
    if len(_tokens(preprint.abstract)) >= 12 and abstract_recall < abstract_floor:
        reasons.append(f"abstract match {abstract_recall:.0%}")
    return {
        "passed": not reasons,
        "chars": chars,
        "words": words,
        "title_recall": round(title_recall, 3),
        "abstract_recall": round(abstract_recall, 3),
        "reasons": reasons,
    }


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _node_text(node: ET.Element) -> str:
    return _SPACE_RE.sub(" ", " ".join(node.itertext())).strip()


def jats_to_markdown(data: bytes) -> str:
    """Render source-declared JATS structure into compact Markdown."""
    lowered = data[:8192].lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError("JATS document declarations are not accepted")
    root = ET.fromstring(data)
    bodies = [node for node in root.iter() if _local_name(node.tag) == "body"]
    body_words = sum(len(_WORD_RE.findall(_node_text(node))) for node in bodies)
    if not bodies or body_words < 500:
        raise ValueError("JATS body is missing or too short")
    article_title = next(
        (_node_text(node) for node in root.iter() if _local_name(node.tag) == "article-title"),
        "",
    )
    lines: list[str] = []
    if article_title:
        lines.extend((f"# {article_title}", ""))

    def render(node: ET.Element, depth: int = 2) -> None:
        tag = _local_name(node.tag)
        if tag == "title":
            return
        if tag == "sec":
            title = next(
                (_node_text(child) for child in node if _local_name(child.tag) == "title"),
                "",
            )
            if title:
                lines.extend((f"{'#' * min(depth, 6)} {title}", ""))
            for child in node:
                render(child, depth + 1)
            return
        if tag == "abstract":
            heading = next(
                (_node_text(child) for child in node if _local_name(child.tag) == "title"),
                "Abstract",
            )
            lines.extend((f"## {heading or 'Abstract'}", ""))
            for child in node:
                render(child, 3)
            return
        if tag == "p":
            value = _node_text(node)
            if value:
                lines.extend((value, ""))
            return
        if tag == "list-item":
            value = _node_text(node)
            if value:
                lines.append(f"- {value}")
            return
        if tag in {"fig", "table-wrap"}:
            label = next(
                (_node_text(child) for child in node if _local_name(child.tag) == "label"),
                "",
            )
            caption = next(
                (_node_text(child) for child in node if _local_name(child.tag) == "caption"),
                "",
            )
            value = ": ".join(part for part in (label, caption) if part)
            if value:
                lines.extend((value, ""))
            if tag == "table-wrap":
                for row in node.iter():
                    if _local_name(row.tag) != "tr":
                        continue
                    cells = [
                        _node_text(cell)
                        for cell in row
                        if _local_name(cell.tag) in {"td", "th"}
                    ]
                    if cells:
                        lines.append(" | ".join(cells))
                lines.append("")
            return
        if tag == "ref-list":
            lines.extend(("## References", ""))
            for child in node.iter():
                if _local_name(child.tag) == "ref":
                    value = _node_text(child)
                    if value:
                        lines.append(f"- {value}")
            lines.append("")
            return
        if tag in {"front", "article-meta", "title-group", "contrib-group"}:
            return
        for child in node:
            render(child, depth)

    for child in root:
        tag = _local_name(child.tag)
        if tag in {"body", "back"}:
            render(child)
        elif tag == "front":
            for node in child.iter():
                if _local_name(node.tag) == "abstract":
                    render(node)
    return _clean_markdown(lines)


class _FullTextHTMLParser(HTMLParser):
    """Small HTML text renderer that keeps source headings and paragraphs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.heading_level = 0
        self.heading: list[str] = []
        self.skipped = 0
        self.in_body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "body":
            self.in_body = True
        if tag in {"script", "style", "nav", "header", "footer", "aside", "form"}:
            self.skipped += 1
            return
        if not self.in_body or self.skipped:
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = int(tag[1])
            self.heading = []
        elif tag == "li":
            self.lines.append("\n- ")
        elif tag in {"p", "div", "section", "article", "tr", "figure", "figcaption"}:
            self.lines.append("\n")
        elif tag in {"td", "th"}:
            self.lines.append(" | ")
        elif tag == "br":
            self.lines.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "nav", "header", "footer", "aside", "form"}:
            self.skipped = max(0, self.skipped - 1)
            return
        if self.skipped:
            return
        if self.heading_level and tag == f"h{self.heading_level}":
            value = _SPACE_RE.sub(" ", "".join(self.heading)).strip()
            if value:
                self.lines.extend((f"\n{'#' * self.heading_level} {value}\n", "\n"))
            self.heading_level = 0
            self.heading = []
        elif tag == "body":
            self.in_body = False
        elif self.in_body and tag in {"p", "li", "tr", "figure", "figcaption"}:
            self.lines.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.in_body or self.skipped:
            return
        if self.heading_level:
            self.heading.append(data)
        else:
            self.lines.append(data)


def html_to_markdown(data: bytes) -> str:
    parser = _FullTextHTMLParser()
    parser.feed(data.decode("utf-8", errors="replace"))
    parser.close()
    return _clean_markdown(parser.lines)


def _clean_markdown(parts: list[str]) -> str:
    text = "".join(parts)
    cleaned: list[str] = []
    for raw in text.splitlines():
        line = _SPACE_RE.sub(" ", raw).strip()
        if line:
            cleaned.append(line)
        elif cleaned and cleaned[-1] != "":
            cleaned.append("")
    return "\n".join(cleaned).strip() + "\n"


def _trusted_full_text_url(url: str, preprint: Preprint) -> bool:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower()
    allowed = {
        "arxiv.org", "www.arxiv.org", "biorxiv.org", "www.biorxiv.org",
        "medrxiv.org", "www.medrxiv.org",
    }
    return host in allowed and preprint.source in host


def _write_candidate(workdir: Path, name: str, text: str) -> Path:
    path = workdir / name
    path.write_text(text, encoding="utf-8")
    return path


def _ocr_pdf(pdf: Path, workdir: Path) -> str:
    if not shutil.which("pdftoppm") or not shutil.which("tesseract"):
        raise RuntimeError("OCR tools are not installed")
    pages = workdir / "ocr-pages"
    pages.mkdir(exist_ok=True)
    prefix = pages / "page"
    subprocess.run(
        ["pdftoppm", "-r", "200", "-png", str(pdf), str(prefix)],
        check=True,
        capture_output=True,
        text=True,
        timeout=600,
    )
    chunks: list[str] = []
    def page_number(path: Path) -> int:
        match = re.search(r"-(\d+)$", path.stem)
        return int(match.group(1)) if match else 0

    for page in sorted(pages.glob("page-*.png"), key=page_number):
        result = subprocess.run(
            ["tesseract", str(page), "stdout", "-l", "eng", "--psm", "1"],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        chunks.append(result.stdout.strip())
    if not chunks:
        raise RuntimeError("OCR produced no pages")
    return "\n\n".join(chunks) + "\n"


def select_manuscript_source(
    preprint: Preprint,
    pdf: Path,
    workdir: Path,
    config: dict,
    *,
    fetcher: Callable[..., bytes] = _get,
    loader: Callable | None = None,
    ocr: Callable[[Path, Path], str] = _ocr_pdf,
) -> ManuscriptSource:
    """Choose JATS, HTML, validated PDF text, or validated OCR in that order."""
    attempts: list[dict] = []
    structured = (
        ("jats", preprint.jats_url, jats_to_markdown),
        ("html", preprint.html_url, html_to_markdown),
    )
    for kind, url, converter in structured:
        if not url:
            continue
        if not _trusted_full_text_url(url, preprint):
            attempts.append({"kind": kind, "url": url, "error": "untrusted URL"})
            continue
        try:
            data = fetcher(url, retries=METADATA_RETRIES)
            text = converter(data)
            validation = validate_text(text, preprint)
            attempts.append({"kind": kind, "url": url, "validation": validation})
            if validation["passed"]:
                path = _write_candidate(workdir, f"manuscript-{kind}.md", text)
                tool = "official JATS XML" if kind == "jats" else "official archive HTML"
                return ManuscriptSource(path, kind, url, tool, validation, attempts)
        except (OSError, ValueError, ET.ParseError, urllib.error.URLError) as exc:
            attempts.append({"kind": kind, "url": url, "error": str(exc)})

    if loader is None:
        from peerreviewagents.ingest.loader import load_manuscript_record

        loader = load_manuscript_record
    try:
        parsed = loader(str(pdf), config)
        validation = validate_text(parsed.text, preprint)
        attempts.append({"kind": "pdf", "validation": validation})
        if validation["passed"]:
            return ManuscriptSource(
                pdf,
                "pdf",
                preprint.pdf_url,
                str(parsed.ingest.get("tool") or "PDF converter"),
                validation,
                attempts,
            )
    except Exception as exc:
        attempts.append({"kind": "pdf", "error": str(exc)})

    try:
        text = ocr(pdf, workdir)
        validation = validate_text(text, preprint, relaxed=True)
        attempts.append({"kind": "ocr", "validation": validation})
        if validation["passed"]:
            path = _write_candidate(workdir, "manuscript-ocr.txt", text)
            return ManuscriptSource(
                path,
                "ocr",
                preprint.pdf_url,
                "Tesseract OCR",
                validation,
                attempts,
            )
    except Exception as exc:
        attempts.append({"kind": "ocr", "error": str(exc)})

    detail = []
    for attempt in attempts:
        reason = attempt.get("error")
        if not reason:
            reason = ", ".join((attempt.get("validation") or {}).get("reasons") or [])
        detail.append(f"{attempt['kind']}: {reason or 'validation failed'}")
    raise ManuscriptSourceUnreadable(
        "no manuscript representation passed validation. " + " | ".join(detail)
    )
