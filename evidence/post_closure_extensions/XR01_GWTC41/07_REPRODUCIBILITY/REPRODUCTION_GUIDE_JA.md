# 再現手順

## 依存環境

- Python 3.12.13
- numpy 2.5.2
- scipy 1.17.0
- h5py 3.14.0
- curl 8.5.0相当

隔離環境で `07_REPRODUCIBILITY/requirements.txt` を導入する。

## package整合性

archive展開直後に次を実行する。

```bash
python VERIFY_PACKAGE.py
sha256sum -c SHA256SUMS.txt
```

## 派生出力の独立検証

`verify_xr01.py` は凍結runnerをimportせず、summary tripletからpredictor、660 cellから
event response、固定乱数1,000,000置換を独立再生する。

```bash
python 07_REPRODUCIBILITY/verify_xr01.py
python -m unittest discover -s 05_TESTS -v
```

## 生データからの完全再実行

Zenodo record 20275769の公開HDF5を1事象ずつ取得する。各fileはsize/MD5照合後に処理し、
派生表を保存して即時削除される。約7.91 GBの転送が必要で、raw event HDFは保持しない。

再実行は新しい作業copyで行うこと。完成済みarchive上では `RUN_STATUS.json` が存在するため、
runnerは上書きを拒否する。

```bash
python 04_SRC/run_xr01.py --root .
```

Zenodoの将来版へ自動追随してはならない。record `20275769`、release tag
`IGWN-GWTC4p1-18965dda8_5`、各fileの固定size/MD5を使う。
