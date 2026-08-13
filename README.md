# GWBH Reproducibility Repository

A **lightweight publication reproducibility repository** for the eight-branch gravitational-wave black-hole dependency/provenance audit. It keeps the browsable audit evidence, deterministic verification tools, and compact numerical reproduction modules in Git, while the two frozen large evidence containers are distributed as Release assets.

## What this repository provides

- final branch closure evidence for B01–B08;
- the frozen 28-pair identity matrix and 16-edge cross-branch dependency atlas;
- allowed/forbidden claim boundaries and reopen conditions;
- B01 confirmatory packages for the two exact permutation results;
- a self-contained B08 numerical reproduction module driven by Release Assets A01 and A02;
- integrity, source-provenance, and Release-asset verification tools.

## What this repository is not

This is not the historical Master-of-All container and it does not attempt to replay every superseded or failed development RUN. The reproducibility target is the **final reported audit state** and the evidence needed to verify or recompute that state.

## Repository layers

```text
GitHub repository tree
        |
        +-- browsable evidence / contracts / verification scripts
        +-- B01 confirmatory modules
        +-- B08 numerical reproduction module
        |
        +--> Release Asset A01
        |    GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip
        |
        +--> Release Asset A02
             GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip
```

A01 is the canonical integrated Project Master containing all eight branch Masters and the final XBICA integration evidence. A02 stores the 21 byte-identical B08 large-posterior payloads in a compact container and can regenerate the two original B08 large evidence companions byte-for-byte.

## Quick verification

From the repository root:

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
python scripts/verify_release_assets.py /path/to/downloaded/release-assets
```

## B08 numerical reproduction

```bash
python reproduction_modules/B08/run_reproduction.py \
  --project-master /path/to/GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip \
  --b08-payload /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  --output-dir ./reconstructed_outputs/B08
```

See `reproduction_modules/B08/README.md` for scope, environment, outputs, and verification criteria.

## B08 companion reconstruction

```bash
python scripts/reconstruct_b08_original_companions.py \
  /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  ./reconstructed_outputs/B08_companions
```

The reconstructed ZIP identities are fixed in `release_assets/README.md`.

## Final closure

`FINAL_PROJECT_SCIENTIFIC_CLOSED_EIGHT_BRANCH_DEPENDENCY_ATLAS_COMPLETE_NO_CROSS_BRANCH_NUMERIC_PROPAGATION`

Final 16-edge classification:

- PARTIAL_STRUCTURAL: 8
- IDENTITY_ONLY: 3
- BLOCKED_PUBLIC_ASSET: 3
- BLOCKED_SCHEMA: 2
- DIRECT_NUMERIC: 0

## Scientific boundary

Integrity verification and numerical reproduction are distinct from physical validation. Structural adjacency is not promoted to numerical propagation or causation. B03 remains a public-asset NO-GO, B04 remains a schema HOLD, B07 records that no compatible replication test was executed, and B08 remains a bounded released-output dependency audit with primary status 10/12. Successful B08 recomputation does not determine a true H0 value, prove cosmological bias, or resolve the Hubble tension.

## Navigation

- `REPRODUCTION_GUIDE.md`
- `REPRODUCIBILITY_SCOPE.md`
- `indexes/REPRODUCTION_REQUIREMENT_MATRIX.csv`
- `indexes/UPSTREAM_PUBLIC_ASSET_REGISTRY.csv`
- `release_assets/README.md`
- `LICENSE`
- `LICENSE_AND_DATA_PROVENANCE.md`
