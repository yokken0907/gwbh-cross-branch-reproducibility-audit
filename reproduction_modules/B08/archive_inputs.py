"""Read the two frozen Release assets without environment-specific paths."""
from pathlib import Path
import csv
import hashlib
import io
import json
import zipfile

A01_FILENAME = "GWBHXBICA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_PROJECT_CLOSURE.zip"
A01_SHA256 = "87247fb2a664c127570008586cf17110f60e9dc4544899291bca70afa8e1d1f2"
A02_FILENAME = "GWBH_B08_COMPACT_REPRODUCTION_PAYLOADS_v1.0.0.zip"
A02_SHA256 = "2bdcfeae243a6eec84a6b87b64faa35ce22fbe38a2a189ebc02b97d7337fe8f9"
B08_MASTER_SUFFIX = "B08_GWBH-SSIDA/GWBHSSIDA_MASTER_REFERENCE_PACKAGE_v1.0.0_FINAL_CLOSURE.zip"
PHASE7_SUFFIX = "CANONICAL_LINEAGE/GWBHSSIDA_PHASE7_RUN01_v0.8.0_RESULTS_FOR_REVIEW.zip"
PHASE6_SUFFIX = "inputs/GWBHSSIDA_PHASE6_RUN01_v0.7.0_RESULTS_FOR_REVIEW.zip"
PHASE5_SUFFIX = "inputs/GWBHSSIDA_PHASE5_RUN01_v0.6.0_RESULTS_FOR_REVIEW.zip"


def sha256_file(path, block=16 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()


def _single_suffix(z, suffix):
    hits = [n for n in z.namelist() if n.endswith(suffix)]
    if len(hits) != 1:
        raise KeyError(f"Expected exactly one member ending {suffix!r}; found {len(hits)}")
    return hits[0]


def _nested_zip_bytes(data, suffix):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return z.read(_single_suffix(z, suffix))


def verify_release_assets(a01, a02):
    a01 = Path(a01)
    a02 = Path(a02)
    checks = {
        "A01_exists": a01.is_file(),
        "A02_exists": a02.is_file(),
    }
    if checks["A01_exists"]:
        checks["A01_sha256"] = sha256_file(a01) == A01_SHA256
    if checks["A02_exists"]:
        checks["A02_sha256"] = sha256_file(a02) == A02_SHA256
    if not all(checks.values()):
        raise RuntimeError(f"Release asset verification failed: {checks}")
    return checks


def open_b08_master(a01):
    with zipfile.ZipFile(a01) as z:
        return z.read(_single_suffix(z, B08_MASTER_SUFFIX))


def open_phase5_result(a01):
    b08 = open_b08_master(a01)
    p7 = _nested_zip_bytes(b08, PHASE7_SUFFIX)
    p6 = _nested_zip_bytes(p7, PHASE6_SUFFIX)
    return _nested_zip_bytes(p6, PHASE5_SUFFIX)


def read_phase5_recovered(a01, basename):
    p5 = open_phase5_result(a01)
    with zipfile.ZipFile(io.BytesIO(p5)) as z:
        return z.read(_single_suffix(z, f"work/recovered/{basename}"))


def read_expected_b08_closure(a01, basename):
    b08 = open_b08_master(a01)
    with zipfile.ZipFile(io.BytesIO(b08)) as z:
        return z.read(_single_suffix(z, f"DIRECT_FINAL_CLOSURE/{basename}"))


def load_compact_payload_manifest(a02):
    with zipfile.ZipFile(a02) as z:
        hits = [n for n in z.namelist() if n.endswith("/PAYLOAD_MANIFEST.csv") and "/manifests/" not in n]
        if len(hits) != 1:
            raise KeyError(f"Expected one root PAYLOAD_MANIFEST.csv; found {len(hits)}")
        root = hits[0].rsplit("/", 1)[0]
        rows = list(csv.DictReader(io.StringIO(z.read(hits[0]).decode("utf-8"))))
        return root, rows


def verify_compact_payloads(a02):
    root, rows = load_compact_payload_manifest(a02)
    failures = []
    with zipfile.ZipFile(a02) as z:
        for r in rows:
            member = f"{root}/payloads/{r['filename']}"
            if member not in z.namelist():
                failures.append((r["filename"], "missing"))
                continue
            data = z.read(member)
            if len(data) != int(r["size_bytes"]):
                failures.append((r["filename"], "size"))
                continue
            if hashlib.sha256(data).hexdigest() != r["sha256"]:
                failures.append((r["filename"], "sha256"))
    if failures:
        raise RuntimeError(f"Compact B08 payload verification failed: {failures}")
    return rows


def load_payload_jsons(a02):
    root, rows = load_compact_payload_manifest(a02)
    out = {}
    with zipfile.ZipFile(a02) as z:
        for r in rows:
            member = f"{root}/payloads/{r['filename']}"
            obj = json.loads(z.read(member))
            out[r["filename"]] = obj
    return out



def _extract_first_posterior_h0_array(data):
    """Extract posterior.content.H0 without decoding the entire Bilby JSON."""
    posterior = data.find(b'"posterior"')
    if posterior < 0:
        raise KeyError('posterior')
    marker = b'"H0"'
    pos = posterior
    while True:
        pos = data.find(marker, pos)
        if pos < 0:
            raise KeyError('posterior H0 array')
        colon = data.find(b':', pos + len(marker))
        if colon < 0:
            raise KeyError('posterior H0 colon')
        j = colon + 1
        while j < len(data) and data[j] in b' \t\r\n':
            j += 1
        if j < len(data) and data[j:j+1] == b'[':
            start = j
            depth = 0
            in_string = False
            escape = False
            for k in range(start, len(data)):
                c = data[k]
                if in_string:
                    if escape:
                        escape = False
                    elif c == 92:
                        escape = True
                    elif c == 34:
                        in_string = False
                else:
                    if c == 34:
                        in_string = True
                    elif c == 91:
                        depth += 1
                    elif c == 93:
                        depth -= 1
                        if depth == 0:
                            return json.loads(data[start:k+1])
            raise ValueError('unterminated posterior H0 array')
        pos = colon + 1


def load_payload_h0_samples(a02):
    root, rows = load_compact_payload_manifest(a02)
    out = {}
    with zipfile.ZipFile(a02) as z:
        for r in rows:
            member = f"{root}/payloads/{r['filename']}"
            out[r['filename']] = _extract_first_posterior_h0_array(z.read(member))
    return out

def primary_payload_names(a02):
    with zipfile.ZipFile(a02) as z:
        member = _single_suffix(z, "manifests/PRIMARY_ORIGINAL_PAYLOAD_MANIFEST.csv")
        rows = list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8"))))
        return [r["filename"] for r in rows]
