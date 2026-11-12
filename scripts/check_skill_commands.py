#!/usr/bin/env python3
"""Parse every engine command in the local-review skill without running one.

An earlier version of the skill told the agent to run

    python -m peerreviewagents.engine --provider claude-code --model X review ...

and the engine rejected it. `--provider` and `--model` were defined on each
subcommand's parser, not at the top level, so argparse refused the command
before any work started. Nothing caught it, because the only thing that would
have is running the review, which costs a review.

Engine 0.9 has one console command, `peerreview`, with two subcommands, and
each one parses its own arguments: `peerreview --help` lists `review` and
`report` and carries no options of its own. That makes the same class of
mistake easy to repeat in the other direction, by writing an option before the
subcommand where there is nothing to accept it.

Argparse can answer the question for free. This extracts each `peerreview ...`
command from the skill's fenced bash blocks, fills in the angle-bracket
placeholders, and hands the result to the parser the engine itself builds for
that subcommand. Parsing touches no files, spends nothing, and calls no model.

Only three engine names are imported, and all three come off
`peerreviewagents.__all__`: `CLI_COMMANDS`, `review_parser` and
`report_parser`, each parser taking its own `prog` so a usage line names
whatever invoked it. Nothing here reaches into `peerreviewagents.cli` or
`peerreviewagents.plugin`: those are the engine's internals, free to move
between releases, and a check that imported one would break on an upgrade
rather than on a change to the surface the engine supports. Running a review
from Python goes through `review`, or through `review_main` and `report_main`,
which the engine exports as well.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import shlex
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "local-review" / "SKILL.md"
PACKAGE = "peerreviewagents"
ENGINE_COMMAND = "peerreview"

# Where the engine has to be present for this check to mean anything. On a
# laptop the engine is optional, so a missing one is reported and skipped. In
# CI it is installed from the lock file, so a missing one is the lock file
# being wrong, and skipping it is how the guard came to be worth nothing: the
# pin named a release with no engine package in it and the job stayed green.
REQUIRE_ENGINE = "INSILICO_REQUIRE_ENGINE"
FALSE_VALUES = {"", "0", "false", "no", "off"}

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
    """The argv the engine would see, or None when this is another program.

    The command is found by its name rather than by position, so a line that
    runs it out of a virtual environment or through a runner is read the same
    way as a bare `peerreview`.
    """
    filled = PLACEHOLDER.sub("placeholder", command)
    try:
        words = shlex.split(filled)
    except ValueError as error:
        raise SystemExit(f"{SKILL.name}: cannot read this command: {command}\n  {error}")
    for index, word in enumerate(words):
        if PurePosixPath(word).name != ENGINE_COMMAND:
            continue
        if index and words[index - 1] == "-m":
            return None
        return words[index + 1 :]
    return None


def engine_required() -> bool:
    """Whether a missing engine is a failure rather than a skip.

    `INSILICO_REQUIRE_ENGINE` decides it outright, either way, so an editor can
    demand the real answer locally and a job can waive it. With nothing set,
    any CI run requires the engine.
    """
    setting = os.environ.get(REQUIRE_ENGINE)
    if setting is not None:
        return setting.strip().lower() not in FALSE_VALUES
    return os.environ.get("CI", "").strip().lower() not in FALSE_VALUES


def load_parsers():
    """The engine's own parsers, one per subcommand. Raises with no engine."""
    from peerreviewagents import CLI_COMMANDS, report_parser, review_parser

    return CLI_COMMANDS, {"review": review_parser, "report": report_parser}


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
            f"{SKILL.name} contains no {ENGINE_COMMAND} commands, so this check "
            "proved nothing.",
            file=sys.stderr,
        )
        return 1

    try:
        known, parsers = load_parsers()
    except Exception as error:  # pragma: no cover - depends on the environment
        if engine_required():
            print(
                f"{PACKAGE} is not importable here ({error}), so this check proved "
                "nothing about the skill's commands. The installed release has to "
                "contain the engine package. Set "
                f"{REQUIRE_ENGINE}=0 only to waive the check deliberately.",
                file=sys.stderr,
            )
            return 1
        print(
            f"skipped: {PACKAGE} is not importable in this interpreter ({error}). "
            "Run this check with the interpreter that runs the reviews, or set "
            f"{REQUIRE_ENGINE}=1 to make a missing engine a failure.",
        )
        return 0

    failures = []
    for command, argv in found:
        subcommand = argv[0] if argv else ""
        if subcommand not in known:
            failures.append(
                (
                    command,
                    f"{subcommand!r} is not one of the engine's commands "
                    f"({', '.join(known)})",
                )
            )
            continue
        # Both parsers take their own `prog`, and naming it here makes a
        # rejection read as the command the skill tells an editor to type.
        parser = parsers[subcommand](prog=f"{ENGINE_COMMAND} {subcommand}")
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                parser.parse_args(argv[1:])
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
