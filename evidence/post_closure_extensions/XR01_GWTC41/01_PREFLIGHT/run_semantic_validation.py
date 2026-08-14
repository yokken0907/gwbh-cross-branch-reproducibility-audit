#!/usr/bin/env python3
"""Validate GWTC-4.1 summary-column semantics on one locked out-of-frame event."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import h5py
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "01_PREFLIGHT/SEMANTIC_VALIDATION_SELECTION.json"
RESULT_PATH = ROOT / "01_PREFLIGHT/SEMANTIC_VALIDATION_RESULT.json"
SUMMARY_PATH = ROOT / "03_INPUT/IGWN-GWTC4p1-18965dda8_5-PESummaryTable.hdf5"
MANIFEST_PATH = ROOT / "03_INPUT/ZENODO_FILE_MANIFEST.csv"
SELECTION_SHA256 = "5c1c91c45dc86c94ad21eae94ea3fe1e4d30fbfe5d594929609c878b1288ca99"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def decode(value) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def close(a: float, b: float) -> bool:
    return bool(abs(a - b) <= 1e-10 * max(1.0, abs(a), abs(b)))


def main() -> int:
    if RESULT_PATH.exists():
        raise SystemExit("SEMANTIC_RESULT_ALREADY_EXISTS")
    if digest(SELECTION_PATH, "sha256") != SELECTION_SHA256:
        raise SystemExit("SEMANTIC_SELECTION_LOCK_HASH_MISMATCH")
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    with MANIFEST_PATH.open(newline="", encoding="utf-8") as stream:
        manifest = {row["filename"]: row for row in csv.DictReader(stream)}
    source = manifest[selection["official_filename"]]
    if int(source["size_bytes"]) != int(selection["expected_size_bytes"]) or source["md5"] != selection["expected_md5"]:
        raise SystemExit("SEMANTIC_SOURCE_MANIFEST_MISMATCH")

    # Read only string fields first to identify the single out-of-frame row.
    with h5py.File(SUMMARY_PATH, "r") as hdf:
        dataset = hdf["summary_info"]
        identities = dataset.fields(["gw_name", "result_samples_key"])[:]
        indices = [
            index
            for index, row in enumerate(identities)
            if decode(row["gw_name"]).upper() == selection["event"]
            and decode(row["result_samples_key"]) == selection["model"]
        ]
        if len(indices) != 1:
            raise SystemExit(f"SEMANTIC_SUMMARY_ROW_COUNT:{len(indices)}")
        numeric_fields = [
            f"{parameter}_{part}"
            for parameter in selection["parameters"]
            for part in ("median", "lower", "upper")
        ]
        numeric_row = dataset.fields(numeric_fields)[indices[0]]
        summary = {
            parameter: {
                "median": float(numeric_row[f"{parameter}_median"]),
                "lower": float(numeric_row[f"{parameter}_lower"]),
                "upper": float(numeric_row[f"{parameter}_upper"]),
            }
            for parameter in selection["parameters"]
        }

    temporary_path: Path | None = None
    result_rows = []
    posterior_scalars = 0
    started = utc_now()
    observed_size = None
    observed_md5 = None
    observed_sha256 = None
    try:
        with tempfile.TemporaryDirectory(prefix="gwbh_xr01_semantic_") as temporary:
            temporary_path = Path(temporary) / selection["official_filename"]
            partial = temporary_path.with_suffix(temporary_path.suffix + ".part")
            subprocess.run(
                [
                    "curl", "--location", "--fail", "--silent", "--show-error",
                    "--retry", "5", "--retry-all-errors", "--connect-timeout", "30",
                    "--max-time", "1800", "--output", str(partial), source["content_url"],
                ],
                check=True,
                timeout=1850,
            )
            partial.replace(temporary_path)
            observed_size = temporary_path.stat().st_size
            observed_md5 = digest(temporary_path, "md5")
            observed_sha256 = digest(temporary_path, "sha256")
            if observed_size != int(selection["expected_size_bytes"]) or observed_md5 != selection["expected_md5"]:
                raise SystemExit("SEMANTIC_EVENT_IDENTITY_FAIL")
            with h5py.File(temporary_path, "r") as hdf:
                group = hdf[selection["model"]]
                dataset = group["posterior_samples"]
                names = tuple(dataset.dtype.names or ())
                for parameter in selection["parameters"]:
                    if parameter not in names:
                        raise SystemExit(f"SEMANTIC_PARAMETER_MISSING:{parameter}")
                    raw = np.asarray(dataset.fields(parameter)[:], dtype=float).reshape(-1)
                    posterior_scalars += int(raw.size)
                    values = raw[np.isfinite(raw)]
                    if values.size < 20 or values.size != raw.size:
                        raise SystemExit(f"SEMANTIC_NONFINITE_OR_LT20:{parameter}:{raw.size}:{values.size}")
                    q05, q50, q95 = np.quantile(values, [0.05, 0.5, 0.95], method="linear")
                    item = summary[parameter]
                    error_checks = {
                        "median_equals_q50": close(item["median"], float(q50)),
                        "lower_equals_median_minus_q05": close(item["lower"], float(q50 - q05)),
                        "upper_equals_q95_minus_median": close(item["upper"], float(q95 - q50)),
                    }
                    endpoint_checks = {
                        "lower_equals_q05": close(item["lower"], float(q05)),
                        "upper_equals_q95": close(item["upper"], float(q95)),
                    }
                    result_rows.append({
                        "parameter": parameter,
                        "raw_samples": int(raw.size),
                        "finite_samples": int(values.size),
                        "summary": item,
                        "posterior_quantiles": {"q05": float(q05), "q50": float(q50), "q95": float(q95)},
                        "asymmetric_error_checks": error_checks,
                        "asymmetric_error_interpretation_pass": all(error_checks.values()),
                        "endpoint_checks": endpoint_checks,
                        "endpoint_interpretation_exact_match": all(endpoint_checks.values()),
                    })
            temporary_path.unlink(missing_ok=True)
    finally:
        raw_retained = bool(temporary_path and temporary_path.exists())

    all_error_pass = len(result_rows) == len(selection["parameters"]) and all(row["asymmetric_error_interpretation_pass"] for row in result_rows)
    endpoint_matches = sum(row["endpoint_interpretation_exact_match"] for row in result_rows)
    result = {
        "validation_id": "GWBH_ERIA_XR01_GWTC41_OUT_OF_FRAME_SEMANTIC_VALIDATION",
        "started_at_utc": started,
        "completed_at_utc": utc_now(),
        "selection_sha256": SELECTION_SHA256,
        "event": selection["event"],
        "event_in_candidate_frame": False,
        "model": selection["model"],
        "official_identity": {
            "filename": selection["official_filename"],
            "expected_size_bytes": selection["expected_size_bytes"],
            "observed_size_bytes": observed_size,
            "expected_md5": selection["expected_md5"],
            "observed_md5": observed_md5,
            "observed_sha256": observed_sha256,
            "pass": observed_size == selection["expected_size_bytes"] and observed_md5 == selection["expected_md5"],
        },
        "parameter_results": result_rows,
        "posterior_scalar_elements_read": posterior_scalars,
        "candidate_summary_numeric_values_accessed": 0,
        "candidate_posterior_elements_accessed": 0,
        "out_of_frame_summary_numeric_values_accessed": len(selection["parameters"]) * 3,
        "out_of_frame_posterior_elements_accessed": posterior_scalars,
        "asymmetric_error_interpretation_pass_count": sum(row["asymmetric_error_interpretation_pass"] for row in result_rows),
        "endpoint_interpretation_exact_match_count": endpoint_matches,
        "released_byte_semantics": "median=q50; lower=median-q05; upper=q95-median" if all_error_pass else "UNRESOLVED",
        "official_notebook_endpoint_description_reproduces_released_bytes": endpoint_matches == len(result_rows),
        "raw_event_hdf_retained": raw_retained,
        "status": "PASS_ASYMMETRIC_ERROR_MAGNITUDES" if all_error_pass and not raw_retained else "NO_GO_SEMANTIC_UNRESOLVED",
        "claim_boundary": "Byte-level semantics of one locked out-of-frame GWTC-4.1 event only; not an official LVK erratum and not a candidate scientific result.",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "posterior_scalar_elements_read": posterior_scalars, "raw_event_hdf_retained": raw_retained}, indent=2))
    return 0 if result["status"] == "PASS_ASYMMETRIC_ERROR_MAGNITUDES" else 2


if __name__ == "__main__":
    raise SystemExit(main())
