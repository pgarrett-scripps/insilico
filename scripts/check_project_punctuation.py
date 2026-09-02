"""Check In Silico-owned documentation and rendered editorial pages."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path


FORBIDDEN = {
    chr(0x2014): "em dash",
    chr(59): "semicolon",
}
TEXT_ATTRIBUTES = {
    "alt",
    "aria-description",
    "aria-label",
    "content",
    "placeholder",
    "title",
}
IGNORED_ELEMENTS = {"code", "pre", "script", "style"}
EDITORIAL_PAGES = ("criteria", "development", "policy", "submit")
SOURCE_FILES = (
    Path("AGENTS.md"),
    Path("LICENSE"),
    Path("README.md"),
    Path(".github/ISSUE_TEMPLATE/submit.yml"),
)


class ProseParser(HTMLParser):
    """Collect visible editorial text and human-readable attributes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignored_depth = 0
        self.fragments: list[tuple[int, str, str]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag in IGNORED_ELEMENTS:
            self.ignored_depth += 1

        if self.ignored_depth:
            return

        for name, value in attrs:
            if name in TEXT_ATTRIBUTES and value:
                self.fragments.append((self.getpos()[0], f"{name} attribute", value))

    def handle_endtag(self, tag: str) -> None:
        if tag in IGNORED_ELEMENTS and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.fragments.append((self.getpos()[0], "text", data))


def _violations(path: Path, fragments: list[tuple[int, str, str]]) -> list[str]:
    failures = []
    for line, location, fragment in fragments:
        for character, name in FORBIDDEN.items():
            if character in fragment:
                excerpt = " ".join(fragment.split())
                failures.append(f"{path}:{line}: {name} in {location}: {excerpt[:160]}")
    return failures


def source_violations(path: Path) -> list[str]:
    fragments = [
        (line, "text", text)
        for line, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
    ]
    return _violations(path, fragments)


def html_violations(path: Path) -> list[str]:
    parser = ProseParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return _violations(path, parser.fragments)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", nargs="?", default="dist")
    args = parser.parse_args()
    site = Path(args.site)

    if not site.is_dir():
        parser.error(f"site directory does not exist: {site}")

    rendered = [site / name / "index.html" for name in EDITORIAL_PAGES]
    missing = [path for path in (*SOURCE_FILES, *rendered) if not path.is_file()]
    if missing:
        parser.error(f"required file does not exist: {missing[0]}")

    failures = [
        failure
        for path in SOURCE_FILES
        for failure in source_violations(path)
    ]
    failures.extend(
        failure
        for path in rendered
        for failure in html_violations(path)
    )

    if failures:
        print("Project-authored prose contains forbidden punctuation:")
        print("\n".join(failures))
        return 1

    print("Project-authored prose contains no em dashes or semicolons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
