#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile, json, base64, hashlib

def sha256_file(p, block=16*1024*1024):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(block),b''): h.update(b)
    return h.hexdigest()

def make_zi(m):
    zi=zipfile.ZipInfo(filename=m['filename'], date_time=tuple(m['date_time']))
    zi.compress_type=m['compress_type']
    zi.comment=base64.b64decode(m['comment_b64'])
    zi.extra=base64.b64decode(m['extra_b64'])
    zi.internal_attr=m['internal_attr']; zi.external_attr=m['external_attr']
    zi.create_system=m['create_system']; zi.create_version=m['create_version']; zi.extract_version=m['extract_version']
    zi.flag_bits=m['flag_bits']; zi.volume=m['volume']
    return zi

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('compact_zip', type=Path)
    ap.add_argument('output_dir', type=Path)
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.compact_zip) as z:
        root=[n.split('/')[0] for n in z.namelist() if n.endswith('ORIGINAL_ZIPINFO_METADATA.json')][0]
        meta=json.loads(z.read(root+'/ORIGINAL_ZIPINFO_METADATA.json'))
        for group,g in meta.items():
            out=args.output_dir/g['original_filename']
            with zipfile.ZipFile(out,'w') as w:
                for m in g['members']:
                    fn=m['filename']
                    if fn.endswith('/PAYLOAD_MANIFEST.csv'):
                        data=z.read(root+f'/manifests/{group}_ORIGINAL_PAYLOAD_MANIFEST.csv')
                    elif '/payloads/' in fn:
                        data=z.read(root+'/payloads/'+Path(fn).name)
                    else:
                        raise RuntimeError(f'Unmapped original member: {fn}')
                    if len(data)!=m['file_size']:
                        raise RuntimeError(f'Size mismatch for {fn}')
                    zi=make_zi(m)
                    w.writestr(zi,data,compress_type=m['compress_type'])
            got=sha256_file(out)
            ok=(got==g['original_sha256'] and out.stat().st_size==g['original_size_bytes'])
            print(f"{group}: {'PASS' if ok else 'FAIL'} {out.name} {out.stat().st_size} {got}")
            if not ok: raise SystemExit(2)
if __name__=='__main__': main()
