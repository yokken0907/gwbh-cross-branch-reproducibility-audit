# GWBH-XBICA Master Reference Package v1.0.0

## 最終状態
- Master: `MASTER_COMPLETE`
- Project: `FINAL_CLOSED`
- Scientific closure:
  `FINAL_PROJECT_SCIENTIFIC_CLOSED_EIGHT_BRANCH_DEPENDENCY_ATLAS_COMPLETE_NO_CROSS_BRANCH_NUMERIC_PROPAGATION`

## このMasterに入っているもの
- 8本のcanonical branch Master ZIPをexact byteで全て埋め込み
- XBICA Phase4 canonical scientific closure
- 原計画書
- 16-edge final dependency atlas
- 8-branch synthesis
- 28-pair identity anchor matrix
- project allowed / forbidden claims
- unresolved / reopen register
- frozen XBICA contracts
- reproducibility guide / manifests / hashes

## 最終科学的意味
このプロジェクトは、8枝を一本の数値因果鎖として証明したものではありません。
代わりに、公開データ・公開スキーマ・release/frame・replication条件の下で、
どこまで構造的/identity-levelに接続でき、どこで接続不能になるかを再現可能に固定しました。

Final atlas:
- PARTIAL_STRUCTURAL 8
- IDENTITY_ONLY 3
- BLOCKED_PUBLIC_ASSET 3
- BLOCKED_SCHEMA 2
- DIRECT_NUMERIC 0
- UNRESOLVED_ATTRIBUTION 8

## B08 large evidence
B08の約700MBの2 companionは容量重複を避けるためMasterへ再格納していません。
Phase5でouter SHA/CRC/payload manifest/全payload SHAを再検証済みです。

完全かつコンパクトな最終保存は6点:
1. このProject Master ZIP
2. sidecar
3. B08 Phase3 companion ZIP
4. sidecar
5. B08 Phase5 companion ZIP
6. sidecar

このMasterに8 branch Masterが埋め込まれているため、最終監査後は個別branch Masterを
作業保管から削除しても復元可能です。
