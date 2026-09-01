#!/usr/bin/env bash
# Queue a review of every paper in the launch corpus under the current
# pipeline. The corpus was cleared before the 0.5.0 batch, so each run is a
# fresh first review; if a bundle for the current draft already exists, pass
# "/review replace" as the command input instead.
#
# Dispatches are staggered so a dozen panels do not hit the API rate limit at
# once; runs still overlap, which is fine.
#
# Usage: scripts/queue_rereviews.sh [stagger-seconds]
# Requires: gh authenticated with workflow scope on this repo.
set -euo pipefail

STAGGER="${1:-180}"

URLS=(
  https://www.biorxiv.org/content/10.1101/2024.09.04.611121v1
  https://www.biorxiv.org/content/10.1101/2025.10.25.684498v1
  https://www.biorxiv.org/content/10.1101/2025.01.06.631593v1
  https://www.biorxiv.org/content/10.1101/2025.11.10.687295v1
  https://www.biorxiv.org/content/10.64898/2026.06.19.733273v1
  https://arxiv.org/abs/2607.14410
  https://www.biorxiv.org/content/10.64898/2026.05.13.724352v1
  https://arxiv.org/abs/2607.19161
  https://arxiv.org/abs/2607.24356
  https://www.biorxiv.org/content/10.1101/2025.09.15.675920v1
  https://www.biorxiv.org/content/10.64898/2026.06.30.735694v1
  https://www.biorxiv.org/content/10.64898/2026.02.13.705817v2
  https://www.biorxiv.org/content/10.64898/2026.06.11.731363v1
)

for url in "${URLS[@]}"; do
  echo "dispatching: $url"
  gh workflow run review.yml -f url="$url"
  if [ "$url" != "${URLS[-1]}" ]; then
    sleep "$STAGGER"
  fi
done

echo "all dispatched — watch with: gh run list --workflow review.yml"
