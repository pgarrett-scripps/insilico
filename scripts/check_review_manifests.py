"""Verify artifact hashes for review bundles that publish a manifest.

Legacy bundles predate manifests and remain valid. Every new bundle includes
one, so a changed, missing, or unlisted artifact fails its review pull request.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REVIEWS = REPO / "docs" / "reviews"


def verify(manifest_path: Path) -> list[str]:
    bundle = manifest_path.parent
    label = bundle.relative_to(REPO)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{label}: unreadable manifest ({exc})"]

    expected = manifest.get("files")
    if manifest.get("schema_version") != 1 or not isinstance(expected, dict):
        return [f"{label}: unsupported or malformed manifest"]

    # Every file under the bundle but the manifest itself, named the way the
    # manifest names it: a path relative to the bundle. Published bundles are
    # flat, so this reads the same files the old listing of the top level did.
    # Walking is what keeps a file written into a subfolder from being the one
    # artifact no digest covers, which is also why the manifest excludes itself
    # by path rather than by name.
    actual_names = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file() and path != manifest_path
    }
    expected_names = set(expected)
    errors = [
        f"{label}: artifact list differs, expected {sorted(expected_names)}, "
        f"found {sorted(actual_names)}"
    ] if actual_names != expected_names else []

    for name in sorted(actual_names & expected_names):
        digest = hashlib.sha256((bundle / name).read_bytes()).hexdigest()
        if digest != expected[name]:
            errors.append(f"{label}: SHA-256 mismatch for {name}")
    return errors


def main() -> int:
    manifests = sorted(REVIEWS.glob("**/manifest.json"))
    errors = [error for path in manifests for error in verify(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Verified {len(manifests)} review artifact manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
