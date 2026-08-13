# 再現性マップ

- RUN02–RUN06の各starter ZIPには、そのRUNの契約、実行コード、テスト、manifestが含まれる。
- 各result ZIPは外部SHA-256と内部manifestで固定される。
- RUN06の元成果物は実行証跡として非正本扱いで保持し、残留失敗JSONを除去した修正版を正本とする。
- 公式HDF5は再取得可能な外部資産として本体を同梱せず、provenanceのみ保存する。
- RUN07はファイル照合・コピー・manifest生成のみで、科学計算を行わない。
