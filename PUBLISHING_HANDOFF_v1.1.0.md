# Publishing handoff — v1.1.0 candidate

This handoff is procedural. No GitHub commit, tag, release, DOI deposition, or external overwrite was performed during package generation.

## Pre-publication checks

Run from the repository root:

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
python scripts/verify_post_closure_extensions.py
python scripts/scan_public_tree.py
```

Expected summaries:

- repository tree: all manifest payloads PASS;
- key results: 32/32 PASS;
- post-closure verification: 59/59 PASS;
- local-path/secret/temp scan: PASS.

Verify the repository-source ZIP and candidate A03/A04 assets against the sidecars supplied in the outer paper set before upload. A01/A02 are historical immutable assets and must not be rebuilt or renamed.

```bash
python scripts/verify_release_assets.py --post-closure-only /path/to/A03-A04-review-assets
```

## Suggested publication sequence

1. Review the four v1.1.0 manuscript/Supplement A–C PDF and DOCX pairs and Supplement D.
2. Review `CLAIM_BOUNDARY.md`, `RELEASE_NOTES_v1.1.0.md`, and the exact source CSV for the post-closure figure.
3. Create a repository commit from this source tree without importing the surrounding review ZIPs into Git history.
4. Create a `v1.1.0` release only after commit review.
5. Retain A01/A02 by their exact v1.0.0 identities. Attach A03/A04 and their sidecars as separately versioned assets if the update is accepted.
6. Record any eventual release URL or DOI in a new metadata-only revision; do not retroactively alter this candidate's integrity records.

## Required scientific wording

- Historical Master/branch closures and the 16-edge atlas are unchanged.
- B04/U02 remains `NO_GO`; the Zenodo 21454847 audit was schema/provenance-only.
- Historical U03 RUN01 remains a formal gate-stop and was not repaired.
- U03 is not strict preregistered replication.
- XR01 is not strict replication and uses a substituted model.
- No further immediate same-data analysis is recommended after XR01.

## Prohibited release shortcuts

- Do not label v1.1.0 as already public before the release exists.
- Do not replace historical archive contents under an existing filename or tag.
- Do not add upstream raw HDF files to the Git tree.
- Do not infer causal, universal, anomaly, GR/no-hair, or new-physics claims from the rank associations.
