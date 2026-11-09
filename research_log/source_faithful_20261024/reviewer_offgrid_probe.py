"""Bounded falsification of an intentionally excluded stronger minimum claim.

Before testing: enumerate midpoint multipliers in addition to the density grid,
look for a strictly smaller covering bank, then independently confirm any found
counterexample with exact LP vertex enumeration. Search failure would establish
nothing globally. This does not change the valid on-grid minimum claim.
"""
import ast
from fractions import Fraction
import itertools
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.compressed_bank import build_compressed_bank
refpath=ROOT/'research_log/pruning_study_20261023/reviewer_adversarial_probe.py'
fn=next(n for n in ast.parse(refpath.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='reference')
ns={'Fraction':Fraction};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(refpath),'exec'),ns)
reference=ns['reference']
SEED=2026102413;rng=random.Random(SEED);budget=2000;witness=None
records=[]
for index in range(budget):
    n=rng.randrange(2,6);w=[rng.randrange(1,31) for _ in range(n)]
    v=[rng.randrange(1,16) for _ in range(n)];W=rng.randrange(sum(w)+1)
    bank=build_compressed_bank(w,v,W);k=bank['bank_size']
    if k<=1:continue
    grid=[Fraction(*p) for p in bank['root_tail_grid']]
    candidates=sorted(set(grid+[(a+b)/2 for a,b in zip(grid,grid[1:])]))
    order=bank['order'];states=[]
    for d in range(n+1):
        for p in range(1<<d):
            chosen=[order[j] for j in range(d) if p>>j&1]
            used=sum(w[i] for i in chosen)
            if used>W:continue
            P=sum(v[i] for i in chosen);R=W-used;rem=R;U=Fraction(P)
            for i in order[d:]:
                fraction=min(Fraction(rem,w[i]),Fraction(1));U+=fraction*v[i];rem-=fraction*w[i]
            states.append((d,p,P,R,U.numerator//U.denominator))
    masks=[]
    for lam in candidates:
        mask=0
        for j,(d,p,P,R,floor) in enumerate(states):
            value=P+lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:])
            if value<floor+1:mask|=1<<j
        masks.append(mask)
    full=(1<<len(states))-1
    for size in range(1,k):
        for choice in itertools.combinations(range(len(candidates)),size):
            covered=0
            for j in choice:covered|=masks[j]
            if covered==full:
                selected=[candidates[j] for j in choice]
                confirmation=[]
                for d,p,P,R,floor in states:
                    U=reference(w,v,W,d,p)
                    actual=min(P+lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:]) for lam in selected)
                    confirmation.append(U.numerator//U.denominator==actual.numerator//actual.denominator)
                witness=dict(index=index,weights=w,values=v,capacity=W,grid=bank['root_tail_grid'],
                    grid_minimum=k,grid_bank=bank['bank'],offgrid_bank=[[x.numerator,x.denominator] for x in selected],
                    offgrid_size=size,all_prefix_vertex_checks=len(confirmation),
                    vertex_floor_mismatches=confirmation.count(False))
                break
        if witness:break
    records.append(dict(index=index,grid_minimum=k,candidates=len(candidates),feasible_states=len(states)))
    if witness:break
out=dict(seed=SEED,budget=budget,instances_generated=index+1,nontrivial_search_cases=len(records),
    classification='DERIVED exact rational counterexample search',witness=witness,search_records=records)
path=Path(__file__).with_name('reviewer_offgrid_probe.json')
if path.exists():raise RuntimeError('Refuse overwrite')
path.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='search_records'},indent=2))
if witness and witness['vertex_floor_mismatches']:raise RuntimeError('RESEARCH_INTEGRITY_STOP: search confirmation conflict')
