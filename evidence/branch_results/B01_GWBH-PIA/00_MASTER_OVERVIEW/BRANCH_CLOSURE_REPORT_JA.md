# GWBH-PIA 第一枝・科学的閉鎖報告

## 判定
**PASS_GWBHPIA_FIRST_BRANCH_SCIENTIFIC_CLOSURE**

## 閉鎖対象
GWTC-4公開データにおける重力波連星ブラックホールのrelease更新差、
固定release内の公開解析チェーン依存性、要約表スクリーニング、
上位事象およびTier B境界事象の直接posterior監査を閉鎖する。

## 独立確認
- Release drift：rho 0.88095238、
  exact片側p 0.00362103
- Fixed-release analysis-chain dependence：rho
  0.95238095、
  exact片側p 0.00057044、
  Kendall tau-b 0.85714286

## スクリーニング追跡
screen rank 1～7は全件直接監査済みであり、
posterior中央値W1は
0.087447～
0.124259、
CLEARは17/24～
21/24だった。

事前固定したTier B境界は、
rank 8がposterior中央値W1
0.067994、
CLEAR 16/24、
rank 13がposterior中央値W1
0.053221、
CLEAR 11/24だった。

上端から下端へ全体依存性は弱まったが、rank 13でもfinal spinなど
個別パラメータには大きな依存性が残った。

## 限定的結論
GWTC-4の公開要約情報は、事前定義された適格事象群の中で、
posterior公開解析チェーン依存性の順位を監査する低コストな
スクリーニング層として機能した。

本結果は波形モデル単独の誤差、特定モデルの正しさ、
ブラックホール新物理、観測異常を示さない。

## 停止
Tier Cは本枝で直接監査しない。
RUN21以後に新しい確認p値を追加しない。
RUN32でRUN01～RUN31をマスターパッケージ化する。
次枝の第一候補は人口推論への伝播監査とする。
