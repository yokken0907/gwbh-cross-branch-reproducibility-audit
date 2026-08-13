#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
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
print(f"{'PASS' if not bad else 'FAIL'} {len(rows)-len(bad)}/{len(rows)} repository payload files")
if bad:
 for x in bad:print('  ',x)
raise SystemExit(0 if not bad else 2)
