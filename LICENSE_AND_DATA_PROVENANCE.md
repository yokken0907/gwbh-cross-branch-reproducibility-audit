# License and Data Provenance

The root `LICENSE` defines the repository-authored licensing split:

- original repository source code: MIT License;
- original documentation, indexes, and synthesis metadata: CC BY 4.0;
- third-party scientific data/materials: original provider licenses and terms remain controlling.

Upstream LVK, GWOSC, Zenodo, DCC, and other third-party assets are not relicensed by inclusion, indexing, hashing, or preservation inside this repository or its Release assets.

The v1.1.0 Git extract excludes the official GWTC-5.0/GWTC-4.1 PE notebooks and HDF5 summary files used by U03/XR01. Their identities and provenance are retained in the corresponding input-audit and preflight records. The complete review archives likewise retain no raw event posterior HDF files; reruns reacquire them from the official public source and delete them after derived-output persistence.

The authoritative provenance for scientific inputs is the source-freeze, provenance, configuration, manifest, and sidecar material preserved in the corresponding branch/run evidence. When an external public asset is not embedded, its frozen identifier must be used rather than substituting an unrecorded source.
