# GWBH-RRIDA MASTER REFERENCE / FINAL CLOSURE PACKAGE v1.0.0

## 正式状態

- 枝: `04_GWBH-RRIDA_重力波連星ブラックホール合体後天体・リングダウン推論依存性監査`
- Master status: `FINAL_CLOSED`
- 最終科学判定: `COMPLETE_STOPPED / HOLD_PRIMARY_SCHEMA_UNRESOLVED`
- Phase 6 / RUN03: **NOT AUTHORIZED / NOT PERFORMED**
- Phase 7: **NOT AUTHORIZED / NOT PERFORMED**
- P02 posterior値解釈: **0**
- M01算出: **0/22 pair**
- 物理主張: **0**

## このHOLDの意味

Phase 5で凍結した契約は、P02 `final_spin`を数値利用する前に、両endpointで共通の**宣言済みsupport**が確認できることを要求した。RUN01は44/44 `.dat` headerで`af`列を一意に認識したが、config gateは0/44だった。RUN02は凍結済み44 configを正常に構造解析したが、`af-min`、`af-max`、`fix-af`の直接宣言は全件0で、`DEFAULT`宣言・継承参照も0だった。

したがって、software defaultの推定、sample最小最大値の代用、別parameterへの差替え、事後的な契約変更を行わず、数値payloadを開く前に停止した。これは「final spinに物理的supportが存在しない」「pyRingが不正」「将来も証拠が得られない」という主張ではない。**凍結した公開archiveと凍結契約の組合せでは、許可された方法でsupportを立証できなかった**という監査結論である。

## 正本と文書優先順位

科学証拠の唯一のcanonical resultは次である。

`canonical/GWBHRRIDA_PHASE6_RUN02_v0.7.1_RESULTS_FOR_REVIEW.zip`

SHA-256: `8f59624885d9525719739a8e25b057870790745de5f7c780e3ba55b3297fb2e5`（972,496 bytes）

このZIP内部にRUN01からPhase 0までの10個のresult ZIP chainが再帰的に保存されている。`final_state/`と`frozen_contract/`は閲覧用のexact copyであり、canonical ZIPより優先されない。

ただしRUN02内の`NEXT_RUN_REQUIREMENTS_JA.md`はRUN02生成時点の引継ぎ文であり、その後の独立監査前に書かれた履歴である。最終的な続行可否は、本masterの`MASTER_STATUS.json`と`final_state/FINAL_CLOSURE_ADJUDICATION.json`が上位に立つ。

## RUN01訂正

RUN01ではconfig parse失敗後の空辞書同士を比較し、22 pairの`config_equal_except_mode`を誤って`true`と記録した。RUN02は同じ22 pairを過不足なく`NOT_EVALUATED`へ訂正した。数値処理は行われていないため数値影響は0だが、RUN01の`true`をconfig同一性の証拠として利用してはならない。

## 再開条件

同じarchiveと同じ証拠をreaderだけ変更して再実行するRUN03は行わない。再開は、P02の共通宣言supportを凍結契約に沿って直接確定できる新しい公式公開証拠が得られた場合に限り、**post-closure update**として本masterを改変せず別系統で行う。

## 整合性確認

外部sidecar、`MASTER_MANIFEST.csv`、`SHA256SUMS.txt`、および`tools/verify_master.py`で、master全体と10段の入れ子chainをnetworkなしで検証できる。
