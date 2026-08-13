# 再現性ガイド

## 参照順序
1. `README_JA.md`
2. `CLOSURE/PHASE4_FINAL_CLOSURE_REPORT.json`
3. `CLOSURE/FINAL_TRACK_DISPOSITION.json`
4. `CLOSURE/ALLOWED_CLAIMS.json`
5. `CLOSURE/FORBIDDEN_CLAIMS.json`
6. `CLOSURE/FINAL_UNRESOLVED_REGISTER.json`
7. `PREREGISTRATION/ADAPTED_COMMON5_PREREGISTRATION.json`
8. `REPRODUCIBILITY/LINEAGE_MAP.json`

## 完全なRUN履歴
`CANONICAL_LINEAGE/GWBHERIA_PHASE4_RUN01_v0.5.0_RESULTS_FOR_REVIEW.zip`
がPhase3→Phase2→Phase1 RUN02→RUN01→Phase0を再帰格納し、
Phase0には元の第7枝計画書と第1枝Masterが含まれる。

## 再開条件
閉鎖済み契約を緩和して再開してはならない。
parameter削減、model置換、derived quantity、posterior取得による別再現試験は
`FINAL_UNRESOLVED_REGISTER.json` のreopen条件に従う新規extensionとして事前登録する。
