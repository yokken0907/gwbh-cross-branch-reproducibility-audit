#!/usr/bin/env python3

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"MANIFEST.csv", "SHA256SUMS.txt"}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def included_files() -> list[Path]:
    result = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in EXCLUDED or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        result.append(path)
    return sorted(result, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> int:
    data = []
    for path in included_files():
        relative = path.relative_to(ROOT).as_posix()
        data.append({"path": relative, "size_bytes": path.stat().st_size, "sha256": sha256(path)})
    with (ROOT / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "size_bytes", "sha256"))
        writer.writeheader()
        writer.writerows(data)
    (ROOT / "SHA256SUMS.txt").write_text(
        "".join(f"{row['sha256']}  {row['path']}\n" for row in data), encoding="utf-8"
    )
    print(f"manifest_files={len(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
