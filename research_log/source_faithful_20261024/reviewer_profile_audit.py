"""Independent full-transpile control for the exact local resource profiler.

Plan: match both native and decomposed counts AND depths on declared additional
fixed-depth circuits, including empty, reduced ratios, ties and unequal words.
No extrapolation to physical duration or finite-precision rotation synthesis.
"""
import hashlib
import json
from pathlib import Path
import sys
from qiskit import transpile
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons,profile
from simulation.source_faithful_20261024.width_controls import build_exact_control
from simulation.pruning_study_20261023.circuits import BuildBudget

fixtures=[([],[],0,0),([6,4],[3,4],5,1),([6,4],[3,2],7,0),([3,7,2],[8,1,3],6,2)]
skeletons=primitive_skeletons();rows=[]
for w,v,W,d in fixtures:
    for engine in ['qft_direct','compact_exact']:
        c=build_exact_control(w,v,W,d,engine=engine,width_policy='normalized')
        actual=c.to_qiskit();common=transpile(actual,basis_gates=['u','cx'],optimization_level=0)
        estimated=profile(c,skeletons,BuildBudget(max_gates=2000000,max_seconds=60))
        matches=dict(native_counts=estimated['native_counts']==dict(actual.count_ops()),
            native_depth=estimated['native_depth']==actual.depth(),
            common_counts=estimated['common_counts']==dict(common.count_ops()),
            common_depth=estimated['common_depth']==common.depth())
        rows.append(dict(weights=w,values=v,capacity=W,depth=d,engine=engine,
            metadata=c.metadata,qubits=c.num_qubits,profile=estimated,
            actual_common_counts=dict(common.count_ops()),actual_common_depth=common.depth(),matches=matches))
out=dict(classification='DERIVED exact netlist/transpiler resource comparison',
    fixtures=len(fixtures),conditions=len(rows),mismatches=sum(not all(r['matches'].values()) for r in rows),
    rows=rows,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        ROOT/'simulation/source_faithful_20261024/resource_profile.py',
        ROOT/'simulation/source_faithful_20261024/width_controls.py']})
dest=Path(__file__).with_name('reviewer_profile_audit.json')
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if out['mismatches']:raise RuntimeError('RESEARCH_INTEGRITY_STOP: local profiler differs from full transpile')
