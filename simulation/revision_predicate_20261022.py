"""Dense statevector verification of the existing threshold phase oracle."""
import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from knapsack_oracle import build_knapsack_oracle,oracle_marked_set


def main():
    w,v,cap=[2,3,4,5],[3,4,5,8],8
    rows=[]
    for tau in range(sum(v)+2):
        oracle,_=build_knapsack_oracle(w,v,cap,tau)
        qc=QuantumCircuit(oracle.num_qubits)
        qc.h(range(len(w)))
        state=Statevector.from_instruction(qc.compose(oracle)).data
        expected=np.zeros_like(state)
        marked=set(oracle_marked_set(w,v,cap,tau))
        for x in range(1<<len(w)):
            expected[x]=(-1 if x in marked else 1)/np.sqrt(1<<len(w))
        error=float(np.max(np.abs(state-expected)))
        flat=oracle.decompose(reps=3)
        rows.append({'tau':tau,'qubits':oracle.num_qubits,'gates':len(flat.data),
                     'depth':flat.depth(),'gate_counts':dict(flat.count_ops()),
                     'max_amplitude_error':error,'mismatch':error>1e-10,
                     'workspace_leakage':float(np.sum(np.abs(state[1<<len(w):])**2))})
    out={'classification':'SIMULATED_DENSE_STATEVECTOR_WITH_DERIVED_GATE_COUNTS',
         'weights':w,'values':v,'capacity':cap,'thresholds':len(rows),
         'selection_basis_states_per_threshold':16,
         'mismatches':sum(r['mismatch'] for r in rows),'rows':rows}
    p=Path(__file__).resolve().parents[1]/'research_log/revision_20261022_predicate_results.json'
    p.write_text(json.dumps(out,indent=2))
    print('SIMULATED',len(rows),'thresholds; mismatches',out['mismatches'],flush=True)


if __name__=='__main__':
    main()
