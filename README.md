# lotraAI runtime and automatic installation

**English** | [简体中文](README.zh-CN.md)

## Quick start

> Install or update lotraAI Image2Slide in this project from https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime.

Codex downloads and runs the official program. The same sentence covers installation and file-differential updates.

## Agent entry

Use `.lotraAI-build/install-entry/Launcher.json` when present. Otherwise obtain `tools/install_lotra.ps1` for Windows or `tools/install_lotra.sh` for macOS/Linux from this repository's `release` branch and run it with the project path. It selects the platform, prepares private Python if needed, reads `releases/current.json` and calls the common installer. Do not recreate download scripts or print full manifests/logs.

## Complete bundle

The complete bundle remains split into ordered parts of at most 128 MiB. The current part count and identities are recorded in the [bundle manifest](releases/v1.33.0-bundle.json). Parts are transport units; the program checks every part and the whole archive before exposing the final ZIP. It preserves verified cache entries and owned partial downloads across retries.

Ask Codex to download the complete bundle when you need local installation or an offline copy. The existing installation entry supports `--download-bundle OUTPUT_DIR`; Windows bootstrap uses `-DownloadBundle OUTPUT_DIR`, and the shell bootstrap accepts `PROJECT --download-bundle OUTPUT_DIR`. `tools/fetch_bundle.py --project PROJECT --output-dir OUTPUT_DIR` delegates to the same entry under prepared Python 3.12.

For a supplied extracted bundle, use its `installer/install.ps1 -Project PROJECT` or `sh installer/install.sh PROJECT`. The recorded Python entry also accepts `--bundle-root EXTRACTED_ROOT`. All routes use the same differential coordinator. macOS Math is fetched separately on first preparation; the full bundle includes the existing Windows/Linux Math packages, not the macOS DMGs.

## Maintainer publication

Prepared releases include `Publish-v1.33.0.ps1`, `Publish-v1.33.0.sh`, `publish_lotra.py` and an exact `Publish-plan.json`. The program skips matching uploaded assets, retries only failed parts and switches the current branches only after all required assets are present. See [publication instructions](docs/publishing-v133.md).

First installation selects the current operating system and architecture. Large resource packages can use resumable, verified parts that the program merges automatically. Existing installations use managed file manifests: add new files, replace changed files, remove retired owned files and retain unchanged active files without downloading or rewriting them. Matching content is reused across renamed paths. Personal knowledge, fonts, tasks, source images and PPTs remain private in `.lotraAI-build`.

A complete bundle remains available as ordered parts for local installation, offline storage and recovery. It uses the same maintained downloader and content cache; updates do not require downloading the full bundle. See [runtime installation and complete bundles](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime).

## Platforms and release scope

Product version remains **1.33.0**. Python/OCR resources cover Windows AMD64, Linux x86_64/aarch64 and macOS Apple Silicon/Intel. Complete Math preparation has resource routes for Windows AMD64, Linux x86_64 and both macOS architectures. macOS requires 13 or later and downloads its pinned Math disk image once; that disk image is not included in the complete bundle. Linux ARM64 has core resources but no supplied complete Math package; the installer reports that limitation.

This update was implemented and reviewed statically. Product tests, syntax/import/CLI checks, installation runs, reconstruction/rendering and performance/effect measurements were not run, as requested. Publication hashes identify distribution bytes and do not establish runtime or reconstruction acceptance. Historical tags and archives are retained.

See [workflow details](https://github.com/jiang-zl/lotraAI-image2slide-skill/blob/release/skills/lotra-image2slide-skill/references/workflow-v133.md).
