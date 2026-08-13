# GWBH-SSIDA Master Reference Package v1.0.0

## 最終状態
- Master: `MASTER_COMPLETE`
- Branch: `FINAL_CLOSED`
- Scientific closure: `FINAL_SCIENTIFIC_CLOSED_PUBLIC_OUTPUT_DEPENDENCY_AUDIT_COMPLETE_PARTIAL_PRIMARY_10_OF_12`
- Primary: `PARTIAL_PRIMARY_VALID_10_OF_12_TWO_PUBLIC_OUTPUT_LIMITED`

## 科学的意味
GWTC-5の公開standard-siren H0 posteriorは、監査したpipeline / catalog / weighting /
population model / IFAR等の公開解析選択に対して完全には不変ではない。

ただし本枝は:
- 真のH0を決定しない
- ハッブルテンションを解決しない
- posterior差をbias/errorへ因果帰属しない

Phase4 primaryはC01-C10の10/12がvalid。
C11/C12はGW170817のpublic artifactがgrid+density表現だったためprimaryではPUBLIC_OUTPUT_LIMITED。
Phase5の公式grid-density変換はpost-hoc diagnosticでありprimaryへ昇格しない。

## 外部large evidence
容量重複を避けるため、Phase3/Phase5のlarge evidence companionはMaster ZIPへ再格納していない。
`EXTERNAL_EVIDENCE/FINAL_EVIDENCE_SET.json` とpayload manifestに完全なSHA identityを固定済み。

完全保存はMaster 2点 + companion 4点の6ファイル。
