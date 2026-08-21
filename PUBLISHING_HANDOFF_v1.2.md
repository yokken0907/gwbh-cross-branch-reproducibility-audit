# Publishing handoff - v1.2

This source tree is the publication-layer correction version. The frozen scientific baseline is v1.1.0.

## Required checks

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
python scripts/verify_post_closure_extensions.py
python scripts/scan_public_tree.py
python scripts/verify_release_assets.py /path/to/A01-A04
```

Expected: repository tree all PASS; key results 32/32 PASS; post-closure verification 59/59 PASS; public-tree scan PASS; A01-A04 identities PASS.

## GitHub publication sequence

1. Commit this exact v1.2 source tree to the default branch.
2. Do **not** move or overwrite the existing v1.1.0 tag.
3. Create a new immutable tag `v1.2` from the reviewed v1.2 commit.
4. If a GitHub Release object is desired, create a new v1.2 Release from that tag; do not replace historical Release v1.0.0.
5. A01/A02 remain v1.0.0 Release assets. A03/A04 remain independently versioned archives with their existing filenames and hashes.

## Scientific wording rule

U03/XR01 are within-product summary-to-full-posterior rank-association results. XR01 is a disjoint-cohort recurrence with a substituted middle model, not strict replication. Historical machine-readable calibration/transport labels remain frozen provenance identifiers.
