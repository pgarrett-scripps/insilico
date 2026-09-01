#!/usr/bin/env bash
# Queue a re-review of every published paper under the current pipeline.
#
# Dispatches one review.yml run per URL with `/review replace`, so a draft we
# already reviewed is overwritten by a fresh run and a draft the archive has
# since updated becomes a new round instead (replace never crosses drafts).
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
  gh workflow run review.yml -f url="$url" -f command="/review replace"
  if [ "$url" != "${URLS[-1]}" ]; then
    sleep "$STAGGER"
  fi
done

echo "all dispatched — watch with: gh run list --workflow review.yml"
