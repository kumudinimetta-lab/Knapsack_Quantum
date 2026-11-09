"""Fresh orthogonal-Schur spectral audit; never overwrites archived data."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.linalg import schur
from scipy.stats import binom, beta

from exact_knapsack import reduced_cost_fixing, dynamic_programming
from quantum_backtracking import (build_threshold_tree, build_walk_operator,
                                  efficiency_order, detection_accept_prob, _fejer_at_zero)
from revision_audit_20261022 import GENERATORS, ROOT


def spectral_measure(walk):
    triangular, basis = schur(walk.toarray(), output="real", check_finite=False)
    phases, weights = [], []
    i = 0
    while i < len(triangular):
        if i + 1 < len(triangular) and abs(triangular[i+1, i]) > 1e-12:
            angle = math.acos(float(np.clip((triangular[i,i]+triangular[i+1,i+1])/2,-1,1)))
            weight = float(basis[0,i]**2 + basis[0,i+1]**2)
            phases.extend([angle,-angle])
            weights.extend([weight/2,weight/2])
            i += 2
        else:
            phases.append(0.0 if triangular[i,i] > 0 else math.pi)
            weights.append(float(basis[0,i]**2))
            i += 1
    return np.array(phases), np.array(weights)


def main():
    records=[]
    start=time.perf_counter()
    for gen in GENERATORS:
        for n in [8,10,12,14,16,18]:
            for trial in range(20):
                seed=n*1000+trial
                # Match the original spectral benchmark's R=50, rather than
                # the distinct R=100 classical/oracle benchmark.
                w,v,cap,kind=gen(n,seed=seed,R=50)
                fi,core,fo=reduced_cost_fixing(n,w,v,cap)
                residual=cap-sum(w[i] for i in fi)
                cw,cv=[w[i] for i in core],[v[i] for i in core]
                opt=dynamic_programming(cw,cv,residual)
                m=len(core)
                for label,tau in [('marked',opt),('unmarked',opt+1)]:
                    r={'class':kind,'n':n,'seed':seed,'m':m,'case_type':label,'tau':tau}
                    if m==0:
                        r['status']='EMPTY_CORE_SEED'
                        records.append(r)
                        continue
                    tree=build_threshold_tree(cw,cv,residual,tau,efficiency_order(cw,cv),max_nodes=2000)
                    if tree is None:
                        r['status']='TREE_CAP'
                        records.append(r)
                        continue
                    r['T']=tree.size
                    r['marked']=any(tree.marked)
                    if tree.size==1:
                        r['status']='IMMEDIATELY_PRUNED' if not tree.marked[0] else 'MARKED_ROOT'
                        records.append(r)
                        continue
                    walk=build_walk_operator(tree,m)
                    try:
                        phases,weights=spectral_measure(walk)
                        s=max(1,math.ceil(math.log2(2*math.sqrt(tree.size*m)+1)))
                        p=float(sum(a*_fejer_at_zero(phi,s) for phi,a in zip(phases,weights)))
                        # Independent direct sparse iteration, not an eigenvector formula.
                        direct=detection_accept_prob(walk,0,s)
                        w0=float(sum(weights[np.abs(phases)<=1e-10]))
                        r.update(s=s,p_accept=p,direct_accept=direct,
                                 accept_difference=abs(p-direct),weight_sum=float(sum(weights)),w0=w0)
                        p_majority=float(binom.sf(math.ceil(3*11/8)-1,11,p))
                        r['agreement']=(p_majority>=0.5)==r['marked']
                        if r['marked']:
                            r['endpoint_valid']=w0>=0.5-1e-8
                        else:
                            endpoints=[]
                            for c in [0.125,0.25,0.5,1,2]:
                                phi=c/math.sqrt(tree.size*m)
                                mu=float(sum(weights[np.abs(phases)<=phi]))
                                bound=phi*phi*tree.size*m/4
                                endpoints.append({'c':c,'mu':mu,'bound':bound,'valid':mu<=bound+1e-10})
                            r['effective_gap_checks']=endpoints
                            r['endpoint_valid']=all(x['valid'] for x in endpoints)
                        r['status']='COMPLETED'
                    except (np.linalg.LinAlgError,ValueError) as exc:
                        r['status']='NUMERICAL_FAILURE'
                        r['error']=str(exc)
                    records.append(r)
            print('SIMULATED Schur audit:',kind,n,'conditions',len(records),flush=True)
    complete=[r for r in records if r['status']=='COMPLETED']
    summary={'conditions':len(records),'completed':len(complete),
             'counts':{str(k):v for k,v in Counter((r['status'],r['case_type']) for r in records).items()},
             'predicate_disagreements':sum(not r['agreement'] for r in complete),
             'endpoint_violations':sum(not r['endpoint_valid'] for r in complete),
             'max_accept_difference':max(r['accept_difference'] for r in complete),
             'max_normalization_error':max(abs(r['weight_sum']-1) for r in complete)}
    out={'classification':'SIMULATED','manifest':{'n':[8,10,12,14,16,18],
         'trials':20,'seed':'1000*n+trial','max_nodes':2000,'pe_constant':2,'K':11,
         'spectral_method':'orthogonal real Schur','date':'2026-10-23',
         'coefficient_range_R':50,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
         'summary':summary,'elapsed_seconds':time.perf_counter()-start,'records':records}
    path=ROOT/'research_log/revision_20261022_spectral_results.json'
    path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    main()
