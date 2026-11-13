#!/usr/bin/env python3
"""Parse every command the published documents give, without running one.

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

The first version of this check read the skill and the engine's two parsers
only, so the same mistake went on living in the pages an editor actually
follows: `docs/development.md` documented `--model` and `--offline` on
`publish` long after this repository's own parser stopped accepting either.
So every document a reader is given is read here, every command in it is routed
to whatever would really run it, and the flags the prose names are checked
against the same parsers:

- `peerreview review` and `peerreview report` against the engine's own parsers
- `scripts/*.py` against that script's `build_parser`, or, for a script that
  defines none, against the fact that it takes no arguments
- `npm run <target>` against the scripts in `package.json`
- a program this repository does not own, `git` or `uv`, is named in
  OUTSIDE_PROGRAMS and reported as unchecked rather than passed over in silence
- every `--flag` the prose puts in backticks has to be a flag one of those
  parsers accepts, and a flag the prose says does not exist has to be absent

Only three engine names are imported, and all three come off
`peerreviewagents.__all__`: `CLI_COMMANDS`, `review_parser` and
`report_parser`, each parser taking its own `prog` so a usage line names
whatever invoked it. Nothing here reaches into `peerreviewagents.cli` or
`peerreviewagents.plugin`: those are the engine's internals, free to move
between releases, and a check that imported one would break on an upgrade
rather than on a change to the surface the engine supports. Running a review
from Python goes through `review`, or through `review_main` and `report_main`,
which the engine exports as well.

Parsing touches no files, spends nothing, and calls no model.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib
import io
import json
import os
import re
import shlex
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
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
FILLED = "placeholder"

# Programs from outside this repository. Their arguments are their own business,
# and a command that runs one is counted and reported rather than parsed. The
# list is explicit so that a document naming some new tool fails here and is
# either added on purpose or corrected.
OUTSIDE_PROGRAMS = frozenset({"git", "uv", "pip", "cd", "export", "source", "date", "echo"})

# A flag the prose puts in backticks is a claim that it exists, and it has to be
# a flag some parser accepts.
FLAG_IN_PROSE = re.compile(r"`(--[a-zA-Z][\w-]*)`")

# The exceptions, named rather than guessed at. These are flags the documents
# mention in order to say they are gone, and whether a sentence denies a flag or
# merely describes leaving it off is not something a regular expression can be
# trusted to tell apart ("with no `--paper`" describes a real flag). So the two
# claims are kept apart by hand: a flag listed here has to be absent from every
# parser, and every other flag in the prose has to be present in one. Either way
# a document and the parsers cannot drift apart quietly.
ABSENT_FLAGS = frozenset({"--provider", "--model", "--offline", "--policy"})

# Flags that belong to a program above rather than to anything here.
OUTSIDE_FLAGS = frozenset({"--silent", "--help", "--version"})


def published_documents() -> list[Path]:
    """Every document a reader is handed: the site's pages, the README, the skill."""
    pages = sorted((REPO / "docs").glob("*.md"))
    return [path for path in (*pages, REPO / "README.md", SKILL) if path.is_file()]


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
    filled = PLACEHOLDER.sub(FILLED, command)
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


def npm_targets() -> set[str]:
    """The script names `npm run` will accept here."""
    package = json.loads((REPO / "package.json").read_text(encoding="utf-8"))
    return set(package.get("scripts") or {})


def is_python(word: str) -> bool:
    """Whether this word runs a Python interpreter, however it is spelled."""
    return re.fullmatch(r"python[\d.]*", PurePosixPath(word).name) is not None


def shell_lines(text: str) -> list[str]:
    """Every command in the document's bash blocks, one per entry.

    Comments are dropped, a `NAME=value` line is remembered so that a later
    `$NAME` reads as what the document said it was, and the shell's own
    separators are split so that `a && b` is two commands rather than one
    unparseable one.
    """
    found: list[str] = []
    variables: dict[str, str] = {}
    for block in bash_blocks(text):
        for line in commands(block):
            if line.startswith("#"):
                continue
            assignment = re.fullmatch(r"([A-Za-z_]\w*)=(\S+)", line)
            if assignment:
                variables[assignment.group(1)] = assignment.group(2)
                continue
            for name, value in variables.items():
                line = line.replace(f"${{{name}}}", value).replace(f"${name}", value)
            for piece in re.split(r"&&|\|\||[;|]", line):
                piece = piece.split("#", 1)[0].strip()
                if piece:
                    found.append(piece)
    return found


