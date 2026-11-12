"""Commands regression checks."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[2]

from review_commands import CommandError, parse_command  # noqa: E402


def check_command_parsing_is_strict() -> None:
    """`/review openrouter <model>` is parsed here, from untrusted text.

    An issue comment is the least trustworthy input this repo takes, and the
    model name it can carry ends up in a config value and in a published
    record. So the parser accepts known provider names and slugs matching a
    strict pattern, and refuses everything else with a message written for the
    editor who typed it. Nothing is sanitised into working.

    The hosted lane that acted on these commands is retired, so this guards the
    parser rather than a running pipeline. It stays because the parser is the
    one place in the repo that reads a stranger's text, and a loosened pattern
    here is a real hole whenever the lane is revived.
    """
    ok = parse_command("/review openrouter nvidia/nemotron-3-ultra:free")
    assert ok == {"replace": False, "provider": "openrouter",
                  "model": "nvidia/nemotron-3-ultra:free"}, ok
    assert parse_command("/review")["provider"] is None,\
        "a bare /review must name no provider of its own"
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

    # Only the first line is a command. a comment may say more below it.
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
