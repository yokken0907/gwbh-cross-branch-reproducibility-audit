# GWBH 再現性リポジトリ

本リポジトリは、8枝の重力波ブラックホール dependency / provenance 監査について、**最終報告状態を第三者が検証・再計算するための軽量再現性リポジトリ**である。

**v1.2** は論文に対応するpublication-layer correction版である。凍結済みv1.1.0科学baseline、すなわちProject Master、8枝closure、28-pair identity matrix、16-edge atlas、B01/B08数値結果、U03/XR01数値証拠は変更しない。v1.2で変更するのは外部読者向け用語、version metadata、figure/source label、integrity bookkeepingのみである。A01/A02のbyte identityは歴史的GitHub Release v1.0.0に固定される。

## Version lineage

- **v1.0.0 GitHub Release**: A01/A02の不変release-asset baseline。
- **v1.1.0 repository tag**: post-closure科学更新を含む凍結科学baseline。移動・上書きしない。
- **v1.2**: publication-layer correction版。v1.1.0から科学数値・歴史的closureは変更しない。

本修正版source treeを識別する予定のimmutable tagは `v1.2` である。静的repository fileはversion identityを記載するものであり、GitHub UIのlive公開状態そのものを主張しない。

## 科学的境界

U03/XR01は各凍結PE frame内での**成果物内summary-to-full-posterior順位相関**のみを支持する。predictorとresponseは同じreleased PE productsから構成されscale情報を共有するため、外部予測性能の検証ではない。XR01は異なるGWTC-4.1非重複cohortで同じ限定的順位相関が再現したことを示すが、strict replicationではない。model truth/superiority、因果的systematics、cross-branch propagation、GR/Kerr/no-hair、anomaly、新物理を主張しない。

## 外部読者向け用語

`Master`、`NO_GO/HOLD`、`RUNxx/Uxx/Pxx/Mxx`、`RESULTS_FOR_REVIEW`、historical `ERRATUM` の意味は `TERMINOLOGY_GUIDE.md` を参照。これらはprovenance保持用のtechnical identifiersであり、物理的null result、公式LVK erratum、journal peer reviewを意味しない。
