#!/usr/bin/env python3
"""Independent derived-output verifier; does not import the frozen runner."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "06_RUN_OUTPUT"
MODELS = ("IMRPhenomXPHM-SpinTaylor", "SEOBNRv5PHM", "NRSur7dq4")
PAIRS = ((MODELS[0], MODELS[1]), (MODELS[0], MODELS[2]), (MODELS[1], MODELS[2]))
PARAMETERS = ("chirp_mass_source", "chi_eff", "luminosity_distance", "final_mass_source", "final_spin")
CANDIDATE_COUNT = 44
CELL_COUNT = CANDIDATE_COUNT * len(PAIRS) * len(PARAMETERS)
TRIPLET_COUNT = CANDIDATE_COUNT * len(MODELS) * len(PARAMETERS)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def independent_mc(x: np.ndarray, y: np.ndarray) -> tuple[float, int]:
    rank_x = rankdata(x, method="average")
    rank_y = rankdata(y, method="average")
    cx = rank_x - rank_x.mean()
    cy = rank_y - rank_y.mean()
    denominator = float(np.sqrt(np.dot(cx, cx) * np.dot(cy, cy)))
    observed = float(np.dot(cx, cy) / denominator)
    rng = np.random.Generator(np.random.PCG64DXSM(20260813))
    extreme = 0
    remaining = 1_000_000
    while remaining:
        batch = min(7777, remaining)
        order = np.argsort(rng.random((batch, y.size)), axis=1, kind="stable")
        statistics = cy[order] @ cx / denominator
        extreme += int(np.count_nonzero(statistics >= observed - 1e-15))
        remaining -= batch
    return observed, extreme


def verify() -> dict:
    checks: list[dict] = []

    def record(name: str, passed: bool, observed=None, expected=None) -> None:
        checks.append({"check": name, "pass": bool(passed), "observed": observed, "expected": expected})

    lock = json.loads((ROOT / "02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json").read_text(encoding="utf-8"))
    lock_failures = []
    for item in lock["locked_files"]:
        path = ROOT / item["path"]
        if not path.exists() or path.stat().st_size != int(item["size_bytes"]) or sha256(path) != item["sha256"]:
            lock_failures.append(item["path"])
    record("all_pre_posterior_locked_files_unchanged", not lock_failures, lock_failures, [])

    candidates = rows(ROOT / "03_INPUT/CANDIDATE_EVENT_FREEZE.csv")
    events = [row["event"] for row in candidates]
    record("candidate_frame_exactly_44_unique_events", len(events) == CANDIDATE_COUNT and len(set(events)) == CANDIDATE_COUNT, [len(events), len(set(events))], [CANDIDATE_COUNT, CANDIDATE_COUNT])

    triplets = rows(OUTPUT / "SUMMARY_TRIPLETS.csv")
    record("summary_triplets_exactly_660", len(triplets) == TRIPLET_COUNT, len(triplets), TRIPLET_COUNT)
    record("summary_triplets_all_pass", all(row["triplet_pass"] == "True" for row in triplets), sum(row["triplet_pass"] == "True" for row in triplets), TRIPLET_COUNT)
    triplet_map = {
        (row["event"], row["model"], row["parameter"]): {
            "median": float(row["median"]),
            "lower": float(row["lower_error"]),
            "upper": float(row["upper_error"]),
        }
        for row in triplets
    }
    replay_predictor = {}
    for event in events:
        maxima = []
        for parameter in PARAMETERS:
            pair_values = []
            for model_a, model_b in PAIRS:
                a = triplet_map[(event, model_a, parameter)]
                b = triplet_map[(event, model_b, parameter)]
                denominator = ((a["lower"] + a["upper"]) + (b["lower"] + b["upper"])) / 4.0
                pair_values.append(abs(b["median"] - a["median"]) / max(denominator, 1e-12))
            maxima.append(max(pair_values))
        replay_predictor[event] = float(np.median(maxima))
    predictor_rows = {row["event"]: float(row["predictor"]) for row in rows(OUTPUT / "EVENT_PREDICTORS.csv")}
    predictor_diff = max(abs(replay_predictor[event] - predictor_rows[event]) for event in events)
    record("predictor_independent_replay", predictor_diff <= 1e-15, predictor_diff, "<=1e-15")

    cells = rows(OUTPUT / "CELL_METRICS.csv")
    counts = rows(OUTPUT / "POSTERIOR_VALUE_COUNTS.csv")
    identities = rows(OUTPUT / "EVENT_FILE_IDENTITY.csv")
    record("posterior_cell_frame_44x15", len(cells) == CELL_COUNT, len(cells), CELL_COUNT)
    record("posterior_count_frame_44x3x5", len(counts) == TRIPLET_COUNT, len(counts), TRIPLET_COUNT)
    record("all_posterior_count_gates_pass", all(row["minimum_20_pass"] == "True" for row in counts), sum(row["minimum_20_pass"] == "True" for row in counts), TRIPLET_COUNT)
    record("all_w1_dual_replay_tolerances_pass", all(float(row["independent_W1_abs_diff"]) <= 1e-10 * max(1.0, abs(float(row["raw_W1"]))) for row in cells), max(float(row["independent_W1_abs_diff"]) for row in cells), "cellwise <=1e-10*max(1,abs(W1))")
    record("all_44_official_identities_pass", len(identities) == CANDIDATE_COUNT and all(row["identity_pass"] == "True" for row in identities), sum(row["identity_pass"] == "True" for row in identities), CANDIDATE_COUNT)
    record("all_44_event_hdfs_deleted", len(identities) == CANDIDATE_COUNT and all(row["deleted_after_use"] == "True" for row in identities), sum(row["deleted_after_use"] == "True" for row in identities), CANDIDATE_COUNT)
    identity_map = {row["event"]: row for row in identities}
    record("identity_manifest_size_md5_replay", all(identity_map[row["event"]]["observed_size_bytes"] == row["size_bytes"] and identity_map[row["event"]]["observed_md5"] == row["official_md5"] for row in candidates), True, True)

    by_event_cells: dict[str, list[float]] = defaultdict(list)
    for row in cells:
        by_event_cells[row["event"]].append(float(row["full_norm_W1"]))
    full_response = {event: float(np.median(by_event_cells[event])) for event in events}
    balanced_raw: dict[str, list[float]] = defaultdict(list)
    for row in rows(OUTPUT / "BALANCED_EVENT_REPETITIONS.csv"):
        balanced_raw[row["event"]].append(float(row["event_median_balanced_norm_W1"]))
    balanced_response = {event: float(np.median(balanced_raw[event])) for event in events}
    event_metrics = {row["event"]: row for row in rows(OUTPUT / "EVENT_METRICS.csv")}
    full_diff = max(abs(full_response[event] - float(event_metrics[event]["full_response"])) for event in events)
    balanced_diff = max(abs(balanced_response[event] - float(event_metrics[event]["balanced_response"])) for event in events)
    record("full_event_response_independent_replay", full_diff <= 1e-15, full_diff, "<=1e-15")
    record("balanced_event_response_independent_replay", balanced_diff <= 1e-15, balanced_diff, "<=1e-15")

    x = np.asarray([replay_predictor[event] for event in events])
    y = np.asarray([full_response[event] for event in events])
    y_balanced = np.asarray([balanced_response[event] for event in events])
    scipy_rho = float(spearmanr(x, y).statistic)
    scipy_balanced_rho = float(spearmanr(x, y_balanced).statistic)
    primary = json.loads((OUTPUT / "PRIMARY_TEST.json").read_text(encoding="utf-8"))
    secondary = json.loads((OUTPUT / "SECONDARY_TESTS.json").read_text(encoding="utf-8"))
    record("primary_scipy_spearman_replay", abs(scipy_rho - float(primary["observed_spearman_rho"])) <= 1e-15, scipy_rho, primary["observed_spearman_rho"])
    record("balanced_scipy_spearman_replay", abs(scipy_balanced_rho - float(secondary["balanced_response_test"]["observed_spearman_rho"])) <= 1e-15, scipy_balanced_rho, secondary["balanced_response_test"]["observed_spearman_rho"])
    mc_rho, mc_extreme = independent_mc(x, y)
    record("primary_fixed_rng_monte_carlo_replay", abs(mc_rho - float(primary["observed_spearman_rho"])) <= 1e-15 and mc_extreme == int(primary["one_sided_extreme_count"]), {"rho": mc_rho, "extreme": mc_extreme}, {"rho": primary["observed_spearman_rho"], "extreme": primary["one_sided_extreme_count"]})
    expected_p = (mc_extreme + 1) / 1_000_001
    record("primary_plus_one_p_replay", abs(expected_p - float(primary["one_sided_plus_one_p"])) <= 1e-18, expected_p, primary["one_sided_plus_one_p"])
    expected_verdict = "SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT" if mc_rho > 0 and expected_p <= 0.05 else "NOT_SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT"
    record("primary_verdict_replay", primary["verdict"] == expected_verdict, primary["verdict"], expected_verdict)

    error_rows = rows(OUTPUT / "ERROR_LEDGER.csv")
    record("error_ledger_empty", len(error_rows) == 0, len(error_rows), 0)
    retained_event_files = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*combined_PEDataRelease.hdf5")]
    record("no_raw_event_hdf_retained", not retained_event_files, retained_event_files, [])
    status = json.loads((OUTPUT / "RUN_STATUS.json").read_text(encoding="utf-8"))
    record("terminal_status_complete", status["status"] == "NUMERIC_RUN_COMPLETE", status["status"], "NUMERIC_RUN_COMPLETE")
    record("no_historical_closure_effect", status["historical_closure_effect"] == "NONE", status["historical_closure_effect"], "NONE")

    passed = all(check["pass"] for check in checks)
    return {
        "verification_timestamp_utc": utc_now(),
        "verifier": "07_REPRODUCIBILITY/verify_xr01.py",
        "verifier_imports_frozen_runner": False,
        "status": "PASS" if passed else "FAIL",
        "checks_passed": sum(check["pass"] for check in checks),
        "checks_total": len(checks),
        "checks": checks,
        "primary_replay": {"rho": mc_rho, "extreme_count": mc_extreme, "plus_one_p": expected_p, "verdict": expected_verdict},
    }


if __name__ == "__main__":
    result = verify()
    destination = OUTPUT / "INDEPENDENT_REPRODUCIBILITY_VERIFICATION.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "checks_passed", "checks_total", "primary_replay")}, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
