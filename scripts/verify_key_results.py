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
# Independently versioned post-closure results (no historical reclassification)
pc=ROOT/'evidence/post_closure_extensions'
b04=json.loads((pc/'B04_U02/DECISION.json').read_text())
checks += [
 ('B04-U02-NO_GO',b04['decision_code']=='B04_U02_REOPEN_NOT_SATISFIED'),
 ('B04-U02-no-numeric',not b04['numeric_analysis_performed'] and b04['p02_values_read']==0 and b04['m01_values_computed']==0),
]
for label,path,n,rho,verdict in [
 ('U03',pc/'U03_GWTC5/06_RUN_OUTPUT/PRIMARY_TEST.json',22,0.9017504234895539,'SUPPORTED_RELEASE_SPECIFIC_ALTTRIAD_SUMMARY_SCREENING_CALIBRATION'),
 ('XR01',pc/'XR01_GWTC41/06_RUN_OUTPUT/PRIMARY_TEST.json',44,0.9468639887244539,'SUPPORTED_CROSS_RELEASE_ALTERNATE_TRIAD_SUMMARY_SCREENING_TRANSPORT'),
]:
    result=json.loads(path.read_text())
    checks += [
      (f'{label}-n',result['n']==n),
      (f'{label}-rho',close(result['observed_spearman_rho'],rho,1e-15)),
      (f'{label}-perms',result['permutations']==1000000),
      (f'{label}-p',close(result['one_sided_plus_one_p'],9.99999000001e-7,1e-18)),
      (f'{label}-verdict',result['verdict']==verdict),
    ]
run01=json.loads((pc/'U03_GWTC5/PARENT_REFERENCE/RUN01_DECISION.json').read_text())
next_step=json.loads((pc/'NEXT_STEP_DECISION.json').read_text())
checks += [
 ('U03-historical-RUN01-preserved',run01['decision']=='NO_GO_NUMERIC_COMPLETE_FRAME_LT8' and run01['parent_closure_effect']=='NONE'),
 ('POSTCLOSURE-next-step-NO_GO',next_step['decision']=='NO_GO_FURTHER_IMMEDIATE_SAME_DATA_ANALYSIS__XR01_EXTENSION_COMPLETE'),
]
failed=[n for n,ok in checks if not ok]
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
print(f'SUMMARY: {len(checks)-len(failed)}/{len(checks)} PASS')
raise SystemExit(0 if not failed else 2)