def _subparser_action(parser: argparse.ArgumentParser):
    """The subcommand action of this parser, if it has one.

    ``_actions`` and ``_SubParsersAction`` are argparse's own internals, not the
    engine's. They are stable across the interpreters this repository runs on,
    and reading them is how the parser can be asked what it accepts instead of
    being told a second time here.
    """
    for action in parser._actions:  # noqa: SLF001
        if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            return action
    return None


def fill_choices(parser: argparse.ArgumentParser, argv: list[str]) -> list[str]:
    """Replace a placeholder with a value the parser would accept.

    `--decision <the user's answer>` documents a choice, and a parser that
    limits the choices would reject the word `placeholder` for a reason that
    says nothing about the document. The option's own first choice is used, so
    what is parsed is a command of the shape the document gives.
    """
    target = parser
    rest = argv
    action = _subparser_action(parser)
    if action is not None and argv and argv[0] in (action.choices or {}):
        target = action.choices[argv[0]]
        rest = argv[1:]
    options = {
        name: option
        for option in (*parser._actions, *target._actions)  # noqa: SLF001
        for name in option.option_strings
    }
    filled = list(rest)
    for index, word in enumerate(filled):
        if word != FILLED or not index:
            continue
        option = options.get(filled[index - 1])
        if option is not None and option.choices:
            filled[index] = str(next(iter(option.choices)))
    return argv[: len(argv) - len(rest)] + filled


def parse_with(parser: argparse.ArgumentParser, argv: list[str]) -> str | None:
    """None when the parser accepts this argv, else the reason it does not."""
    stderr = io.StringIO()
    try:
        with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
            parser.parse_args(fill_choices(parser, argv))
    except SystemExit:
        reason = stderr.getvalue().strip().splitlines()
        return reason[-1] if reason else "rejected by the parser"
    except Exception as error:  # a type= callable of this repository's own
        return f"{type(error).__name__}: {error}"
    return None


def script_parser(script: Path) -> argparse.ArgumentParser | None:
    """The parser a script in this repository builds, if it builds one.

    The source is read before anything is imported, so a script that defines no
    parser is never executed as a module merely to find that out.
    """
    if "def build_parser(" not in script.read_text(encoding="utf-8"):
        return None
    sys.path.insert(0, str(SCRIPTS))
    module = importlib.import_module(script.stem)
    return module.build_parser()


def check_command(
    command: str,
    *,
    engine: tuple[object, dict] | None,
    targets: set[str],
) -> tuple[str, str | None]:
    """What ran this command, and the reason it would be rejected, if any."""
    filled = PLACEHOLDER.sub(FILLED, command)
    try:
        words = shlex.split(filled)
    except ValueError as error:
        return "unreadable", f"cannot be read as a command: {error}"
    if not words:
        return "empty", None

    engine_argv = engine_arguments(command)
    if engine_argv is not None:
        if engine is None:
            return "engine (skipped)", None
        known, parsers = engine
        subcommand = engine_argv[0] if engine_argv else ""
        if subcommand not in known:
            return (
                "engine",
                f"{subcommand!r} is not one of the engine's commands ({', '.join(known)})",
            )
        # Both parsers take their own `prog`, and naming it here makes a
        # rejection read as the command the document tells an editor to type.
        parser = parsers[subcommand](prog=f"{ENGINE_COMMAND} {subcommand}")
        return "engine", parse_with(parser, engine_argv[1:])

    program = PurePosixPath(words[0]).name
    if is_python(words[0]):
        rest = words[1:]
        if not rest:
            return "python", "runs an interpreter with no script"
        if rest[0] == "-m":
            return "python -m", None if len(rest) > 1 else "runs -m with no module"
        script = (REPO / rest[0]).resolve()
        if not script.is_file():
            return "python", f"{rest[0]} is not a file in this repository"
        try:
            script.relative_to(REPO)
        except ValueError:
            return "python", f"{rest[0]} is outside this repository"
        parser = script_parser(script)
        if parser is None:
            extra = [word for word in rest[1:] if word]
            if extra:
                return (
                    f"python {script.name}",
                    f"{script.name} defines no parser, so it takes no arguments, "
                    f"but this passes {' '.join(extra)}",
                )
            return f"python {script.name}", None
        return f"python {script.name}", parse_with(parser, rest[1:])

    if program == "npm":
        rest = words[1:]
        if rest[:1] in (["install"], ["ci"]):
            return "npm", None
        if rest[:1] != ["run"]:
            return "npm", f"npm {' '.join(rest) or '(nothing)'} is not install, ci or run"
        wanted = [word for word in rest[1:] if not word.startswith("-")]
        if len(wanted) != 1:
            return (
                "npm run",
                "npm run takes one script name, but this line gives "
                f"{len(wanted)} ({' '.join(wanted) or 'none'}). Put each command on its own line.",
            )
        if wanted[0] not in targets:
            return (
                "npm run",
                f"{wanted[0]!r} is not a script in package.json ({', '.join(sorted(targets))})",
            )
        return "npm run", None

    if program in OUTSIDE_PROGRAMS:
        return f"{program} (not checked)", None
    return program, (
        f"{program} is not a program this check knows. Add it to OUTSIDE_PROGRAMS if "
        "it belongs to something other than this repository."
    )


