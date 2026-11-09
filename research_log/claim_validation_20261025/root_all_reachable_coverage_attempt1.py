"""Fresh all-state audit without production bank/LP helpers. See ROOT_AUDIT_PLAN."""
from collections import Counter
from fractions import Fraction
from functools import cmp_to_key
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'research_log/source_faithful_20261024'
DATA = ROOT / 'research_log/pruning_study_20261023'
def read_lines(path):
    return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def parameters(w, v, indices, bank):
    return [(a, b, sum(max(b*v[i]-a*w[i], 0) for i in indices)) for a, b in bank]
def bound_floor(coefficients, remaining):
    return min((a*remaining+c)//b for a, b, c in coefficients)
def fail(details):
    (HERE / 'root_all_reachable_failure.json').write_text(json.dumps(details, indent=2))
    raise AssertionError('RESEARCH_INTEGRITY_STOP: '+str(details))

def main():
    target = HERE / 'root_all_reachable_rows.jsonl'
    assert not target.exists(), 'Preserve all previous raw attempts'
    paths = [Path(__file__), HERE / 'ROOT_AUDIT_PLAN.md', OLD / 'theory_banks_dp_free.jsonl']
    free = {r['id']: r for r in read_lines(paths[-1])}
    total = Counter()
    started = time.perf_counter()
    panels = {}
    with target.open('x', encoding='utf8') as out:
        for panel, registry_name in [('main', 'inputs.json'), ('core', 'inputs_core700.json')]:
            registry = DATA / registry_name
            grid_path = OLD / f'theory_banks_{panel}.jsonl'
            continuous_path = OLD / f'theory_banks_continuous_{panel}.jsonl'
            paths += [registry, grid_path, continuous_path]
            inputs = json.loads(registry.read_text())['records']
            grid = {r['id']: r for r in read_lines(grid_path)}
            continuous = {r['id']: r for r in read_lines(continuous_path)}
            assert len(inputs) == len(grid) == len(continuous) == 700
            counts = Counter()
            for number, item in enumerate(inputs):
                ident = item['id']
                w, v, cap = item['weights'], item['values'], item['capacity']
                n = len(w)
                order = sorted(range(n), key=cmp_to_key(lambda i,j: (v[j]*w[i] > v[i]*w[j])-(v[j]*w[i] < v[i]*w[j])))
                assert order == grid[ident]['result']['order'] == free[ident]['result']['order']
                for saved in [grid[ident], continuous[ident]]:
                    assert (w,v,cap) == (saved['weights'],saved['values'],saved['capacity'])
                banks = dict(root_tail=grid[ident]['result']['root_tail_grid'],
                             minimum_grid=grid[ident]['result']['bank'],
                             dp_free=free[ident]['result']['bank'],
                             continuous=continuous[ident]['result']['bank'])
                states = 0
                max_reachable = 1
                reachable = {0}
                for depth in range(n+1):
                    suffix = order[depth:]
                    ratios = {Fraction(0)} | {Fraction(v[i],w[i]) for i in suffix}
                    reference = parameters(w,v,suffix,[(x.numerator,x.denominator) for x in ratios])
                    coefficients = {name:parameters(w,v,suffix,bank) for name,bank in banks.items()}
                    for consumed in sorted(reachable):
                        remaining = cap-consumed
                        expected = bound_floor(reference, remaining)
                        for name, constants in coefficients.items():
                            actual = bound_floor(constants, remaining)
                            if actual != expected:
                                fail(dict(panel=panel,id=ident,depth=depth,remaining=remaining,
                                          bank=name,expected=expected,actual=actual))
                        states += 1
                    if depth < n:
                        reachable |= {s+w[order[depth]] for s in reachable if s+w[order[depth]] <= cap}
                        max_reachable = max(max_reachable,len(reachable))
                row = dict(id=ident,panel=panel,n=n,reachable_states=states,bank_floor_comparisons=4*states,
                           predicate_floor_mismatches=0,status='complete',max_reachable_weights=max_reachable,
                           classification='DERIVED exact all-reachable-state coverage; not gate simulation')
                out.write(json.dumps(row)+'\n')
                out.flush()
                counts.update(instances=1,reachable_states=states,bank_floor_comparisons=4*states,
                              empty_inputs=int(n==0),all_fit_inputs=int(sum(w)<=cap))
                if (number+1)%100==0:
                    print(panel,number+1,dict(counts),flush=True)
            panels[panel]=dict(counts)
            total.update(counts)
    result = dict(classification='DERIVED exact arithmetic coverage',panels=panels,total=dict(total),
                  status='PASS',predicate_floor_mismatches=0,seconds_measured=time.perf_counter()-started,
                  reference='Independent full suffix dual breakpoint enumeration; no greedy LP/bank helper imports',
                  scope='All reachable quotient states of the 700 original and 700 core registries, all four banks. Integer-P equivalence extends floors to all integer thresholds; NOT exhaustive gate validation.',
                  hashes={str(p.relative_to(ROOT)):digest(p) for p in paths+[target]})
    (HERE / 'root_all_reachable_summary.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2),flush=True)

if __name__ == '__main__':
    main()
