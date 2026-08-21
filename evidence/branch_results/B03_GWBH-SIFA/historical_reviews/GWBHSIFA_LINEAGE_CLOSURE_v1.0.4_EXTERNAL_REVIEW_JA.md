# GWBH-SIFA LINEAGE_CLOSURE v1.0.4 外部独立検算

## 結論

- 正式runnerの出力判定は `COMPLETE_STOPPED / HOLD_AMBIGUOUS_LINEAGE`。
- L01–L10は全件 unresolved、Phase 4および数値計算は未実行。
- HOLDは、`LIVE_GITLAB_PIPE_VT_HELPER_V040` と `LIVE_GITLAB_PIPE_VT_HELPER_V043` に由来するL07 review候補2件だけで契約上成立する。
- ただし、DCC record監査に判定非変更の重要な実装上の不整合を1件検出した。このため、本runを「DCC depth-1監査が正常完了した証拠」やGO／NO-GO根拠として使用してはならない。

## DCC監査の不整合

対象URL：

- `https://dcc.ligo.org/LIGO-T2400110/public`
- `https://dcc.ligo.org/LIGO-T2400073/public`

両URLはHTTP 200を返したが、取得本文は正式recordではなく、次のDCCエラーページだった。

`Requested version of document does not exist.`

両本文は各4,128 bytesで、SHA-256も同一だった。

`18dd87f1c0dca902a53a4c1d893653459d27e6ab2e301de2031d4e3ae2e94ec9`

runnerはHTTP statusだけで成功を判定したため、両recordを `PASS`、そこから導出した空のdirect-link indexも `PASS` と記録し、DCC直接リンク0件・全source terminalと報告した。これは「record取得成功」または「depth-1直接リンク探索完了」を意味しない。

この不整合は現判定を変えない。L07 review queueが非空なので、DCC状態にかかわらず `HOLD_AMBIGUOUS_LINEAGE` が成立する。ただし、内部 `INDEPENDENT_REVIEW.json` のPASSはDCC本文の意味的正常性を検査していないため、外部検算としては無条件PASSにできない。

## L01–L10

| ID | 状態 | 主な候補とindependence family | 未解消理由 |
|---|---|---|---|
| L01 | Unresolved | `BBHMass_FlexibleMixtures.h5` lead／`POPULATION_DATA_RELEASE_CHAIN` | production-direct exact filenameなし |
| L02 | Unresolved | 適格候補なし | production spin representationの直接証拠なし |
| L03 | Unresolved | `at_least_one_search_far_rule`／`GWTC4_POPULATION_PAPER_CHAIN` | 適格familyが1系統のみ |
| L04 | Unresolved | `snr_10` supporting leadsのみ | production-linked適格証拠なし |
| L05 | Unresolved | `far_lt_1_per_year`、`far_lt_0.25_per_year`／`GWTC4_POPULATION_PAPER_CHAIN` | 同一family内の候補だけで、直接証拠も独立2 family一致もなし |
| L06 | Unresolved | `cWB,GstLAL,MBTA,PyCBC`／`GWTC4_POPULATION_PAPER_CHAIN` | 適格familyが1系統のみ |
| L07 | Unresolved | `o1_o2_o3_o4a_mixture` review候補2件／`GWPOPULATION_PIPE_REPO_HISTORY` | v0.4.0・v0.4.3 tagged code由来の同一family候補が未査定 |
| L08 | Unresolved | 適格候補なし | exact `gwpopulation` version／commitなし |
| L09 | Unresolved | v1.0.3由来5 tag／`GWPOPULATION_PIPE_REPO_HISTORY` | 5件は既査定nonresolving leadであり、直接証拠ではない |
| L10 | Unresolved | opaque provenance candidate／`GWTC4_POPULATION_PAPER_CHAIN` | exact output–selection mappingではない |

resolvedは0/10。auto-promotionは0件、eligible conflictは0件。v1.0.3のprior adjudication適用は5件で、いずれも証拠昇格していない。

## 検証結果

- starter SHA-256 sidecar：一致
- starter内部manifest：38/38一致
- Foundation内部manifest：167/167一致
- v1.0.3 checkpoint内部manifest：77/77一致
- preflight：PASS、issue 0件
- unit tests：27/27 PASS
- runner内independent review：PASS、issue 0件
- 追加独立検算：DCC semantic-error未検出を1件指摘
- network transport failure：0件。ただしDCC 2件はsemantic error pageであり、正常record取得ではない
- HDF収録／open：0
- events row access：0
- selection estimator／found mask／pdet／VT／ESS：未実行
- population／event posterior：未読
- Phase 4：未実行
- 結果ZIP：87ファイル、CRC PASS
- 結果manifest：86/86一致（manifest自身を除く）
- 結果ZIP SHA-256 sidecar：一致

## 将来修正が必要な点

次版starterでは、少なくとも以下を事前固定してから再実行する必要がある。

1. HTTP 200でもDCCの `<dl class="error">`、`Requested version of document does not exist.`、期待document ID不在を検出する。
2. その状態を `PASS` ではなく、契約で明示した `PUBLICLY_UNAVAILABLE`、review blocker、またはnetwork／source unresolved状態のいずれかへ分類する。
3. semantic error pageを模擬するunit testと、independent reviewによるDCC record identity検査を追加する。

本検算ではコード・契約・正式結果ZIPを変更せず、再実行もしていない。
