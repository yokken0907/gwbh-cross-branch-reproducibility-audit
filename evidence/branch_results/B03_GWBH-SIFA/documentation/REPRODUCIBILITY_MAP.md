# REPRODUCIBILITY MAP

1. Verify the master ZIP against its external `.sha256` sidecar.
2. Verify `MASTER_MANIFEST.csv` / `SHA256SUMS.txt`.
3. Open `canonical/GWBHSIFA_LINEAGE_CLOSURE_v1.0.8_RESULTS_FOR_REVIEW.zip` and verify its internal `outputs/RESULT_MANIFEST.csv`.
4. Read `outputs/LINEAGE_CLOSURE_REPORT.json` and `outputs/LINEAGE_CLOSURE_REQUIREMENT_MATRIX.csv`.
5. Follow the two frozen ZIPs under v1.0.8: v1.0.7 checkpoint and L07 ADJUDICATION v1.0.0.
6. From v1.0.7, follow the recursively frozen prior LINEAGE_CLOSURE and Foundation result ZIPs as needed.
7. No network access is required to reproduce the **final closure decision from the frozen snapshot**; v1.0.8 itself was a deterministic no-refetch integration run.
8. Reproducing original external acquisition steps is a separate historical task and is not required to recompute the frozen v1.0.8 decision.
