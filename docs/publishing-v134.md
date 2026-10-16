# Publish the prepared v1.34.0 runtime

Use scripts/publish-v1.34.0.sh in the prepared release checkout. Its private
.lotraAI-build/publication/v1.34.0/Publish-plan.json binds both repository commits,
the single v1.34.0 tags, exact source/runtime assets and previous release branch
identities. Assets-root.txt can point at an existing local asset directory.

```sh
bash scripts/publish-v1.34.0.sh --check-local
bash scripts/publish-v1.34.0.sh --publish --jobs 2
```

The first command verifies selected local hashes without credentials, network
or uploads. The second uses existing GitHub credentials and uploads the prepared
runtime resources. A previously published matching source release is retained.
Re-run the same command after interruption. Matching remote assets are kept;
conflicting assets and changed tags/branches stop publication for inspection.
No historical release/tag/asset retirement is allowed by this version's plan.

Only after all declared assets match does the publisher publish the releases,
advance the stable installation branches without force, and independently check
public metadata and pinned channel resources. A successful result is PUBLISHED;
PUBLICATION_PENDING retains progress and the exact next action. The publisher
does not execute product tests, reconstruct art or create new capability claims.

Credentials stay in memory and are not saved in plans or command arguments.
Ordered full-bundle parts are materialized one at a time during upload; the
prepared full archive remains unchanged. Keep the prepared plan, asset directory
and source/runtime release checkouts available until publication is confirmed.
