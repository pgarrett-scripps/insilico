"""Verify the locked review environment without contacting a model provider."""
import re
from importlib.metadata import version
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    locked = dict(re.findall(r"^([a-zA-Z0-9_.-]+)==([^\s\\]+)",
                             (root / "requirements.txt").read_text(), re.MULTILINE))
    if not {"peerreviewagents", "rustypaper", "pyyaml"} <= locked.keys():
        raise RuntimeError("production lock is missing a direct dependency")
    for name, expected in locked.items():
        actual = version(name)
        if actual != expected:
            raise RuntimeError(f"{name}: expected {expected}, installed {actual}")

    import rustypaper

    # The engine is the whole pipeline now, so this imports what the reviews
    # actually run through. It used to import the LangGraph panel and assert the
    # role-specific models in peerreview.toml, both of which engine 0.8.0
    # deletes, and a lock naming a release with no engine package in it is
    # exactly what this check exists to catch.
    from peerreviewagents.engine.__main__ import build_parser
    from peerreviewagents.engine.bundle import plan_review

    assert callable(build_parser) and callable(plan_review)
    assert callable(rustypaper.convert)
    print(f"Verified {len(locked)} locked packages and the review runtime imports")


if __name__ == "__main__":
    main()
