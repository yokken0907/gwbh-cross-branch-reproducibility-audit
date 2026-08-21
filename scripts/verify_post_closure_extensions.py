#!/usr/bin/env python3
"""Deterministically verify the browsable post-closure evidence layer."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "evidence" / "post_closure_extensions"
U03 = BASE / "U03_GWTC5"
XR01 = BASE / "XR01_GWTC41"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def close(a, b, tol=1e-15):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


checks: list[tuple[str, bool]] = []


def check(name: str, condition) -> None:
    checks.append((name, bool(condition)))


# B04/U02: schema/provenance-only terminal NO_GO.
b04 = load_json(BASE / "B04_U02" / "DECISION.json")
check("B04-decision-NO_GO", b04["decision"] == "NO_GO")
check("B04-reopen-not-satisfied", b04["decision_code"] == "B04_U02_REOPEN_NOT_SATISFIED")
check("B04-schema-provenance-only", b04["scope"] == "schema/provenance-only")
check("B04-no-numeric-analysis", not b04["numeric_analysis_authorized"] and not b04["numeric_analysis_performed"])
check("B04-zero-values", b04["p02_values_read"] == 0 and b04["m01_values_computed"] == 0)
check("B04-closure-unchanged", b04["historical_b04_closure_changed"] is False)


def verify_run(base: Path, expected_n: int, expected_cells: int, expected_rho: float,
               expected_finite: int, expected_verdict: str, label: str) -> set[str]:
    primary = load_json(base / "06_RUN_OUTPUT" / "PRIMARY_TEST.json")
    decision = load_json(base / "06_RUN_OUTPUT" / "DECISION.json")
    independent = load_json(base / "06_RUN_OUTPUT" / "INDEPENDENT_REPRODUCIBILITY_VERIFICATION.json")
    internal = load_json(base / "06_RUN_OUTPUT" / "INTERNAL_VALIDATION.json")
    events = load_csv(base / "06_RUN_OUTPUT" / "EVENT_METRICS.csv")
    cells = load_csv(base / "06_RUN_OUTPUT" / "CELL_METRICS.csv")
    counts = load_csv(base / "06_RUN_OUTPUT" / "POSTERIOR_VALUE_COUNTS.csv")
    errors = load_csv(base / "06_RUN_OUTPUT" / "ERROR_LEDGER.csv")
    post_log = (base / "07_REPRODUCIBILITY" / "POST_RUN_TEST_LOG.txt").read_text(encoding="utf-8")

    check(f"{label}-n", primary["n"] == expected_n and len(events) == expected_n)
    check(f"{label}-cells", len(cells) == expected_cells and decision["posterior_cells"] == expected_cells)
    check(f"{label}-rho", close(primary["observed_spearman_rho"], expected_rho))
    check(f"{label}-permutations", primary["permutations"] == 1_000_000)
    check(f"{label}-extreme-count", primary["one_sided_extreme_count"] == 0)
    check(f"{label}-plus-one-p", close(primary["one_sided_plus_one_p"], 9.99999000001e-7, 1e-18))
    check(f"{label}-verdict", primary["verdict"] == expected_verdict and decision["decision"] == expected_verdict)
    check(f"{label}-no-rescue", decision["event_replacement_or_rescue"] is False)
    check(f"{label}-no-closure-effect", decision["historical_closure_effect"] == "NONE")
    check(f"{label}-claim-flags", not decision["strict_replication_claim"] and not decision["model_superiority_claim"] and not decision["new_physics_claim"])
    check(f"{label}-independent-23-of-23", independent["status"] == "PASS" and independent["checks_passed"] == 23 and independent["checks_total"] == 23 and all(item["pass"] for item in independent["checks"]))
    check(f"{label}-independent-code-path", independent["verifier_imports_frozen_runner"] is False)
    check(f"{label}-internal-validation", internal["status"] == "PASS" and internal["observed_events"] == expected_n and internal["observed_cells"] == expected_cells)
    check(f"{label}-posterior-count-frame", len(counts) == expected_cells)
    check(f"{label}-finite-scalars", sum(int(row["finite_values"]) for row in counts) == expected_finite)
    check(f"{label}-no-nonfinite-scalars", all(int(row["nonfinite_values"]) == 0 for row in counts))
    check(f"{label}-minimum-count-gate", all(row["minimum_20_pass"] == "True" for row in counts))
    check(f"{label}-empty-error-ledger", len(errors) == 0)
    check(f"{label}-post-run-tests-11", ("11/11" in post_log) or ("Tests run: 11" in post_log and "Result: PASS" in post_log))
    return {row["event"] for row in events}


u_events = verify_run(
    U03, 22, 330, 0.9017504234895539, 5_173_800,
    "SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION", "U03",
)
x_events = verify_run(
    XR01, 44, 660, 0.9468639887244539, 9_872_875,
    "SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT", "XR01",
)
check("cohorts-disjoint", u_events.isdisjoint(x_events))

# Historical RUN01 is preserved, not repaired.
run01 = load_json(U03 / "PARENT_REFERENCE" / "RUN01_DECISION.json")
check("RUN01-formal-gate-stop", run01["decision"] == "NO_GO_NUMERIC_COMPLETE_FRAME_LT8")
check("RUN01-zero-complete-events", run01["gate_counts"]["numeric_complete_events"] == 0)
check("RUN01-122-upper-lower-failures", run01["gate_counts"]["triplets_upper_less_than_lower"] == 122)
check("RUN01-no-closure-effect", run01["parent_closure_effect"] == "NONE")
check("RUN01-stopped-before-posterior", "posterior sample access" in run01["stopped_before"])

# Publication figure source must be a lossless concatenation of the two event tables.
figure_rows = load_csv(BASE / "figures" / "PostClosure_EventMetrics_Source.csv")
check("figure-row-count", len(figure_rows) == 66)
check("figure-panel-counts", sum(row["panel"] == "A" for row in figure_rows) == 22 and sum(row["panel"] == "B" for row in figure_rows) == 44)
check("figure-event-union", {row["event"] for row in figure_rows} == u_events | x_events)

source_rows = {}
for base, panel in ((U03, "A"), (XR01, "B")):
    for row in load_csv(base / "06_RUN_OUTPUT" / "EVENT_METRICS.csv"):
        source_rows[(panel, row["event"])] = row
check(
    "figure-values-exact",
    all(
        close(row["predictor"], source_rows[(row["panel"], row["event"])]["predictor"])
        and close(row["full_response"], source_rows[(row["panel"], row["event"])]["full_response"])
        for row in figure_rows
    ),
)

# Repository extract deliberately excludes third-party raw source containers.
forbidden = [p for p in BASE.rglob("*") if p.is_file() and (p.suffix.lower() in {".hdf5", ".h5", ".ipynb", ".pyc"} or "__pycache__" in p.parts)]
check("repository-extract-no-upstream-raw-or-cache", not forbidden)

synthesis = load_json(BASE / "POST_CLOSURE_SYNTHESIS.json")
check("synthesis-no-closure-effect", synthesis["historical_closure_effect"] == "NONE")
check("synthesis-atlas-unchanged", synthesis["historical_states"]["edge_counts"] == {
    "PARTIAL_STRUCTURAL": 8,
    "IDENTITY_ONLY": 3,
    "BLOCKED_PUBLIC_ASSET": 3,
    "BLOCKED_SCHEMA": 2,
    "DIRECT_NUMERIC": 0,
})
next_step = load_json(BASE / "NEXT_STEP_DECISION.json")
check("next-step-NO_GO", next_step["decision"] == "NO_GO_FURTHER_IMMEDIATE_SAME_DATA_ANALYSIS__XR01_EXTENSION_COMPLETE")
check("next-step-no-closure-effect", next_step["existing_master_or_branch_closure_effect"] == "NONE")

failed = [name for name, passed in checks if not passed]
for name, passed in checks:
    print(("PASS" if passed else "FAIL"), name)
print(f"SUMMARY: {len(checks) - len(failed)}/{len(checks)} PASS")
raise SystemExit(0 if not failed else 2)
