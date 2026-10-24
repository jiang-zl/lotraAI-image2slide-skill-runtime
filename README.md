# lotraAI bundle and runtime distribution


<!-- workflow-v137:start -->
1.37.5 remains a portable skill: project-local `start → next → submit` packets,
incremental original observation/binding, complete quality gates and formal export.
A checkpoint or native build is not an accepted result. Use `delivery-check` for
the current task and exact final PPTX bytes. No replacement harness, resident
service or extra model key is required; an optional checker does not control a
third-party harness's reply.
1.37.5 integrates incident recovery, actual font identities, source-only observation diagnostics, short-branch paint checks, logical text and editable effects, first-render local review, and explicit capture-target mapping. Complete source, render and accepted-delivery gates remain required.
<!-- workflow-v137:end -->

Prefer a qualified local PowerPoint/WPS backend, with optional LibreOffice fallback. Every final file gets actual export/save checks; user-selected output roots default to the project directory. Runtime 1.14.0 binaries are reused. Physical WPS/macOS qualification requires the corresponding host.



**Current product release: 1.37.5** · Development/default branch: `dev` · Version branch: `1.37.5`

Publication uses dev and 1.37.5. Runtime binaries remain 1.14.0; unchanged platform resources remain in the existing `v1.34.0` resource release. The formal product tag is `v1.37.5`. Branches use `dev` or `X.Y.Z`; tags use `vX.Y.Z` without extra suffixes.

This release has current Windows/Linux regression, installation and authored-task delivery evidence. The official DeepSeek incident run reached an actual native/rendered checkpoint and closed the current arrow diagnosis; whole-artwork acceptance/export were deferred at the human's request. See the release and validation reports for scope and retained failures. Actual public README and bundle-download first/repeat checks are recorded after publication.

[English](README.md) · [简体中文](README.zh-CN.md)

This repository distributes the complete lotraAI bundle and platform runtime resources, and maintains automatic installation, differential updates and download manifests. Product documentation, examples and skill source are in the [main repository](https://github.com/jiang-zl/lotraAI-image2slide-skill).

## Current complete bundle: 1.37.5

The complete file is `lotraAI-image2slide-v1.37.5-bundle.zip`, including the skill and the currently bundled resources. Its size, SHA-256 and ordered parts are recorded in the [bundle manifest](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/download/v1.37.5/v1.37.5-bundle.json).

Resources cover Windows x64, Linux x64, and macOS on Apple Silicon and Intel. macOS requires 13 or later; when LibreOffice fallback is needed its Math DMG is downloaded separately and is not embedded in the complete bundle. Linux ARM64 has core resources but lacks a complete Math package. See the [installation guide](docs/installation.md).

## Quick Start

### 1. Ask Codex to install or update

Send this one sentence in your working project. You do not need to download the complete bundle first:

~~~text
Install or update lotraAI Image2Slide in this project from https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime.
~~~

Codex runs the maintained entry for your platform, prepares project-local resources and registers the single `lotra-image2slide-skill`. The program handles downloads, resume, verification and part assembly. An existing installation prefers the entry recorded in `.lotraAI-build/install-entry/Launcher.json`; first-install entries are described in the [installation guide](docs/installation.md).

Already have the complete ZIP? Supply the file or its absolute local path, then send:

~~~text
Install or update Image2Slide in this project using the supplied lotraAI-image2slide-v1.37.5-bundle.zip.
~~~

### 2. Attach a reference image and start reconstructing

~~~text
Use $lotra-image2slide-skill to rebuild this image as an editable PPT.
~~~

Runtime resources and private task state live in the project's `.lotraAI-build` directory. See the [main repository](https://github.com/jiang-zl/lotraAI-image2slide-skill) for usage and examples.

## Download and install by operating system

Alternatively, open a terminal in your Image2Slide working project and run the command for your system. The entry selects the operating system and architecture automatically and serves both first installation and updates.

**Windows (PowerShell)**

```powershell
$url = 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.ps1'
curl.exe -fL --retry 2 --connect-timeout 20 $url -o install-lotra.ps1
if ($LASTEXITCODE -eq 7) { curl.exe --noproxy '*' -fL --retry 2 --connect-timeout 20 $url -o install-lotra.ps1 }
if ($LASTEXITCODE -eq 0) { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-lotra.ps1 -Project (Get-Location).Path }
```

**macOS (Terminal, Apple Silicon / Intel)**

```sh
curl -fL --retry 2 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.sh' -o install-lotra.sh && sh install-lotra.sh "$PWD"
```

**Linux / WSL (Terminal)**

```sh
curl -fL --retry 2 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.sh' -o install-lotra.sh && sh install-lotra.sh "$PWD"
```

The skill package also includes `scripts/install-runtime.ps1` and `scripts/install-runtime.sh` to prepare or update a chosen project's runtime. All entries share the same installer, resource verification, cache and differential synchronization. See the installation guide for arguments and installation from an extracted bundle.

## Download and assemble

To keep a complete copy, give Codex this repository URL and send:

~~~text
Download the complete lotraAI Image2Slide installation bundle into this project.
~~~

The [1.37.5 bundle release](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/tag/v1.37.5) provides 19 parts (`.part001` through `.part019`, up to 128 MiB each), ordered byte segments of the same ZIP. The program follows the manifest, verifies each part, reassembles the archive and checks the complete SHA-256 before exposing the final ZIP. Interrupted downloads retain resumable progress.

Downloading and installation share the maintained program and content cache. An extracted bundle can use its bundled installer to enter the same installation flow. See [complete bundles and local installation](docs/installation.md#complete-bundles-and-local-installation) for commands.

## Differential updates

Use the same Quick Start sentence to update. New files are added, changed files replaced and retired managed files removed. Unchanged active files are neither downloaded nor rewritten. Identical content is reused when paths change, and routine updates do not require the complete bundle again.

Your knowledge library, fonts, tasks, originals, PPTs and global skills are preserved. User-modified or unrecognized files are retained and reported as conflicts; cleanup applies only to owned managed files.

[Installation](docs/installation.md) · [1.37.5 installation catalog](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/download/v1.37.5/release.json) · [Provenance](NOTICE.md) · [Release and evidence notes](docs/release-status.md)

## Local applications and output location

Backend selection uses actual PDF/edit/save/reopen capability, not installation detection. Windows PowerPoint is qualified on the tested host; WPS and the macOS PowerPoint adapter require their own host probe. Native Math remains editable OMML. LibreOffice fallback uses an owned private TEMP/profile and never counts a PNG as a successful PDF.

Tell the agent “save to DIRECTORY”; otherwise the project is the output root. Each export creates `output-slide-YYYY-MM-DD-HHMMSS-mmm`, containing `Final_editable.pptx` and `Report.md`. Private task/probe data remains in `.lotraAI-build`. The project launcher provides `presentation-backend --project PROJECT`, `presentation-backend --project PROJECT --backend powerpoint --save-preferences`, `export TASK --output-root DIRECTORY`, and `validate-presentation FILE --project PROJECT --out NEW_AUDIT_DIRECTORY`. An unavailable explicit backend reports its exact failure. Existing files are preserved.
