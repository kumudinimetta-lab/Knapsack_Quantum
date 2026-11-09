"""Append-only continuous-bank compilation with retained gzip interval tables."""
import argparse,collections,gzip,hashlib,json,statistics,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.continuous_bank import build_continuous_bank
from exact_knapsack import dynamic_programming


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--panel',choices=['main','core','independent'],default='main');args=parser.parse_args()
    source=HERE/f'theory_banks_{args.panel}.jsonl'
    sources={str(p):sha(p) for p in [source,Path(__file__),ROOT/'simulation/source_faithful_20261024/continuous_bank.py',ROOT/'simulation/source_faithful_20261024/compressed_bank.py']}
    output=HERE/f'theory_banks_continuous_{args.panel}.jsonl'
    manifest=HERE/f'theory_banks_continuous_{args.panel}_before_manifest.json'
    if not manifest.exists():manifest.write_text(json.dumps(dict(source_hashes=sources,
        scope='Minimum cardinality among all nonnegative rational multipliers for exact provided arrays and static prefix order; integer threshold predicates only. Pseudopolynomial preprocessing is not free.'),indent=2))
    folder=HERE/'theory_continuous_interval_records';folder.mkdir(exist_ok=True)
    seen={json.loads(x)['id'] for x in output.read_text().splitlines() if x.strip()} if output.exists() else set()
    with output.open('a',encoding='utf8') as handle:
        for num,line in enumerate(source.read_text().splitlines()):
            case=json.loads(line)
            if case['id'] in seen:continue
            result=build_continuous_bank(case['weights'],case['values'],case['capacity'])
            freq=result.get('coverage_interval_frequencies')
            if freq is not None:
                raw=json.dumps(freq,separators=(',',':')).encode()
                artifact=folder/(case['id']+'.json.gz')
                if artifact.exists():raise RuntimeError('Refuse to overwrite existing continuous interval artifact')
                artifact.write_bytes(gzip.compress(raw,mtime=0))
                del result['coverage_interval_frequencies']
                result['coverage_interval_artifact']=dict(path=str(artifact),sha256=sha(artifact),
                    uncompressed_sha256=hashlib.sha256(raw).hexdigest(),intervals=len(freq))
            comparison_dp=None
            if case['capacity']<=5000:
                started=time.perf_counter();opt=dynamic_programming(case['weights'],case['values'],case['capacity'])
                comparison_dp=dict(optimum=opt,seconds=time.perf_counter()-started)
            contradiction=(result['minimum_among_nonnegative_rationals'] and
                case['result']['minimum_on_density_grid'] and result['bank_size']>case['result']['bank_size'])
            row=dict(id=case['id'],category=case['category'],instance_class=case['instance_class'],n=case['n'],
                weights=case['weights'],values=case['values'],capacity=case['capacity'],result=result,
                exact_density_grid_minimum=case['result']['bank_size'] if case['result']['minimum_on_density_grid'] else None,
                cardinality_contradiction=contradiction,comparison_profit_dp=comparison_dp,source_hashes=sources)
            handle.write(json.dumps(row)+'\n');handle.flush()
            if contradiction:raise RuntimeError('RESEARCH_INTEGRITY_STOP: rational minimum exceeds density-grid feasible reference')
            if num%50==0:print(args.panel,num+1,result['status'],case['result']['bank_size'],result['bank_size'],flush=True)
    rows=[json.loads(x) for x in output.read_text().splitlines() if x.strip()]
    summary=dict(panel=args.panel,attempted=len(rows),status_counts=dict(collections.Counter(r['result']['status'] for r in rows)),
        bank_size_median=statistics.median(r['result']['bank_size'] for r in rows),bank_size_max=max(r['result']['bank_size'] for r in rows),
        strict_density_grid_improvements=sum(r['exact_density_grid_minimum'] is not None and r['result']['bank_size']<r['exact_density_grid_minimum'] for r in rows),
        total_reachable_states=sum(r['result']['reachable_state_count'] for r in rows),
        total_affine_constraints=sum(r['result']['affine_constraint_count'] for r in rows),
        total_preprocessing_seconds=sum(r['result']['preprocessing_seconds'] for r in rows),
        total_comparison_dp_seconds=sum((r['comparison_profit_dp'] or {}).get('seconds',0) for r in rows),
        numerator_bits_max=max(r['result']['max_numerator_bits'] for r in rows),
        denominator_bits_max=max(r['result']['max_denominator_bits'] for r in rows),
        cardinality_contradictions=sum(r['cardinality_contradiction'] for r in rows),source_sha256=sha(output))
    (HERE/f'theory_banks_continuous_{args.panel}_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
