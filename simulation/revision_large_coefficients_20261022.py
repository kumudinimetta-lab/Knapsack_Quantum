"""Large-coefficient comparison with independent exact meet-in-the-middle."""
from bisect import bisect_right
import json
from pathlib import Path
import time
import ortools
from ortools.algorithms.python import knapsack_solver
from exact_knapsack import reduced_cost_fixing,branch_and_bound
from revision_audit_20261022 import GENERATORS,ROOT


def meet_in_the_middle(w,v,capacity):
    middle=len(w)//2
    halves=[]
    for indices in [range(middle),range(middle,len(w))]:
        pairs=[(0,0)]
        for i in indices:
            pairs += [(ww+w[i],vv+v[i]) for ww,vv in pairs if ww+w[i]<=capacity]
        halves.append(pairs)
    right=sorted(halves[1])
    weights=[r[0] for r in right]
    best=[]
    current=0
    for _,value in right:
        current=max(current,value);best.append(current)
    return max(vv+best[bisect_right(weights,capacity-ww)-1] for ww,vv in halves[0])


def main():
    records=[]
    for gen in GENERATORS:
        for n in [20,24,28]:
            for trial in range(3):
                seed=20261022+n*100+trial
                w,v,cap,kind=gen(n,seed=seed,R=1000000)
                start=time.perf_counter()
                exact=meet_in_the_middle(w,v,cap)
                mitm_time=time.perf_counter()-start
                solver=knapsack_solver.KnapsackSolver(
                    knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,'audit')
                solver.set_time_limit(1.0)
                solver.init(v,[w],[cap])
                start=time.perf_counter();ov=solver.solve();ot=time.perf_counter()-start
                start=time.perf_counter()
                fi,core,fo=reduced_cost_fixing(n,w,v,cap)
                residual=cap-sum(w[i] for i in fi)
                cv,nodes,pruned,depth,capped=branch_and_bound(
                    [w[i] for i in core],[v[i] for i in core],residual,max_nodes=100000)
                ours=sum(v[i] for i in fi)+cv
                bt=time.perf_counter()-start
                records.append({'class':kind,'n':n,'trial':trial,'seed':seed,
                    'weights':w,'values':v,'capacity':cap,'m':len(core),
                    'mitm_optimum':exact,'mitm_seconds':mitm_time,
                    'or_value':ov,'or_certified':bool(solver.is_solution_optimal()),'or_seconds':ot,
                    'bb_value':ours,'bb_nodes':nodes,'bb_capped':capped,'bb_seconds':bt,
                    'bb_mismatch':not capped and ours!=exact,
                    'or_mismatch':solver.is_solution_optimal() and ov!=exact})
        print('MEASURED large-coefficient cases:',kind,flush=True)
    summary={'attempted':len(records),'bb_capped':sum(r['bb_capped'] for r in records),
             'or_cutoff':sum(not r['or_certified'] for r in records),
             'bb_mismatches':sum(r['bb_mismatch'] for r in records),
             'or_mismatches':sum(r['or_mismatch'] for r in records)}
    out={'classification':'MEASURED_CLASSICAL','manifest':{'R':1000000,'n':[20,24,28],
         'trials':3,'seed':'20261022+100*n+trial','or_time_limit_seconds':1,
         'bb_node_cap':100000,'ortools_version':ortools.__version__},
         'summary':summary,'records':records}
    (ROOT/'research_log/revision_20261022_large_coefficients_results.json').write_text(json.dumps(out,indent=2))
    print(summary,flush=True)


if __name__=='__main__':
    main()
