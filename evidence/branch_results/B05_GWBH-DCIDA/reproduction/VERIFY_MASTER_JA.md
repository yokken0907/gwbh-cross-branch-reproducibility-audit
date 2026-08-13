# Master verification

1. 外部sidecarでMaster ZIPのSHA-256を確認する。
2. ZIPを展開し `MASTER_MANIFEST.csv` のsize/SHA-256を全件確認する。
3. `references/CANONICAL_CHAIN.csv` の11 artifactを `artifacts/run_history/` で確認する。
4. 各nested result ZIPのsidecarとCRCを確認する。
5. 最終科学主張は `closure/CLAIM_BOUNDARY_REGISTER.csv` を超えない。
