"""Separate append-only DP-free sufficient bank comparison, no old raw edits."""
import collections
import hashlib
import json
import statistics
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.compressed_bank import build_dp_free_bank


def main():
    out=HERE/'theory_banks_dp_free.jsonl'
    seen={json.loads(x)['id'] for x in out.read_text().splitlines() if x.strip()} if out.exists() else set()
    sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'simulation/source_faithful_20261024/compressed_bank.py']}
    manifest=HERE/'theory_banks_dp_free_before_manifest.json'
    if not manifest.exists():manifest.write_text(json.dumps(dict(source_hashes=sources,scope='No reachability DP; sufficient adjacent-density-group radius criteria; separate from exact finite-grid minimum compiler'),indent=2))
    with out.open('a',encoding='utf8') as handle:
        for panel in ['main','core','independent']:
            path=HERE/f'theory_banks_{panel}.jsonl';sha=hashlib.sha256(path.read_bytes()).hexdigest()
            for line in path.read_text().splitlines():
                case=json.loads(line)
                if case['id'] in seen:continue
                result=build_dp_free_bank(case['weights'],case['values'],case['capacity'])
                old=case['result']
                contradiction=(result['bank_size']>old['root_tail_size'] or
                    (old['minimum_on_density_grid'] and result['bank_size']<old['bank_size']))
                row=dict(id=case['id'],category=case['category'],instance_class=case['instance_class'],n=case['n'],
                    result=result,exact_dp_bank_size=old['bank_size'] if old['minimum_on_density_grid'] else None,
                    exact_dp_status=old['status'],source_exact_bank_file=str(path),source_exact_bank_sha256=sha,
                    source_hashes=sources,cardinality_contradiction=contradiction)
                handle.write(json.dumps(row)+'\n');handle.flush()
                if contradiction:raise RuntimeError('RESEARCH_INTEGRITY_STOP: sufficient bank contradicts finite-grid minimum/reference bound')
    rows=[json.loads(x) for x in out.read_text().splitlines() if x.strip()]
    summary={}
    for category in sorted({r['category'] for r in rows}):
        rr=[r for r in rows if r['category']==category]
        summary[category]=dict(inputs=len(rr),status_counts=dict(collections.Counter(r['result']['status'] for r in rr)),
            root_tail_size_median=statistics.median(r['result']['root_tail_size'] for r in rr),
            bank_size_median=statistics.median(r['result']['bank_size'] for r in rr),
            strict_root_tail_compressions=sum(r['result']['bank_size']<r['result']['root_tail_size'] for r in rr),
            total_seconds=sum(r['result']['preprocessing_seconds'] for r in rr),
            total_radius_comparisons=sum(r['result']['radius_comparisons'] for r in rr),
            cardinality_contradictions=sum(r['cardinality_contradiction'] for r in rr))
    (HERE/'theory_banks_dp_free_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
