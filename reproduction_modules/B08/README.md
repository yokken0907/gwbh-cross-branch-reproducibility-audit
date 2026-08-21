# B08 numerical reproduction module

## Purpose

This module recomputes the final B08 public-output dependency metrics from the two frozen GitHub Release assets:

- **A01** — `GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip`
- **A02** — `GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip`

It implements the corrected Phase4 RUN02 primary path and the Phase5 robustness/post-hoc path used by the final B08 closure.

## Scope

The module recomputes:

- corrected primary comparisons C01–C10;
- preserved primary limitation status for C11/C12;
- robustness comparisons R01–R17;
- post-hoc GW170817 diagnostics D01–D02;
- the frozen cross-model robustness matrix.

The small combined/bright GW170817 artifacts are extracted from the canonical B08 lineage inside A01. The 21 large posterior payloads are read from A02.

## Required assets

| Asset | Filename | SHA-256 |
|---|---|---|
| A01 | `GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip` | `87247fb2a664c127570008586cf17110f60e9dc4544899291bca70afa8e1d1f2` |
| A02 | `GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip` | `2bdcfeae243a6eec84a6b87b64faa35ce22fbe38a2a189ebc02b97d7337fe8f9` |

## Environment

The canonical analysis environment is recorded in `ENVIRONMENT.md` and `requirements.txt`.
The public reproduction entry point itself uses Python standard-library code for the frozen final metric path and does not require user-specific filesystem paths.

## Execution

From the repository root:

```bash
python reproduction_modules/B08/run_reproduction.py \
  --project-master /path/to/GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip \
  --b08-payload /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  --output-dir ./reconstructed_outputs/B08
```

## Expected outputs

- `H0_POSTERIOR_SUMMARY_CORRECTED.csv`
- `PAIRED_DEPENDENCY_METRICS_CORRECTED.csv`
- `ROBUSTNESS_PAIRED_METRICS.csv`
- `POSTHOC_BRIGHT_DIAGNOSTIC_METRICS.csv`
- `CROSS_MODEL_ROBUSTNESS_MATRIX.csv`
- `B08_REPRODUCTION_REPORT.json`

A successful run reports:

- `status = PASS`;
- 10 primary metric rows PASS and C11/C12 remain public-output-limited;
- 17/17 robustness rows PASS;
- 2/2 post-hoc diagnostic rows PASS;
- GW170817 post-hoc sample digest `f63ceb3dee1dd8b043e4f67faef9aa001ca8b4ab3da3401a63ee223031919703`.

The script verifies computed metrics against the final canonical B08 closure contained in A01.

## Original evidence-companion reconstruction

A02 also supports byte-for-byte regeneration of the two original large evidence companions through:

```bash
python scripts/reconstruct_b08_original_companions.py \
  /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  ./reconstructed_outputs/B08_companions
```

Expected original companion identities are documented in `release_assets/README.md`.

## Claim boundary

Successful numerical reproduction verifies the archived released-output calculations. It does **not** determine a true H0 value, establish cosmological bias, identify a physically correct variant, or resolve the Hubble tension. C11/C12 remain primary public-output-limited comparisons; the GW170817 grid-density conversion is retained only as a separately labelled post-hoc diagnostic.
