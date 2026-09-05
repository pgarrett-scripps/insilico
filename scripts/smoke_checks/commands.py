"""Commands regression checks."""
from __future__ import annotations

import sys
from pathlib import Path

import tomllib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[2]

from run_review import (  # noqa: E402
    CommandError,
)


def check_command_parsing_is_strict() -> None:
    """`/review openrouter <model>` is parsed here, from untrusted text.

    An issue comment is the least trustworthy input this repo takes, and the
    model name it can carry ends up in a config value and in a published
    record. So the parser accepts known provider names and slugs matching a
    strict pattern, and refuses everything else with a message written for the
    editor who typed it. Nothing is sanitised into working.
    """
    from run_review import parse_command

    ok = parse_command("/review openrouter nvidia/nemotron-3-ultra:free")
    assert ok == {"replace": False, "provider": "openrouter",
                  "model": "nvidia/nemotron-3-ultra:free"}, ok
    assert parse_command("/review")["provider"] is None,\
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
    assert 'overrides["models"] = {}' in code,\
        "a named model must clear the tag table, or it reviews nothing"
    assert 'overrides["agent_models"] = {}' in code,\
        "a named model must clear the per-agent overrides too"


def check_rerun_does_not_inherit_the_prior_round() -> None:
    """A same-draft re-review must not be wired as a revision.

    Two properties, both load-bearing. It stays round 1, because nothing was
    revised. And `revision_of` never reaches the pipeline config, because that
    is what hands the editor the earlier round's decision, score and numbered
    required revisions as its reference point, a re-review that inherits the
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
    assert "revision_of" not in code,\
        "a same-draft re-review must not inherit the verdict it is testing"


def check_desk_screen_is_non_enforcing() -> None:
    config = tomllib.loads((REPO / "peerreview.toml").read_text(encoding="utf-8"))
    assert config["desk_screen_mode"] == "warm"
