"""Append-only bank compilation study on unchanged canonical input arrays."""
import argparse
import collections
import hashlib
import json
import math
import statistics
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.compressed_bank import build_compressed_bank
from exact_knapsack import dynamic_programming


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--panel',choices=['main','core','independent'],default='main');args=parser.parse_args()
    registry_path=ROOT/'research_log/pruning_study_20261023'/dict(main='inputs.json',core='inputs_core700.json',independent='inputs_stress_independent.json')[args.panel]
    registry=json.loads(registry_path.read_text(encoding='utf8'))
    wanted=dict(main='main700',core='core700',independent='independent_large')[args.panel]
    records=[r for r in registry['records'] if r['category']==wanted]
    out=HERE/f'theory_banks_{args.panel}.jsonl'
    sources={str(p):sha(p) for p in [registry_path,Path(__file__),ROOT/'simulation/source_faithful_20261024/compressed_bank.py']}
    manifest=HERE/f'theory_banks_{args.panel}_before_manifest.json'
    if not manifest.exists():manifest.write_text(json.dumps(dict(panel=args.panel,inputs=len(records),source_hashes=sources,
        scope='Same given arrays; all feasible efficiency-prefix states and all integer thresholds. Pseudopolynomial offline compilation, not end-to-end quantum acceleration.'),indent=2))
    seen=set()
    if out.exists():seen={json.loads(line)['id'] for line in out.read_text().splitlines() if line.strip()}
    with out.open('a',encoding='utf8') as handle:
        for num,row in enumerate(records):
            if row['id'] in seen:continue
            w,v,W=row['weights'],row['values'],row['capacity']
            result=build_compressed_bank(w,v,W)
            dp=None;dp_seconds=None
            if W<=5000:
                started=time.perf_counter();dp=dynamic_programming(w,v,W);dp_seconds=time.perf_counter()-started
            record=dict(id=row['id'],category=row['category'],instance_class=row['instance_class'],
                n=row['n'],seed=row.get('seed'),weights=w,values=v,capacity=W,result=result,
                gcd_weights=math.gcd(*w) if w else 1,gcd_profits=math.gcd(*v) if v else 1,
                source_hashes=sources,comparison_profit_dp=dict(optimum=dp,seconds=dp_seconds,
                    scope='MEASURED local Python reference time, not a competitive solver benchmark; demonstrates preprocessing is not free'),
                no_optimum_advice=True)
            handle.write(json.dumps(record)+'\n');handle.flush()
            if num%50==0:print(args.panel,num+1,'/',len(records),result['status'],result['original_grid_size'],result['root_tail_size'],result['bank_size'],flush=True)
    final=[json.loads(line) for line in out.read_text().splitlines() if line.strip()]
    complete=[r for r in final if r['result']['minimum_on_density_grid']]
    summary=dict(panel=args.panel,attempted=len(final),status_counts=dict(collections.Counter(r['result']['status'] for r in final)),
        original_grid_size_median=statistics.median(r['result']['original_grid_size'] for r in final),
        root_tail_size_median=statistics.median(r['result']['root_tail_size'] for r in final),
        bank_size_median=statistics.median(r['result']['bank_size'] for r in final),
        bank_size_max=max(r['result']['bank_size'] for r in final),
        total_reachable_states=sum(r['result']['reachable_state_count'] for r in final),
        total_coverage_comparisons=sum(r['result']['coverage_comparisons'] for r in final),
        total_preprocessing_seconds=sum(r['result']['preprocessing_seconds'] for r in final),
        total_comparison_dp_seconds=sum(r['comparison_profit_dp']['seconds'] or 0 for r in final),
        strict_root_tail_compressions=sum(r['result']['bank_size']<r['result']['root_tail_size'] for r in complete),
        source_sha256=sha(out))
    (HERE/f'theory_banks_{args.panel}_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
