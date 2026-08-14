#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED = {
 'integrity/REPOSITORY_MANIFEST.csv',
 'integrity/REPOSITORY_TREE_SHA256SUMS.txt',
 'integrity/REPOSITORY_STATUS.json',
 'integrity/FINAL_REPOSITORY_AUDIT.json',
}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
rows=list(csv.DictReader((ROOT/'integrity/REPOSITORY_MANIFEST.csv').open()))
bad=[]
for r in rows:
 p=ROOT/r['path']; ok=p.exists() and p.stat().st_size==int(r['size_bytes']) and sha(p)==r['sha256']
 if not ok:bad.append(r['path'])
listed={r['path'] for r in rows}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in EXCLUDED}
missing_from_manifest=sorted(actual-listed)
missing_from_tree=sorted(listed-actual)
if missing_from_manifest:
 bad.extend(f'UNLISTED:{p}' for p in missing_from_manifest)
if missing_from_tree:
 bad.extend(f'MISSING:{p}' for p in missing_from_tree)
print(f"{'PASS' if not bad else 'FAIL'} {len(rows)-sum(not x.startswith(('UNLISTED:','MISSING:')) for x in bad)}/{len(rows)} repository payload hashes; coverage {len(listed & actual)}/{len(actual)}")
if bad:
 for x in bad:print('  ',x)
raise SystemExit(0 if not bad else 2)
