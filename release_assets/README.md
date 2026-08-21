# Release and review assets

The published v1.0.0 GitHub Release consists of A01 and A02 plus their `.sha256` sidecars; those identities remain immutable. Repository v1.2 preserves the v1.1.0 scientific baseline and references the independently versioned post-closure archives A03 and A04. v1.2 does not rename or rebuild A01-A04. Large ZIP files belong in a release or review bundle, not in the ordinary Git tree.

## A01 — Integrated Project Master

- Filename: `GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip`
- Size: `232729672` bytes
- SHA-256: `87247fb2a664c127570008586cf17110f60e9dc4544899291bca70afa8e1d1f2`
- Role: canonical integrated evidence container with all eight branch Masters and final XBICA evidence.

## A02 — B08 compact reproduction payload

- Filename: `GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip`
- Size: `261539386` bytes
- SHA-256: `2bdcfeae243a6eec84a6b87b64faa35ce22fbe38a2a189ebc02b97d7337fe8f9`
- Role: compact storage of the 21 byte-identical B08 posterior JSON payloads and the metadata required to reconstruct the original evidence companions.

A02 is not an approximate or reduced numerical summary. Its payload files are byte-identical to the originals, with container compression used to reduce distribution size.

## Original companion identities regenerated from A02

### Primary companion

- Filename: `GWBHSSIDA_PHASE3_RUN02_v0.4.1_LARGE_EVIDENCE_COMPANION.zip`
- Original size: `361229152` bytes
- Original SHA-256: `f5ecc497adbcb23d0c29b179af5f5b99d67abdcb32ae262091d511d1ab914846`

### Robustness companion

- Filename: `GWBHSSIDA_PHASE5_RUN01_v0.6.0_ROBUSTNESS_EVIDENCE_COMPANION.zip`
- Original size: `353406315` bytes
- Original SHA-256: `42ab5135ed77a036f034ef5fb87d3e1c0f3718a59a485622a111000807ce3b07`

Reconstruct and verify both from a clean output directory:

```bash
python scripts/reconstruct_b08_original_companions.py \
  /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  ./reconstructed_outputs/B08_companions
```

The script exits non-zero if either reconstructed byte size or SHA-256 differs from the frozen original identity.

## A03 - GWTC-5.0 U03 independent reconsideration

- Filename: `GWBH_ERIA_U03_ALTTRIAD_COMMON5_INDEPENDENT_RECONSIDERATION_v1.0.0_RESULTS_FOR_REVIEW_REGENERATED_20260814.zip`
- Size: `2113550` bytes
- SHA-256: `ebd351477ba0954eab3b78950e3451a380f4c9bb5d3ddd80cdfb052200e79427`
- Role: complete self-verifying archive for the corrected all-22 retrospective within-product summary-to-full-posterior rank association, including the immutable historical RUN01 gate-stop references.
- Historical closure effect: `NONE`.

## A04 - GWTC-4.1 XR01 disjoint-cohort rank association

- Filename: `GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_v1.0.0_RESULTS_FOR_REVIEW.zip`
- Size: `2456341` bytes
- SHA-256: `7895c6405d7083d736f9b3157af53420ddcab9fcaa364120d91e44cb7e8d67ec`
- Role: complete self-verifying archive for the all-44 target-value-blind recurrence of the within-product rank association and its formal next-step `NO_GO` decision.
- Historical closure effect: `NONE`.

A03/A04 are not additions to the historical eight-branch Master and do not replace A01. Their identities and sidecars are listed in `indexes/POST_CLOSURE_RELEASE_ASSET_MANIFEST.csv`.
