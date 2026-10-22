# Publication bindings for 1.37.2

- Product/version branch/tag: 1.37.2 / 1.37.2 / v1.37.2; the formal product tag is in the source repository.
- Both repositories use dev as the development/default branch. The numeric branch serves the released product.
- Follow releases/current.json for the maintained installer, product catalog and complete-bundle manifest.
- The current complete bundle has 19 parts: 18 inherited immutable parts and one new tail part. Use the manifest order, URLs, byte counts and SHA-256.
- Runtime binaries remain 1.14.0; resource assets remain in their existing releases. No new binary release is needed.
- Generate all OS entries from the canonical templates and verify product-version bindings before packaging.
- Parse final loose assets and ZIP members, then verify Windows/Linux installation evidence separately from historical Math/export evidence.
- Preserve earlier product tags, published assets, private user data and global skills. Historical publisher scripts target their named releases only.
- Physical macOS qualification, reconstruction and Office editing are not established by the installer checks.
