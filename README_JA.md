# GWBH 再現性リポジトリ

本リポジトリは、8枝の重力波ブラックホール dependency / provenance 監査について、**最終的に報告された監査状態を第三者が検証・再計算するための軽量再現性リポジトリ**である。v1.1.0はv1.0.0のMaster・branch closure・16-edge atlasを変更せず、独立にversionされたB04/U02、U03、XR01のpost-closure証拠層を追加する。

Status: 2026-08-14生成のv1.1.0 source/release candidate。明示的に公開されるまではpublic GitHub releaseはv1.0.0である。

## 収録するもの

- B01–B08の最終closure証拠
- 28-pair identity matrixと16-edge cross-branch atlas
- allowed / forbidden claim boundaryとreopen条件
- B01 exact permutation結果のconfirmatory package
- Release Asset A01/A02から直接動作するB08数値再現module
- Zenodo 21454847に対するB04/U02 schema/provenance-only `NO_GO`
- GWTC-5.0 U03 22事象screening-calibration証拠
- GWTC-4.1 XR01 44事象conceptual-transport証拠
- integrity、source provenance、Release asset検証script

## 本リポジトリの対象外

これは研究過程の全旧RUNを時系列に再演するMaster-of-Allではない。再現対象は、**最終報告結果と、それを検証・再計算するために必要な証拠**である。

## Repository layers

```text
GitHub repository tree
        |
        +-- evidence / contracts / verification scripts
        +-- B01 confirmatory modules
        +-- B08 numerical reproduction module
        +-- post_closure_extensions/
        |    B04/U02 decision, U03 and XR01 evidence extracts
        |
        +--> Release Asset A01: Integrated Project Master
        |
        +--> Release Asset A02: B08 compact reproduction payloads
        |
        +--> Review Asset A03: GWTC-5.0 U03 reconsideration
        |
        +--> Review Asset A04: GWTC-4.1 XR01 transport
```

A01は8枝canonical MasterとXBICA最終統合証拠を含む正本Project Master。A02はB08の大型posterior JSON 21本をbyte-identicalのまま圧縮保持し、元の大型evidence companion 2本をbyte-for-byteで復元できる。A03/A04は独立したpost-closure拡張archiveであり、A01を置換しない。

## Quick verification

```bash
python scripts/verify_repository_tree.py
python scripts/verify_key_results.py
python scripts/verify_post_closure_extensions.py
python scripts/verify_release_assets.py /path/to/downloaded/release-assets
```

## B08数値再現

```bash
python reproduction_modules/B08/run_reproduction.py \
  --project-master /path/to/GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip \
  --b08-payload /path/to/GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip \
  --output-dir ./reconstructed_outputs/B08
```

詳細は`reproduction_modules/B08/README.md`を参照。

## 既存の最終科学閉鎖（不変）

`FINAL_PROJECT_SCIENTIFIC_CLOSED_EIGHT_BRANCH_DEPENDENCY_ATLAS_COMPLETE_NO_CROSS_BRANCH_NUMERIC_PROPAGATION`

16 edge:

- PARTIAL_STRUCTURAL: 8
- IDENTITY_ONLY: 3
- BLOCKED_PUBLIC_ASSET: 3
- BLOCKED_SCHEMA: 2
- DIRECT_NUMERIC: 0

## 科学的境界

integrity PASSや数値再現PASSは、物理的真理の証明とは別である。B03はpublic-asset NO-GO、B04はschema HOLD、B07はcompatible replication test未実行、B08はprimary 10/12のreleased-output dependency auditとして維持する。U03/XR01は公開PE内の限定的screening calibrationおよびconceptual transportであり、strict replication、model truth/superiority、因果的systematics、cross-branch propagation、GR/Kerr/no-hair、anomaly、新物理を主張しない。

XR01後の同一データ追加variantは`NO_GO_FURTHER_IMMEDIATE_SAME_DATA_ANALYSIS__XR01_EXTENSION_COMPLETE`で停止した。再開には新しい公式PE releaseまたは独立cohortと、target値閲覧前の新規audit/preregistration/SHA-256 lockが必要である。
