"""Paired descriptive analyses. No regression of a model on its own inputs."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
RUNS=['main_single_v1','representative_wrappers_v1','core_changed_single_v1',
      'core_changed_wrappers_v1','independent_single_v1','scaled_single_v1']
METRICS=['ccx','gates','gate_depth','qubits']
METHODS=['simple','root_dual','bank2','bank4','exact_lp']

def lines(path):
    with path.open(encoding='utf8') as handle:
        for line in handle:
            if line.strip(): yield json.loads(line)

def descriptive(values):
    values=sorted(v for v in values if v is not None and math.isfinite(v))
    if not values: return dict(n=0)
    return dict(n=len(values),minimum=values[0],q10=values[int(.1*(len(values)-1))],
        median=statistics.median(values),q90=values[int(.9*(len(values)-1))],maximum=values[-1],
        below_one=sum(v<1-1e-12 for v in values),equal_one=sum(abs(v-1)<=1e-12 for v in values),
        above_one=sum(v>1+1e-12 for v in values))

def cost(resource,metric):
    r=resource['resources']
    return r['gate_counts']['ccx'] if metric=='ccx' else r[metric]

def ratio(a,b):
    return a/b if b else (1.0 if not a else None)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--allow-partial',action='store_true')
    args=parser.parse_args()
    resources={};build_status={};source_files=[]
    expected=0
    for name in RUNS:
        folder=HERE/'runs'/name;manifest=json.loads((folder/'manifest.json').read_text())
        path=folder/'resource_records.jsonl';source_files.extend([path,folder/'manifest.json'])
        rows=list(lines(path));expected+=len(manifest['ids'])*len(manifest['methods'])
        if not args.allow_partial and len(rows)!=len(manifest['ids'])*len(manifest['methods']):
            raise RuntimeError('Resource run incomplete: '+name)
        build_status[name]=dict(expected=len(manifest['ids'])*len(manifest['methods']),
            observed=len(rows),status=dict(Counter(r['status'] for r in rows)))
        for row in rows:
            key=(row['id'],row['method'])
            if key in resources: raise RuntimeError('Duplicate resource key')
            resources[key]=row
    aliases={r['core_id']:r['resource_id'] for r in json.loads((HERE/'core_resource_aliases.json').read_text())['records']}
    source_files.extend([HERE/'core_resource_aliases.json',Path(__file__).resolve()])
    trees=[]
    for name in ['trees_full.jsonl','trees_core_v3.jsonl','trees_independent_v2.jsonl']:
        path=HERE/name
        if path.exists(): trees.extend(lines(path));source_files.append(path)
    initial_fixed_status=defaultdict(Counter)
    tree_index={r['id']:r for r in trees}
    for tree in trees:
        for condition in tree['thresholds']:
            for method,t in condition['trees'].items():
                initial_fixed_status[(tree['category'],method)]['complete' if t['complete'] else str(t['cap_reason'])]+=1
    overlay_path=HERE/'trees_timecap_reruns.jsonl'
    overlays=list(lines(overlay_path)) if overlay_path.exists() else []
    if not args.allow_partial and len(overlays)!=183:
        raise RuntimeError('Time-cap reruns incomplete')
    if overlay_path.exists(): source_files.append(overlay_path)
    for row in overlays:
        tree=tree_index[row['id']]
        condition=next(t for t in tree['thresholds'] if t['target_kind']==row['target_kind'])
        old=condition['trees'][row['method']]
        if old!=row['old_status'] or condition['tau']!=row['tau'] or row['conflict']:
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: rerun overlay mismatch')
        condition['trees'][row['method']]=row['newtree']
    counts=Counter(r['category'] for r in trees)
    if not args.allow_partial and counts!=Counter(main700=700,core700=700,highbit_scaled=15,independent_large=45):
        raise RuntimeError('Tree panels incomplete: '+str(counts))
    registry={}
    for name in ['inputs.json','inputs_core700.json','inputs_stress_independent.json']:
        path=HERE/name;source_files.append(path)
        registry.update({r['id']:r for r in json.loads(path.read_text(encoding='utf8'))['records']})
    def get_resource(ident,method): return resources.get((aliases.get(ident,ident),method))
    circuit_pairs=defaultdict(list)
    resource_rows=[]
    comparisons=[('exact_single','fixedpoint_single'),('exact_wrapper','fixedpoint_wrapper'),
                 ('exact_single','exact_wrapper'),('root_dual','exact_single'),
                 ('bank2','exact_single'),('bank4','exact_single'),('simple','exact_single')]
    for tree in trees:
        if len(tree['thresholds'])!=2 or len({c['target_kind'] for c in tree['thresholds']})!=2:
            raise RuntimeError('Threshold condition count conflict')
        ident,category=tree['id'],tree['category']
        for a,b in comparisons:
            ra,rb=get_resource(ident,a),get_resource(ident,b)
            for metric in METRICS:
                status='complete' if ra and rb and ra['status']==rb['status']=='complete' else 'missing_or_capped'
                if status!='complete' and ('wrapper' in a or 'wrapper' in b) and registry[ident].get('trial',999)>=3:
                    status='not_scheduled_representative_panel'
                value=ratio(cost(ra,metric),cost(rb,metric)) if status=='complete' else None
                rr=dict(id=ident,category=category,instance_class=tree['instance_class'],n=tree['n'],
                    comparison=a+'/'+b,metric=metric,status=status,ratio=value,classification='DERIVED')
                resource_rows.append(rr)
                if status=='complete':
                    for group in ['ALL',tree['instance_class'],'n='+str(tree['n'])]:
                        circuit_pairs[(category,group,a+'/'+b,metric)].append(value)
    conditions=[];proxy_groups=defaultdict(list);coverage=defaultdict(Counter)
    tree_summary=defaultdict(lambda:defaultdict(Counter))
    certificate_ratios=defaultdict(list)
    for tree in trees:
        ident,cat=tree['id'],tree['category']
        for method,alg in tree['algorithms'].items():
            acc=tree_summary[cat][method]
            acc['algorithm_'+alg['status']]+=1
            if alg['status']=='complete' and not alg['calls']: acc['classically_resolved_no_detection_calls']+=1
            if alg['status']=='complete':
                acc['completed_value_or_witness_mismatches']+=int(not alg['audit_optimum_match'] or not alg['witness_valid'])
        for condition in tree['thresholds']:
            for method,t in condition['trees'].items():
                acc=tree_summary[cat][method]
                acc['trees_complete' if t['complete'] else 'trees_capped']+=1
                if not t['complete']: acc['cap_'+str(t['cap_reason'])]+=1
                if t['complete'] and t['nodes']==1: acc['root_rejected']+=1
                cert=condition['certificates']['simple' if method=='simple' else 'root_dual']['bound']
                if t['nodes']>cert:
                    raise RuntimeError('RESEARCH_INTEGRITY_STOP: tree count above certificate')
                if t['complete']: certificate_ratios[(cat,method)].append(cert/t['nodes'])
            for weak in ['simple','root_dual','bank2','bank4']:
                tw,ts=condition['trees'][weak],condition['trees']['exact_lp']
                rw,rs=get_resource(ident,weak),get_resource(ident,'exact_single')
                for metric in ['ccx','gates','gate_depth']:
                    key=(cat,weak,metric,condition['target_kind'])
                    status=('resource_missing_or_capped' if not rw or not rs or rw['status']!='complete' or rs['status']!='complete'
                            else 'tree_capped' if not tw['complete'] or not ts['complete'] else 'complete')
                    trivial=tw['complete'] and ts['complete'] and tw['nodes']==ts['nodes']==1
                    resolved=all(a['status']=='complete' and not a['calls'] for a in tree['algorithms'].values())
                    out=dict(id=ident,category=cat,instance_class=tree['instance_class'],n=tree['n'],
                        target_kind=condition['target_kind'],tau=condition['tau'],weak=weak,metric=metric,status=status,
                        weak_nodes_processed=tw['nodes'],exact_nodes_processed=ts['nodes'],weak_tree_complete=tw['complete'],
                        exact_tree_complete=ts['complete'],both_root_rejected=trivial,classification='DERIVED conditional work proxy; tree counts MEASURED')
                    out['classically_resolved_without_detection']=resolved
                    coverage[key][status]+=1
                    if status=='complete':
                        if tw['nodes']<ts['nodes']:
                            raise RuntimeError('RESEARCH_INTEGRITY_STOP: weaker tree smaller than exact LP tree')
                        cw,cs=cost(rw,metric),cost(rs,metric)
                        out.update(weak_cost=cw,exact_cost=cs,tree_ratio=tw['nodes']/ts['nodes'])
                        for factor in [0,.25,1,10,100]:
                            h=factor*cs
                            value=ratio((cw+h)*math.sqrt(tw['nodes']),(cs+h)*math.sqrt(ts['nodes']))
                            out['proxy_ratio_h_'+str(factor)]=value
                            for subset in ['all_complete']+([] if trivial else ['nontrivial_complete'])+([] if trivial or resolved else ['requires_detection_complete']):
                                for group in ['ALL',tree['instance_class']]:
                                    proxy_groups[(cat,group,weak,metric,condition['target_kind'],subset,factor)].append(value)
                        # Break-even shared overhead is algebraic, not a physical estimate.
                        r=math.sqrt(ts['nodes']/tw['nodes'])
                        out['h_limit_in_exact_cost_units']=(max(0,(r*cs-cw)/(1-r))/cs if r<1 and cs else None)
                        out['cheaper_for_all_nonnegative_h']=(tw['nodes']==ts['nodes'] and cw<cs)
                    conditions.append(out)
    suffix='_partial' if args.allow_partial else ''
    def write_csv(name,rows):
        path=HERE/(name+suffix+'.csv');fields=list(dict.fromkeys(k for r in rows for k in r))
        with path.open('w',encoding='utf8',newline='') as h:
            writer=csv.DictWriter(h,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    write_csv('paired_resource_rows',resource_rows);write_csv('paired_condition_rows',conditions)
    result=dict(scope='Descriptive paired offline resources and CLASSICAL tree sizes. Proxy ratios are not measured quantum runtime or speedup.',
        initial_fixed_tree_status=[dict(category=k[0],method=k[1],**dict(v)) for k,v in sorted(initial_fixed_status.items())],
        timecap_rerun_overlays=len(overlays),
        build_status=build_status,total_build_records=len(resources),expected_build_records=expected,
        tree_panels=dict(counts),tree_summary={cat:{m:dict(c) for m,c in methods.items()} for cat,methods in tree_summary.items()},
        resource_pairs=[dict(category=k[0],group=k[1],comparison=k[2],metric=k[3],**descriptive(v)) for k,v in sorted(circuit_pairs.items())],
        proxy_pairs=[dict(category=k[0],group=k[1],weak=k[2],metric=k[3],target_kind=k[4],subset=k[5],overhead_exact_cost_units=k[6],**descriptive(v)) for k,v in sorted(proxy_groups.items())],
        proxy_coverage=[dict(category=k[0],weak=k[1],metric=k[2],target_kind=k[3],**dict(v)) for k,v in sorted(coverage.items())],
        certificate_to_observed_tree=[dict(category=k[0],method=k[1],**descriptive(v)) for k,v in sorted(certificate_ratios.items())],
        source_sha256={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        taxonomy={'compiled_resources':'DERIVED','tree_counts_and_caps':'MEASURED classical','proxy_statistics':'DERIVED','overhead_settings':'HARDCODED'},
        limitations=['Complete-pair ratios exclude capped trees/builds; coverage separately retained.',
            'Two thresholds on one input are not independent instances; targets summarized separately.',
            'Root-rejected conditions separately identified, not silently removed.',
            'Common reflection/branching overhead is varied, not implemented.',
            'Out-of-place compiler gate lists are upper constructions, not lower bounds or best known circuits.',
            'Actual-T proxies do not assume T is freely known for a quantum algorithm.',
            'Qubits, gate depth and CCX counts are separate units; no physical/classical runtime crossover.',
            'Static leaf-only fixed-order trees are not optimized classical BnB/COMBO trees.',
            'Leaf marking and complete walk/reflection costs are outside the compiled prune-predicate resources.'])
    (HERE/('paired_summary'+suffix+'.json')).write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(dict(build_status=build_status,tree_panels=dict(counts)),indent=2))

if __name__=='__main__':main()
