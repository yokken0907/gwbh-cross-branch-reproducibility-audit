#!/usr/bin/env python3
"""Create the one-time XR01 target-posterior lock."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "02_ANALYSIS_LOCK/PRE_POSTERIOR_LOCK.json"
LOCKED_PATHS = (
    "00_INPUT_AUDIT/OFFICIAL_SOURCE_REFERENCES.md",
    "00_INPUT_AUDIT/ZENODO_RECORD_20275769_API.json",
    "01_PREFLIGHT/schema_mask_preflight.py",
    "01_PREFLIGHT/SCHEMA_MASK_PREFLIGHT.json",
    "01_PREFLIGHT/REJECTED_EVENT_SCHEMA.csv",
    "01_PREFLIGHT/SEMANTIC_VALIDATION_SELECTION.json",
    "01_PREFLIGHT/run_semantic_validation.py",
    "01_PREFLIGHT/SEMANTIC_VALIDATION_RESULT.json",
    "01_PREFLIGHT/SCIENTIFIC_VALUE_DECISION.json",
    "02_ANALYSIS_LOCK/build_preposterior_lock.py",
    "02_ANALYSIS_LOCK/OUTCOME_BLIND_ANALYSIS_PROTOCOL.json",
    "02_ANALYSIS_LOCK/PRE_POSTERIOR_ACCESS_ATTESTATION.json",
    "02_ANALYSIS_LOCK/CLAIM_BOUNDARY.md",
    "03_INPUT/CANDIDATE_EVENT_FREEZE.csv",
    "03_INPUT/ZENODO_FILE_MANIFEST.csv",
    "03_INPUT/GWTC4p1_PE_data_release.ipynb",
    "03_INPUT/IGWN-GWTC4p1-18965dda8_5-PESummaryTable.hdf5",
    "04_SRC/run_xr01.py",
    "05_TESTS/test_xr01.py",
    "07_REPRODUCIBILITY/requirements.txt",
    "07_REPRODUCIBILITY/PRE_RUN_ENVIRONMENT.json",
    "07_REPRODUCIBILITY/PRE_RUN_TEST_LOG.txt",
    "07_REPRODUCIBILITY/verify_xr01.py",
    "PARENT_IMMUTABILITY_ATTESTATION.json",
    "PARENT_REFERENCE/PROJECT_MASTER_STATUS.json",
    "PARENT_REFERENCE/B07_MASTER_STATUS.json",
    "PARENT_REFERENCE/B04_ZENODO21454847_DECISION.json",
    "PARENT_REFERENCE/POSTCLOSURE_EXECUTIVE_DECISION.json",
    "PARENT_REFERENCE/GWTC5_OBRC_DECISION.json",
)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    if DESTINATION.exists():
        raise SystemExit("PRE_POSTERIOR_LOCK_ALREADY_EXISTS")
    attestation = json.loads((ROOT / "02_ANALYSIS_LOCK/PRE_POSTERIOR_ACCESS_ATTESTATION.json").read_text(encoding="utf-8"))
    if attestation["candidate_numeric_summary_values_accessed"] != 0:
        raise SystemExit("CANDIDATE_SUMMARY_ALREADY_ACCESSED")
    if attestation["candidate_posterior_elements_accessed"] != 0:
        raise SystemExit("CANDIDATE_POSTERIOR_ALREADY_ACCESSED")
    semantic = json.loads((ROOT / "01_PREFLIGHT/SEMANTIC_VALIDATION_RESULT.json").read_text(encoding="utf-8"))
    if semantic["status"] != "PASS_ASYMMETRIC_ERROR_MAGNITUDES":
        raise SystemExit("SEMANTIC_VALIDATION_NOT_PASS")
    files = []
    for relative in LOCKED_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"LOCK_TARGET_MISSING:{relative}")
        files.append({"path": relative, "size_bytes": path.stat().st_size, "sha256": sha256(path)})
    lock = {
        "lock_id": "GWBH_ERIA_XR01_GWTC41_PRE_POSTERIOR_LOCK_v1.0.0",
        "created_at_utc": utc_now(),
        "run_id_authorized": "GWBH_ERIA_XR01_GWTC41_COMMON5_TRANSPORT_RUN01",
        "evidence_label": "PUBLIC_DATA_TARGET_VALUE_BLIND_PREREGISTERED_CROSS_RELEASE_CONCEPTUAL_TRANSPORT",
        "candidate_frame_events": 44,
        "candidate_summary_numeric_values_accessed_at_lock": 0,
        "candidate_posterior_elements_accessed_at_lock": 0,
        "candidate_predictors_responses_correlations_accessed_at_lock": 0,
        "out_of_frame_semantic_posterior_elements_accessed": 79150,
        "locked_files_count": len(files),
        "locked_files": files,
        "authorized_next_action": "Execute 04_SRC/run_xr01.py exactly once; any lock drift is a formal stop.",
        "event_replacement_or_rescue_authorized": False,
        "historical_closure_effect": "NONE"
    }
    DESTINATION.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"lock_id": lock["lock_id"], "locked_files_count": len(files), "candidate_posterior_elements_accessed_at_lock": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
