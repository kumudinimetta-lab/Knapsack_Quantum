"""Recover only a hash-verified pre-continuous driver snapshot.

The current driver gained a --continuous branch after older raw ledgers pinned
its previous bytes. Reverse only that observed extension in memory. Write a
new snapshot ONLY if its SHA256 exactly equals the hash in the historical raw
ledger. No experimental data or current driver is edited.
"""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;source=HERE/'bank_circuit_experiments.py'
row=json.loads((HERE/'bank_circuits_main.jsonl').read_text().splitlines()[0])
expected=next(v for k,v in row['source_hashes'].items() if k.endswith('bank_circuit_experiments.py'))
data=source.read_bytes();text=data.decode('utf8')
newline='\r\n' if '\r\n' in text else '\n'
replacements=[
    (";parser.add_argument('--continuous',action='store_true')",''),
    ("    if args.dp_free and args.continuous:raise ValueError('Choose one construction')"+newline,''),
    ("else f'theory_banks_continuous_{args.panel}.jsonl' if args.continuous else",'else'),
    (' if args.dp_free else "_continuous" if args.continuous else ""',' if args.dp_free else ""'),
]
for old,new in replacements:
    if text.count(old)!=1:raise RuntimeError('UNRESOLVED: observed extension does not match exactly')
    text=text.replace(old,new)
recovered=text.encode('utf8');actual=hashlib.sha256(recovered).hexdigest()
if actual!=expected:raise RuntimeError('UNRESOLVED: reconstructed historical bytes do not match pinned hash')
dest=HERE/'bank_circuit_experiments_before_continuous.py'
if dest.exists() and dest.read_bytes()!=recovered:raise RuntimeError('Refuse overwrite of different snapshot')
if not dest.exists():dest.write_bytes(recovered)
out=dict(status='EXACT_HASH_MATCH',historical_sha256=expected,current_sha256=hashlib.sha256(data).hexdigest(),
    recovered_path=str(dest),method='Reverse only observed --continuous extension; require exact historical SHA256',
    replacements=len(replacements),raw_ledger_edited=False,current_driver_edited=False)
log=HERE/'historical_bank_driver_recovery.json'
if log.exists():raise RuntimeError('Refuse overwrite of recovery log')
log.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
