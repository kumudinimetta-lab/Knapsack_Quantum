"""Independent exhaustive tiny fixing audit; original code/data are read-only."""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'simulation'))
from exact_knapsack import reduced_cost_fixing,lp_bound
HERE=Path(__file__).resolve().parent

def lp_vertices(w,v,W,items):
    if W<0:return None
    best=Fraction(0)
    items=list(items)
    for mask in range(1<<len(items)):
        selected=[i for j,i in enumerate(items) if mask>>j&1]
        wt=sum(w[i] for i in selected)
        if wt>W:continue
        val=sum(v[i] for i in selected)
        best=max(best,Fraction(val))
        for j,i in enumerate(items):
            if not mask>>j&1:
                best=max(best,val+min(Fraction(W-wt,w[i]),Fraction(1))*v[i])
    return best

def one_case(w,v,W,category,seed=None):
    n=len(w)
    order=sorted(range(n),key=lambda i:Fraction(v[i],w[i]),reverse=True)
    rem=W;L=0;greedy=[]
    for i in order:
        if w[i]<=rem:rem-=w[i];L+=v[i];greedy.append(i)
    before=[];used=0
    for i in order:
        if used+w[i]>W:break
        before.append(i);used+=w[i]
    fi,core,fo=reduced_cost_fixing(n,w,v,W)
    failures=[];opposite=[];gfi=[];gfo=[];gc=[]
    for i in range(n):
        forced=0 if i in before else 1
        cap=W-forced*w[i]
        ref=lp_vertices(w,v,cap,[j for j in range(n) if j!=i])
        upper=None if ref is None else forced*v[i]+ref
        observed=lp_bound(w,v,cap,[j for j in range(n) if j!=i])
        if ref is None:
            if observed!=-float('inf'):failures.append(['lp_infeasible',i,str(observed)])
        elif observed!=ref:failures.append(['lp_value',i,str(observed),str(ref)])
        fixed=upper is None or upper<L
        (gfi if forced==0 else gfo).append(i) if fixed else gc.append(i)
        opposite.append({'item':i,'forced_opposite_bit':forced,'exact_upper':str(upper),
                         'strictly_below_L':fixed})
    if (fi,core,fo)!=(gfi,gc,gfo):failures.append(['fixing_partition',fi,core,fo,gfi,gc,gfo])
    if sorted(fi+core+fo)!=list(range(n)):failures.append(['partition_coverage'])
    if len(set(fi+core+fo))!=n:failures.append(['partition_duplicate'])
    original={x:sum(v[i] for i in range(n) if x>>i&1) for x in range(1<<n)
              if sum(w[i] for i in range(n) if x>>i&1)<=W}
    good={x for x,z in original.items() if z>=L}
    rc=W-sum(w[i] for i in fi);offset=sum(v[i] for i in fi)
    reconstruct={}
    for y in range(1<<len(core)):
        if sum(w[i] for j,i in enumerate(core) if y>>j&1)<=rc:
            x=sum(1<<i for i in fi)+sum(1<<i for j,i in enumerate(core) if y>>j&1)
            reconstruct[x]=offset+sum(v[i] for j,i in enumerate(core) if y>>j&1)
            if x not in original or reconstruct[x]!=original[x]:failures.append(['reconstruction',x,y])
    reconstructed_good={x for x,z in reconstruct.items() if z>=L}
    if good!=reconstructed_good:failures.append(['bijection',sorted(good),sorted(reconstructed_good)])
    for x in good:
        if any(not x>>i&1 for i in fi) or any(x>>i&1 for i in fo):failures.append(['lost_good',x])
    greedy_mask=sum(1<<i for i in greedy)
    if greedy_mask not in good or greedy_mask not in reconstructed_good:failures.append(['greedy_witness_lost'])
    opt=max(original.values())
    if max(reconstruct.values())!=opt:failures.append(['optimum_lost'])
    # Tiny-domain tests check every integer threshold; random larger cases use
    # all distinct attainable values and their successors, which partition all sets.
    thresholds=range(L,sum(v)+2) if category=='exhaustive_tiny' else sorted(
        {L,sum(v)+1,*[z for z in original.values() if z>=L],*[z+1 for z in original.values() if z+1>=L]})
    for tau in thresholds:
        if {x for x,z in original.items() if z>=tau}!={x for x,z in reconstruct.items() if z>=tau}:
            failures.append(['threshold_bijection',tau])
    below_lost=[x for x,z in original.items() if z<L and x not in reconstruct]
    return {'category':category,'seed':seed,'weights':w,'values':v,'capacity':W,
        'L':L,'greedy_mask':greedy_mask,'greedy_not_whole_LP_prefix':set(greedy)!=set(before),
        'root_whole_prefix':before,'fixed_in':fi,'core':core,'fixed_out':fo,
        'residual_capacity':rc,'value_offset':offset,'opposite_checks':opposite,
        'original_assignment_encodings':1<<n,'feasible_assignments':len(original),
        'good_original_assignments':len(good),'residual_assignment_encodings':1<<len(core),
        'thresholds_checked':len(thresholds),'optimum':opt,
        'below_L_lost_expected':len(below_lost),'below_L_example':below_lost[0] if below_lost else None,
        'failures':failures}

