# Official source references

- GWTC-5.0 Parameter estimation data release, Part 1: https://zenodo.org/records/20348005
- GWTC-5.0 Parameter estimation data release, Part 2: https://zenodo.org/records/20348006
- GWTC-5.0 observations paper record: https://dcc.ligo.org/LIGO-P2600152/public
- GWTC-5.0 Tests of General Relativity data release audited for B04/U02 context: https://zenodo.org/records/21454847

The exact summary HDF5 and official PE notebook bytes used here are retained under `03_INPUT/`. The 22 event HDF files are not retained; their official URLs, sizes and MD5 values are frozen in `03_INPUT/CANDIDATE_EVENT_FREEZE.csv`, while observed SHA-256 values and deletion attestations are recorded in `06_RUN_OUTPUT/EVENT_FILE_IDENTITY.csv`.

The official notebook states that `*_lower` and `*_upper` are q05 and q95 values. The released HDF5 bytes do not implement that statement. The bounded out-of-candidate posterior comparison is recorded under `01_DESIGN_AUDIT/` and must be described as a documented notebook/data inconsistency, not an official LVK erratum.
