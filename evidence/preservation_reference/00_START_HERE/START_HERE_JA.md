# ブラックホール検証 — MASTER OF ALL v1.0.0

このフォルダを、今後このブラックホール検証プロジェクトを参照する**最上位の入口**として使用してください。

## 最終状態

- Project: `GWBH-XBICA`
- Status: `MASTER_COMPLETE / FINAL_CLOSED`
- Scientific closure:
  `FINAL_PROJECT_SCIENTIFIC_CLOSED_EIGHT_BRANCH_DEPENDENCY_ATLAS_COMPLETE_NO_CROSS_BRANCH_NUMERIC_PROPAGATION`

## まず何を見ればよいか

### 1. プロジェクト全体を知りたい
`../01_PROJECT_MASTER/GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip`

これが**主たる参照先**です。
8本すべてのcanonical branch Masterがexact byteで内部に埋め込まれています。
全8枝の結論、dependency atlas、claim boundary、unresolved/reopen条件もここから辿れます。

Project Master SHA-256:
`87247fb2a664c127570008586cf17110f60e9dc4544899291bca70afa8e1d1f2`

### 2. 最終Masterがどう検証されたか確認したい
`../02_FINAL_AUDIT/GWBHXBICA_PHASE5_RUN01_v1.0.0_RESULTS_FOR_REVIEW.zip`

Phase5の最終packaging / independent review / integrity auditです。

Final Audit SHA-256:
`e5f1f54bf12d57130679a37e8277993fcc03707f623d94e24e8aa68da71b333b`

### 3. B08 GWBH-SSIDA の大容量raw evidenceが必要
`../03_EXTERNAL_EVIDENCE/B08_PHASE3/`
`../04_EXTERNAL_EVIDENCE/B08_PHASE5/`

これらは容量重複を避けるためProject Master本体には再格納されていません。
完全なbyte-level evidence再現時のみ参照してください。

## 8枝の位置づけ

- B01 GWBH-PIA — event-level PE / analysis-chain dependency
- B02 GWBH-PIPA — population inference
- B03 GWBH-SIFA — selection/injection; `NO_GO_PUBLIC_ASSETS_INSUFFICIENT`
- B04 GWBH-RRIDA — remnant/ringdown; `HOLD_PRIMARY_SCHEMA_UNRESOLVED`
- B05 GWBH-DCIDA — candidate/detection/catalog surface
- B06 GWBH-SCDQDA — public strain/DQ/calibration
- B07 GWBH-ERIA — independent-release transport; no replication test executed
- B08 GWBH-SSIDA — standard-siren cosmology; partial primary 10/12

## 最終横断atlas

- `PARTIAL_STRUCTURAL`: 8
- `IDENTITY_ONLY`: 3
- `BLOCKED_PUBLIC_ASSET`: 3
- `BLOCKED_SCHEMA`: 2
- `DIRECT_NUMERIC`: 0
- `UNRESOLVED_ATTRIBUTION`: 8

## 重要な解釈境界

このプロジェクトは、8枝を一本の数値因果鎖として証明したものではありません。
成果は、公開データ・公開スキーマ・release/frame・replication条件のもとで、
**どこまで接続可能で、どこで再現可能性が途切れるかを固定した依存性・provenance atlas**
です。

真のH0、ハッブルテンション解決、新しいブラックホール基本法則は主張しません。

## 完全性確認

`../99_INTEGRITY/MASTER_OF_ALL_MANIFEST.csv`
`../99_INTEGRITY/SHA256SUMS.txt`
`../99_INTEGRITY/PACKAGE_STATUS.json`

を参照してください。
