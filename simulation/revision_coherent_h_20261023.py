"""Exact all-input sparse-statevector checks including coherent depth dispatch."""
import json
from pathlib import Path
from oracle_h.node_bound_reversible import build_coherent_node_bound,exact_node_bound


def main():
    rows=[]
    for w,v,cap in [([2,3,4,5],[3,4,5,8],8),([3,5,7,8],[3,5,7,8],13),
                     ([4,7,6],[5,6,2],7)]:
        circuit=build_coherent_node_bound(w,v,cap)
        m,db=len(w),circuit.depth_register_bits
        inputs=range(1<<circuit.num_inputs)
        bad=dirty=0
        for target in [0,1]:
            flags,garbage=circuit.simulate_columns(inputs,target)
            dirty+=garbage
            for p,f in enumerate(flags):
                prefix=p&((1<<m)-1)
                depth=(p>>m)&((1<<db)-1)
                threshold=p>>(m+db)
                exact=None if depth>m else exact_node_bound(w,v,cap,depth,prefix)
                expected=target^int(exact is None or exact<threshold)
                bad+=f!=expected
        rows.append({'weights':w,'values':v,'capacity':cap,'k':circuit.k,
                     'depth_register_bits':db,'threshold_bits':circuit.threshold_bits,
                     'statevector_columns':2*len(inputs),'predicate_mismatches':bad,
                     'dirty_columns':dirty,**circuit.resources()})
    out={'classification':'SIMULATED_EXACT_SPARSE_STATEVECTOR',
         'scope':'All prefix, depth, threshold and target input encodings on three listed instances; clean initial workspace.',
         'rows':rows}
    p=Path(__file__).resolve().parents[1]/'research_log/revision_20261023_coherent_h_results.json'
    p.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    assert all(r['predicate_mismatches']==r['dirty_columns']==0 for r in rows)


if __name__=='__main__':
    main()
