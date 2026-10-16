#!/usr/bin/env bash
set -euo pipefail
script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(CDPATH= cd -- "${script_dir}/.." && pwd)"
state="${repo_root}/.lotraAI-build/publication/v1.33.0-single"
asset_root="${LOTRAAI_PUBLICATION_ASSETS:-${state}/assets}"
if [ -z "${LOTRAAI_PUBLICATION_ASSETS:-}" ] && [ -f "${state}/Assets-root.txt" ]; then
  IFS= read -r asset_root < "${state}/Assets-root.txt"
fi
exec python3 -B "${repo_root}/tools/publish_v133.py" \
  --plan "${state}/Publish-plan.json" --asset-root "${asset_root}" "$@"
