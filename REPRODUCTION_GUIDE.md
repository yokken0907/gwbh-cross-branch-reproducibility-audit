# Reproduction guide

## 1. Verify the Git tree

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
```

## 2. Obtain and verify Release assets

Required Release assets:

- A01 — `GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip`
- A02 — `GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip`

Separately versioned post-closure review archives referenced by the v1.2 publication package:

- A03 — `GWBH_ERIA_U03_ALTTRIAD_COMMON5_INDEPENDENT_RECONSIDERATION_v1.0.0_RESULTS_FOR_REVIEW_REGENERATED_20260814.zip`
- A04 — `GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_v1.0.0_RESULTS_FOR_REVIEW.zip`

Each asset is accompanied by a `.sha256` sidecar. Verify all four files with:

```bash
python scripts/verify_release_assets.py /path/to/downloaded/release-assets
```

Use `--established-only` for an A01/A02-only v1.0.0 download, or `--post-closure-only` for an
A03/A04-only review bundle.

Exact filenames, byte sizes, SHA-256 values, roles, and sidecar identities are frozen in `indexes/RELEASE_ASSET_MANIFEST.csv`.
The independent A03/A04 identities are recorded separately in `indexes/POST_CLOSURE_RELEASE_ASSET_MANIFEST.csv`; this preserves the published v1.0.0 A01/A02 manifest unchanged.

## 3. B01 exact confirmatory results

The archived B01 RUN13/RUN21 confirmatory packages are under `reproduction_modules/B01/`. `scripts/verify_key_results.py` checks the frozen exact Spearman/permutation values and permutation count.

## 4. B08 full relevant numerical recomputation

Run:

```bash
python reproduction_modules/B08/run_reproduction.py \
  --project-master /path/to/A01.zip \
  --b08-payload /path/to/A02.zip \
  --output-dir ./reconstructed_outputs/B08
```

The module verifies A01/A02 identities, all 21 compact payloads, recalculates corrected C01–C10, preserves C11/C12 as public-output-limited, recalculates R01–R17 and D01–D02, and compares the resulting metrics against the final canonical B08 closure inside A01.

## 5. Reconstruct original B08 evidence companions

```bash
python scripts/reconstruct_b08_original_companions.py \
  /path/to/A02.zip \
  ./reconstructed_outputs/B08_companions
```

The two reconstructed ZIPs must match the original byte sizes and SHA-256 values documented in `release_assets/README.md`.

## 6. Canonical branch audit and cross-branch atlas

A01 contains all eight canonical branch Masters, the frozen cross-branch contracts, the 28-pair identity matrix, the 16-edge atlas, claim boundaries, and reopen register. The browsable extracts under `evidence/` permit fast inspection; A01 remains the canonical integrated evidence container.

## 7. Source-level reruns

For branches whose upstream third-party public inputs are not duplicated, use `indexes/UPSTREAM_PUBLIC_ASSET_REGISTRY.csv` plus the branch source-freeze/provenance records in A01. Source-level reruns may require reacquisition from the original public provider.

## 8. Post-closure evidence verification

First verify the repository extracts:

```bash
python scripts/verify_post_closure_extensions.py
```

For archive-level verification, unpack A03/A04 separately and run each archive's `VERIFY_PACKAGE.py`. The complete archives include their own manifests and checksums. The Git extracts deliberately omit upstream notebook/HDF5 files and archive-level manifests that enumerate those omitted bytes.

Historical U03 RUN01 remains a formal `NO_GO_NUMERIC_COMPLETE_FRAME_LT8`. The corrected U03 within-product rank-association analysis and XR01 disjoint-cohort recurrence analysis are separately versioned and must not be used to reclassify that result or the B07 closure. Historical machine-readable calibration/transport labels are retained only as provenance identifiers.
