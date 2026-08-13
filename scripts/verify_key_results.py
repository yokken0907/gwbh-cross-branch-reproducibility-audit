#!/usr/bin/env python3
from pathlib import Path
import csv,json,math
ROOT=Path(__file__).resolve().parents[1]
def close(a,b,tol=5e-7): return abs(float(a)-float(b))<=tol
checks=[]
# B01
b=ROOT/'evidence/branch_results/B01_GWBH-PIA/03_CUMULATIVE_RESULTS'
r13=json.loads((b/'RELEASE_DRIFT_CONFIRMATORY/RUN13_CONFIRMATORY_REPORT.json').read_text())
r21=json.loads((b/'FIXED_RELEASE_MODEL_DEPENDENCE/RUN21_REPORT.json').read_text())
checks += [('B01-R13-rho',close(r13['primary_rho'],0.8809523809523809)),('B01-R13-p',close(r13['primary_exact_one_sided_p'],0.003621031746031746,1e-12)),('B01-R13-perms',r13['primary_permutations']==40320),('B01-R21-rho',close(r21['primary_spearman_rho'],0.9523809523809523)),('B01-R21-p',close(r21['primary_exact_one_sided_p'],0.000570436507936508,1e-12)),('B01-R21-perms',r21['primary_permutations']==40320)]
# Atlas counts
with (ROOT/'evidence/final_project/DIRECT_PROJECT_CLOSURE/FINAL_DEPENDENCY_ATLAS.csv').open(encoding='utf-8-sig') as f: ed=list(csv.DictReader(f))
counts={}
for r in ed: counts[r['final_class']]=counts.get(r['final_class'],0)+1
expected={'PARTIAL_STRUCTURAL':8,'IDENTITY_ONLY':3,'BLOCKED_PUBLIC_ASSET':3,'BLOCKED_SCHEMA':2,'DIRECT_NUMERIC':0}
for k,v in expected.items(): checks.append((f'ATLAS-{k}',counts.get(k,0)==v))
checks.append(('ATLAS-total',len(ed)==16))
# B08 key numeric
with (ROOT/'evidence/branch_results/B08_GWBH-SSIDA/DIRECT_FINAL_CLOSURE/KEY_NUMERIC_FINDINGS.csv').open(encoding='utf-8') as f: rr={r['id']:r for r in csv.DictReader(f)}
for id_,dm,w1 in [('C08',-9.066,0.558),('C09',-7.968,0.517),('R17',-8.515,0.556)]:
    checks.append((f'{id_}-delta',abs(float(rr[id_]['delta_median'])-dm)<0.0015))
    checks.append((f'{id_}-w1',abs(float(rr[id_]['normalized_w1'])-w1)<0.0015))
failed=[n for n,ok in checks if not ok]
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
print(f'SUMMARY: {len(checks)-len(failed)}/{len(checks)} PASS')
raise SystemExit(0 if not failed else 2)
