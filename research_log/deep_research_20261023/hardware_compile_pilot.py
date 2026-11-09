"""Bounded offline feasibility audit. Never accesses IBM accounts or submits jobs."""
import ast
import hashlib
import json
import math
from pathlib import Path
import sys
import traceback
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore', category=DeprecationWarning)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'simulation'))
from exact_knapsack import efficiency_order, reduced_cost_fixing
from knapsack_oracle import build_knapsack_oracle, oracle_marked_set
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
import qiskit

source = ROOT / 'simulation/run_ibm_hardware.py'
tree = ast.parse(source.read_text(encoding='utf-8'))
instances = next(ast.literal_eval(node.value) for node in tree.body
                 if isinstance(node, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'INSTANCES'
                         for t in node.targets))

def greedy(w, v, capacity):
    rem, val = capacity, 0
    for i in efficiency_order(w, v):
        if w[i] <= rem:
            rem -= w[i]
            val += v[i]
    return val

def diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    if n == 1:
        qc.z(0)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

def original_mask(y, fi, core):
    return sum(1 << i for i in fi) + sum(1 << i for j, i in enumerate(core)
                                        if (y >> j) & 1)

out = {
    'date': '2026-10-23', 'qiskit_version': qiskit.__version__,
    'scope': 'Offline static compilation of one threshold Grover iteration; no hardware jobs',
    'metric_labels': {
        'inputs': 'HARDCODED', 'exact_enumeration': 'DERIVED',
        'ideal_grover_success': 'DERIVED', 'compiler_resources': 'DERIVED',
        'measured_hardware_quantities': None},
    'runner_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'oracle_sha256': hashlib.sha256((ROOT/'simulation/knapsack_oracle.py').read_bytes()).hexdigest(),
    'compiler': {'basis_gates': ['rz', 'sx', 'x', 'cx'],
                 'optimization_level': 1, 'seed_transpiler': 23},
    'instances': [], 'failures': []}

for inst in instances:
    try:
        w, v, capacity = inst['weights'], inst['values'], inst['capacity']
        n = len(w)
        lower = greedy(w, v, capacity)
        fi, core, fo = reduced_cost_fixing(n, w, v, capacity)
        rw = [w[i] for i in core]
        rv = [v[i] for i in core]
        rc = capacity-sum(w[i] for i in fi)
        voff = sum(v[i] for i in fi)
        mismatch = []
        for tau in range(lower, sum(v)+2):
            full = set(oracle_marked_set(w,v,capacity,tau))
            recon = {original_mask(y,fi,core) for y in oracle_marked_set(rw,rv,rc,tau-voff)}
            if full != recon:
                mismatch.append(tau)
        diagnostics = []
        for tau in [lower, lower+1]:
            marked = oracle_marked_set(w,v,capacity,tau)
            opt = max(sum(v[i] for i in range(n) if x >> i & 1)
                      for x in range(1 << n)
                      if sum(w[i] for i in range(n) if x >> i & 1) <= capacity)
            nonoptimal = [x for x in marked if sum(v[i] for i in range(n) if x >> i & 1) < opt]
            p = len(marked)/(1 << n)
            theta = math.asin(math.sqrt(p))
            diagnostics.append({'tau': tau, 'marked_count': len(marked),
                'marked_nonoptimal_count': len(nonoptimal), 'optimal_value': opt,
                'probabilities_j012': [math.sin((2*j+1)*theta)**2 for j in range(3)]})
        oracle, _ = build_knapsack_oracle(w,v,capacity,lower+1)
        qc = QuantumCircuit(oracle.num_qubits)
        qc.h(range(n))
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser(n), list(range(n)), inplace=True)
        resources = []
        for topology in ['all_to_all','path']:
            coupling = None if topology == 'all_to_all' else CouplingMap.from_line(qc.num_qubits)
            compiled = transpile(qc, basis_gates=out['compiler']['basis_gates'],
                                 coupling_map=coupling, optimization_level=1, seed_transpiler=23)
            resources.append({'topology':topology,'qubits':compiled.num_qubits,
                'depth':compiled.depth(),'two_qubit_gates':sum(1 for ins in compiled.data if ins.operation.num_qubits == 2),
                'operations':dict(compiled.count_ops())})
        row = {'name':inst['name'], 'input':inst,'greedy_incumbent':lower,
               'fixed_in':fi,'core':core,'fixed_out':fo,
               'equivalence_checked_thresholds':sum(v)+2-lower,
               'equivalence_mismatches':mismatch,'diagnostics':diagnostics,
               'one_iteration_resources':resources}
        out['instances'].append(row)
        print(inst['name'], len(core), resources, flush=True)
    except Exception:
        err = {'name':inst.get('name'),'traceback':traceback.format_exc()}
        out['failures'].append(err)
        print(err, flush=True)
outpath = Path(__file__).with_name('hardware_compile_pilot.json')
outpath.write_text(json.dumps(out, indent=2)+'\n',encoding='utf-8')
print('Saved', outpath, flush=True)
