"""Verify the locked review environment without contacting a model provider."""
import json
import re
from importlib.metadata import Distribution, version
from pathlib import Path

ENGINE = "peerreviewagents"
# The engine is not on PyPI, so it is pinned to the GitHub archive of one
# commit rather than to a release number. Both files name that archive, and the
# installed distribution records the URL it was built from, so the three can be
# held against each other.
ARCHIVE = re.compile(rf"^{ENGINE} @ (\S+)", re.MULTILINE)


def archive_url(path: Path) -> str:
    found = ARCHIVE.findall(path.read_text())
    if len(found) != 1:
        raise RuntimeError(f"{path.name} names {len(found)} {ENGINE} archives, expected one")
    return found[0]


def installed_archive() -> str:
    """The URL pip built the installed engine from, as pip recorded it."""
    recorded = Distribution.from_name(ENGINE).read_text("direct_url.json")
    if not recorded:
        raise RuntimeError(
            f"the installed {ENGINE} carries no direct_url.json, so it did not "
            "come from the archive the lock pins. Reinstall from requirements.txt."
        )
    return str(json.loads(recorded).get("url") or "")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    locked = dict(re.findall(r"^([a-zA-Z0-9_.-]+)==([^\s\\]+)",
                             (root / "requirements.txt").read_text(), re.MULTILINE))
    if not {"rustypaper", "pyyaml"} <= locked.keys():
        raise RuntimeError("production lock is missing a direct dependency")
    for name, expected in locked.items():
        actual = version(name)
        if actual != expected:
            raise RuntimeError(f"{name}: expected {expected}, installed {actual}")

    declared = archive_url(root / "requirements.in")
    pinned = archive_url(root / "requirements.txt")
    if declared != pinned:
        raise RuntimeError(f"{ENGINE}: requirements.in asks for {declared}, lock pins {pinned}")
    built_from = installed_archive()
    if built_from != pinned:
        raise RuntimeError(f"{ENGINE}: lock pins {pinned}, installed build came from {built_from}")

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
    # asserts that the locked release has them, and it asks for them by their
    # public names: 0.9 exports both parsers and the command list, so nothing
    # here imports `peerreviewagents.cli` or `peerreviewagents.plugin`, which
    # are the engine's own internals and free to move between releases.
    from peerreviewagents import CLI_COMMANDS, report_parser, review_parser

    assert CLI_COMMANDS == ("review", "report"), f"unexpected engine commands: {CLI_COMMANDS}"
    assert callable(review_parser) and callable(report_parser)
    assert callable(rustypaper.convert)
    print(f"Verified {len(locked)} locked packages, the engine built from "
          f"{pinned.rsplit('/', 1)[-1]}, and the review runtime imports")


if __name__ == "__main__":
    main()
