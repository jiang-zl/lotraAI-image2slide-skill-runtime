# Installation and updates

[简体中文](installation.zh-CN.md) · [Back to README](../README.md)

## Recommended route

Send this in your Codex working project:

> Install or update lotraAI Image2Slide in this project from https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime.

For an existing installation, prefer `.lotraAI-build/install-entry/Launcher.json`. On first installation, the platform entry prepares private Python when needed and calls the common installer. Resource preparation precedes registration of the single main skill at `.agents/skills/lotra-image2slide-skill/SKILL.md`.

You do not need to preinstall global Python, run global pip or supply another model API key. Codex and your PPTX viewing/editing software are provided separately.

## Run an entry manually

Run the following from a directory containing this repository's files. Replace the example with an **existing working project directory**, rather than your home directory or a filesystem root.

Windows PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_lotra.ps1 -Project 'C:\work\my-project'
```

macOS / Linux / WSL:

```sh
sh tools/install_lotra.sh '/absolute/path/to/my-project'
```

Use the same entry to update. It adds new files, replaces changed files and removes retired managed files. Unchanged active files are neither downloaded nor rewritten. User-modified or unrecognized files are preserved and reported as conflicts. Personal knowledge, fonts, tasks, originals, PPTs and global skills are preserved.

## Complete bundles and local installation

The complete bundle consists of 18 ordered, manifest-defined parts. The downloader handles resume, per-part verification, assembly and whole-archive verification. To download into a chosen directory:

Windows:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_lotra.ps1 -Project 'C:\work\my-project' -DownloadBundle 'C:\downloads\lotraAI'
```

macOS / Linux / WSL:

```sh
sh tools/install_lotra.sh '/absolute/path/to/my-project' --download-bundle '/absolute/path/to/downloads'
```

For an extracted bundle, run its local entry from the **extracted bundle root**:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\install.ps1 -Project 'C:\work\my-project'
```

```sh
sh installer/install.sh '/absolute/path/to/my-project'
```

The recorded Python installation entry also accepts `--bundle-root EXTRACTED_ROOT`. These routes share the same differential coordinator and content cache.

The complete resources include the Windows/Linux x64 Math packages. macOS Math uses a separate initial online DMG download, which is not embedded in the complete bundle. Preparing a fresh macOS environment still requires that download.

## Platform requirements

- Windows: AMD64 / x64 resources are supplied.
- Linux / WSL: x64 has core and Math resources. Use a case-sensitive project filesystem; in WSL, a dedicated directory under the Linux user's home is suitable.
- macOS: 13 or later, with separate Apple Silicon and Intel resource routes.
- Linux ARM64: core resources are available, but the complete Math package is missing. The current full installer stops before main-skill registration and explains the limitation.

Platform coverage describes supplied resources, not completed hardware qualification for this version. See [release and evidence notes](release-status.md).

## Read the installation result

The program returns a compact summary and keeps detailed records in the project's `.lotraAI-build` directory:

| File | Purpose |
| --- | --- |
| `install-entry/Launcher.json` | Entry for later installation, updates and complete-bundle downloads |
| `Active-skill.json` | Currently selected skill |
| `Bundle-install.json` | Facts about prepared runtime resources and capabilities |

`core_ready`, `render_ready`, `native_edit_ready` and acceptance of a particular reconstruction are separate records. Completing installation does not establish the quality of a rebuilt figure.

When Codex performs the work, prefer the entry and compact result. Read the relevant detailed log only for a specific error, without expanding all manifests, cache contents and logs into the conversation.
