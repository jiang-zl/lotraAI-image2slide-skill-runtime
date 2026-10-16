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
