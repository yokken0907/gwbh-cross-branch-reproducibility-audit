# Release assets

The Release consists of A01 and A02 plus their `.sha256` sidecars. The large ZIP files belong in the GitHub Release, not in the ordinary Git tree.

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
