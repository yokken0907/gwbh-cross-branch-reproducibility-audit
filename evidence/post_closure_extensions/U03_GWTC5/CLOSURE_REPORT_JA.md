# GWBH-ERIA U03 alternate-triad 独立再検討 最終閉鎖報告

## 1. 最終判断

新run `GWBH_ERIA_U03_ALTTRIAD_COMMON5_OBRC_RUN01` は、凍結した全22事象契約を完遂し、次の一次判定で閉鎖した。

`SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION`

観測Spearman rhoは `0.9017504234895539`。正方向の固定1,000,000 Monte Carlo置換では観測値以上が0回で、plus-one pは `9.99999000001e-7`。極端確率の99% Clopper–Pearson区間は `[0, 5.298303330489366e-6]` だった。この結論は凍結support rule `rho > 0 and p <= 0.05` を満たす。

Project Master、B07 closure、B04 closure、歴史的preregistration、RUN01はいずれも変更していない。

## 2. 独立再検討で確定した停止理由の意味

RUN01は凍結した `upper >= lower` gateを忠実に実行し、122/330 tripletで不成立、0/22事象eligibleとして正式NO_GOで閉鎖した。これは契約違反や実装失敗ではない。

しかし、公式PE notebookの列説明と配布HDF5の実装が矛盾していた。候補22事象のposteriorをblindに保つため、候補外で事前固定した `GW241109_115924 / IMRPhenomXPHM-SpinTaylor` のみを意味検証に使った。5項目すべてでsummary値はposterior分位点から次のようにexactに再現された。

| summary列 | 配布byteの実装 |
|---|---|
| `median` | q50 |
| `lower` | median − q05 |
| `upper` | q95 − median |

したがってRUN01 gateは「5th percentile <= 95th percentile」を検査しておらず、非対称誤差の左幅と右幅を比較していた。歴史的RUN01のNO_GOを変更する根拠にはならないが、同じNO_GOを科学的最終回答として反復するのも妥当でないと判断した。

意味検証用HDFは公式size/MD5を照合し、検証後に削除した。候補posterior閲覧は0のまま新契約を固定した。選択ファイル内の手入力時刻に誤りがあったため、元のlock SHA-256を保持したまま別erratumでfilesystem作成時刻と実行順を開示した。

## 3. 新解析の科学的価値と証拠階層

価値がある問いは、物理モデルの真偽ではなく、低コストsummary scoreが同一公開リリース内のfull posterior model-distanceを順位screenできるかである。posterior responseは未閲覧だったため、summary側既閲覧という制約を明示したうえでoutcome-blind calibrationを行う追加価値が残っていた。

証拠区分は以下に固定した。

`POST_SUMMARY_UNBLINDED_CANDIDATE_POSTERIOR_BLIND_RETROSPECTIVE_CALIBRATION`

summary値を既に閲覧していたため、旧8事象のpredictor層化選抜は再利用しなかった。固定済み22事象を全件含めることで、summary閲覧後のcohort選抜裁量、event replacement、p値rescueを除いた。

## 4. 凍結した設計

### 対象

- release: GWTC-5.0 `IGWN-GWTC5p0-29ebe06b7_25`
- event: 過去に固定・schema pass済みの22件を全件使用
- model: `IMRPhenomXPHM-SpinTaylor`, `IMRPhenomXPNR`, `NRSur7dq4`
- parameter: `chirp_mass_source`, `chi_eff`, `luminosity_distance`, `final_mass_source`, `final_spin`
- model pair × parameter: 3 × 5 = 15 cell/event、計330 cell

### 修正summary predictor

各model pair・parameterについて、配布表の `lower`/`upper` を非対称誤差幅として

`S90 = abs(median_b - median_a) / max((((lower_a + upper_a) + (lower_b + upper_b))/4), 1e-12)`

を計算した。parameterごとに3 pairの最大値、eventごとに5 parameterの中央値をとった。

### posterior response

各cellでunweighted 1-Wasserstein distanceを、2 posteriorのIQR平均で正規化した。IQR scaleが非正の場合だけ連結標本の母標準偏差へfallbackし、最小 `1e-12` とした。event responseは15 normalized cellの中央値。

