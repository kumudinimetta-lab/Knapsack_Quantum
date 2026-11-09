"""Additional lineage check; does not modify the completed all-state driver."""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'research_log/source_faithful_20261024'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
path = OLD / 'theory_banks_dp_free.jsonl'
rows = [json.loads(s) for s in path.read_text().splitlines()]
counts = Counter()
cache = {}
for row in rows:
    source = Path(row['source_exact_bank_file'])
    if source not in cache:
        cache[source] = (sha(source), {r['id']: r for r in map(json.loads, source.read_text().splitlines())})
    digest, source_rows = cache[source]
    assert digest == row['source_exact_bank_sha256']
    assert row['id'] in source_rows
    assert row['n'] == source_rows[row['id']]['n']
    assert row['category'] == source_rows[row['id']]['category']
    counts[row['category']] += 1
result = dict(classification='DERIVED source-lineage checks', records=len(rows),counts=dict(counts),
              hash_conflicts=0,id_conflicts=0,metadata_conflicts=0,
              paths_sha256={str(p.relative_to(ROOT)):value[0] for p,value in cache.items()},
              driver_sha256=sha(Path(__file__)),bank_file_sha256=sha(path))
(HERE / 'root_bank_lineage.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
