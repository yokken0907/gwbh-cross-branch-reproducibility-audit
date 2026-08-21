# B07-U03 alternate-triad 独立再検討・数値RUN・監査

## 結論

独立run `GWBH_ERIA_U03_ALTTRIAD_COMMON5_OBRC_RUN01` は全gateを通過し、凍結した一次判定は次のとおりです。

`SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION`

- 全22事象、全330 posterior距離セルを使用
- Spearman rho = `0.9017504234895539`
- 正方向、固定1,000,000 Monte Carlo置換
- extreme count = `0`
- plus-one p = `9.99999000001e-7`
- event replacement、rescue、モデル・パラメータ削減、結果閲覧後の契約変更 = `0`

これは、GWTC-5.0のこの22事象・3モデル・common-5に限り、修正したpublic-summary scoreがfull-posterior model-distanceの順位screenとして機能することを支持します。モデルの真偽・優越性、波形系統誤差の因果帰属、B01/B07のstrict replication、GR/Kerr/new physicsを支持しません。

## なぜRUN01を変更せず別runにしたか

歴史的RUN01は凍結済み契約を正しく実行し、`upper >= lower` を満たす事象が0/22だったため `NO_GO_NUMERIC_COMPLETE_FRAME_LT8` で正式閉鎖されています。本成果物はその判定を修復・再分類・上書きしていません。

独立監査で、公式GWTC-5 PE notebookが `*_lower`/`*_upper` を5th/95th percentile値と説明する一方、配布summary HDF5の数値は非負の非対称誤差幅であることを確認しました。候補22事象を一切開かずに固定した候補外事象 `GW241109_115924` を照合すると、common-5の5/5項目で次が機械精度で一致しました。

- `median = q50`
- `lower = median - q05`
- `upper = q95 - median`

したがってRUN01の `upper >= lower` は、区間端点の順序ではなく左右誤差幅の大小を検査していました。RUN01は契約上有効なNO_GOのままですが、意図したscreening questionについては非情報的です。

## 新しい証拠区分

本runは次の区分です。

`POST_SUMMARY_UNBLINDED_CANDIDATE_POSTERIOR_BLIND_RETROSPECTIVE_CALIBRATION`

RUN01で候補summary 990 scalarが既閲覧である一方、新契約のSHA-256 lock時点で候補22事象のposterior element、W1 response、相関、p値は0でした。よって「fully prospective」「data-publication holdout」「independent replication」とは表現しません。

## 主要ファイル

- `CLOSURE_REPORT_JA.md`: 科学判断、設計、結果、限界の統合報告
- `DECISION.json`: 機械可読な最終判定
- `02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json`: 候補posterior閲覧前の17ファイルSHA-256 lock
- `02_ANALYSIS_LOCK/OUTCOME_BLIND_ANALYSIS_PROTOCOL.json`: 凍結解析契約
- `01_DESIGN_AUDIT/SEMANTIC_VALIDATION_RESULT.json`: lower/upper意味監査
- `06_RUN_OUTPUT/`: 全数値出力と監査表
- `06_RUN_OUTPUT/INDEPENDENT_REPRODUCIBILITY_VERIFICATION.json`: runner非importの23/23独立検証
- `07_REPRODUCIBILITY/REPRODUCTION_GUIDE_JA.md`: 再現手順

## 親成果物

Project Masterは `FINAL_CLOSED`、B07は `FINAL_CLOSED_NO_REPLICATION_TEST_EXECUTED` のままです。B04/U02も既存の `NO_GO / B04_U02_REOPEN_NOT_SATISFIED` のままです。本成果物は独立post-closure extensionであり、親成果物を変更していません。
