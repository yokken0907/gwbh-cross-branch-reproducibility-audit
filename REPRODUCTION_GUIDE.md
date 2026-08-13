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

Each asset is accompanied by a `.sha256` sidecar. Verify all four files with:

```bash
python scripts/verify_release_assets.py /path/to/downloaded/release-assets
```

Exact filenames, byte sizes, SHA-256 values, roles, and sidecar identities are frozen in `indexes/RELEASE_ASSET_MANIFEST.csv`.

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
