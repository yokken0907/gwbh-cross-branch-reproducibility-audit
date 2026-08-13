# Stopping rule

Phase 5の全結果は`COMPLETE_STOPPED`であり、同じrunnerはPhase 6を開始しない。

- `FROZEN`: predecessor chain、22 pair、primary parameter、M01、0.5 threshold、Phase 6 execution/stop policy、component hashがすべて一致し、通信・payload・数値・holdout accessが0。
- `HOLD_PHASE5_PREDECESSOR_INTEGRITY`: Phase 4または入れ子のPhase 3/2 identity、manifest、status、pair/object/inventory evidenceに不整合。
- `HOLD_PHASE5_CONTRACT_INTEGRITY`: parameter、pair selection、metric、threshold、Phase 6 policy、contract component hashに不整合。
- `HOLD_IMPLEMENTATION_ERROR`: code、tests、manifest、result生成、independent review、packagingに異常。

Phase 6では22組すべてをeffect-based early stopなしで処理する。全22組resolvedなら`PRIMARY_RESULT_COMPLETE`、1組以上resolvedかつ残りunresolvedなら`PRIMARY_RESULT_PARTIAL`、0組resolvedなら`HOLD_PRIMARY_SCHEMA_UNRESOLVED`とする。archive/input不整合は`HOLD_PRIMARY_INPUT_INTEGRITY`、実装異常は`HOLD_IMPLEMENTATION_ERROR`とする。いずれも`COMPLETE_STOPPED`でPhase 7を自動開始しない。

