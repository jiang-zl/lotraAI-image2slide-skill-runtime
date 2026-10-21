# Publishing

The current product publication is 1.37.1. Use [publication bindings](publication-checklist.md)
and releases/current.json for the current version and immutable content identities.
Both repositories use dev and the numeric version branch; the product's formal
vX.Y.Z tag and small installation assets are in the source repository.

The complete bundle has 19 manifest-ordered parts. Its 18 unchanged parts and
existing runtime resources are reused at their original URLs. Runtime binaries
remain 1.14.0. Generate entries, validate final distributed bytes and check the
published catalog, hashes and installation commands before channel activation.

The publish_v133.py/publish_v134.py programs and their versioned guides are
historical publishers for those releases. They are not the current publication
command. Prepared plans and binary upload inputs remain private in .lotraAI-build.
Never infer a current installation PASS from an older receipt.
