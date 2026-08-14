# GWBH-PIA マスター参照パッケージ v1.0.0

## 目的
重力波連星ブラックホール推論依存性監査のRUN01～RUN31を、
過去スレッドへ戻らず即時参照できる研究資産として統合した。

## 最初に読むファイル
1. `00_MASTER_OVERVIEW/BRANCH_CLOSURE_REPORT_JA.md`
2. `00_MASTER_OVERVIEW/CLAIM_BOUNDARIES.md`
3. `04_SYNTHESIS/CONFIRMATORY_RESULT_INDEX.csv`
4. `04_SYNTHESIS/DIRECT_AUDIT_SCREENING_RANKS_1_8_AND_13.csv`
5. `07_NEXT_BRANCH_CONNECTIONS/RESULT_TO_NEXT_BRANCH_MAP.csv`

## 収録範囲
- RUN01～RUN13：release drift監査
- RUN14～RUN21：固定release公開解析チェーン依存性監査
- RUN22～RUN30：カタログスクリーニングと直接追跡
- RUN31：第一枝科学的閉鎖

## 再現性
`08_ARCHIVED_RUN_PACKAGES/`に各RUNの正本結果ZIPとSHA-256を収録した。
生HDF5、strain、仮想環境、キャッシュは含めない。
元データのURL、ファイル名、サイズ、checksumは各RUNパッケージ内にある。

## 次枝
第一候補は、事象レベルの質量・スピンposterior依存性が
人口推論へどう伝播するかの監査である。
