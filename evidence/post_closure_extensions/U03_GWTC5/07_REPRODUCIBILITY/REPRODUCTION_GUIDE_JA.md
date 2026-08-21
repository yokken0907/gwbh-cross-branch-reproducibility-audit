# 再現ガイド

## 必要環境

- Python 3.12.13
- h5py 3.14.0
- numpy 2.3.5
- scipy 1.17.0
- curl 8.5.0相当
- Zenodoの公式event HDF 22件を順次取得できるネットワーク
- 一時的に最大約250 MBの空き領域

## 注意

このarchiveのrun directoryは再実行防止のため `RUN_STATUS.json` が存在する。監査済み成果物を上書きして再実行してはならない。再現する場合はarchive全体を別の新規directoryへ複製し、`06_RUN_OUTPUT` を空にしたうえで、元archiveとは別のreplay IDとして扱うこと。

## 1. 完成成果物の検証

archive rootで次を実行する。

```bash
sha256sum -c SHA256SUMS.txt
PYTHONPATH=/path/to/h5py python 07_REPRODUCIBILITY/verify_obrc.py
PYTHONPATH=/path/to/h5py python -m unittest discover -s 05_TESTS -v
```

期待値:

- package SHA-256: 全件PASS
- independent verifier: 23/23 PASS
- synthetic tests: 11/11 PASS

## 2. 新規replay

`06_RUN_OUTPUT` が空である独立複製に対して:

```bash
PYTHONPATH=/path/to/h5py python 04_SRC/run_obrc.py --root .
```

runnerは開始時に `02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json` の17ファイルをsize/SHA-256照合する。1ファイルでも違えばposteriorを開かず停止する。

## 3. データ処理

runnerは `03_INPUT/CANDIDATE_EVENT_FREEZE.csv` の順序で各event HDFを取得する。

1. official sizeとMD5を照合し、SHA-256を記録
2. exact `C00:<model>/posterior_samples` と5 fieldを検査
3. finite count gateを適用
4. 15 full W1と独立ECDF replay、80反復balanced値を計算
5. 派生表を原子的保存
6. event HDFを即時削除

どのgateでも失敗した時点で正式NO_GOを記録し、event/model/parameterの置換をしない。

## 4. 一次置換検定

全22件通過後にのみ、average-rank Spearman rhoと固定1,000,000 Monte Carlo置換を計算する。RNGは `numpy.random.PCG64DXSM(20260813)`、one-sided plus-one pを用いる。独立verifierはbatch幅7777で同じ乱数列とextreme countを再現する。

## 5. 保持しないデータ

22 event HDFはarchiveに含めない。公式filename、size、MD5、実測SHA-256、取得時間、削除確認は `06_RUN_OUTPUT/EVENT_FILE_IDENTITY.csv` に残す。summary HDF5と公式notebookは小さいためarchive内に保持する。
