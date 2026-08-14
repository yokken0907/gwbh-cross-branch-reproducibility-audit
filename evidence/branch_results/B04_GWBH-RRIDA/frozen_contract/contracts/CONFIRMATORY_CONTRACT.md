# Confirmatory contract

Phase 6のprimary analysis unitは、`PRIMARY_PAIR_SET.csv`に固定された22のevent-specific pyRing Kerr pairである。各pairは同一event・同一family・同一10M start tokenに属し、Phase 3でD05だけが明示差として認識された`B_DIRECT_PARTIAL` routeである。

primary parameterは`P02 final_spin`、primary metricは`M01`、operational thresholdは`M01 >= 0.5`である。0.5は両endpointの90% interval width平均の半分に相当する、事前固定したscale上の運用境界である。判定には丸め前の値を使う。

Phase 3で未解決だったprior、support、software、parameter schema等を「同一」と仮定して完全統制比較へ昇格させない。Phase 6のheader/config gateで必要条件を満たさないpairは`UNRESOLVED_NO_IMPUTATION`とし、別parameter・別pair・別eventへ差し替えない。

threshold超過はoutput sensitivityの運用分類であり、物理的新発見、一般相対論の破れ、Kerr/no-hair検定、統計的有意差、原因軸の単独因果効果を意味しない。
