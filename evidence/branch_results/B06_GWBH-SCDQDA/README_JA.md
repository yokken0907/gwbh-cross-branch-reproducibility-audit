# GWBH-SCDQDA Master Reference Package v1.0.0

**科学閉鎖状態:** FINAL_CLOSED  
**Phase9:** assembly only / no new science

## 最終要約
- full candidate-release-detector metadata: 5345
- public provenance complete: 5174
- calibration-coverage-limited metadata: 171
- original selected C7 identities: 24
- bounded strain identities: 23
- candidate-detector strain windows: 40
- final classes:
  - PUBLIC_REPRESENTATION_SPECIFIC: 35
  - CALIBRATION_LIMITED: 5
- gating exact-zero presence window-sensitive: 1
- materiality threshold: OMITTED
- unresolved items: 4

`STRAIN_PRODUCT_SENSITIVE=0` は「公開strain productに数値差が無い」という意味ではない。
Phase3でconfirmatory materiality thresholdを凍結しなかったため、そのconfirmatory classを有効化していない。

## 大容量raw evidence
Phase5 RUN03 raw evidenceはMaster外部companionとしてexact SHA-256固定。
Master内にouter SHA、result manifest、160 payload個別SHA、取得ledger、環境、正式report/reviewを収録している。

## 禁止される解釈
production-searchへの影響、検出真偽、FAR/p_astro、PE parameter shift、population/ringdown影響を本Masterから推論しない。
