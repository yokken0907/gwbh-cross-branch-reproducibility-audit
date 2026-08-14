# XR01 GWTC-4.1 cross-release transport 検証

## 結論

独立run `GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_RUN01` は全gateを完遂し、
凍結した一次判定は次のとおりです。

`SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT`

- GWTC-4.1 O4aの固定44事象
- `IMRPhenomXPHM-SpinTaylor / SEOBNRv5PHM / NRSur7dq4`
- common-5、660 full-posterior distance cell
- Spearman rho = `0.9468639887244539`
- 正方向、固定1,000,000 Monte Carlo置換
- extreme count = `0`
- plus-one p = `9.99999000001e-7`
- event replacement、rescue、結果閲覧後の変更 = `0`

これは、GWTC-5.0で得たsummary screening calibrationが、別O4a cohortと1モデルを
置換したtriadでも成立するという限定的なconceptual transportを支持します。
strict replication、model truth/superiority、物理的waveform-systematics、GR/Kerr/new physicsを
支持しません。

## なぜ追加価値があったか

前runの主な未解決境界は「別release・別cohort・別triadへ運べるか」でした。GWTC-4.1には
IMRPhenomXPNRがないためexact replicationは不可能でしたが、数値値を未閲覧のまま、XPHM、
SEOBNRv5PHM、NRSur7dq4とcommon-5が揃う44事象をschema/mask-onlyで固定できました。

候補外事象 `GW230605_065343` でsummary semanticsを先に監査し、5/5parameterで
`median=q50; lower=median-q05; upper=q95-median` を再現しました。候補44件のsummary数値と
posteriorは、この意味監査と29-file SHA lockの時点で0アクセスでした。

## 主要ファイル

- `CLOSURE_REPORT_JA.md`: 設計・gate・結果・限界の統合報告
- `DECISION.json`: 機械可読な一次判定
- `NEXT_STEP_DECISION.json`: 追加の同一データ解析を行わない判断
- `02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json`: 29ファイルのtarget値閲覧前SHA lock
- `02_ANALYSIS_LOCK/OUTCOME_BLIND_ANALYSIS_PROTOCOL.json`: 凍結統計契約
- `06_RUN_OUTPUT/`: 全派生数値出力と監査表
- `06_RUN_OUTPUT/INDEPENDENT_REPRODUCIBILITY_VERIFICATION.json`: 23/23独立検証
- `07_REPRODUCIBILITY/REPRODUCTION_GUIDE_JA.md`: 再現手順

既存Project Master、B07、B04、過去のpreregistration/RUN01/GWTC-5 extensionは変更していません。
