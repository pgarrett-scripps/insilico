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

    import peerreviewagents
    import rustypaper

    # What a review actually goes through in 0.9. The engine runs as a Claude
    # Code plugin, so the installed package's job is to start that run and to
    # read what it wrote: `review` runs one, `import_paper` ingests the
    # manuscript, `write_reports` renders the run folder. Those three are the
    # package's own public surface, and a lock naming a release that ships none
    # of them is exactly what this check exists to catch. It used to import
    # `peerreviewagents.engine`, which 0.9.0 deletes with no shim.
    for name in ("review", "import_paper", "write_reports"):
        assert callable(getattr(peerreviewagents, name)), f"{name} is not importable"

    # And the two commands the local-review skill tells an editor to run have to
    # be the two the installed console script offers. check_skill_commands.py
    # parses every command on that page against these same parsers. This only
    # asserts that the locked release has them.
    from peerreviewagents.cli.main import COMMANDS, report_parser
    from peerreviewagents.plugin.starter import build_parser as review_parser

    assert COMMANDS == ("review", "report"), f"unexpected engine commands: {COMMANDS}"
    assert callable(review_parser) and callable(report_parser)
    assert callable(rustypaper.convert)
    print(f"Verified {len(locked)} locked packages and the review runtime imports")


if __name__ == "__main__":
    main()
