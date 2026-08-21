# XR01 GWTC-4.1 cross-release transport 最終閉鎖報告

## 1. 最終判断

固定run `GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_RUN01` は44/44事象、660/660 cellを
完遂し、一次判定を次で閉鎖した。

`SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT`

観測Spearman rhoは `0.9468639887244539`。正方向の固定1,000,000 Monte Carlo置換で
観測値以上は0回、plus-one pは `9.99999000001e-7`、極端確率の99% Clopper–Pearson区間は
`[0, 5.298303330489366e-6]` だった。凍結support rule `rho > 0 and p <= 0.05` を満たす。

## 2. 追加作業の科学的価値

既存GWTC-5.0検証は1 release、22事象、1 triadの内部calibrationに限定されていた。残る主要な
再現性上の問いは、同じ安価なsummary scoreとfull-posterior responseの対応が別cohortへ運べるか
だった。GWTC-4.1にはIMRPhenomXPNRがないためstrict replicationは不可能だが、未閲覧のO4a
44事象で `IMRPhenomXPHM-SpinTaylor / SEOBNRv5PHM / NRSur7dq4` とcommon-5が成立した。

このため、変更をreleaseと中央modelの置換に限定し、predictor、response、集約、方向、alpha、
置換検定を既存設計から運ぶconceptual transportには実質的な追加価値があると判断した。

証拠区分は次であり、公開時系列上のprospective studyやstrict replicationではない。

`PUBLIC_DATA_TARGET_VALUE_BLIND_PREREGISTERED_CROSS_RELEASE_CONCEPTUAL_TRANSPORT`

## 3. 値blind preflightと意味監査

Zenodo record `20275769`、DOI `10.5281/zenodo.20275769`、release tag
`IGWN-GWTC4p1-18965dda8_5` を固定した。summary compound tableからstring identityとboolean
maskだけを読み、数値summary fieldを要求せずに次を得た。

| 項目 | 結果 |
|---|---:|
| summary rows | 379 |
| target-model rows | 218 |
| target modelを1つ以上持つevent | 87 |
| exact triad/common-5 mask PASS | 44 |
| 除外event | 43 |
| 候補numeric summary access | 0 |
| 候補posterior access | 0 |

公式notebookはlower/upperを5th/95th percentile endpointと説明するため、候補外に固定した
`GW230605_065343 / C00:IMRPhenomXPHM-SpinTaylor` だけで意味監査した。5項目、各15,830 sample、
計79,150 posterior scalarで次をexact tolerance内に再現した。

- `median = q50`
- `lower = median - q05`
- `upper = q95 - median`

endpoint解釈は0/5項目でexact matchだった。raw semantic HDFは削除した。この監査後も候補44件の
numeric summary/posterior accessは0で、protocol、runner、tests、inputsを含む29ファイルをSHA固定した。

## 4. 凍結設計

### 対象

- release: GWTC-4.1 `IGWN-GWTC4p1-18965dda8_5`
- event: schema/mask-onlyで固定した全44件
- model: `IMRPhenomXPHM-SpinTaylor`, `SEOBNRv5PHM`, `NRSur7dq4`
- parameter: `chirp_mass_source`, `chi_eff`, `luminosity_distance`,
  `final_mass_source`, `final_spin`
- model pair × parameter: 3 × 5 = 15 cell/event、計660 cell

### Predictor

各model pair・parameterについて、配布lower/upperを非対称誤差幅として

`S90 = abs(median_b - median_a) / max((((lower_a + upper_a) + (lower_b + upper_b))/4), 1e-12)`

を計算した。parameterごとに3 pairの最大値、eventごとに5 parameterの中央値をとった。

### Response

各cellのunweighted 1-Wasserstein distanceを、2 posteriorのIQR平均で正規化した。IQRが非正なら
連結標本の母標準偏差、最小 `1e-12` へfallbackする。event responseは15 cellの中央値とした。
SciPy W1と独立empirical-CDF積分を全cellで照合した。

