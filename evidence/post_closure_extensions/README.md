# Post-closure extensions

This directory is a **separately versioned evidence layer** added after the historical eight-branch Project Master reached final closure. It does not edit, replace, reopen, or reclassify the Project Master, any branch closure, the 28-pair identity matrix, or the frozen 16-edge atlas.

## Contents

- `B04_U02/DECISION.json` — schema/provenance-only audit of Zenodo record 21454847 (`pSEOB.tar.gz`, `QNMRF.tar.gz`, and `RD.tar.gz`). It stopped at `NO_GO / B04_U02_REOPEN_NOT_SATISFIED` before numerical analysis. P02 values read = 0; M01 values computed = 0.
- `U03_GWTC5/` — browsable extract of the independently versioned GWTC-5.0 alternate-triad/common-five reconsideration. The historical RUN01 gate stop is preserved under `PARENT_REFERENCE/`; the corrected all-22 rank-association analysis is a different analysis with a disclosed retrospective-summary/posterior-outcome-blind evidence class.
- `XR01_GWTC41/` — browsable extract of the target-value-blind GWTC-4.1 all-44 disjoint-cohort rank-association analysis. It uses a substituted middle model and is not an exact-triad strict replication.
- `figures/` — publication figure and its exact 66-row event-level source table.
- `POST_CLOSURE_SYNTHESIS.json` — compact machine-readable status map.
- `NEXT_STEP_DECISION.json` — formal stop decision after XR01.

## Full review archives

The repository extracts omit third-party upstream notebook/HDF5 files and the archive-level manifests that enumerate those omitted bytes. The complete self-verifying archives remain separately versioned review archives A03 and A04:

- A03: `GWBH_ERIA_U03_ALTTRIAD_COMMON5_INDEPENDENT_RECONSIDERATION_v1.0.0_RESULTS_FOR_REVIEW_REGENERATED_20260814.zip`
- A04: `GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_v1.0.0_RESULTS_FOR_REVIEW.zip`

Each full archive includes its own `MANIFEST.csv`, `SHA256SUMS.txt`, and `VERIFY_PACKAGE.py`. The repository-wide integrity manifest covers this browsable extract.

## Scientific boundary

The U03 and XR01 results support positive within-product summary-to-full-posterior rank associations within two exact frozen PE frames. Predictor and response use the same released PE products and share scale information, so this is not external predictive validation. They do not establish waveform-model truth or superiority, causal waveform systematics, B01/B07 strict replication, cross-branch numerical propagation, population/selection/ringdown/cosmology effects, GR/Kerr/no-hair consistency, anomaly, new physics, or frame-external generalization.

## 日本語要約

この層は既存 Master／各 branch の科学的 closure を変更しない独立 extension である。B04/U02 は schema/provenance-only の `NO_GO`、U03 は22事象の限定的な事後的 summary-to-full-posterior 順位相関解析、XR01 は44事象の非重複コホートで同じ正の順位相関が再現した cross-release 解析である。XR01後の同一データ追加解析は outcome-unblinded multiplicity のため `NO_GO` とした。
