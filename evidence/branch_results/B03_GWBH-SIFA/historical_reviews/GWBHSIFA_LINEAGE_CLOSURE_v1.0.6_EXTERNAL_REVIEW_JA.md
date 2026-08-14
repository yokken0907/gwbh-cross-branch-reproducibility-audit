# GWBH-SIFA LINEAGE_CLOSURE v1.0.6 外部独立検算

検算日: 2026-08-10 (UTC)

## 1. 結論

正式runnerは未改変で1回実行され、`COMPLETE_STOPPED / HOLD_AMBIGUOUS_LINEAGE`で正常停止した。

この最終判定は妥当である。L01–L10は全件未解消であり、L07に未査定のproduction-linked候補2件が残るため、凍結契約上は`HOLD_AMBIGUOUS_LINEAGE`が必須となる。Phase 4、HDF row access、selection数値計算は実行されていない。

ただし、DCC probeの下位semantic分類に、最終判定へ影響しない実装・仕様不整合を1件確認した。正式結果ZIPは変更していない。

## 2. 正本・実行整合性

- starter ZIP SHA-256: `5bc6a1f218cf6a779db6af6e3f3f169637d1fc55ec8fbc20bbb17c764f29d144`
- starter sidecar: 一致
- starter ZIP CRC: PASS
- starter manifest: 52/52 PASS
- Foundation v1.0.1内部manifest: 167/167 PASS
- v1.0.3 adjudication正本内部manifest: 77/77 PASS
- v1.0.5 checkpoint内部manifest: 96/96 PASS
- preflight: PASS、issue 0件
- unit tests: 53/53 PASS
- runner内independent review: PASS、issue 0件

## 3. DCC reference-resolution

- resolver controls: 2/2 `PASS_IDENTITY`、HTTP 200
- target: `LIGO-T2400110`、`LIGO-T2400073`
- target probes: 各42件、合計84件
  - unversioned public alias: 各1件
  - legacy bare-ID resolver: 各1件
  - version-qualified public path v1–v20: 各20件
  - legacy version resolver v1–v20: 各20件
- target HTTP response: 84/84 HTTP 200
- transport/network transient: 0件
- accepted public identity: 0件
- target resolution state: 2/2 `REFERENCE_NOT_PUBLICLY_RESOLVED`
- depth-1 discovery: 0件（identity PASS前には実行されていない）
- controlの科学証拠混入: 0件

`REFERENCE_NOT_PUBLICLY_RESOLVED`は、凍結されたpublic probe範囲で公開record identityを解決できなかったという限定結論であり、対象documentの絶対不存在を意味しない。

## 4. L01–L10とHOLD根拠

全要件がUnresolvedで、resolvedは0/10である。

- L01、L02、L08、L09: production-direct exact evidenceなし
- L03: eligible evidenceは`GWTC4_POPULATION_PAPER_CHAIN`の1 independence familyのみ
- L04: production-linked eligible evidenceなし
- L05: eligible evidenceは`GWTC4_POPULATION_PAPER_CHAIN`の1 familyのみ
- L06: eligible evidenceは`GWTC4_POPULATION_PAPER_CHAIN`の1 familyのみ
- L07: eligible evidenceなし。`LIVE_GITLAB_PIPE_VT_HELPER_V040`と`LIVE_GITLAB_PIPE_VT_HELPER_V043`の2件がreview queue入り。両者は同一`GWPOPULATION_PIPE_REPO_HISTORY` family
- L10: opaque provenance候補が1 familyのみで、exact mappingではない

review queue 2件が残るため、NO-GOへの遷移は禁止され、`HOLD_AMBIGUOUS_LINEAGE`となる。eligible conflictは0件、auto-promotionは0件、v1.0.3 prior adjudication適用は5件で、いずれもevidence promotionには使われていない。

## 5. 判定非影響のsemantic分類不整合

84 target probeの内訳は次のとおりである。

- 74件: `DCC_SEMANTIC_ERROR`
- 10件: `DCC_IDENTITY_MISMATCH`

後者10件の本文には、`This document is not publicly accessible.` と明記され、同時に`<dl class="error">`が存在する。しかし次の2点により、private/auth surfaceまたはsemantic errorとして捕捉されていない。

1. `semantic_error_html_class_regex`が過剰にescapeされ、`<dl class="error">`にmatchしない。
2. private-access文言が`auth_page_markers`に含まれていない。

その結果、期待document IDが本文に無いことだけを理由に`DCC_IDENTITY_MISMATCH`へ分類された。README・contractが意図する「authentication/private surfaceを`DCC_AUTH_REQUIRED`として分離する」という下位分類とは一致しない。

影響評価:

- 10件は公開identity PASSではなく、transport failureでもない。
- `DCC_IDENTITY_MISMATCH`、`DCC_SEMANTIC_ERROR`、`DCC_AUTH_REQUIRED`はいずれも凍結policy上terminal probe stateである。
- target 2件の`REFERENCE_NOT_PUBLICLY_RESOLVED`は変わらない。
- L07 review queue 2件だけで`HOLD_AMBIGUOUS_LINEAGE`が成立する。

したがって、最終HOLD判定、network failure 0件、depth-1未実行という主要結果は有効である。一方、正式outputを「private/auth surfaceが0件だった」という根拠には使用してはならない。

次版では、実取得したprivate-access pageを使う回帰test、regex escape修正、private-access markerの`DCC_AUTH_REQUIRED`優先分類、independent reviewでの誤分類検出を追加する必要がある。

## 6. 結果ZIP検証

- result ZIP SHA-256: `1bb81607f823ee520401c9aebb54ffec5c5250ccf85e831a9549b53c37e17e67`
- external sidecar: 一致
- ZIP CRC: PASS
- ZIP file count: 192
- internal result manifest: 191/191 PASS
- manifest外の余分なmember: 0件
- unsafe path: 0件
- HDF/H5 member: 0件
- source ledger: 29/29 terminal
- LIVE HTTP sources: 19/19 PASS、HTTP 200
- events rows read: 0
- selection estimator / found mask / pdet / VT / ESS: 未実行
- Phase 4: 未実行

正式成果物は独立監査に必要なcontract、registry、policy、source cache、DCC probe audit、evidence table、review queue、upstream/checkpoint、tests、logs、manifestを収録している。