### 一次検定

- n = 44
- average-rank Spearman rho
- positive alternative
- 1,000,000 fixed permutations
- PCG64DXSM seed 20260813
- plus-one p
- alpha = 0.05
- support = `rho > 0 and p <= 0.05`

event replacement、complete-case reduction、model/parameter削減、方向変更、adaptive permutation、
rescue、secondaryによるprimary overrideを禁止した。

## 5. Gateと数値実行

| 項目 | 結果 |
|---|---:|
| summary semantic triplet | 660/660 PASS |
| event HDF official size/MD5 | 44/44 PASS |
| event bytes processed | 7,909,707,404 |
| posterior model/parameter array | 660/660 PASS |
| posterior scalar read / finite | 9,872,875 / 9,872,875 |
| nonfinite posterior scalar | 0 |
| finite array minimum / maximum | 11,604 / 19,933 |
| full W1 cell | 660/660 |
| dual W1最大絶対差 | 2.2737367544323206e-13 |
| raw event HDF retained | 0 |
| event replacement / rescue | 0 / 0 |

runは `2026-08-14T02:28:28Z` から `03:39:54Z` まで4,286秒。公開file取得合計は
約4,162.32秒だった。各HDFはidentity検証・計算・派生表保存後に即時削除した。

## 6. 結果

### 一次

| 指標 | 値 |
|---|---:|
| Spearman rho | 0.9468639887244539 |
| permutations | 1,000,000 |
| observed以上 | 0 |
| plus-one p | 9.99999000001e-7 |
| predictor ties / response ties | 0 / 0 |
| 判定 | SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT |

predictor範囲は `[0.017818038426800548, 1.8148762009655421]`、full response範囲は
`[0.02081106108540429, 0.8710380428279254]` だった。

### 凍結secondary（primary overrideなし）

- balanced response rho = `0.9496828752642706`
- balanced fixed-permutation p = `9.99999000001e-7`
- Kendall tau-b = `0.8118393234672304`, two-sided p = `7.989037484902967e-15`
- leave-one-event-out rho range = `[0.9430685593476291, 0.9557535487768046]`

## 7. 独立再現性監査

事後verifierは凍結runnerをimportせず、660 summary tripletからpredictor、660 distance cellから
responseを再構築した。runnerと異なるbatch幅7777で固定1,000,000置換を再生し、rho、extreme=0、
plus-one p、verdictを完全再現した。29/29 lock hash不変、44/44 identity/deletion、raw HDF 0、
error ledger 0を含む23/23 checkがPASS。事後合成試験も11/11 PASSだった。

## 8. 解釈とclaim boundary

結果は、別O4a cohortかつSEOBNRv5PHMを含むtriadでも、summary scoreとfull posterior差の強い正の
順位関係があることを支持する。これは既存calibrationのcross-release / alternate-triad conceptual
transportである。

ただしpredictorとresponseは同じ各releaseのposterior productに由来する。従って、物理モデルの
真偽・優越性、差の因果的waveform-systematic帰属、population/selection/ringdown/cosmology、
GR/Kerr/no-hair/anomaly/new physics、固定frame外への一般化は支持しない。XPNR不在のため
strict replicationでもない。既存Master/B07/B04または過去runのclosureは変更しない。

## 9. 次段判断

同じGWTC-4.1結果で別predictor、部分event、別parameter、別triadを試すことは、結果閲覧後の
多重性と高い重複に対して追加価値が小さい。よって現時点は

`NO_GO_FURTHER_IMMEDIATE_SAME_DATA_ANALYSIS__XR01_EXTENSION_COMPLETE`

で停止する。再開条件は、互換する新しい公式PE releaseまたは真にdisjointな公開cohortが利用可能に
なり、そのtarget値閲覧前に新しいidentity/schema/semantic audit、preregistration、SHA lockを
完了できることとする。
