# 再現性ガイド

## Masterだけで確認できるもの
- 元詳細計画書
- Phase0–4のpre-strain lineage（Phase4 RUN02 ZIP内に再帰格納）
- Phase6–8のmetrics / robustness / closure（Phase8 RUN01 ZIP内に再帰格納）
- P01–P05 final closure
- 最終40 candidate-detector class
- allowed / forbidden claims
- unresolved + reopen conditions
- Phase5の正式取得status/report/review
- Phase5 160 raw payloadすべての個別SHA-256とaccess/request ledger

## 生strainをビット単位で再計算する場合のみ必要
外部large-evidence companion:
`GWBHSCDQDA_PHASE5_RUN03_v0.6.2_RESULTS_FOR_REVIEW.zip`

期待outer SHA-256:
`67184994b89944bf0b8a9da90650c7d57a20c4cda895076ee5920a3c7b692e5a`

Masterはこのlarge companionそのものを重複格納しない。
companionが存在する場合は、outer SHAとMaster内 `STRAIN_PAYLOAD_BYTE_INDEX.csv` の160個別SHAを照合する。

## 科学的境界
Masterの結論は公開O4a H1/L1 product layerに限定。
production search input、significance、FAR/p_astro、PE、population、ringdownへの数値影響は主張しない。