各full W1はSciPy実装と独立empirical-CDF積分の双方で計算し、cellwise toleranceを超えた時点で停止する契約とした。

### 一次検定

- n = 22
- statistic = average-rank Spearman rho
- alternative = positive
- 1,000,000 fixed Monte Carlo permutations
- RNG = `PCG64DXSM(20260813)`
- p = `(extreme + 1)/(1,000,000 + 1)`
- alpha = 0.05
- support = `rho > 0 and p <= 0.05`

tieはaverage rankで扱い、constant vectorはnon-support。adaptive permutation、両側・負方向rescue、event/model/parameter除外は禁止した。

## 5. Gate・数値実行・保持方針

| 項目 | 結果 |
|---|---:|
| summary semantic triplet | 330/330 PASS |
| event HDF official size/MD5 | 22/22 PASS |
| event bytes processed | 4,427,375,872 |
| posterior model/parameter count gate | 330/330 PASS |
| posterior scalar read | 5,173,800 |
| finite posterior scalar | 5,173,800 |
| nonfinite posterior scalar | 0 |
| finite cell minimum / maximum | 11,908 / 20,091 |
| full W1 cells | 330/330 |
| dual W1最大絶対差 | 5.684341886080802e-14 |
| raw event HDF retained | 0 |
| event replacement / rescue | 0 / 0 |

各HDFはCSV固定順に1件ずつ取得し、identity検証、posterior計算、派生表の原子的保存後に即時削除した。全取得所要は約3,597.65秒、run全体は `2026-08-13T19:30:51Z` から `20:31:51Z` までだった。

## 6. 結果

### 一次

| 指標 | 値 |
|---|---:|
| n | 22 |
| Spearman rho | 0.9017504234895539 |
| permutation | 1,000,000 |
| observed以上 | 0 |
| plus-one p | 9.99999000001e-7 |
| predictor ties | 0 |
| response ties | 0 |
| 判定 | SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION |

predictor範囲は `[0.024168698499380303, 0.17246237889433702]`、full response範囲は `[0.024708596651471588, 0.10047556592572497]` だった。

### 凍結secondary（primary overrideなし）

- balanced response Spearman rho = `0.9062676453980801`
- balanced fixed 1,000,000-permutation plus-one p = `9.99999000001e-7`
- Kendall tau-b = `0.7662337662337663`, two-sided p = `1.7950735147639608e-8`
- leave-one-event-out rho range = `[0.887012987012987, 0.9428571428571428]`

secondaryは一次判定を変更していない。

## 7. 独立再現性監査

事後verifierは凍結runnerをimportせず、summary tripletからpredictorを再構築し、330 cellからevent responseを再集約し、SciPy Spearmanを再計算した。さらにrunnerと異なるbatch幅7777で同じ固定乱数列を生成し、1,000,000置換のextreme count 0とplus-one pを再現した。

`06_RUN_OUTPUT/INDEPENDENT_REPRODUCIBILITY_VERIFICATION.json` は23/23 check PASS。事後合成試験は11/11 PASS。pre-posterior lock対象17ファイルは全てrun後も同一SHA-256だった。

## 8. 解釈とclaim boundary

強い正の順位関係は、このrelease固有のsummary scoreがfull posterior差のscreenとして有用であることを支持する。ただし、predictorとresponseは同じ公開posterior productに由来する。したがってこれは外部の物理検証ではなく、同一資産内の圧縮指標calibrationである。

次を主張してはならない。

- B01/B07のstrictまたはindependent replication/non-replication
- waveform modelの真偽、信頼性、優越性
- 差の純粋なwaveform-systematic因果帰属
- population、selection、ringdown、cosmologyへの伝播
- GR、Kerr、no-hair、anomaly、new physics
- 別release、別event、別triad、別parameterへの一般化
- notebook/HDF5矛盾をLVKの公式erratumと呼ぶこと

## 9. 閉鎖状態

本成果物は独立した完成済みpost-closure archiveとして閉鎖する。今回の問いに対する追加の救済解析は不要であり、同じデータで別predictor・部分event・部分parameterを試すことは推奨しない。将来別releaseへ運ぶ場合は新しいidentity/schema/semantic auditと別契約が必要である。
