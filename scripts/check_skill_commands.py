#!/usr/bin/env python3
"""Parse every engine command in the local-review skill without running one.

The skill told the agent to run

    python -m peerreviewagents.engine --provider claude-code --model X review ...

and the engine rejected it. `--provider` and `--model` are defined on each
subcommand's parser, not at the top level, so argparse refused the command
before any work started. Nothing caught it, because the only thing that would
have is running the review, which costs a review.

Argparse can answer the question for free. This extracts each
`-m peerreviewagents.engine ...` command from the skill's fenced bash blocks,
fills in the angle-bracket placeholders, and hands the result to the engine's
own parser with `parse_args`. Parsing touches no files, spends nothing, and
calls no model.
"""

from __future__ import annotations

import contextlib
import io
import re
import shlex
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "local-review" / "SKILL.md"
MODULE = "peerreviewagents.engine"

# The skill writes paths and values the editor fills in. A placeholder's text is
# documentation, so it is replaced by something argparse will accept rather than
# resolved: no file is opened here.
PLACEHOLDER = re.compile(r"<[^<>\n]+>")


def bash_blocks(text: str) -> list[str]:
    """Every fenced bash block in the document, in order."""
    return re.findall(r"^```bash\n(.*?)^```", text, re.MULTILINE | re.DOTALL)


def commands(block: str) -> list[str]:
    """Split a block into commands, joining backslash continuations."""
    joined = block.replace("\\\n", " ")
    return [line.strip() for line in joined.splitlines() if line.strip()]


def engine_arguments(command: str) -> list[str] | None:
    """The argv the engine would see, or None when this is another program."""
    filled = PLACEHOLDER.sub("placeholder", command)
    try:
        words = shlex.split(filled)
    except ValueError as error:
        raise SystemExit(f"{SKILL.name}: cannot read this command: {command}\n  {error}")
    if MODULE not in words:
        return None
    index = words.index(MODULE)
    if index == 0 or words[index - 1] != "-m":
        return None
    return words[index + 1 :]


def main() -> int:
    if not SKILL.is_file():
        print(f"no skill at {SKILL}", file=sys.stderr)
        return 1

    text = SKILL.read_text(encoding="utf-8")
    found = []
    for block in bash_blocks(text):
        for command in commands(block):
            argv = engine_arguments(command)
            if argv is not None:
                found.append((command, argv))

    if not found:
        print(
            f"{SKILL.name} contains no {MODULE} commands, so this check proved nothing.",
            file=sys.stderr,
        )
        return 1

    try:
        from peerreviewagents.engine.__main__ import build_parser
    except Exception as error:  # pragma: no cover - depends on the environment
        print(
            f"skipped: {MODULE} is not importable in this interpreter ({error}). "
            "Run this check with the interpreter that runs the reviews.",
        )
        return 0

    failures = []
    for command, argv in found:
        parser = build_parser(prog=f"python -m {MODULE}")
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                parser.parse_args(argv)
        except SystemExit:
            reason = stderr.getvalue().strip().splitlines()
            failures.append((command, reason[-1] if reason else "rejected by the parser"))

    if failures:
        print("the skill gives commands the engine's parser rejects:", file=sys.stderr)
        for command, reason in failures:
            print(f"  {command}", file=sys.stderr)
            print(f"    {reason}", file=sys.stderr)
        return 1

    print(f"ok  {len(found)} engine command(s) in {SKILL.name} parse against the real parser")
    return 0


if __name__ == "__main__":
    sys.exit(main())
