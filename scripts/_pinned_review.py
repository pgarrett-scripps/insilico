"""Review a specific arXiv version rather than the current one. Testing only.

`resolve()` deliberately always returns the *latest* version of a preprint,
because a review has to describe what is actually posted now. That is correct
in production and makes the revision pipeline impossible to exercise: to test
a v1 -> v2 round you have to first hold a review of v1, and by the time v2
exists the resolver will only ever hand you v2.

This pins the version for the first leg of that test. It changes nothing about
how a review is produced — the pinned Preprint goes through the ordinary
run_review path — so what it exercises is the real bundle writer, the real
round record, and afterwards the real `--revise` flow resolving forward to v2
and diffing against the recorded v1 bytes.

Not wired into the CLI on purpose. Reviewing a stale revision is a thing to do
deliberately in a test, not an option an editor should find sitting on the
production command.

    python scripts/_pinned_review.py 2607.24356 1
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import run_review  # noqa: E402
from fetch_preprint import resolve as _real_resolve  # noqa: E402


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    arxiv_id, want = sys.argv[1], sys.argv[2]

    def pinned(url: str):
        pp = _real_resolve(url)
        latest = pp.version
        pp.version = want
        pp.pdf_url = f"https://arxiv.org/pdf/{arxiv_id}v{want}"
        pp.url = f"https://arxiv.org/abs/{arxiv_id}"
        print(
            f"pinned    v{want} (latest is v{latest or '?'}) — {pp.pdf_url}",
            file=sys.stderr,
        )
        return pp

    run_review.resolve = pinned
    sys.argv = [
        "run_review.py",
        "--url", f"https://arxiv.org/abs/{arxiv_id}",
        "--submitter", "insilico-test",
        "--submitter-is-author", "no",
    ] + sys.argv[3:]
    return run_review.main()


if __name__ == "__main__":
    raise SystemExit(main())
