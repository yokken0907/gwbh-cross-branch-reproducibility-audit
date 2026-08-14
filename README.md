# GWBH Reproducibility Repository

A **lightweight publication reproducibility repository** for the frozen eight-branch gravitational-wave black-hole dependency/provenance audit, plus separately versioned post-closure extensions. Version 1.1.0 preserves the v1.0.0 Master and branch closures byte-for-byte, adds browsable B04/U02, U03, and XR01 evidence, and keeps large or independently archived evidence in release assets.

Status: v1.1.0 source/release candidate prepared on 2026-08-14. The current public GitHub release remains v1.0.0 until the candidate is explicitly published.

## What this repository provides

- final branch closure evidence for B01–B08;
- the frozen 28-pair identity matrix and 16-edge cross-branch dependency atlas;
- allowed/forbidden claim boundaries and reopen conditions;
- B01 confirmatory packages for the two exact permutation results;
- a self-contained B08 numerical reproduction module driven by Release Assets A01 and A02;
- the B04/U02 Zenodo 21454847 schema/provenance-only `NO_GO` record;
- the independently versioned GWTC-5.0 U03 all-22 screening-calibration evidence;
- the independently versioned GWTC-4.1 XR01 all-44 conceptual-transport evidence;
- integrity, source-provenance, and Release-asset verification tools.

## What this repository is not

This is not the historical Master-of-All container and it does not silently rewrite superseded, failed, or gated RUNs. The reproducibility target is the **final reported audit state**, the preserved historical stopping decisions, and the independent post-closure evidence needed to verify the v1.1.0 publication update.

## Repository layers

```text
GitHub repository tree
        |
        +-- browsable evidence / contracts / verification scripts
        +-- B01 confirmatory modules
        +-- B08 numerical reproduction module
        +-- post_closure_extensions/
        |    B04/U02 decision, U03 and XR01 evidence extracts
        |
        +--> Release Asset A01
        |    GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip
        |
        +--> Release Asset A02
        |    GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip
        |
        +--> Review Asset A03
        |    independently reconsidered GWTC-5.0 U03 archive
        |
        +--> Review Asset A04
             GWTC-4.1 XR01 transport archive
```

A01 is the canonical integrated Project Master containing all eight branch Masters and the final XBICA integration evidence. A02 stores the 21 byte-identical B08 large-posterior payloads in a compact container and can regenerate the two original B08 large evidence companions byte-for-byte. A03 and A04 are independent scientific extension archives; they are not replacements for A01.

## Quick verification

From the repository root:

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
python scripts/verify_post_closure_extensions.py
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

## Historical final closure (unchanged)

`FINAL_PROJECT_SCIENTIFIC_CLOSED_EIGHT_BRANCH_DEPENDENCY_ATLAS_COMPLETE_NO_CROSS_BRANCH_NUMERIC_PROPAGATION`

Final 16-edge classification:

- PARTIAL_STRUCTURAL: 8
- IDENTITY_ONLY: 3
- BLOCKED_PUBLIC_ASSET: 3
- BLOCKED_SCHEMA: 2
- DIRECT_NUMERIC: 0

## Scientific boundary

Integrity verification and numerical reproduction are distinct from physical validation. Structural adjacency is not promoted to numerical propagation or causation. B03 remains a public-asset NO-GO, B04 remains a schema HOLD, B07 records that no compatible replication test was executed, and B08 remains a bounded released-output dependency audit with primary status 10/12. The post-closure U03 and XR01 analyses support only a within-public-PE summary-screening calibration and one conceptual transport. They do not establish strict replication, waveform-model truth or superiority, causal systematics, cross-branch propagation, GR/Kerr/no-hair conclusions, anomaly, or new physics.

After XR01, further immediate same-data variants are formally `NO_GO_FURTHER_IMMEDIATE_SAME_DATA_ANALYSIS__XR01_EXTENSION_COMPLETE`. Reopen requires a genuinely new official PE release or disjoint compatible cohort and a new pre-value audit/preregistration/lock.

## Navigation

- `REPRODUCTION_GUIDE.md`
- `REPRODUCIBILITY_SCOPE.md`
- `indexes/REPRODUCTION_REQUIREMENT_MATRIX.csv`
- `indexes/UPSTREAM_PUBLIC_ASSET_REGISTRY.csv`
- `release_assets/README.md`
- `evidence/post_closure_extensions/README.md`
- `evidence/post_closure_extensions/CLAIM_BOUNDARY.md`
- `LICENSE`
- `LICENSE_AND_DATA_PROVENANCE.md`
