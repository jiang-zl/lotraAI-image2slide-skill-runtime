# Complete bundle and online resources

| Resource | Version / scope |
| --- | --- |
| Product and main skill | lotraAI Image2Slide 1.37.4 |
| Offline companion | 1.14.0; pinned dependencies and OCR resources |
| Python | 3.12.15; Windows AMD64, Linux x86-64/aarch64, macOS x86-64/arm64 |
| Math | Windows/Linux x86-64 bundled; macOS 13+ pinned official DMG download |
| Installer | One shared project-local installation and managed differential update core |
| Integrity | Bundle/catalog manifests, engine inventories, pinned byte counts and SHA-256 |

The complete ZIP is transported as 19 ordered pieces, each at most 128 MiB.
Its skill, Python engines, dependency wheels, OCR models and Windows/Linux Math
resources are included. macOS Math is obtained separately when LibreOffice fallback is needed. Qualified local Office can satisfy Math/render/save without that download.
Linux ARM64 has core resources but lacks the complete Math package; installation
stops before registering a complete skill on an unsupported complete route.

Online installation selects only the current platform. Managed differential
updates add, replace and delete owned files, retaining unchanged bytes and
private knowledge, fonts, tasks and sources. The selected runtime binary version
is independent of the product version. Follow releases/current.json for the current product catalog and bundle
manifest. Resource records may retain earlier immutable release URLs when their
bytes are unchanged. Historical releases/v*.json files are not the current channel.
Installation checks and reconstruction acceptance are described separately in
[release status](release-status.md).
