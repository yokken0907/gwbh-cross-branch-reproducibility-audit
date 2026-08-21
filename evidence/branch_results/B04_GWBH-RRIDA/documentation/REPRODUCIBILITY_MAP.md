# REPRODUCIBILITY MAP

1. Verify the outer master ZIP against its external `.sha256` sidecar.
2. Extract the master and verify `MASTER_MANIFEST.csv` and `SHA256SUMS.txt`, or run `python3 tools/verify_master.py` from the extracted root.
3. Verify `canonical/GWBHRRIDA_PHASE6_RUN02_v0.7.1_RESULTS_FOR_REVIEW.zip` against its embedded sidecar and SHA-256 `8f59624885d9525719739a8e25b057870790745de5f7c780e3ba55b3297fb2e5`.
4. Open the canonical ZIP and verify its `RESULT_MANIFEST.csv`, `RESULT_STATUS.json`, and `outputs/PHASE6_RUN02_REPORT.json`.
5. Inspect `outputs/CONFIG_STRUCTURE_AUDIT.csv`, `CONFIG_DECLARATION_LEDGER.csv`, `CONFIG_TARGET_KEY_AUDIT.csv`, and `CONFIG_KEY_SUMMARY.csv` to reproduce the 44-config support-key counts.
6. Inspect `outputs/RUN01_CORRECTION_LEDGER.csv` and `PAIR_CONFIG_ADJUDICATION.csv` to confirm 22 `true -> NOT_EVALUATED` corrections and zero config-equality adjudications.
7. Follow the nested RUN01 ZIP and inspect `ENDPOINT_SCHEMA_AUDIT.csv` and `ACCESS_AUDIT.json` to confirm 44 header recognitions, zero config-gate passes, and zero numerical rows.
8. Follow each predecessor ZIP recursively to Phase 0; `provenance/NESTED_ARCHIVE_CHAIN.csv` fixes all ten SHA-256 values.
9. Recompute the 12-component frozen contract using `provenance/CONTRACT_COMPONENT_LEDGER.csv`; the aggregate is `999385ea235041e21be0b7394f65716a16672726f0e431c6afcbf3390faba899`.
10. Read `final_state/FINAL_CLOSURE_ADJUDICATION.json` and `MASTER_STATUS.json` for the post-RUN02 continuation decision.

No network access is required to reproduce the final closure decision from this frozen package. Reproducing the historical source acquisition is separate and requires the exact external archive identity recorded in `documentation/SOURCE_SCOPE_AND_ARCHIVE_IDENTITY.md`.
