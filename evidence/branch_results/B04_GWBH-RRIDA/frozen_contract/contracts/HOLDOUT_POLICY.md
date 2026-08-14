# Holdout policy

GWTC-5はTGR run/output levelで封印を維持する。Phase 5はGWTC-5 paper、release、archive、run、config、posterior、plot data、event membershipを照会・開封しない。

GWTC-4.0 pyRing archiveもPhase 5では数値的・内容的に封印する。Phase 5が読むのは監査済み結果ZIP内の構造CSV、status、manifest、既知archive identity、member path/size inventoryだけである。`.dat`、`.ini`、header、sample、scientific valueは開かない。

