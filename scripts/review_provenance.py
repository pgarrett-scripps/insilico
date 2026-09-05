"""Record software identity and public review configuration."""
from __future__ import annotations

import hashlib
import json
import os
import platform
from importlib.metadata import distributions
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from review_paths import REPO


def environment_record() -> dict:
    """Record versions without publishing paths, package URLs, or environment variables."""
    packages = {
        dist.metadata["Name"]: dist.version
        for dist in distributions()
        if dist.metadata.get("Name")
    }
    lock = REPO / "requirements.txt"
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "packages": dict(sorted(packages.items())),
        "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None,
        "lock_applied": os.environ.get("INSILICO_LOCKED_ENVIRONMENT") == "true",
    }


def pipeline_version() -> dict[str, str]:
    """Identify exactly which referee panel produced a review.

    Production installs an immutable package release, so its version is the
    reproducibility identifier. Local editable installs also record the Git
    revision when one is available, which distinguishes worktree experiments
    made before a release exists.
    """
    info = {"sha": os.environ.get("PEERREVIEW_PIPELINE_SHA", "")}
    if not info["sha"]:
        info["sha"] = _installed_pipeline_sha()
    try:
        from importlib.metadata import version

        info["version"] = version("peerreviewagents")
    except Exception:  # noqa: BLE001 - metadata is best-effort
        info["version"] = "unknown"
    return info


def insilico_version() -> dict[str, str]:
    """Identify the journal code and configuration that launched the run."""
    sha = os.environ.get("GITHUB_SHA", "").strip()
    dirty = ""
    try:
        import subprocess  # noqa: PLC0415

        if not sha:
            sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO,
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return {"sha": f"{sha}+dirty" if sha and dirty else sha or "unknown"}


_PUBLIC_CONFIG_KEYS = {
    "agent_models",
    "article_type",
    "cache_ttl",
    "caveman",
    "conversion_gate",
    "data_vendors",
    "desk_screen",
    "desk_screen_mode",
    "enable_debate",
    "enable_journal_recommender",
    "manuscript_char_budget",
    "markdown_attempts",
    "max_debate_rounds",
    "max_node_cost_usd",
    "max_output_tokens",
    "max_rounds",
    "models",
    "only_reviewers",
    "openai_base_url",
    "panel_quorum_fraction",
    "provider",
    "reasoning_model",
    "request_timeout_s",
    "research_enabled",
    "review_strictness",
    "revision_mode",
    "single_model",
    "synthesis_word_budget",
    "target_journal",
    "temperature",
    "tool_vendors",
}


def _public_url(value: object) -> str | None:
    """Return a reproducible endpoint without credentials or query data."""
    if value in (None, ""):
        return None
    try:
        parsed = urlsplit(str(value))
        host = parsed.hostname
        if not parsed.scheme or not host:
            return None
        display_host = f"[{host}]" if ":" in host else host
        netloc = f"{display_host}:{parsed.port}" if parsed.port else display_host
        return urlunsplit((parsed.scheme.lower(), netloc, parsed.path, "", ""))
    except ValueError:
        return None


def _public_config_value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        try:
            return str(value.resolve().relative_to(REPO))
        except ValueError:
            return str(value)
    if isinstance(value, dict):
        return {
            str(key): _public_config_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if not any(
                secret in str(key).lower()
                for secret in ("key", "token", "secret", "password")
            )
        }
    if isinstance(value, (list, tuple)):
        return [_public_config_value(item) for item in value]
    return str(value)


def configuration_record(config: dict | None) -> dict:
    """Canonical public configuration, excluding paths and undeclared fields."""
    public = {
        key: _public_config_value(value)
        for key, value in sorted((config or {}).items())
        if key in _PUBLIC_CONFIG_KEYS and key != "openai_base_url"
    }
    if "openai_base_url" in (config or {}):
        public["openai_base_url"] = _public_url(config["openai_base_url"])
    encoded = json.dumps(
        public,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "resolved": public}


def journal_profile_record(config: dict | None) -> dict:
    """Hash the exact local journal profile supplied to the panel."""
    config = config or {}
    journal = str(config.get("target_journal") or "")
    directory = Path(config.get("journals_dir") or REPO / "journals")
    if not directory.is_absolute():
        directory = REPO / directory
    path = directory / f"{journal}.toml"
    if not journal or not path.is_file():
        return {"journal": journal, "sha256": ""}
    return {
        "journal": journal,
        "path": str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _installed_pipeline_sha() -> str:
    """HEAD of the checkout the installed pipeline is imported from, or ''.

    Marked ``+dirty`` when that checkout has uncommitted changes, because a
    rerun against a working tree is exactly when the sha alone would lie: two
    reviews would name the same commit while running different code.
    """
    try:
        import subprocess  # noqa: PLC0415 - only needed on this path

        import peerreviewagents

        repo = Path(peerreviewagents.__file__).resolve().parent.parent
        if not (repo / ".git").exists():
            return ""
        run = lambda *a: subprocess.run(  # noqa: E731
            a, cwd=repo, capture_output=True, text=True, timeout=5, check=True
        ).stdout.strip()
        sha = run("git", "rev-parse", "HEAD")
        dirty = run("git", "status", "--porcelain")
        return f"{sha}+dirty" if dirty else sha
    except Exception:  # noqa: BLE001 - identification is best-effort
        return ""
