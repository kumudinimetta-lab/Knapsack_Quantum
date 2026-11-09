"""Independent LP-vertex check of the theory agent's off-grid boundary case."""
import ast
from fractions import Fraction
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.compressed_bank import build_compressed_bank
p=ROOT/'research_log/pruning_study_20261023/reviewer_adversarial_probe.py'
fn=next(x for x in ast.parse(p.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='reference')
ns={'Fraction':Fraction};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'),ns)
rows=[];w=v=None
w=[9,9];v=[1,1];W=10;lam=Fraction(1,11)
for d in range(3):
    for prefix in range(1<<d):
        exact=ns['reference'](w,v,W,d,prefix)
        if exact is None:continue
        selected=prefix.bit_count();P=selected;R=W-9*selected
        dual=P+lam*R+(2-d)*max(1-9*lam,0)
        rows.append(dict(depth=d,prefix=prefix,exact=str(exact),offgrid=str(dual),
            exact_floor=exact.numerator//exact.denominator,
            offgrid_floor=dual.numerator//dual.denominator))
bank=build_compressed_bank(w,v,W)
out=dict(classification='DERIVED exact LP vertex and rational comparisons',
    weights=w,values=v,capacity=W,density_grid_minimum=bank['bank_size'],
    density_grid_bank=bank['bank'],offgrid_bank=[[1,11]],offgrid_size=1,
    feasible_prefix_checks=len(rows),floor_mismatches=sum(r['exact_floor']!=r['offgrid_floor'] for r in rows),
    includes_complete_leaves=True,rows=rows)
dest=Path(__file__).with_name('reviewer_offgrid_analytic.json')
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if out['floor_mismatches'] or out['density_grid_minimum']!=2:raise RuntimeError('RESEARCH_INTEGRITY_STOP: boundary witness conflict')