def main():
    started=time.perf_counter();path=HERE/'fixing_bijection_rows.jsonl'
    if path.exists():raise RuntimeError('Refuse to overwrite an existing audit output')
    summary={'scope':'Exact fixing preservation for every feasible assignment value>=greedy L',
      'taxonomy':{'reference_and_counts':'DERIVED exact enumeration','host_seconds':'MEASURED',
                  'input_domains_and_seeds':'HARDCODED'},
      'source_sha256':hashlib.sha256((ROOT/'simulation/exact_knapsack.py').read_bytes()).hexdigest(),
      'seed':2026102309,'counts':{},'first_failures':[]}
    totals={}
    def consume(w,v,W,category,seed=None):
        row=one_case(list(w),list(v),W,category,seed)
        handle.write(json.dumps(row)+'\n')
        counts=totals.setdefault(category,{'instances':0,'opposite_LP_checks':0,'original_encodings':0,
          'feasible_assignments':0,'good_assignments':0,'residual_encodings':0,'threshold_set_checks':0,
          'empty_core_cases':0,'all_fit_cases':0,'greedy_nonprefix_cases':0,'cases_with_below_L_losses':0,
          'failure_cases':0,'failure_count':0})
        counts['instances']+=1;counts['opposite_LP_checks']+=len(w)
        for dest,source in [('original_encodings','original_assignment_encodings'),('feasible_assignments','feasible_assignments'),
                            ('good_assignments','good_original_assignments'),('residual_encodings','residual_assignment_encodings'),
                            ('threshold_set_checks','thresholds_checked')]:counts[dest]+=row[source]
        counts['empty_core_cases']+=not row['core'];counts['all_fit_cases']+=W>=sum(w)
        counts['greedy_nonprefix_cases']+=row['greedy_not_whole_LP_prefix']
        counts['cases_with_below_L_losses']+=row['below_L_lost_expected']>0
        counts['failure_cases']+=bool(row['failures']);counts['failure_count']+=len(row['failures'])
        if row['failures'] and len(summary['first_failures'])<10:summary['first_failures'].append(row)
        if row['failures']:raise RuntimeError('RESEARCH_INTEGRITY_STOP: fixing or reconstruction mismatch; retained in rows')
    with path.open('x',encoding='utf-8') as handle:
        for n in range(4):
            for w in itertools.product(range(1,4),repeat=n):
                for v in itertools.product(range(1,4),repeat=n):
                    for W in range(sum(w)+2):consume(w,v,W,'exhaustive_tiny')
            print('completed exhaustive n',n,flush=True)
        adversarial=[([],[],0),([4,7,6],[5,6,2],7),([1,1],[1,1],1),
            ([6,5,2],[12,9,3],8),([10,1,1],[100,2,1],2),
            ([5,5,5],[5,5,5],9),([1,2,3],[4,5,6],6),([8,16],[16,8],16)]
        for w,v,W in adversarial:consume(w,v,W,'explicit_adversarial')
        rng=random.Random(summary['seed'])
        for trial in range(300):
            n=rng.randrange(0,9);magnitude=1009 if trial%3==0 else 19
            w=[rng.randrange(1,magnitude+1) for _ in range(n)]
            v=[rng.randrange(1,magnitude+1) for _ in range(n)]
            W=rng.randrange(0,sum(w)+3)
            consume(w,v,W,'seeded_random',summary['seed'])
        # Explicitly retained counterexamples to stronger unsupported statements.
        summary['rejected_claim_counterexamples']=[
          {'claim':'Fixing preserves all feasible assignments even below L',
           'weights':[1],'values':[1],'capacity':1,'L':1,'fixed_in':[0],
           'lost_assignment_at_tau0':0},
          {'claim':'Opposite upper<=L safely preserves all >=L assignments',
           'weights':[1,1],'values':[1,1],'capacity':1,'L':1,
           'opposite_upper':'1','good_assignments':[1,2],
           'reason':'Equality is attainable, so strict inequality cannot be replaced by nonstrict.'}]
    summary['counts']=totals;summary['host_seconds']=time.perf_counter()-started
    summary['source_unchanged']=summary['source_sha256']==hashlib.sha256((ROOT/'simulation/exact_knapsack.py').read_bytes()).hexdigest()
    summary['rows_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    (HERE/'fixing_bijection_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
