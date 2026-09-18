# Repository record: direct-wave amplitude convention audit

Manuscript: **Reference-time and analysis dependence of fitted direct-wave amplitudes after rational quasinormal-mode filtering in numerical-relativity ringdowns**

Revision: final-candidate minor revision, 2026-09-18.

Reproducibility bundle:
`DIRECT_WAVE_AMPLITUDE_REPRODUCIBILITY_ARCHIVE_v1.0.0_20260918.zip`

SHA-256:
`5b8af8da53213fb290db5dae8e77a7636bde8ad6abd7ae73030577e8b9db0240`

The bundle supplied with the manuscript contains:
- analysis scripts for the frozen major-revision reanalysis;
- machine-readable source tables for every numerical result quoted in the manuscript;
- exact software/environment and source-commit records;
- input SHA-256 authority and pre-analysis specification;
- filter-start, interpolation, FFT, taper, endpoint, fit-window, covariance, basis, and conditioning conventions;
- the minor-revision reference-epoch transport table and sign-convention record.

Reference-epoch convention:
`y(t)=C(t0) exp[-i omega (t-t0)]`,
`C(t1)=C(t0) exp[-i omega (t1-t0)]`.

All quoted Kerr QNMs use the regular/prograde `sign=+1` branch in the pinned qnmfits implementation.

This record identifies the exact archive by cryptographic hash; the manuscript submission package carries the corresponding archive file.