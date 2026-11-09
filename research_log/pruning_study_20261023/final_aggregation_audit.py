"""Independent reconstruction of final joins, overlays and descriptive ratios.

Read-only inputs; never imports or reruns analyze_paired.py and never rewrites its outputs.
"""
import collections
import copy
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
summary=load(HERE/'paired_summary.json');summary_hash=sha(HERE/'paired_summary.json')
failures=[]
def check(test,detail):
    if not test:failures.append(detail)
def number_equal(a,b):
    return a==b if a is None or b is None else math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
def stats(values):
    values=sorted(x for x in values if x is not None and math.isfinite(x))
    if not values:return {'n':0}
    return {'n':len(values),'minimum':values[0],'median':statistics.median(values),
            'q10':values[int(.1*(len(values)-1))],'q90':values[int(.9*(len(values)-1))],
            'maximum':values[-1],'below_one':sum(v<1-1e-12 for v in values),
            'equal_one':sum(abs(v-1)<=1e-12 for v in values),'above_one':sum(v>1+1e-12 for v in values)}
def compare_stats(actual,values,label):
    for k,v in stats(values).items():check(number_equal(actual.get(k),v),[label,k,actual.get(k),v])
for key,digest in summary['source_sha256'].items():
    check(sha(HERE/key)==digest,['summary_source_hash',key])

registry={}
for name in ['inputs.json','inputs_core700.json','inputs_stress_independent.json']:
    for record in load(HERE/name)['records']:
        check(record['id'] not in registry,['duplicate_registry_id',record['id']])
        registry[record['id']]=record
aliases=load(HERE/'core_resource_aliases.json')['records'];aliasmap={a['core_id']:a['resource_id'] for a in aliases}
for a in aliases:
    if a['core_id']!=a['resource_id']:
        check(all(registry[a['core_id']][k]==registry[a['resource_id']][k] for k in ['weights','values','capacity']),['bad_alias',a])
resources={};build_counts={};manifest_errors=[]
for run in summary['build_status']:
    folder=HERE/'runs'/run;manifest=load(folder/'manifest.json');rr=rows(folder/'resource_records.jsonl')
    expected={(i,m) for i in manifest['ids'] for m in manifest['methods']}
    observed={(r['id'],r['method']) for r in rr}
    check(len(rr)==len(observed) and observed==expected,['resource_keyset',run,len(rr),len(observed),len(expected)])
    bc=dict(collections.Counter(r['status'] for r in rr));build_counts[run]=bc
    check(bc==summary['build_status'][run]['status'],['build_status',run])
    check(manifest['module_sha256']==sha(ROOT/'simulation/pruning_study_20261023/circuits.py'),['manifest_circuit_source',run])
    for rel,digest in manifest['dependency_sha256'].items():check(sha(ROOT/rel)==digest,['manifest_dependency',run,rel])
    for r in rr:
        key=(r['id'],r['method']);check(key not in resources,['duplicate_resource_key',key]);resources[key]=r
        check(r['module_sha256']==manifest['module_sha256'],['resource_source_hash',run,key])
        if r['status']=='build_cap':check('qubit' in r['reason'],['unexpected_cap_reason',key,r['reason']])
check(len(resources)==summary['total_build_records']==summary['expected_build_records'],['total_resources',len(resources)])

trees=[]
for name in ['trees_full.jsonl','trees_core_v3.jsonl','trees_independent_v2.jsonl']:
    rr=rows(HERE/name);check(len(rr)==len({r['id'] for r in rr}),['duplicate_tree_id',name]);trees+=rr
index={r['id']:r for r in trees};check(len(trees)==len(index),['duplicate_global_tree_id'])
check(dict(collections.Counter(r['category'] for r in trees))==summary['tree_panels'],['tree_panel_counts'])
timekeys={(r['id'],condition['target_kind'],method) for r in trees for condition in r['thresholds']
          for method,t in condition['trees'].items() if t['cap_reason']=='time_cap'}
