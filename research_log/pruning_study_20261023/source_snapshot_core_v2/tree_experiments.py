"""Versioned structural experiment driver; append-only new JSONL results."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
import sys
import time
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'simulation'))
from benchmark_v5 import (gen_uncorrelated, gen_weakly_correlated,
    gen_strongly_correlated, gen_subset_sum, gen_inverse_strongly)
from exact_knapsack import dynamic_programming
from pruning_study_20261023.trees import (METHODS, bound_at_prefix, cheap_certificate,
    enumerate_threshold_tree, feasible_incumbent, structural_optimize)

GENERATORS = [gen_uncorrelated, gen_weakly_correlated, gen_strongly_correlated,
              gen_subset_sum, gen_inverse_strongly]


def make_inputs():
    records = []
    pilot_ids = []
    cases = [([2,3,4,5], [3,4,5,8], 8), ([3,5,7,8],[3,5,7,8],13),
             ([4,7,6],[5,6,2],7), ([1,2],[3,2],0), ([2,3],[2,3],5)]
    for j, (w,v,W) in enumerate(cases):
        ident = f'small_{j:02d}'
        pilot_ids.append(ident)
        records.append(dict(id=ident, category='small', pilot=True, weights=w,
            values=v, capacity=W, n=len(w), seed=None, instance_class='adversarial_small',
            provenance='Preserved circuit feasibility pilot, 23 October 2026'))
    for n in range(12,25,2):
        for gen in GENERATORS:
            for trial in range(20):
                seed = 1000*n+trial
                w,v,W,cls = gen(n, seed=seed, R=100)
                ident = f'{cls}_n{n}_s{seed}_R100'
                pilot = n == 12 and trial == 0
                if pilot:
                    pilot_ids.append(ident)
                records.append(dict(id=ident, category='main700', pilot=pilot,
                    weights=w, values=v, capacity=W, n=n, seed=seed, trial=trial,
                    instance_class=cls, R=100, cap_ratio=0.5,
                    provenance='Existing benchmark_v5 generator, exact saved arrays; no old raw data edited'))
    # Scaling keeps feasibility and ratio ordering fixed. Targets used in the
    # separate threshold experiment are mapped from the base instance exactly.
    for base in [r for r in records if r['category']=='main700' and r['pilot']]:
        for factor in [1000, 1000000, 1000000000]:
            records.append(dict(id=base['id']+f'_scale{factor}',category='highbit_scaled',
                pilot=False,n=base['n'],seed=base['seed'],instance_class=base['instance_class'],
                weights=[factor*x for x in base['weights']],values=[factor*x for x in base['values']],
                capacity=factor*base['capacity'],scale_factor=factor,base_id=base['id'],
                provenance='Exact uniform scaling of a saved main700 instance; preserves feasible assignments'))
    out = dict(schema_version=1, description='Canonical immutable inputs for tree/circuit pairing',
               pilot_ids=pilot_ids, records=records)
    path = HERE/'inputs.json'
    if path.exists():
        if json.loads(path.read_text(encoding='utf8')) != out:
            raise RuntimeError('Refuse to overwrite a different input registry')
    else:
        path.write_text(json.dumps(out, indent=2),encoding='utf8')
    print('inputs',len(records),'pilot',len(pilot_ids),'sha256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
    return out


def audit(out):
    rng = random.Random(2026102301)
    counts = dict(instances=0, feasible_prefixes=0, hierarchy_failures=0,
                  certificate_failures=0, completed_optimizer_cases=0,
                  optimizer_value_or_witness_failures=0, capped_optimizer_cases=0)
    failures=[]
    for _ in range(100):
        n=rng.randrange(0,8)
        w=[rng.randrange(1,13) for i in range(n)]
        v=[rng.randrange(1,13) for i in range(n)]
        W=rng.randrange(0,sum(w)+3)
        counts['instances']+=1
        for d in range(n+1):
            for prefix in itertools.product((0,1),repeat=d):
                bounds={m:bound_at_prefix(w,v,W,d,prefix,m) for m in METHODS}
                if bounds['exact_lp'] is None:
                    continue
                counts['feasible_prefixes']+=1
                if not (bounds['exact_lp']<=bounds['bank4']<=bounds['bank2']<=bounds['root_dual']
                        and bounds['bank2']<=bounds['simple']):
                    counts['hierarchy_failures']+=1
                    failures.append(dict(weights=w,values=v,capacity=W,prefix=prefix))
        optimum=dynamic_programming(w,v,W)
        for method in METHODS:
            result=structural_optimize(w,v,W,method,node_cap=100000,seconds_cap=2)
            if result['status']=='complete':
                counts['completed_optimizer_cases']+=1
                if result['lower']!=optimum or not result['witness_valid']:
                    counts['optimizer_value_or_witness_failures']+=1
            else:
                counts['capped_optimizer_cases']+=1
            for tau in {optimum,optimum+1}:
                tree=enumerate_threshold_tree(w,v,W,tau,method,node_cap=100000,seconds_cap=2)
                cert=cheap_certificate(w,v,W,tau,0 if method=='simple' else None)
                counts['certificate_failures']+=tree['nodes']>cert['bound']
    out.write_text(json.dumps(dict(counts=counts, failures=failures[:10]),indent=2))
    print('audit',counts,flush=True)
    return counts


def make_independent_inputs():
    source=ROOT/'research_log/revision_20261022_large_coefficients_results.json'
    raw=json.loads(source.read_text(encoding='utf8'))
    records=[]
    for row in raw['records']:
        records.append(dict(id=f"independent_R1000000_{row['class']}_n{row['n']}_s{row['seed']}",
            category='independent_large',pilot=False,n=row['n'],seed=row['seed'],trial=row['trial'],
            instance_class=row['class'],weights=row['weights'],values=row['values'],capacity=row['capacity'],
            reference_optimum=row['mitm_optimum'],reference_method='Archived exact meet-in-the-middle; independently recomputed by this driver',
            joint_data_gcd=math.gcd(*row['weights'],*row['values'],row['capacity']),
            provenance=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    out=dict(schema_version=1,description='Unmodified saved independent R=1000000 inputs, not uniform scaling controls',
             pilot_ids=[],records=records)
    path=HERE/'inputs_stress_independent.json'
    if path.exists() and json.loads(path.read_text())!=out:
        raise RuntimeError('Refuse to overwrite different independent stress inputs')
    if not path.exists(): path.write_text(json.dumps(out,indent=2),encoding='utf8')
    print('independent inputs',len(records),'sha256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
    return out


def mitm_value(weights,values,capacity):
    middle=len(weights)//2
    halves=[]
    for indices in (range(middle),range(middle,len(weights))):
        pairs=[(0,0)]
        for i in indices:
            pairs += [(w+weights[i],v+values[i]) for w,v in pairs if w+weights[i]<=capacity]
        halves.append(pairs)
    right=sorted(halves[1]); rweights=[p[0] for p in right]
    maxima=[]; best=0
    for _,v in right:
        best=max(best,v); maxima.append(best)
    return max(v+maxima[bisect_right(rweights,capacity-w)-1] for w,v in halves[0])


def run(registry, subset, output, *, node_cap=50000, tree_seconds=0.4, algorithm_seconds=1.0):
    records=registry['records']
    selected=([r for r in records if r['id'] in registry['pilot_ids']] if subset=='pilot'
              else records if subset=='core'
              else [r for r in records if r['category'] in ('main700','highbit_scaled','independent_large')])
    seen=set()
    if output.exists():
        for line in output.read_text().splitlines():
            if line.strip(): seen.add(json.loads(line)['id'])
    index={r['id']:r for r in records}
    with output.open('a',encoding='utf8') as handle:
        for num,row in enumerate(selected):
            if row['id'] in seen: continue
            start=time.perf_counter()
            w,v,W=row['weights'],row['values'],row['capacity']
            lower,_=feasible_incumbent(w,v,W)
            # Exact reference DP scales back high-bit controls; no gigantic
            # capacity arrays are allocated for the scaled problems.
            factor=row.get('scale_factor',1)
            base=index.get(row.get('base_id'),row)
            if row['category']=='independent_large':
                optbase=mitm_value(w,v,W)
                if optbase!=row['reference_optimum']:
                    raise RuntimeError('RESEARCH_INTEGRITY_STOP: archived/reference optimum mismatch')
            else:
                optbase=dynamic_programming(base['weights'],base['values'],base['capacity'])
            optimum=factor*optbase
            base_lower,_=feasible_incumbent(base['weights'],base['values'],base['capacity'])
            targets=[('incumbent_plus_one',factor*(base_lower+1)),
                     ('optimum_plus_one',factor*(optbase+1))]
            result=dict(id=row['id'],category=row['category'],instance_class=row['instance_class'],
                n=row['n'],seed=row['seed'],optimum=optimum,incumbent=lower,
                reference_taxonomy=('DERIVED exact classical meet-in-the-middle; archived optimum independently rechecked' if row['category']=='independent_large' else 'DERIVED exact classical DP; scaled controls map base optimum exactly')+'; used only for audit/target benchmark, never optimizer decisions',
                thresholds=[],algorithms={},settings=dict(node_cap=node_cap,tree_seconds=tree_seconds,
                    algorithm_seconds=algorithm_seconds),source='tree_experiments.py')
            for target_kind,tau in targets:
                rr=dict(target_kind=target_kind,tau=tau,trees={},certificates={})
                for method in METHODS:
                    rr['trees'][method]=enumerate_threshold_tree(w,v,W,tau,method,
                        node_cap=node_cap,seconds_cap=tree_seconds)
                rr['certificates']['root_dual']=cheap_certificate(w,v,W,tau)
                rr['certificates']['simple']=cheap_certificate(w,v,W,tau,0)
                result['thresholds'].append(rr)
            for method in METHODS:
                incumbent=([row['original_incumbent_witness'][i] for i in row['core_original_indices']]
                           if row.get('original_incumbent_witness') is not None else None)
                alg=structural_optimize(w,v,W,method,node_cap=node_cap,seconds_cap=algorithm_seconds,
                                        incumbent_witness=incumbent)
                alg['audit_optimum_match']=(alg['lower']==optimum if alg['status']=='complete' else None)
                if row.get('original_weights') is not None:
                    reconstructed=None
                    if alg['status']=='complete' and alg['witness'] is not None:
                        reconstructed=[0]*len(row['original_weights'])
                        for i in row['fixed_in_indices']: reconstructed[i]=1
                        for bit,i in zip(alg['witness'],row['core_original_indices']):
                            reconstructed[i]=bit
                        orig_weight=sum(ww*bit for ww,bit in zip(row['original_weights'],reconstructed))
                        orig_value=sum(vv*bit for vv,bit in zip(row['original_values'],reconstructed))
                        fixed_ok=(all(reconstructed[i]==1 for i in row['fixed_in_indices']) and
                                  all(reconstructed[i]==0 for i in row['fixed_out_indices']))
                        valid=(orig_weight<=row['original_capacity'] and
                               orig_value==row['expected_original_optimum'] and fixed_ok)
                        alg['original_reconstruction_audit']=dict(witness=reconstructed,
                            weight=orig_weight,value=orig_value,fixed_assignments_valid=fixed_ok,
                            matches_original_optimum=orig_value==row['expected_original_optimum'],
                            capacity_feasible=orig_weight<=row['original_capacity'],valid=valid)
                    else:
                        alg['original_reconstruction_audit']=None
                result['algorithms'][method]=alg
            if row.get('original_weights') is not None:
                result['core_offset_audit']=(optimum+row['fixed_in_profit']==row['expected_original_optimum'])
                result['core_metadata']={k:row[k] for k in ['fixed_in_profit','core_original_indices','fixed_in_indices','fixed_out_indices','expected_original_optimum']}
            result['seconds']=time.perf_counter()-start
            handle.write(json.dumps(result)+'\n'); handle.flush()
            integrity_failure=(result.get('core_offset_audit') is False or
                any(a['status']=='complete' and (not a['audit_optimum_match'] or not a['witness_valid']
                    or (a.get('original_reconstruction_audit') is not None and
                        not a['original_reconstruction_audit']['valid'])) for a in result['algorithms'].values()))
            if integrity_failure:
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: completed optimum/witness reconstruction mismatch; failing row retained')
            if num%20==0 or subset=='pilot':
                print(subset,num+1,'/',len(selected),row['id'],round(result['seconds'],3),flush=True)
    print('Finished',subset,output,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['inputs','audit','pilot','full','independent','core'],default='pilot')
    parser.add_argument('--output')
    parser.add_argument('--registry',help='Existing immutable schema_version=1 registry with records list')
    args=parser.parse_args()
    registry=(json.loads(Path(args.registry).read_text(encoding='utf8')) if args.registry
              else make_independent_inputs() if args.mode=='independent' else make_inputs())
    if args.mode=='audit':
        audit(Path(args.output) if args.output else HERE/'tree_audit.json')
    elif args.mode in ('pilot','full','independent','core'):
        if args.mode=='core':
            snapshot=dict(created_by='tree_experiments.py before core run',
                          registry=str(args.registry),files={})
            for source in [Path(__file__),ROOT/'simulation/pruning_study_20261023/trees.py',Path(args.registry)]:
                snapshot['files'][str(source)]=hashlib.sha256(source.read_bytes()).hexdigest()
            manifest=HERE/('tree_core_v2_before_run_manifest.json' if args.output and 'v2' in args.output
                           else 'tree_core_before_run_manifest.json')
            if not manifest.exists(): manifest.write_text(json.dumps(snapshot,indent=2))
        run(registry,args.mode,Path(args.output) if args.output else HERE/f'trees_{args.mode}.jsonl')
