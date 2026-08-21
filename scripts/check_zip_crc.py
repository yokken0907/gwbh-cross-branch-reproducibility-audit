#!/usr/bin/env python3
import zipfile, sys
from pathlib import Path
paths=[]
for a in sys.argv[1:]:
 p=Path(a)
 if p.is_dir(): paths.extend(sorted(p.glob('*.zip')))
 else: paths.append(p)
if not paths:
 print('Usage: python scripts/check_zip_crc.py <zip-or-directory> [...]'); raise SystemExit(2)
fail=[]
for p in paths:
 try:
  with zipfile.ZipFile(p) as z: bad=z.testzip()
  print('PASS' if bad is None else 'FAIL',p.name,'' if bad is None else bad)
  if bad is not None:fail.append(str(p))
 except Exception as e:
  print('FAIL',p,e);fail.append(str(p))
raise SystemExit(1 if fail else 0)
