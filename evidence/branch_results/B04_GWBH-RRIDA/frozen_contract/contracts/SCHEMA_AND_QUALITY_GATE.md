# Schema and quality gate

Phase 6は数値配列を解釈する前に、各endpointで次を順に検査する。

1. 凍結archive identityとexact member path・declared sizeが一致する。
2. header tokenをcasefoldし非英数字を除去した後、`PRIMARY_PARAMETER.csv`のaliasにexact matchする列がendpointごとに1列だけ存在する。
3. 両endpointで同じcanonical `final_spin`へ一意に解決し、direct sampled scalarであることがheader/configから確認できる。
4. 単位はdimensionlessで、declared supportが両endpointで共通である。supportが不明・異なる場合は比較しない。
5. 値はfiniteで、各endpointのrow countは1000以上、width90は正である。
6. weight列が無い場合だけimplicit unit weightを用いる。weight列が1本ある場合はfiniteかつstrictly positiveなlinear weightだけを認める。log weight、負値、0、複数候補、意味不明のweightは変換せず拒否する。
7. config差分がmode-content以外にも見つかった場合、metricを記述的に計算できてもpair gradeを`B_DIRECT_PARTIAL`より上げず、差分を明示する。primary causal claimは行わない。

0置換、範囲外sampleの切り落とし、手動列選択、fuzzy substring match、結果を見たalias追加は禁止する。

