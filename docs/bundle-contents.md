# Complete bundle contents

| Resource | Version / scope |
| --- | --- |
| Product and main skill | lotraAI Image2Slide 1.31.0 |
| Offline companion | 1.14.0; pinned dependency and OCR resources |
| Python | 3.12.15; Windows AMD64, Linux x86-64/aarch64, macOS x86-64/arm64 resources |
| Added Math editor | LibreOffice Math 26.2.6.3, Windows/Linux x86-64 |
| Installer | Project-local preparation followed by registration of one main skill |
| Integrity and provenance | Bundle manifest, nested manifests, engine inventories, upstream notices |

The present complete installer requires the supplied Math resource before publishing the skill. macOS and Linux ARM Python resources alone do not qualify those complete-installation routes. Actual host rendering and Office edit/save/reopen behavior remain separate checks.

The complete ZIP preserves all skill, runtime, engine, model, and renderer payload bytes from the source bundle. Packaging revision `github-publication-1` normalizes `installer/install.sh` to LF and updates `Bundle-manifest.json` and its internal checksum. Functional validation remains `NOT_RUN_PER_USER_REQUEST`.

The manifest copy in `manifests/v1.31.0/Bundle-manifest.json` describes paths inside the extracted ZIP. Only the complete bundle is a delivery artifact; no separate skill/runtime ZIP or SHA sidecar is produced for download.