overlays=rows(HERE/'trees_timecap_reruns.jsonl')
overlaykeys={(r['id'],r['target_kind'],r['method']) for r in overlays}
check(len(overlays)==len(overlaykeys)==len(timekeys)==183,['overlay_counts',len(overlays),len(overlaykeys),len(timekeys)])
check(overlaykeys==timekeys,['overlay_target_set'])
initial_algorithms={r['id']:copy.deepcopy(r['algorithms']) for r in trees}
newcomplete=0
for o in overlays:
    r=index[o['id']];condition=next(t for t in r['thresholds'] if t['target_kind']==o['target_kind'])
    old=condition['trees'][o['method']]
    check(old==o['old_status'] and condition['tau']==o['tau'] and not o['conflict'],['overlay_old_or_tau',o['key']])
    check(o['newtree']['node_cap']==old['node_cap']==50000 and o['newtree']['seconds_cap']==5.0,['overlay_budget',o['key']])
    check(o['newtree']['nodes']>=old['nodes'],['overlay_prefix_count',o['key']])
    for p,digest in o['source_hashes'].items():check(sha(HERE/p)==digest,['overlay_source',o['key'],p])
    for p,digest in o['code_hashes'].items():check(sha(Path(p))==digest,['overlay_code',o['key'],p])
    newcomplete+=o['newtree']['complete'];condition['trees'][o['method']]=o['newtree']
check(newcomplete==23,['overlay_completed_count',newcomplete])
for r in trees:check(initial_algorithms[r['id']]==r['algorithms'],['algorithm_mutated_by_overlay',r['id']])

def resource(ident,method):return resources.get((aliasmap.get(ident,ident),method))
def cost(r,metric):return r['resources']['gate_counts']['ccx'] if metric=='ccx' else r['resources'][metric]
def div(x,y):return x/y if y else (1.0 if not x else None)
resource_values=collections.defaultdict(list);proxy_values=collections.defaultdict(list)
coverage=collections.defaultdict(collections.Counter);cert_values=collections.defaultdict(list)
tree_counts=collections.defaultdict(lambda:collections.defaultdict(collections.Counter));examples=[]
comparisons=[('exact_single','fixedpoint_single'),('exact_wrapper','fixedpoint_wrapper'),
             ('exact_single','exact_wrapper'),('root_dual','exact_single'),('bank2','exact_single'),
             ('bank4','exact_single'),('simple','exact_single')]
for r in trees:
    ident,cat=r['id'],r['category']
    check(len(r['thresholds'])==2 and {x['target_kind'] for x in r['thresholds']}=={'incumbent_plus_one','optimum_plus_one'},['target_keys',ident])
    for a,b in comparisons:
        ra,rb=resource(ident,a),resource(ident,b)
        if ra and rb and ra['status']==rb['status']=='complete':
            for metric in ['ccx','gates','gate_depth','qubits']:
                value=div(cost(ra,metric),cost(rb,metric))
                for group in ['ALL',r['instance_class'],'n='+str(r['n'])]:resource_values[(cat,group,a+'/'+b,metric)].append(value)
    for method,algorithm in r['algorithms'].items():
        tc=tree_counts[cat][method];tc['algorithm_'+algorithm['status']]+=1
        if algorithm['status']=='complete' and not algorithm['calls']:tc['classically_resolved_no_detection_calls']+=1
        if algorithm['status']=='complete':tc['completed_value_or_witness_mismatches']+=int(not algorithm['audit_optimum_match'] or not algorithm['witness_valid'])
    for condition in r['thresholds']:
        for method,t in condition['trees'].items():
            tc=tree_counts[cat][method];tc['trees_complete' if t['complete'] else 'trees_capped']+=1
            if not t['complete']:tc['cap_'+str(t['cap_reason'])]+=1
            if t['complete'] and t['nodes']==1:tc['root_rejected']+=1
            cert=condition['certificates']['simple' if method=='simple' else 'root_dual']['bound']
            check(t['nodes']<=cert,['certificate_failure',ident,condition['target_kind'],method])
            if t['complete']:cert_values[(cat,method)].append(cert/t['nodes'])
        for weak in ['simple','root_dual','bank2','bank4']:
            tw,ts=condition['trees'][weak],condition['trees']['exact_lp'];rw,rs=resource(ident,weak),resource(ident,'exact_single')
            resolved=all(a['status']=='complete' and not a['calls'] for a in r['algorithms'].values())
            trivial=tw['complete'] and ts['complete'] and tw['nodes']==ts['nodes']==1
            for metric in ['ccx','gates','gate_depth']:
                key=(cat,weak,metric,condition['target_kind'])
                state=('resource_missing_or_capped' if not rw or not rs or rw['status']!='complete' or rs['status']!='complete'
                       else 'tree_capped' if not tw['complete'] or not ts['complete'] else 'complete')
                coverage[key][state]+=1
                if state!='complete':continue
                check(tw['nodes']>=ts['nodes'],['tree_hierarchy',ident,weak])
                cw,cs=cost(rw,metric),cost(rs,metric)
                for factor in [0,.25,1,10,100]:
                    # Algebraically independent of the root's two sqrt products.
                    value=div(cw+factor*cs,cs*(1+factor))*math.sqrt(tw['nodes']/ts['nodes'])
                    subsets=['all_complete']+([] if trivial else ['nontrivial_complete'])+([] if trivial or resolved else ['requires_detection_complete'])
                    for subset in subsets:
                        for group in ['ALL',r['instance_class']]:proxy_values[(cat,group,weak,metric,condition['target_kind'],subset,factor)].append(value)
                    if factor in [0,1,100] and metric=='ccx' and weak=='root_dual' and len(examples)<12:
                        examples.append({'id':ident,'target':condition['target_kind'],'weak':weak,'metric':metric,
                            'Cweak':cw,'Cexact':cs,'Tweak':tw['nodes'],'Texact':ts['nodes'],'overhead_exact_cost_units':factor,'ratio':value})
