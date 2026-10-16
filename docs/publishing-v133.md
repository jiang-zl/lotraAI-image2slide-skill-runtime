# Publish the prepared v1.33.0 release from WSL/Linux

From the runtime repository, run:

```sh
bash scripts/publish-v1.33.0.sh --publish
```

Prepare .lotraAI-build/publication/v1.33.0-single/Publish-plan.json and its
asset directory first. The optional private Assets-root.txt selects an existing
asset directory without copying it. The plan fixes repositories, commits,
asset sizes/digests and exact obsolete same-version release/tag identities.
Credentials come from an existing Git credential helper, gh or process-local
GH_TOKEN/GITHUB_TOKEN; no credential belongs in a plan or upload log.

The publisher skips exact uploaded assets and retries failed transfers within
finite limits. The complete ZIP is read as 18 slices; only the active upload
piece needs temporary disk space. Rerun the same command after interruption.
After every declared resource matches, it publishes release notes, activates
the release branches and removes the exact obsolete v1.33.0-install-r* releases
and tags captured by the prepared plan. Other versions are preserved.

On WSL, when py.exe is already available, the Bash entry runs the same WSL-hosted
publisher through the Windows Python launcher and cURL. This reuses the host
network path while preserving code, plan, progress and upload inputs in their
prepared locations. Native Linux uses python3 and cURL. No system proxy is
changed. Run a single publisher instance at a time.

After publishing, the uploader checks anonymous release metadata and downloads
the public installation entry, catalog and complete-bundle manifest to verify
their identities. Auxiliary releases/tags are retired only after that public
check succeeds. This does not run product reconstruction.
