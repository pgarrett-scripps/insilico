"""Parse editor commands before any model call."""
from __future__ import annotations

import re

# A model slug an editor may name in a comment. Deliberately strict: the
# comment body is untrusted text that ends up in a config value and in a
# published record, so anything outside this alphabet is refused rather than
# sanitised. Covers every real OpenRouter slug, `vendor/model`, optionally
# `:free`, `:nitro`, `@preset`, and nothing that looks like a shell or a path.
_MODEL_SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9._-]*)?/[a-z0-9][a-z0-9._-]*(:[a-z0-9-]+)?$", re.I)

# Providers an editor may select by name. Not the full set the pipeline
# supports, `openai` is omitted because there is no key for it here, and a
# command that silently does nothing is worse than one that is refused.
_SELECTABLE_PROVIDERS = ("anthropic", "openrouter")


class CommandError(ValueError):
    """An editor's command could not be understood. The message is shown to
    them on the issue, so it says what to type instead."""


def parse_command(body: str) -> dict:
    """Read `/review` and its options out of a comment.

    Grammar, deliberately tiny:

        /review                          the configured panel (peerreview.toml)
        /review anthropic                the same, said out loud
        /review openrouter <model>       one model for every agent
        /review replace ...              redo a draft already reviewed

    There is one verb. Whether a run is a first look or a new round is not
    something an editor should have to declare: the archive says which draft
    exists, and a draft we have not reviewed is a new round. `/revise` is
    still accepted because editors have muscle memory for it, and does exactly
    what `/review` does.

    Parsed here rather than in the workflow because the comment is untrusted
    input. Bash sees it only as an environment variable. this is the one place
    it is interpreted, and everything it can produce is either a known constant
    or a string that matched :data:`_MODEL_SLUG_RE`.

    OpenRouter requires an explicit model and always will. Its free tier is a
    rotating set of specific slugs, not a stable "free" alias, so guessing one
    would silently review a paper on whatever happened to be cheapest that
    week and publish the result without anyone having chosen it.
    """
    first = (body or "").strip().splitlines()[0] if (body or "").strip() else ""
    parts = first.split()
    out: dict = {"replace": False, "provider": None, "model": None}
    if not parts or not parts[0].startswith("/"):
        return out

    command = parts[0].lower()
    if command not in ("/review", "/revise"):
        return out

    rest = parts[1:]
    if rest and rest[0].lower() == "replace":
        out["replace"] = True
        rest = rest[1:]
    if not rest:
        return out

    provider = rest[0].lower()
    if provider not in _SELECTABLE_PROVIDERS:
        raise CommandError(
            f"`{rest[0]}` is not a provider I know. Use "
            f"`{command}`, `{command} anthropic`, or "
            f"`{command} openrouter <model>`."
        )
    out["provider"] = provider

    if provider == "anthropic":
        if len(rest) > 1:
            raise CommandError(
                f"`{command} anthropic` takes no model: the Anthropic runs use "
                "the per-stage split in `peerreview.toml`, which is the whole "
                "point of that file. To force one model, use "
                f"`{command} openrouter <model>`."
            )
        return out

    if len(rest) < 2:
        raise CommandError(
            "OpenRouter needs an explicit model, e.g. "
            f"`{command} openrouter nvidia/nemotron-3-ultra:free`. There is no "
            "stable alias for the free tier. The free models are a rotating "
            "set of specific slugs, so naming one is the only way to know what "
            "reviewed the paper."
        )
    model = rest[1]
    if not _MODEL_SLUG_RE.match(model):
        raise CommandError(
            f"`{model}` does not look like an OpenRouter model. They are "
            "`vendor/model`, optionally with a `:tag`, for example "
            "`nvidia/nemotron-3-ultra:free`."
        )
    if len(rest) > 2:
        raise CommandError(
            f"`{command} openrouter <model>` takes exactly one model. Remove "
            "the extra text after the model slug."
        )
    out["model"] = model
    return out