for r in summary['resource_pairs']:
    k=(r['category'],r['group'],r['comparison'],r['metric']);compare_stats(r,resource_values.pop(k,[]),['resource_stats',k])
check(not resource_values,['missing_resource_summary_groups',len(resource_values)])
for r in summary['proxy_pairs']:
    k=(r['category'],r['group'],r['weak'],r['metric'],r['target_kind'],r['subset'],r['overhead_exact_cost_units']);compare_stats(r,proxy_values.pop(k,[]),['proxy_stats',k])
check(not proxy_values,['missing_proxy_summary_groups',len(proxy_values)])
for r in summary['proxy_coverage']:
    k=(r['category'],r['weak'],r['metric'],r['target_kind']);expected=dict(coverage.pop(k,{}))
    check({x:v for x,v in r.items() if x not in ['category','weak','metric','target_kind']}==expected,['coverage',k])
check(not coverage,['missing_proxy_coverage',len(coverage)])
for r in summary['certificate_to_observed_tree']:
    k=(r['category'],r['method']);compare_stats(r,cert_values.pop(k,[]),['certificate_stats',k])
check(not cert_values,['missing_certificate_stats',len(cert_values)])
for cat,ms in tree_counts.items():
    for method,counts in ms.items():check(dict(counts)==summary['tree_summary'][cat][method],['tree_summary',cat,method])
check(sha(HERE/'paired_summary.json')==summary_hash,['summary_changed_during_audit'])
result={'date':'2026-10-24','scope':'Independent read-only reconstruction of final aggregation; no quantum execution',
 'taxonomy':'DERIVED ledger/hash/ratio verification','paired_summary_sha256':summary_hash,
 'resource_attempts':len(resources),'build_status':build_counts,'tree_inputs':len(trees),
 'timecap_overlay_keys':len(overlays),'extra_completed_threshold_conditions':newcomplete,
 'summary_source_hashes_checked':len(summary['source_sha256']),
 'resource_stat_groups_checked':len(summary['resource_pairs']),'proxy_stat_groups_checked':len(summary['proxy_pairs']),
 'coverage_groups_checked':len(summary['proxy_coverage']),'certificate_stat_groups_checked':len(summary['certificate_to_observed_tree']),
 'resource_aliases':len(aliases),'reused_original_resources':sum(a['core_id']!=a['resource_id'] for a in aliases),
 'recomputed_ratio_examples':examples,'failure_count':len(failures),'failures':failures}
dest=HERE/'final_aggregation_audit_result.json';dest.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['recomputed_ratio_examples','failures']},indent=2))
if failures:print(json.dumps(failures[:12],indent=2));raise RuntimeError('RESEARCH_INTEGRITY_STOP: final aggregation audit mismatch')
