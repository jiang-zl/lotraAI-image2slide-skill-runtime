# lotraAI bundle distribution

[English](README.md) · [简体中文](README.zh-CN.md)

This repository distributes the complete lotraAI bundle and its version manifests. Product documentation, examples, and skill source are in the [main repository](https://github.com/jiang-zl/lotraAI-image2slide-skill).

## Current release: v1.31.0


The complete file is `lotraAI-image2slide-v1.31.0-bundle.zip` (2,414,649,382 bytes), including the skill and all supplied runtime resources. SHA-256: `200f65a42b96dca2a0143f43f1c3583d5150958ae1fc7ac8c6dea41969fbe657`.

## Download and assemble

Open the [v1.31.0 bundle release](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/tag/v1.31.0). Its three `.part001` / `.part002` / `.part003` assets are ordered byte segments of the same complete ZIP. Save the release's [download helper](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/download/v1.31.0/fetch_bundle.py), then run:

~~~sh
python3 fetch_bundle.py --output-dir ./downloads
~~~

On Windows, use `py fetch_bundle.py --output-dir .\downloads`. The helper reads the [version manifest](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/download/v1.31.0/v1.31.0.json), checks every part, reassembles the ZIP, and verifies the complete SHA-256 before publishing the output file. Existing different files are preserved.

You can give Codex the [release URL](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/tag/v1.31.0) and ask it to use the manifest and helper to obtain the complete bundle, then extract and install it. An already assembled ZIP can be handed directly to Codex.

The only assembled delivery archive is `lotraAI-image2slide-v1.31.0-bundle.zip`. Transport preserves every archived file and payload. Part sizes follow [GitHub's per-asset limit](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases#storage-and-bandwidth-quotas).

## Quick Start

### 1. Give Codex the complete bundle

Download `lotraAI-image2slide-v1.31.0-bundle.zip`. It includes both the skill and runtime resources (Python, dependencies, OCR, and Math). Place the ZIP in the current project where Codex can access it, or provide its absolute local path in the conversation. You can leave the ZIP unextracted.

### 2. Ask Codex to install it

Send this prompt to Codex:

~~~bash
Please extract the complete lotraAI-image2slide-v1.31.0-bundle.zip I provided.
Use its bundled installer to install the skill into the current project,
named lotra-image2slide-skill. Prepare the included runtime resources
(Python, dependencies, OCR, and Math) before registering the main skill.
When finished, report the skill entry and runtime readiness.
~~~

Codex uses the bundled installer for the current platform, prepares the project-local runtime, and then registers the single `lotra-image2slide-skill`. Runtime resources and private task state live in the project's `.lotraAI-build` directory.

After installation, attach a reference image in the same project and ask Codex to use `$lotra-image2slide-skill`. Manual installation commands remain in the main `lotraAI` repository's installation guide.

[Bundle contents](docs/bundle-contents.md) · [v1.31.0 manifest](releases/v1.31.0.json) · [Provenance](NOTICE.md) · [Publication checklist](docs/publication-checklist.md)
