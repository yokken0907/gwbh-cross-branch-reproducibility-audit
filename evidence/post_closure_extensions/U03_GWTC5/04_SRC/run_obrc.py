#!/usr/bin/env python3
"""Frozen candidate-posterior-blind runner for the all-22 OBRC analysis."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import h5py
import numpy as np
from scipy.stats import beta, kendalltau, rankdata, wasserstein_distance


MODELS = (
    "IMRPhenomXPHM-SpinTaylor",
    "IMRPhenomXPNR",
    "NRSur7dq4",
)
PAIRS = (
    (MODELS[0], MODELS[1]),
    (MODELS[0], MODELS[2]),
    (MODELS[1], MODELS[2]),
)
PARAMETERS = (
    "chirp_mass_source",
    "chi_eff",
    "luminosity_distance",
    "final_mass_source",
    "final_spin",
)
RUN_ID = "GWBH_ERIA_U03_ALTTRIAD_COMMON5_OBRC_RUN01"
PERMUTATIONS = 1_000_000
PERMUTATION_SEED = 20260813
BALANCED_REPETITIONS = 80
BALANCED_MAXIMUM = 4000
BALANCED_BASE_SEED = 20260801
ALPHA = 0.05
TOLERANCE = 1e-15


class FormalStop(RuntimeError):
    def __init__(self, label: str, reason: str, scalars_read: int = 0):
        super().__init__(reason)
        self.label = label
        self.reason = reason
        self.scalars_read = int(scalars_read)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def decode(value: Any) -> str:
    if isinstance(value, (bytes, np.bytes_)):
        return bytes(value).decode("utf-8")
    return str(value)


def finite(values: Any) -> np.ndarray:
    array = np.asarray(values, dtype=float).reshape(-1)
    return array[np.isfinite(array)]


def corrected_s90(a: dict[str, float], b: dict[str, float]) -> float:
    denominator = ((a["lower"] + a["upper"]) + (b["lower"] + b["upper"])) / 4.0
    return float(abs(b["median"] - a["median"]) / max(float(denominator), 1e-12))


def pair_scale(a: np.ndarray, b: np.ndarray) -> float:
    qa = np.quantile(a, [0.25, 0.75], method="linear")
    qb = np.quantile(b, [0.25, 0.75], method="linear")
    value = ((qa[1] - qa[0]) + (qb[1] - qb[0])) / 2.0
    if not np.isfinite(value) or value <= 0:
        value = float(np.std(np.r_[a, b], ddof=0))
    return max(float(value), 1e-12)


def ecdf_wasserstein(a: np.ndarray, b: np.ndarray) -> float:
    """Independent exact 1-D empirical-CDF integral for unweighted samples."""
    a = np.sort(np.asarray(a, dtype=float), kind="mergesort")
    b = np.sort(np.asarray(b, dtype=float), kind="mergesort")
    values = np.sort(np.r_[a, b], kind="mergesort")
    if values.size < 2:
        return 0.0
    deltas = np.diff(values)
    a_cdf = np.searchsorted(a, values[:-1], side="right") / a.size
    b_cdf = np.searchsorted(b, values[:-1], side="right") / b.size
    return float(np.sum(np.abs(a_cdf - b_cdf) * deltas))


def normalized_w1(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float, float]:
    scale = pair_scale(a, b)
    scipy_w1 = float(wasserstein_distance(a, b))
    replay_w1 = ecdf_wasserstein(a, b)
    allowed = 1e-10 * max(1.0, abs(scipy_w1))
    if abs(scipy_w1 - replay_w1) > allowed:
        raise FormalStop(
            "NO_GO_INTERNAL_VALIDATION",
            f"W1_REPLAY_MISMATCH:{scipy_w1}:{replay_w1}:{allowed}",
        )
    return scipy_w1 / scale, scipy_w1, scale, abs(scipy_w1 - replay_w1)


def cell_seed(event: str, model_a: str, model_b: str, parameter: str) -> int:
    key = "|".join((event, model_a, model_b, parameter)).encode("utf-8")
    return BALANCED_BASE_SEED + int.from_bytes(hashlib.sha256(key).digest()[:4], "little") % 1_000_000_000


def balanced_values(a: np.ndarray, b: np.ndarray, seed: int) -> tuple[np.ndarray, int]:
    n = min(a.size, b.size, BALANCED_MAXIMUM)
    if n < 20:
        raise FormalStop("NO_GO_POSTERIOR_COMPLETE_FRAME", f"BALANCED_N_LT20:{n}")
    rng = np.random.Generator(np.random.PCG64DXSM(seed))
    results = np.empty(BALANCED_REPETITIONS, dtype=float)
    for index in range(BALANCED_REPETITIONS):
        sample_a = a[rng.choice(a.size, n, replace=False)] if a.size > n else a[rng.permutation(a.size)]
        sample_b = b[rng.choice(b.size, n, replace=False)] if b.size > n else b[rng.permutation(b.size)]
        results[index] = float(wasserstein_distance(sample_a, sample_b) / pair_scale(sample_a, sample_b))
    return results, int(n)


def ranked_correlation(x: Any, y: Any) -> tuple[float | None, np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rank_x = rankdata(x, method="average")
    rank_y = rankdata(y, method="average")
    centered_x = rank_x - rank_x.mean()
    centered_y = rank_y - rank_y.mean()
    denominator = float(np.sqrt(np.dot(centered_x, centered_x) * np.dot(centered_y, centered_y)))
    if denominator == 0:
        return None, rank_x, rank_y
    return float(np.dot(centered_x, centered_y) / denominator), rank_x, rank_y


def monte_carlo_test(x: Any, y: Any, batch_size: int = 20_000) -> dict[str, Any]:
    observed, rank_x, rank_y = ranked_correlation(x, y)
    if observed is None:
        return {
            "status": "CONSTANT_VECTOR",
            "verdict": "NOT_SUPPORTED_CONSTANT_VECTOR",
            "n": int(len(np.asarray(x))),
        }
    centered_x = rank_x - rank_x.mean()
    centered_y = rank_y - rank_y.mean()
    denominator = float(np.sqrt(np.dot(centered_x, centered_x) * np.dot(centered_y, centered_y)))
    rng = np.random.Generator(np.random.PCG64DXSM(PERMUTATION_SEED))
    extreme = 0
    remaining = PERMUTATIONS
    while remaining:
        current = min(batch_size, remaining)
        keys = rng.random((current, len(centered_y)))
        order = np.argsort(keys, axis=1, kind="stable")
        statistics = centered_y[order] @ centered_x / denominator
        extreme += int(np.count_nonzero(statistics >= observed - TOLERANCE))
        remaining -= current
    p_value = (extreme + 1) / (PERMUTATIONS + 1)
    if extreme == 0:
        ci_lower = 0.0
    else:
        ci_lower = float(beta.ppf(0.005, extreme, PERMUTATIONS - extreme + 1))
    if extreme == PERMUTATIONS:
        ci_upper = 1.0
    else:
        ci_upper = float(beta.ppf(0.995, extreme + 1, PERMUTATIONS - extreme))
    supported = observed > 0 and p_value <= ALPHA
    return {
        "status": "COMPUTED",
        "n": int(len(rank_x)),
        "observed_spearman_rho": observed,
        "x_tie_count": int(len(rank_x) - len(np.unique(rank_x))),
        "y_tie_count": int(len(rank_y) - len(np.unique(rank_y))),
        "alternative": "positive",
        "permutations": PERMUTATIONS,
        "rng": f"PCG64DXSM({PERMUTATION_SEED})",
        "one_sided_extreme_count": extreme,
        "one_sided_plus_one_p": float(p_value),
        "extreme_probability_clopper_pearson_99pct": [ci_lower, ci_upper],
        "alpha": ALPHA,
        "verdict": (
            "SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION"
            if supported
            else "NOT_SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION"
        ),
    }


def verify_lock(root: Path) -> dict[str, Any]:
    lock = load_json(root / "02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json")
    if lock.get("candidate_posterior_elements_accessed_at_lock") != 0:
        raise RuntimeError("PRE_POSTERIOR_LOCK_ATTESTATION_INVALID")
    for item in lock["locked_files"]:
        path = root / item["path"]
        if not path.exists() or path.stat().st_size != int(item["size_bytes"]) or digest(path) != item["sha256"]:
            raise RuntimeError(f"PRE_POSTERIOR_LOCK_HASH_MISMATCH:{item['path']}")
    return lock


def verify_inputs(root: Path) -> list[dict[str, str]]:
    summary = root / "03_INPUT/IGWN-GWTC5p0-29ebe06b7_25-PESummaryTable.hdf5"
    if summary.stat().st_size != 194697:
        raise RuntimeError("SUMMARY_SIZE_MISMATCH")
    if digest(summary, "md5") != "4655c648713f5f7c52256b9dbda7a0ff":
        raise RuntimeError("SUMMARY_MD5_MISMATCH")
    if digest(summary) != "e6437d5763066e0b6f42f913309f4bcc1e1c50a24aa19335ab8d35198216539b":
        raise RuntimeError("SUMMARY_SHA256_MISMATCH")
    candidates = read_csv(root / "03_INPUT/CANDIDATE_EVENT_FREEZE.csv")
    if len(candidates) != 22 or len({row["event"] for row in candidates}) != 22:
        raise RuntimeError("CANDIDATE_FRAME_NOT_EXACTLY_22_UNIQUE_EVENTS")
    expected_triad = "|".join(MODELS)
    for row in candidates:
        if row["model_triad"] != expected_triad:
            raise RuntimeError(f"MODEL_TRIAD_DRIFT:{row['event']}")
        if int(row["size_bytes"]) >= 250_000_000:
            raise RuntimeError(f"FILE_SIZE_CAP_DRIFT:{row['event']}")
    return candidates


TRIPLET_FIELDS = (
    "event", "model", "parameter", "median", "lower_error", "upper_error",
    "q05_reconstructed", "q95_reconstructed", "mask_pass", "finite_pass",
    "nonnegative_error_pass", "positive_width_pass", "triplet_pass",
)
PAIR_FIELDS = ("event", "parameter", "model_a", "model_b", "corrected_S90")
PREDICTOR_FIELDS = ("event", "predictor", "parameter_maximum_S90_json")
IDENTITY_FIELDS = (
    "event", "zenodo_record", "filename", "expected_size_bytes", "observed_size_bytes",
    "expected_md5", "observed_md5", "sha256", "identity_pass", "deleted_after_use",
    "download_seconds",
)
COUNT_FIELDS = ("event", "model", "parameter", "raw_values_read", "finite_values", "nonfinite_values", "minimum_20_pass")
CELL_FIELDS = (
    "event", "model_a", "model_b", "parameter", "finite_n_a", "finite_n_b",
    "raw_W1", "scale", "full_norm_W1", "independent_W1_abs_diff", "balanced_seed",
    "balanced_n_each", "balanced_q05", "balanced_median", "balanced_q95",
)
BALANCED_REP_FIELDS = ("event", "repetition", "event_median_balanced_norm_W1")
EVENT_FIELDS = (
    "event", "predictor", "full_response", "balanced_response", "full_cell_count",
    "predictor_rank", "full_response_rank", "rank_difference",
)
ERROR_FIELDS = ("timestamp_utc", "stage", "event", "label", "reason")


def evaluate_summary(root: Path, candidates: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    requested = ["gw_name", "result_samples_key", "result_file_name"]
    requested += [f"{parameter}_{part}" for parameter in PARAMETERS for part in ("median", "lower", "upper")]
    with h5py.File(root / "03_INPUT/IGWN-GWTC5p0-29ebe06b7_25-PESummaryTable.hdf5", "r") as hdf:
        dataset = hdf["summary_info"]
        names = set(dataset.dtype.names or ())
        masks = [f"{field}.mask" for field in requested if f"{field}.mask" in names]
        missing = [field for field in requested if field not in names]
        if missing:
            raise FormalStop("NO_GO_SUMMARY_SEMANTIC_COMPLETE_FRAME", "SUMMARY_FIELDS_MISSING:" + "|".join(missing))
        rows = dataset.fields(requested + masks)[:]
    index: dict[tuple[str, str], list[Any]] = {}
    for row in rows:
        key = (decode(row["gw_name"]).upper(), decode(row["result_samples_key"]))
        index.setdefault(key, []).append(row)
    manifest = {row["event"]: row for row in candidates}
    triples: dict[tuple[str, str, str], dict[str, float]] = {}
    triplet_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for source in candidates:
        event = source["event"]
        for model in MODELS:
            matches = index.get((event, f"C00:{model}"), [])
            if len(matches) != 1:
                failures.append(f"SUMMARY_ROW_COUNT:{event}:{model}:{len(matches)}")
                continue
            row = matches[0]
            if decode(row["result_file_name"]) != manifest[event]["official_filename"]:
                failures.append(f"SUMMARY_FILE_IDENTITY:{event}:{model}")
            for parameter in PARAMETERS:
                median = float(row[f"{parameter}_median"])
                lower = float(row[f"{parameter}_lower"])
                upper = float(row[f"{parameter}_upper"])
                mask_pass = not any(
                    bool(row[name])
                    for name in (f"{parameter}_median.mask", f"{parameter}_lower.mask", f"{parameter}_upper.mask")
                    if name in (row.dtype.names or ())
                )
                finite_pass = bool(np.isfinite([median, lower, upper]).all())
                nonnegative = finite_pass and lower >= 0 and upper >= 0
                positive_width = nonnegative and lower + upper > 0
                passed = mask_pass and finite_pass and nonnegative and positive_width
                triplet_rows.append({
                    "event": event, "model": model, "parameter": parameter,
                    "median": median, "lower_error": lower, "upper_error": upper,
                    "q05_reconstructed": median - lower, "q95_reconstructed": median + upper,
                    "mask_pass": mask_pass, "finite_pass": finite_pass,
                    "nonnegative_error_pass": nonnegative, "positive_width_pass": positive_width,
                    "triplet_pass": passed,
                })
                if passed:
                    triples[(event, model, parameter)] = {"median": median, "lower": lower, "upper": upper}
                else:
                    failures.append(f"SUMMARY_TRIPLET:{event}:{model}:{parameter}")
    if len(triplet_rows) != 330 or failures:
        raise FormalStop("NO_GO_SUMMARY_SEMANTIC_COMPLETE_FRAME", "|".join(failures[:50]))
    pair_rows: list[dict[str, Any]] = []
    predictors: list[dict[str, Any]] = []
    for source in candidates:
        event = source["event"]
        maxima: dict[str, float] = {}
        for parameter in PARAMETERS:
            values: list[float] = []
            for model_a, model_b in PAIRS:
                score = corrected_s90(triples[(event, model_a, parameter)], triples[(event, model_b, parameter)])
                values.append(score)
                pair_rows.append({"event": event, "parameter": parameter, "model_a": model_a, "model_b": model_b, "corrected_S90": score})
            maxima[parameter] = max(values)
        predictors.append({"event": event, "predictor": float(np.median(list(maxima.values()))), "parameter_maximum_S90_json": json.dumps(maxima, sort_keys=True)})
    return triplet_rows, pair_rows, predictors


def download(source: dict[str, str], destination: Path) -> float:
    partial = destination.with_suffix(destination.suffix + ".part")
    destination.unlink(missing_ok=True)
    partial.unlink(missing_ok=True)
    started = time.monotonic()
    command = [
        "curl", "--location", "--fail", "--silent", "--show-error", "--retry", "5",
        "--retry-delay", "2", "--retry-all-errors", "--connect-timeout", "30",
        "--max-time", "1800", "--output", str(partial), source["content_url"],
    ]
    try:
        subprocess.run(command, check=True, timeout=1850)
    except Exception as error:
        raise FormalStop("NO_GO_SOURCE_ACQUISITION_FAILURE", f"{source['event']}:{type(error).__name__}:{error}") from error
    partial.replace(destination)
    return float(time.monotonic() - started)


def load_event(path: Path, event: str) -> tuple[dict[str, dict[str, np.ndarray]], list[dict[str, Any]], int]:
    values: dict[str, dict[str, np.ndarray]] = {}
    counts: list[dict[str, Any]] = []
    scalar_count = 0
    with h5py.File(path, "r") as hdf:
        for model in MODELS:
            group_name = f"C00:{model}"
            if group_name not in hdf or "posterior_samples" not in hdf[group_name]:
                raise FormalStop("NO_GO_SCHEMA_DRIFT", f"DATASET_MISSING:{event}:{model}", scalar_count)
            dataset = hdf[group_name]["posterior_samples"]
            names = tuple(dataset.dtype.names or ())
            weight_like = [name for name in names if "weight" in name.casefold()]
            if weight_like:
                raise FormalStop("NO_GO_SCHEMA_DRIFT", f"WEIGHT_FIELD:{event}:{model}:{'|'.join(weight_like)}", scalar_count)
            values[model] = {}
            for parameter in PARAMETERS:
                if (
                    parameter not in names
                    or dataset.dtype[parameter].subdtype is not None
                    or not np.issubdtype(dataset.dtype[parameter], np.number)
                ):
                    raise FormalStop("NO_GO_SCHEMA_DRIFT", f"FIELD_MISSING_OR_NONNUMERIC_NONSCALAR:{event}:{model}:{parameter}", scalar_count)
                raw = np.asarray(dataset.fields(parameter)[:], dtype=float).reshape(-1)
                clean = finite(raw)
                scalar_count += int(raw.size)
                passed = clean.size >= 20
                counts.append({
                    "event": event, "model": model, "parameter": parameter,
                    "raw_values_read": int(raw.size), "finite_values": int(clean.size),
                    "nonfinite_values": int(raw.size-clean.size), "minimum_20_pass": passed,
                })
                if not passed:
                    raise FormalStop("NO_GO_POSTERIOR_COMPLETE_FRAME", f"FINITE_LT20:{event}:{model}:{parameter}:{clean.size}", scalar_count)
                values[model][parameter] = clean
    return values, counts, scalar_count


def persist_partial(output: Path, identity: list[dict[str, Any]], counts: list[dict[str, Any]], cells: list[dict[str, Any]], balanced: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    write_csv(output / "EVENT_FILE_IDENTITY.csv", identity, IDENTITY_FIELDS)
    write_csv(output / "POSTERIOR_VALUE_COUNTS.csv", counts, COUNT_FIELDS)
    write_csv(output / "CELL_METRICS.csv", cells, CELL_FIELDS)
    write_csv(output / "BALANCED_EVENT_REPETITIONS.csv", balanced, BALANCED_REP_FIELDS)
    write_csv(output / "ERROR_LEDGER.csv", errors, ERROR_FIELDS)


def close_stop(output: Path, label: str, reason: str, started: str, posterior_scalars: int, completed_events: int, errors: list[dict[str, Any]]) -> int:
    errors.append({"timestamp_utc": utc_now(), "stage": "FORMAL_STOP", "event": "", "label": label, "reason": reason})
    status = {
        "run_id": RUN_ID, "status": label, "formal_no_go": True,
        "reason": reason, "started_at_utc": started, "completed_at_utc": utc_now(),
        "completed_events": completed_events, "candidate_events_required": 22,
        "candidate_posterior_scalars_read": posterior_scalars,
        "primary_test_executed": False, "event_replacement_or_rescue": False,
        "historical_closure_effect": "NONE",
    }
    write_json(output / "RUN_STATUS.json", status)
    write_json(output / "DECISION.json", status)
    write_json(output / "PRIMARY_TEST.json", {"status": "NOT_EXECUTED_FORMAL_GATE_STOP", "verdict": label, "reason": reason})
    write_json(output / "SECONDARY_TESTS.json", {"status": "NOT_EXECUTED_FORMAL_GATE_STOP"})
    write_json(output / "VALUE_ACCESS_ATTESTATION.json", {
        "candidate_summary_scalars_read_this_run": 990,
        "candidate_posterior_scalars_read_this_run": posterior_scalars,
        "completed_candidate_events": completed_events,
        "primary_test_executed": False,
        "event_replacement_or_rescue": False,
    })
    write_csv(output / "ERROR_LEDGER.csv", errors, ERROR_FIELDS)
    return 2


def run(root: Path) -> int:
    verify_lock(root)
    candidates = verify_inputs(root)
    output = root / "06_RUN_OUTPUT"
    output.mkdir(parents=True, exist_ok=True)
    if (output / "RUN_STATUS.json").exists():
        raise RuntimeError("RUN_DIRECTORY_ALREADY_EXECUTED")
    started = utc_now()
    write_json(output / "RUN_STATUS.json", {"run_id": RUN_ID, "status": "SUMMARY_STAGE_IN_PROGRESS", "started_at_utc": started})
    errors: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    count_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    balanced_rows: list[dict[str, Any]] = []
    posterior_scalars = 0
    completed_events = 0
    try:
        triplets, pair_scores, predictors = evaluate_summary(root, candidates)
        write_csv(output / "SUMMARY_TRIPLETS.csv", triplets, TRIPLET_FIELDS)
        write_csv(output / "SUMMARY_PAIR_SCORES.csv", pair_scores, PAIR_FIELDS)
        write_csv(output / "EVENT_PREDICTORS.csv", predictors, PREDICTOR_FIELDS)
    except FormalStop as stop:
        return close_stop(output, stop.label, stop.reason, started, posterior_scalars, completed_events, errors)
    predictor_map = {row["event"]: float(row["predictor"]) for row in predictors}
    event_core: dict[str, dict[str, Any]] = {}
    with tempfile.TemporaryDirectory(prefix="gwbh_obrc_") as temporary:
        temporary_path = Path(temporary)
        for position, source in enumerate(candidates, start=1):
            event = source["event"]
            local = temporary_path / source["official_filename"]
            partial = local.with_suffix(local.suffix + ".part")
            print(f"[{position:02d}/22] {event} DOWNLOAD_START", flush=True)
            try:
                seconds = download(source, local)
                size = local.stat().st_size
                md5 = digest(local, "md5")
                sha256 = digest(local)
                identity_pass = size == int(source["size_bytes"]) and md5 == source["official_md5"]
                identity_row = {
                    "event": event, "zenodo_record": source["zenodo_record"], "filename": source["official_filename"],
                    "expected_size_bytes": source["size_bytes"], "observed_size_bytes": size,
                    "expected_md5": source["official_md5"], "observed_md5": md5, "sha256": sha256,
                    "identity_pass": identity_pass, "deleted_after_use": False, "download_seconds": seconds,
                }
                identity_rows.append(identity_row)
                if not identity_pass:
                    raise FormalStop("NO_GO_IDENTITY_DRIFT", f"OFFICIAL_IDENTITY_FAIL:{event}")
                values, event_counts, scalar_count = load_event(local, event)
                posterior_scalars += scalar_count
                count_rows.extend(event_counts)
                event_cells: list[dict[str, Any]] = []
                event_balanced = np.empty((BALANCED_REPETITIONS, 15), dtype=float)
                cell_index = 0
                for model_a, model_b in PAIRS:
                    for parameter in PARAMETERS:
                        a = values[model_a][parameter]
                        b = values[model_b][parameter]
                        norm, raw, scale, replay_diff = normalized_w1(a, b)
                        seed = cell_seed(event, model_a, model_b, parameter)
                        balanced, balanced_n = balanced_values(a, b, seed)
                        event_balanced[:, cell_index] = balanced
                        row = {
                            "event": event, "model_a": model_a, "model_b": model_b, "parameter": parameter,
                            "finite_n_a": a.size, "finite_n_b": b.size, "raw_W1": raw, "scale": scale,
                            "full_norm_W1": norm, "independent_W1_abs_diff": replay_diff,
                            "balanced_seed": seed, "balanced_n_each": balanced_n,
                            "balanced_q05": float(np.quantile(balanced, .05, method="linear")),
                            "balanced_median": float(np.median(balanced)),
                            "balanced_q95": float(np.quantile(balanced, .95, method="linear")),
                        }
                        event_cells.append(row)
                        cell_index += 1
                if len(event_cells) != 15:
                    raise FormalStop("NO_GO_INTERNAL_VALIDATION", f"CELL_COUNT:{event}:{len(event_cells)}")
                cell_rows.extend(event_cells)
                event_rep = np.median(event_balanced, axis=1)
                for repetition, value in enumerate(event_rep):
                    balanced_rows.append({"event": event, "repetition": repetition, "event_median_balanced_norm_W1": float(value)})
                event_core[event] = {
                    "predictor": predictor_map[event],
                    "full_response": float(np.median([row["full_norm_W1"] for row in event_cells])),
                    "balanced_response": float(np.median(event_rep)),
                }
                completed_events += 1
                print(f"[{position:02d}/22] {event} PASS", flush=True)
            except FormalStop as stop:
                posterior_scalars += stop.scalars_read
                errors.append({"timestamp_utc": utc_now(), "stage": "EVENT_RUNTIME", "event": event, "label": stop.label, "reason": stop.reason})
                persist_partial(output, identity_rows, count_rows, cell_rows, balanced_rows, errors)
                return close_stop(output, stop.label, stop.reason, started, posterior_scalars, completed_events, errors)
            except Exception as error:
                reason = f"{type(error).__name__}:{error}"
                errors.append({"timestamp_utc": utc_now(), "stage": "EVENT_RUNTIME", "event": event, "label": "NO_GO_INTERNAL_VALIDATION", "reason": reason})
                persist_partial(output, identity_rows, count_rows, cell_rows, balanced_rows, errors)
                return close_stop(output, "NO_GO_INTERNAL_VALIDATION", reason, started, posterior_scalars, completed_events, errors)
            finally:
                local.unlink(missing_ok=True)
                partial.unlink(missing_ok=True)
                if identity_rows and identity_rows[-1]["event"] == event:
                    identity_rows[-1]["deleted_after_use"] = not local.exists() and not partial.exists()
                persist_partial(output, identity_rows, count_rows, cell_rows, balanced_rows, errors)
    if completed_events != 22 or len(cell_rows) != 330 or len(count_rows) != 330:
        return close_stop(output, "NO_GO_POSTERIOR_COMPLETE_FRAME", "FINAL_FRAME_NOT_22x15", started, posterior_scalars, completed_events, errors)
    events = [row["event"] for row in candidates]
    x = np.asarray([event_core[event]["predictor"] for event in events], dtype=float)
    y = np.asarray([event_core[event]["full_response"] for event in events], dtype=float)
    y_balanced = np.asarray([event_core[event]["balanced_response"] for event in events], dtype=float)
    primary = monte_carlo_test(x, y)
    secondary_balanced = monte_carlo_test(x, y_balanced)
    kendall = kendalltau(x, y)
    loo: list[dict[str, Any]] = []
    for index, event in enumerate(events):
        keep = np.arange(22) != index
        rho, _, _ = ranked_correlation(x[keep], y[keep])
        loo.append({"removed_event": event, "spearman_rho": rho})
    rho, rank_x, rank_y = ranked_correlation(x, y)
    event_rows: list[dict[str, Any]] = []
    for index, event in enumerate(events):
        event_rows.append({
            "event": event, **event_core[event], "full_cell_count": 15,
            "predictor_rank": float(rank_x[index]), "full_response_rank": float(rank_y[index]),
            "rank_difference": float(rank_y[index]-rank_x[index]),
        })
    write_csv(output / "EVENT_METRICS.csv", event_rows, EVENT_FIELDS)
    write_csv(output / "LEAVE_ONE_EVENT_OUT.csv", loo, ("removed_event", "spearman_rho"))
    secondary = {
        "role": "SECONDARY_ONLY_NO_PRIMARY_OVERRIDE",
        "balanced_response_test": secondary_balanced,
        "kendall_tau_b": {"tau": float(kendall.statistic), "p_value_two_sided": float(kendall.pvalue)},
        "leave_one_event_out_full_response": {
            "minimum_rho": float(min(row["spearman_rho"] for row in loo if row["spearman_rho"] is not None)),
            "maximum_rho": float(max(row["spearman_rho"] for row in loo if row["spearman_rho"] is not None)),
            "rows": 22,
        },
        "primary_override": False,
    }
    write_json(output / "PRIMARY_TEST.json", primary)
    write_json(output / "SECONDARY_TESTS.json", secondary)
    verdict = primary["verdict"]
    decision = {
        "run_id": RUN_ID, "decision": verdict, "decision_class": "FROZEN_ALL22_RETROSPECTIVE_CALIBRATION",
        "primary": primary, "candidate_events": 22, "posterior_cells": 330,
        "event_replacement_or_rescue": False,
        "claim": "Release-specific screening calibration only, within the exact frozen frame.",
        "strict_replication_claim": False, "model_superiority_claim": False,
        "new_physics_claim": False, "historical_closure_effect": "NONE",
    }
    write_json(output / "DECISION.json", decision)
    write_json(output / "VALUE_ACCESS_ATTESTATION.json", {
        "candidate_summary_scalars_read_this_run": 990,
        "candidate_posterior_scalars_read_this_run": posterior_scalars,
        "candidate_events_completed": 22,
        "posterior_model_parameter_cells_read": 330,
        "inter_model_distance_cells_computed": 330,
        "primary_test_executed": True,
        "candidate_posterior_elements_before_protocol_lock": 0,
        "event_replacement_or_rescue": False,
        "raw_event_hdf_files_retained": 0,
    })
    write_json(output / "INTERNAL_VALIDATION.json", {
        "status": "PASS",
        "all_330_w1_values_independently_replayed": True,
        "maximum_w1_absolute_replay_difference": float(max(row["independent_W1_abs_diff"] for row in cell_rows)),
        "expected_events": 22, "observed_events": completed_events,
        "expected_cells": 330, "observed_cells": len(cell_rows),
        "identity_pass_files": sum(bool(row["identity_pass"]) for row in identity_rows),
        "deleted_event_hdf_files": sum(bool(row["deleted_after_use"]) for row in identity_rows),
        "primary_rho_recomputed_from_event_table": rho,
        "primary_rho_matches": bool(abs(float(primary.get("observed_spearman_rho", rho))-float(rho)) <= 1e-15),
    })
    status = {
        "run_id": RUN_ID, "status": "NUMERIC_RUN_COMPLETE", "verdict": verdict,
        "started_at_utc": started, "completed_at_utc": utc_now(),
        "candidate_events": 22, "posterior_cells": 330,
        "primary_test_executed": True, "internal_validation": "PASS",
        "event_replacement_or_rescue": False, "historical_closure_effect": "NONE",
    }
    write_json(output / "RUN_STATUS.json", status)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    return run(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
