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

    import arxiv
    import rustypaper
    from peerreviewagents.default_config import get_config
    from peerreviewagents.graph.review_graph import PeerReviewGraph
    from peerreviewagents.ingest.loader import load_manuscript_record

    assert callable(PeerReviewGraph) and callable(load_manuscript_record)
    assert callable(arxiv.Client) and callable(rustypaper.convert)
    config = get_config(config_path=str(root / "peerreview.toml"))
    assert config["models"], "the production panel must retain its role-specific models"
    print(f"Verified {len(locked)} locked packages and the review runtime imports")


if __name__ == "__main__":
    main()
