#!/usr/bin/env python3
"""Recompute the final B08 primary, robustness, and post-hoc metrics from A01+A02."""
from pathlib import Path
import argparse
import csv
import gc
import io
import json
import math

from archive_inputs import (
    verify_release_assets,
    verify_compact_payloads,
    load_payload_h0_samples,
    primary_payload_names,
    read_phase5_recovered,
    read_expected_b08_closure,
)
from metriclib import clean_samples, summarize, paired, official_grid_density_samples, sample_digest

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
CONFIG = HERE / "config"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def csv_bytes_to_rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))


def json_bytes(data):
    return json.loads(data.decode("utf-8"))


def extract_h0(obj):
    return clean_samples(obj["posterior"]["content"]["H0"])


def floats_close(a, b, rel=1e-12, abs_=1e-12):
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=abs_)


def compare_table(actual_rows, expected_rows, key, metric_fields, status_field="status"):
    aby = {r[key]: r for r in actual_rows}
    eby = {r[key]: r for r in expected_rows}
    failures = []
    for k, e in eby.items():
        if k not in aby:
            failures.append({"key": k, "field": "row", "reason": "missing_actual"})
            continue
        a = aby[k]
        if status_field and a.get(status_field, "") != e.get(status_field, ""):
            failures.append({"key": k, "field": status_field, "actual": a.get(status_field), "expected": e.get(status_field)})
        for field in metric_fields:
            av = a.get(field, "")
            ev = e.get(field, "")
            if av == "" and ev == "":
                continue
            if av == "" or ev == "" or not floats_close(av, ev):
                failures.append({"key": k, "field": field, "actual": av, "expected": ev})
    extra = sorted(set(aby) - set(eby))
    for k in extra:
        failures.append({"key": k, "field": "row", "reason": "unexpected_actual"})
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-master", required=True, type=Path, help="Release Asset A01")
    ap.add_argument("--b08-payload", required=True, type=Path, help="Release Asset A02")
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    asset_checks = verify_release_assets(args.project_master, args.b08_payload)
    payload_manifest = verify_compact_payloads(args.b08_payload)

    p4cfg = read_json(CONFIG / "PHASE4_RUN_CONFIG.json")
    p5cfg = read_json(CONFIG / "PHASE5_RUN_CONFIG.json")
    primary_contract = read_json(CONFIG / "PAIRED_COMPARISON_CONTRACT.json")
    robust_contract = read_json(CONFIG / "ROBUSTNESS_PAIR_CONTRACT.json")
    bright_contract = read_json(CONFIG / "POSTHOC_BRIGHT_DIAGNOSTIC_CONTRACT.json")

    # Load compact large-posterior payloads one-by-one into compact H0 sample arrays.
    payload_h0 = load_payload_h0_samples(args.b08_payload)
    samples = {fn: clean_samples(arr) for fn, arr in payload_h0.items()}
    del payload_h0
    gc.collect()

    # Small public-output artifacts are recovered from the canonical A01 B08 lineage.
    small = {}
    for fn in ["H0_spectral_combined_gw170817.json", "H0_dark_combined_gw170817.json"]:
        obj = json_bytes(read_phase5_recovered(args.project_master, fn))
        small[fn] = clean_samples(obj["posterior"])
    bright = json_bytes(read_phase5_recovered(args.project_master, "GW170817_H0_posterior.json"))

    # Phase4 RUN02 corrected primary path: 10 large primary endpoints + 2 direct combined endpoints.
    primary_names = primary_payload_names(args.b08_payload)
    primary_samples = {fn: samples[fn] for fn in primary_names}
    primary_samples.update(small)

    summary_rows = []
    for fn, arr in sorted(primary_samples.items()):
        summary_rows.append({"filename": fn, **summarize(arr)})
    write_csv(
        outdir / "H0_POSTERIOR_SUMMARY_CORRECTED.csv",
        ["filename", "n", "median", "q16", "q84", "q05", "q95", "q25", "q75", "width68", "width90", "iqr"],
        summary_rows,
    )

    primary_rows = []
    for q in primary_contract:
        if q["id"] in p4cfg["public_output_limited_pair_ids"]:
            primary_rows.append({
                "id": q["id"], "dimension": q["dimension"], "a": q["a"], "b": q["b"],
                "status": "PUBLIC_OUTPUT_LIMITED_GRID_DENSITY_NOT_SAMPLES",
                "delta_median": "", "width68_ratio": "", "normalized_w1": "", "central68_overlap": "",
                "interpretation": q["interpretation"],
            })
        else:
            m = paired(primary_samples[q["a"]], primary_samples[q["b"]])
            primary_rows.append({
                "id": q["id"], "dimension": q["dimension"], "a": q["a"], "b": q["b"],
                "status": "PASS", **m, "interpretation": q["interpretation"],
            })
    write_csv(
        outdir / "PAIRED_DEPENDENCY_METRICS_CORRECTED.csv",
        ["id", "dimension", "a", "b", "status", "delta_median", "width68_ratio", "normalized_w1", "central68_overlap", "interpretation"],
        primary_rows,
    )

    # Phase5 robustness path: all payloads referenced by R01-R17 are already available in A02.
    robust_rows = []
    for q in robust_contract:
        m = paired(samples[q["a"]], samples[q["b"]])
        robust_rows.append({
            "id": q["id"], "axis": q["axis"], "context": q["context"], "a": q["a"], "b": q["b"],
            "confound": q["confound"], "status": "PASS", **m,
        })
    write_csv(
        outdir / "ROBUSTNESS_PAIRED_METRICS.csv",
        ["id", "axis", "context", "a", "b", "confound", "status", "delta_median", "width68_ratio", "normalized_w1", "central68_overlap"],
        robust_rows,
    )

    # Post-hoc GW170817 grid-density diagnostic. This does not change C11/C12 primary status.
    bs = official_grid_density_samples(
        bright["prior"], bright["posterior"],
        N=p5cfg["bright_conversion"]["N"], seed=p5cfg["bright_conversion"]["seed"],
    )
    bdigest = sample_digest(bs)
    posthoc_rows = []
    for q in bright_contract:
        m = paired(bs, small[q["b"]])
        posthoc_rows.append({
            "id": q["id"], "label": q["label"], "a": q["a"], "b": q["b"],
            "status": "PASS_POST_HOC_DIAGNOSTIC", **m,
            "bright_sample_count": len(bs), "bright_sample_sha256": bdigest,
            "seed": p5cfg["bright_conversion"]["seed"],
        })
    write_csv(
        outdir / "POSTHOC_BRIGHT_DIAGNOSTIC_METRICS.csv",
        ["id", "label", "a", "b", "status", "delta_median", "width68_ratio", "normalized_w1", "central68_overlap", "bright_sample_count", "bright_sample_sha256", "seed"],
        posthoc_rows,
    )

    # Cross-model matrix using the frozen Phase5 matrix contract from the canonical run.
    matrix_contract = [
        ("PIPELINE", "FULLPOP", "C01"), ("PIPELINE", "BPL3P", "R01"), ("PIPELINE", "MLTP", "R02"),
        ("SPECTRAL_TO_DES", "FULLPOP", "C02"), ("SPECTRAL_TO_DES", "BPL3P", "R03"), ("SPECTRAL_TO_DES", "MLTP", "R08"),
        ("DES_TO_GLADE", "FULLPOP", "C03"), ("DES_TO_GLADE", "BPL3P", "R05"), ("DES_TO_GLADE", "MLTP", "R10"),
        ("DES_WEIGHTING", "FULLPOP", "C04"), ("DES_WEIGHTING", "BPL3P", "R06"), ("DES_WEIGHTING", "MLTP", "R11"),
        ("GLADE_WEIGHTING", "FULLPOP", "C05"), ("GLADE_WEIGHTING", "BPL3P", "R07"), ("GLADE_WEIGHTING", "MLTP", "R12"),
        ("POP_FULLPOP_TO_BPL3P", "SPECTRAL", "C06"), ("POP_FULLPOP_TO_BPL3P", "DES_LUM", "R13"), ("POP_FULLPOP_TO_BPL3P", "GLADE_LUM", "R14"),
        ("IFAR_FULLPOP", "SPECTRAL", "C08"), ("IFAR_FULLPOP", "DES_LUM", "C09"), ("IFAR_FULLPOP", "DES_UNI", "R17"),
    ]
    pby = {r["id"]: r for r in primary_rows}
    rby = {r["id"]: r for r in robust_rows}
    matrix_rows = []
    for axis, context, pid in matrix_contract:
        src = pby.get(pid) or rby.get(pid)
        matrix_rows.append({
            "axis": axis, "context": context, "pair_id": pid, "status": src.get("status", "MISSING"),
            "delta_median": src.get("delta_median", ""), "width68_ratio": src.get("width68_ratio", ""),
            "normalized_w1": src.get("normalized_w1", ""), "central68_overlap": src.get("central68_overlap", ""),
        })
    write_csv(
        outdir / "CROSS_MODEL_ROBUSTNESS_MATRIX.csv",
        ["axis", "context", "pair_id", "status", "delta_median", "width68_ratio", "normalized_w1", "central68_overlap"],
        matrix_rows,
    )

    # Verification against the final canonical B08 closure inside A01.
    expected_primary = csv_bytes_to_rows(read_expected_b08_closure(args.project_master, "PAIRED_DEPENDENCY_METRICS_CORRECTED.csv"))
    expected_robust = csv_bytes_to_rows(read_expected_b08_closure(args.project_master, "ROBUSTNESS_PAIRED_METRICS.csv"))
    expected_posthoc = csv_bytes_to_rows(read_expected_b08_closure(args.project_master, "POSTHOC_BRIGHT_DIAGNOSTIC_METRICS.csv"))
    metric_fields = ["delta_median", "width68_ratio", "normalized_w1", "central68_overlap"]
    failures = []
    failures += [{"table": "primary", **x} for x in compare_table(primary_rows, expected_primary, "id", metric_fields)]
    failures += [{"table": "robustness", **x} for x in compare_table(robust_rows, expected_robust, "id", metric_fields)]
    failures += [{"table": "posthoc", **x} for x in compare_table(posthoc_rows, expected_posthoc, "id", metric_fields)]

    report = {
        "status": "PASS" if not failures else "FAIL",
        "release_asset_checks": asset_checks,
        "compact_payload_count": len(payload_manifest),
        "primary_pair_status": "10_PASS_2_PUBLIC_OUTPUT_LIMITED",
        "robustness_pairs_pass": sum(r["status"] == "PASS" for r in robust_rows),
        "posthoc_diagnostic_pairs_pass": len(posthoc_rows),
        "bright_sample_count": len(bs),
        "bright_sample_sha256": bdigest,
        "verification_failures": failures,
        "claim_boundary": [
            "This recomputation verifies released downstream-output metrics, not a true H0 value.",
            "It does not establish cosmological bias, physical correctness of a variant, or a Hubble-tension solution.",
            "C11/C12 remain public-output-limited primary comparisons; the GW170817 conversion is post-hoc diagnostic only.",
        ],
    }
    write_json(outdir / "B08_REPRODUCTION_REPORT.json", report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if not failures else 2)


if __name__ == "__main__":
    main()
