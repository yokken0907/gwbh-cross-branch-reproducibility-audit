# Reproducibility Guide

1. Verify the Master ZIP against its `.sha256`.
2. Verify both external evidence companion ZIPs against their `.sha256` sidecars.
3. Read `EXTERNAL_EVIDENCE/FINAL_EVIDENCE_SET.json`.
4. Compare the companion payload manifests stored in this Master to the manifests inside the companion ZIPs.
5. `CANONICAL_LINEAGE/` contains the exact Phase7 canonical review ZIP. Its recursive lineage contains Phase6→Phase5→Phase4→Phase3→Phase2→Phase1→Phase0.
6. `PLAN/` contains the original Branch08 verification plan.
7. `DIRECT_FINAL_CLOSURE/` provides convenience copies of the final scientific artifacts.
8. Phase8 itself performs no scientific analysis.
