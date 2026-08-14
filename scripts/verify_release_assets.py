#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha(path, block=16 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()


def sidecar_target_hash(path):
    parts = path.read_text(encoding="utf-8").strip().split()
    return parts[0] if parts else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base", nargs="?", default=".")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--established-only", action="store_true")
    mode.add_argument("--post-closure-only", action="store_true")
    args = parser.parse_args()
    base = Path(args.base)
    manifests = []
    if not args.post_closure_only:
        manifests.append(ROOT / "indexes/RELEASE_ASSET_MANIFEST.csv")
    if not args.established_only:
        manifests.append(ROOT / "indexes/POST_CLOSURE_RELEASE_ASSET_MANIFEST.csv")
    rows = []
    for manifest in manifests:
        rows.extend(csv.DictReader(manifest.open(encoding="utf-8")))
    failures = []
    passed = 0
    for r in rows:
        asset = base / r["filename"]
        sidecar = base / r["sidecar_filename"]
        asset_ok = (
            asset.is_file()
            and asset.stat().st_size == int(r["size_bytes"])
            and sha(asset) == r["sha256"]
        )
        sidecar_ok = (
            sidecar.is_file()
            and sidecar.stat().st_size == int(r["sidecar_size_bytes"])
            and sha(sidecar) == r["sidecar_sha256"]
            and sidecar_target_hash(sidecar) == r["sha256"]
        )
        ok = asset_ok and sidecar_ok
        print(("PASS" if ok else "FAIL"), r["asset_id"], r["filename"], "+ sidecar")
        if ok:
            passed += 1
        else:
            failures.append({"asset": r["asset_id"], "asset_ok": asset_ok, "sidecar_ok": sidecar_ok})
    print(f"SUMMARY: {passed}/{len(rows)} Release asset pairs PASS")
    if failures:
        for x in failures:
            print(" ", x)
    raise SystemExit(0 if not failures else 2)


if __name__ == "__main__":
    main()