def documented_flags(text: str) -> list[tuple[str, str]]:
    """Each flag the prose names, with the words around it for the report."""
    prose = re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)
    found = []
    for match in FLAG_IN_PROSE.finditer(prose):
        flag = match.group(1)
        if flag in OUTSIDE_FLAGS:
            continue
        before = " ".join(prose[max(0, match.start() - 60) : match.start()].split())
        after = " ".join(prose[match.end() : match.end() + 40].split())
        found.append((flag, f"...{before} `{flag}` {after}..."))
    return found


def accepted_flags(engine: tuple[object, dict] | None) -> set[str]:
    """Every option string the parsers behind these documents accept."""
    parsers: list[argparse.ArgumentParser] = []
    local = script_parser(SCRIPTS / "local_review.py")
    if local is not None:
        parsers.append(local)
    if engine is not None:
        parsers += [build(prog=ENGINE_COMMAND) for build in engine[1].values()]

    found: set[str] = set()
    while parsers:
        parser = parsers.pop()
        for action in parser._actions:  # noqa: SLF001
            found.update(action.option_strings)
            if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
                parsers += list((action.choices or {}).values())
    return found


def main() -> int:
    documents = published_documents()
    if not SKILL.is_file():
        print(f"no skill at {SKILL}", file=sys.stderr)
        return 1

    try:
        engine = load_parsers()
    except Exception as error:  # pragma: no cover - depends on the environment
        if engine_required():
            print(
                f"{PACKAGE} is not importable here ({error}), so this check proved "
                "nothing about the documented commands. The installed release has to "
                "contain the engine package. Set "
                f"{REQUIRE_ENGINE}=0 only to waive the check deliberately.",
                file=sys.stderr,
            )
            return 1
        print(
            f"note: {PACKAGE} is not importable in this interpreter ({error}), so the "
            f"{ENGINE_COMMAND} commands are not parsed and a flag the prose names is "
            "only checked for being gone, not for being present. Run this check with "
            f"the interpreter that runs the reviews, or set {REQUIRE_ENGINE}=1 to make "
            "a missing engine a failure."
        )
        engine = None

    targets = npm_targets()
    accepted = accepted_flags(engine)
    failures: list[tuple[Path, str, str]] = []
    counted: dict[str, int] = {}
    engine_commands = 0

    for document in documents:
        text = document.read_text(encoding="utf-8")
        for command in shell_lines(text):
            ran_by, reason = check_command(command, engine=engine, targets=targets)
            counted[ran_by] = counted.get(ran_by, 0) + 1
            if ran_by.startswith("engine"):
                engine_commands += 1
            if reason:
                failures.append((document, command, reason))
        for flag, context in documented_flags(text):
            if flag in ABSENT_FLAGS and flag in accepted:
                failures.append(
                    (
                        document,
                        context,
                        f"{flag} is listed in ABSENT_FLAGS as a flag these documents "
                        "only mention to say it is gone, but a parser accepts it.",
                    )
                )
            elif engine is None and flag not in ABSENT_FLAGS:
                # Half the parsers are missing, so a flag that is not in the
                # half that loaded proves nothing. The note above says so.
                continue
            elif flag not in ABSENT_FLAGS and flag not in accepted:
                failures.append(
                    (
                        document,
                        context,
                        f"{flag} is documented as a flag, but no parser accepts it. "
                        "Delete the claim, restore the flag, or, if the document says "
                        "it is gone, add it to ABSENT_FLAGS.",
                    )
                )

    if not engine_commands:
        print(
            f"no {ENGINE_COMMAND} commands in {len(documents)} document(s), so this "
            "check proved nothing.",
            file=sys.stderr,
        )
        return 1

    if failures:
        print("the documents give commands or flags the real parsers reject:", file=sys.stderr)
        for document, command, reason in failures:
            print(f"  {document.relative_to(REPO)}: {command}", file=sys.stderr)
            print(f"    {reason}", file=sys.stderr)
        return 1

    summary = ", ".join(f"{count} {name}" for name, count in sorted(counted.items()))
    print(
        f"ok  {sum(counted.values())} command(s) in {len(documents)} document(s) parse "
        f"against the real parsers ({summary})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
