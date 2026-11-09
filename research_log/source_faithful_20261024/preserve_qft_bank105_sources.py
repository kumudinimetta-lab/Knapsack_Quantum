"""Snapshot source bytes only after matching the completed run's pinned hashes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
folder = Path(__file__).parent
run = json.loads((folder / 'qft_bank_full105_manifest.json').read_text())
old = json.loads((folder / 'resource105_manifest.json').read_text())
old_hashes = {p.replace('\\', '/'): digest for p, digest in old['source_sha256'].items()}
rows = []
destination = folder / 'source_snapshot_qft_bank105'
destination.mkdir(exist_ok=False)
for name, expected in run['source_sha256'].items():
    normalized = name.replace('\\', '/')
    source = ROOT / normalized
    content = source.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected:
        raise RuntimeError('RESEARCH_INTEGRITY_STOP: current source differs from run source')
    target = destination / source.name
    target.write_bytes(content)
    rows.append(dict(source=normalized, snapshot=str(target.relative_to(folder)), sha256=actual,
                     identical_to_old_LP_run=old_hashes.get(normalized) == actual if normalized in old_hashes else None))
# Additional direct dependencies are copied and explicitly marked as current
# verified dependencies, not silently attributed to a previously recorded hash.
for name in ['simulation/pruning_study_20261023/circuits.py',
             'simulation/pruning_study_20261023/compact_sensitivity.py',
             'simulation/oracle_h/node_bound_reversible.py']:
    source = ROOT / name
    content = source.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    target = destination / source.name
    target.write_bytes(content)
    rows.append(dict(source=name, snapshot=str(target.relative_to(folder)), sha256=actual,
                     classification='current direct dependency snapshot',
                     identical_to_old_LP_run=old_hashes.get(name) == actual if name in old_hashes else None))
(folder / 'qft_bank105_source_snapshot_manifest.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
print(json.dumps(rows, indent=2))
