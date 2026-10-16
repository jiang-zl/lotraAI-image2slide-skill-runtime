#!/usr/bin/env bash
set -euo pipefail
script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(CDPATH= cd -- "${script_dir}/.." && pwd)"
state="${repo_root}/.lotraAI-build/publication/v1.34.0"
asset_root="${LOTRAAI_PUBLICATION_ASSETS:-${state}/assets}"
if [ -z "${LOTRAAI_PUBLICATION_ASSETS:-}" ] && [ -f "${state}/Assets-root.txt" ]; then
  IFS= read -r asset_root < "${state}/Assets-root.txt"
fi
if [ -n "${WSL_INTEROP:-}" ] && command -v py.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
  exec py.exe -3 -X utf8 -B "$(wslpath -w "${repo_root}/tools/publish_v134.py")" \
    --plan "$(wslpath -w "${state}/Publish-plan.json")" \
    --asset-root "$(wslpath -w "${asset_root}")" "$@"
fi
exec python3 -B "${repo_root}/tools/publish_v134.py" \
  --plan "${state}/Publish-plan.json" --asset-root "${asset_root}" "$@"
