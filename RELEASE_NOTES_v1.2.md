# Release notes - v1.2

Prepared: 2026-08-20

## Scope

v1.2 is a **publication-layer correction release** built from the immutable v1.1.0 scientific baseline. It does not change any historical numerical result, Project Master state, branch closure, preregistration, 28-pair matrix, 16-edge atlas, or A01-A04 byte identity.

## Publication-layer changes

- replaced publication-facing `posterior screening` / `cross-release transport` shorthand with the more precise `within-product summary-to-full-posterior rank association` and `disjoint-cohort recurrence` language;
- retained historical machine-readable calibration/transport labels only as provenance identifiers;
- clarified that U03/XR01 predictor and response derive from the same released PE products and therefore do not constitute external predictive validation;
- changed keywords to `posterior rank association` and `cross-release recurrence`;
- simplified Technical Supplement C naming to `Reproducibility and Archive Guide`;
- distinguished v1.2 publication identity, frozen scientific baseline tag v1.1.0, and historical GitHub Release v1.0.0 A01/A02 identities;
- synchronized the publication figure/source labels with the bounded rank-association interpretation;
- regenerated repository/Supplement D manifests and checksums;
- restored active GitHub funding metadata and incorporated it into the v1.2 integrity manifest.

## Scientific values unchanged

B01 exact-permutation results, B02 association, B03/B04/B07 stop decisions, B05/B06 counts, B08 10/12 primary + 17/17 robustness + 2/2 post-hoc results, the 16-edge atlas, U03 rho `0.9017504234895539`, XR01 rho `0.9468639887244539`, and all historical claim/non-claim boundaries remain unchanged.

## Version rule

The existing v1.1.0 tag is immutable scientific provenance and must not be moved or overwritten. After this exact source tree is committed, create a new immutable `v1.2` tag for the publication version.
