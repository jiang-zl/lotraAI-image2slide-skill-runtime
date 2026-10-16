# Complete bundle and online resources

| Resource | Version / scope |
| --- | --- |
| Product and main skill | lotraAI Image2Slide 1.33.0 |
| Offline companion | 1.14.0; pinned dependencies and OCR resources |
| Python | 3.12.15; Windows AMD64, Linux x86-64/aarch64, macOS x86-64/arm64 |
| Math | Windows/Linux x86-64 bundled; macOS 13+ pinned official DMG download |
| Installer | One shared project-local installation and managed differential update core |
| Integrity | Bundle/catalog manifests, engine inventories, pinned byte counts and SHA-256 |

The complete ZIP is transported as 18 ordered pieces, each at most 128 MiB.
Its skill, Python engines, dependency wheels, OCR models and Windows/Linux Math
resources are included. macOS Math is obtained separately on first installation.
Linux ARM64 has core resources but lacks the complete Math package; installation
stops before registering a complete skill on an unsupported complete route.

Online installation selects only the current platform. Managed differential
updates add, replace and delete owned files, retaining unchanged bytes and
private knowledge, fonts, tasks and sources. The selected runtime binary version
is independent of the product version. See releases/v1.33.0.json and
releases/v1.33.0-bundle.json for exact current resources, hashes and download URLs.
Installation checks and reconstruction acceptance are described separately in
[release status](release-status.md).
