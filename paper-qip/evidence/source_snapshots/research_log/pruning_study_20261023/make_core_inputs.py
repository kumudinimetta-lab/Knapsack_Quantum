"""Create new post-fixing inputs without changing original arrays or data.

The exact optimum is audit-only. It does not choose a fixing or an incumbent.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'simulation'))
from exact_knapsack import reduced_cost_fixing, dynamic_programming
from pruning_study_20261023.trees import feasible_incumbent


def main():
    source = HERE / 'inputs.json'
    original = json.loads(source.read_text(encoding='utf8'))
    records = []
    for row in original['records']:
        if row['category'] != 'main700':
            continue
        w, v, W = row['weights'], row['values'], row['capacity']
        lower, witness = feasible_incumbent(w, v, W)
        fi, core, fo = reduced_cost_fixing(len(w), w, v, W)
        offset = sum(v[i] for i in fi)
        residual_capacity = W - sum(w[i] for i in fi)
        cw, cv = [w[i] for i in core], [v[i] for i in core]
        if residual_capacity < 0 or any(not witness[i] for i in fi) or any(witness[i] for i in fo):
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: fixing rejects saved incumbent')
        optimum = dynamic_programming(w, v, W)
        residual_optimum = dynamic_programming(cw, cv, residual_capacity)
        if offset + residual_optimum != optimum:
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: core/original optimum conflict')
        records.append(dict(
            id=row['id'] + '_exact_core', category='core700', pilot=row['pilot'],
            original_id=row['id'], original_n=row['n'], n=len(core),
            seed=row['seed'], trial=row['trial'], instance_class=row['instance_class'],
            weights=cw, values=cv, capacity=residual_capacity,
            original_weights=w, original_values=v, original_capacity=W,
            fixed_in_indices=fi, fixed_out_indices=fo, core_original_indices=core,
            fixed_in_profit=offset, original_incumbent=lower,
            original_incumbent_witness=witness,
            expected_original_optimum=optimum, audit_core_optimum=residual_optimum,
            fixing_rule='Exact opposite-branch LP < saved greedy feasible incumbent',
            provenance='Deterministic transformation of immutable main700 arrays; optimum used only for audit'))
    output = dict(schema_version=1,
        description='Post-exact-fixing cores, including empty and unchanged cases',
        source_path=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        fixing_source_sha256=hashlib.sha256((ROOT/'simulation/exact_knapsack.py').read_bytes()).hexdigest(),
        pilot_ids=[r['id'] for r in records if r['pilot']], records=records,
        classification={'fixing_counts':'MEASURED classical outcomes', 'reference_optima':'DERIVED exact DP audit-only'})
    path = HERE/'inputs_core700.json'
    if path.exists() and json.loads(path.read_text(encoding='utf8')) != output:
        raise RuntimeError('Refuse to overwrite different core inputs')
    if not path.exists():
        path.write_text(json.dumps(output, indent=2), encoding='utf8')
    summary = dict(records=len(records), empty=sum(r['n']==0 for r in records),
        reduced=sum(r['n']<r['original_n'] for r in records),
        unchanged=sum(r['n']==r['original_n'] for r in records),
        core_sizes=dict(sorted(Counter(r['n'] for r in records).items())),
        original_core_optimum_mismatches=0,
        taxonomy='MEASURED classical fixing outcomes; optima DERIVED by exact DP, not circuit simulation',
        registry_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (HERE/'core_input_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
