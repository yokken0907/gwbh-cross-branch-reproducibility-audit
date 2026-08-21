#!/usr/bin/env python3
"""Value-blind GWTC-4.1 schema/mask preflight for XR01.

This program reads only string identity fields and boolean mask fields from the
compound summary table.  It deliberately does not request any floating-point
summary field and never opens an event posterior file.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import h5py


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "03_INPUT/IGWN-GWTC4p1-18965dda8_5-PESummaryTable.hdf5"
NOTEBOOK = ROOT / "03_INPUT/GWTC4p1_PE_data_release.ipynb"
METADATA = ROOT / "00_INPUT_AUDIT/ZENODO_RECORD_20275769_API.json"
MODELS = (
    "C00:IMRPhenomXPHM-SpinTaylor",
    "C00:SEOBNRv5PHM",
    "C00:NRSur7dq4",
)
PARAMETERS = (
    "chirp_mass_source",
    "chi_eff",
    "luminosity_distance",
    "final_mass_source",
    "final_spin",
)
MASK_FIELDS = tuple(
    f"{parameter}_{part}.mask"
    for parameter in PARAMETERS
    for part in ("median", "lower", "upper")
    if parameter in {"final_mass_source", "final_spin"}
)
IDENTITY_FIELDS = ("gw_name", "result_samples_key", "result_label", "result_file_name")
EXPECTED = {
    SUMMARY.name: {
        "size": 209500,
        "md5": "1e56cb4ebd8631b6f7ccc68bd89e6319",
        "sha256": "df1b28a006c21bb91d88107934eb496451382e78e2ae6371dea6455b0fda8998",
    },
    NOTEBOOK.name: {
        "size": 2887937,
        "md5": "fc8f7abd27d05a88724f91405e20dad3",
        "sha256": "b19de1ab1037ba261013e71d2d15127b3eb082dd0368c1f4e29c6e10f297fd62",
    },
}


def digest(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def decode(value) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    identities = {}
    for path in (SUMMARY, NOTEBOOK):
        expected = EXPECTED[path.name]
        observed = {
            "size": path.stat().st_size,
            "md5": digest(path, "md5"),
            "sha256": digest(path, "sha256"),
        }
        observed["pass"] = observed == expected
        identities[path.name] = {"expected": expected, "observed": observed}
        if not observed["pass"]:
            raise SystemExit(f"OFFICIAL_INPUT_IDENTITY_FAIL:{path.name}")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    if int(metadata["id"]) != 20275769 or metadata["doi"] != "10.5281/zenodo.20275769":
        raise SystemExit("ZENODO_RECORD_IDENTITY_FAIL")
    official_files = {item["key"]: item for item in metadata["files"]}

    requested = list(IDENTITY_FIELDS + MASK_FIELDS)
    required_numeric_schema = tuple(
        f"{parameter}_{part}"
        for parameter in PARAMETERS
        for part in ("median", "lower", "upper")
    )
    with h5py.File(SUMMARY, "r") as hdf:
        dataset = hdf["summary_info"]
        dtype_names = tuple(dataset.dtype.names or ())
        missing_schema = [name for name in IDENTITY_FIELDS + required_numeric_schema if name not in dtype_names]
        missing_masks = [name for name in MASK_FIELDS if name not in dtype_names]
        if missing_schema or missing_masks:
            raise SystemExit("SUMMARY_SCHEMA_MISSING:" + "|".join(missing_schema + missing_masks))
        # Value-blind read: no floating-point field is present in `requested`.
        records = dataset.fields(requested)[:]

    by_event: dict[str, dict[str, dict]] = defaultdict(dict)
    target_rows = 0
    for row in records:
        model = decode(row["result_samples_key"])
        if model not in MODELS:
            continue
        target_rows += 1
        event = decode(row["gw_name"]).upper()
        by_event[event][model] = {
            "result_label": decode(row["result_label"]),
            "result_file_name": decode(row["result_file_name"]),
            "masked_fields": [name for name in MASK_FIELDS if bool(row[name])],
        }

    candidates: list[dict] = []
    rejected: list[dict] = []
    for event, rows in sorted(by_event.items()):
        missing_models = [model for model in MODELS if model not in rows]
        masked_fields = [f"{model}:{name}" for model in MODELS if model in rows for name in rows[model]["masked_fields"]]
        filenames = sorted({row["result_file_name"] for row in rows.values()})
        expected_filename = f"IGWN-GWTC4p1-18965dda8_5-{event}-combined_PEDataRelease.hdf5"
        file_item = official_files.get(expected_filename)
        filename_pass = filenames == [expected_filename]
        if not missing_models and not masked_fields and filename_pass and file_item is not None:
            candidates.append({
                "event": event,
                "zenodo_record": 20275769,
                "official_filename": expected_filename,
                "size_bytes": int(file_item["size"]),
                "official_md5": file_item["checksum"].split(":", 1)[1],
                "content_url": file_item["links"]["self"],
                "model_triad": "|".join(model.removeprefix("C00:") for model in MODELS),
                "common5_summary_triplets_unmasked": True,
                "summary_rows_exact": True,
                "candidate_numeric_summary_values_accessed": False,
                "candidate_posterior_values_accessed": False,
            })
        else:
            rejected.append({
                "event": event,
                "missing_models": "|".join(missing_models),
                "masked_fields": "|".join(masked_fields),
                "summary_filenames": "|".join(filenames),
                "expected_filename": expected_filename,
                "summary_filename_pass": filename_pass,
                "zenodo_file_manifest_pass": file_item is not None,
            })

    if len(candidates) != 44:
        raise SystemExit(f"FROZEN_ELIGIBLE_COUNT_NOT_44:{len(candidates)}")

    candidate_fields = (
        "event", "zenodo_record", "official_filename", "size_bytes", "official_md5",
        "content_url", "model_triad", "common5_summary_triplets_unmasked",
        "summary_rows_exact", "candidate_numeric_summary_values_accessed",
        "candidate_posterior_values_accessed",
    )
    rejected_fields = (
        "event", "missing_models", "masked_fields", "summary_filenames",
        "expected_filename", "summary_filename_pass", "zenodo_file_manifest_pass",
    )
    write_csv(ROOT / "03_INPUT/CANDIDATE_EVENT_FREEZE.csv", candidates, candidate_fields)
    write_csv(ROOT / "01_PREFLIGHT/REJECTED_EVENT_SCHEMA.csv", rejected, rejected_fields)

    file_rows = []
    for item in sorted(metadata["files"], key=lambda value: value["key"]):
        file_rows.append({
            "filename": item["key"],
            "size_bytes": int(item["size"]),
            "md5": item["checksum"].split(":", 1)[1],
            "content_url": item["links"]["self"],
        })
    write_csv(
        ROOT / "03_INPUT/ZENODO_FILE_MANIFEST.csv",
        file_rows,
        ("filename", "size_bytes", "md5", "content_url"),
    )

    result = {
        "preflight_id": "GWBH_ERIA_XR01_GWTC41_SCHEMA_MASK_PREFLIGHT",
        "completed_at_utc": "2026-08-14T02:18:00Z",
        "source_release": "GWTC-4.1 / IGWN-GWTC4p1-18965dda8_5",
        "zenodo_record": 20275769,
        "zenodo_doi": "10.5281/zenodo.20275769",
        "official_input_identity": identities,
        "summary_rows_total": len(records),
        "target_model_rows": target_rows,
        "events_with_any_target_model": len(by_event),
        "eligible_event_count": len(candidates),
        "eligible_events": [row["event"] for row in candidates],
        "rejected_event_count": len(rejected),
        "target_models": list(MODELS),
        "common_parameters": list(PARAMETERS),
        "floating_point_summary_fields_requested_or_read": [],
        "boolean_mask_fields_read": list(MASK_FIELDS),
        "posterior_files_opened": 0,
        "candidate_summary_numeric_values_accessed": False,
        "candidate_posterior_values_accessed": False,
        "status": "PASS_44_SCHEMA_MASK_ELIGIBLE",
        "claim_boundary": "Official identity, compound-dtype schema, string row identity and boolean masks only; no numeric summary value or posterior element was read.",
    }
    write_json(ROOT / "01_PREFLIGHT/SCHEMA_MASK_PREFLIGHT.json", result)
    print(json.dumps({"status": result["status"], "eligible_event_count": len(candidates), "rejected_event_count": len(rejected)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
