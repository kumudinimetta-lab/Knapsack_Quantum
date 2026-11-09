"""Hash-gated recovery of two sequential historical research-driver versions.

The first attempt targeted the pre-DP-free hash after removing only the later
continuous extension, so it failed without writing a snapshot. This attempt
distinguishes both historical hashes, tests newline encoding explicitly, and
accepts only an exact raw-ledger SHA256 match. Current code/raw stay untouched.
"""
import hashlib
import itertools
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;current=HERE/'bank_circuit_experiments.py'
text=current.read_text(encoding='utf8').replace('\r\n','\n')
def pinned(name):
    row=json.loads((HERE/name).read_text().splitlines()[0])
    return next(v for k,v in row['source_hashes'].items() if k.endswith('bank_circuit_experiments.py'))
targets={'before_continuous':pinned('bank_circuits_main_dp_free.jsonl'),'before_dp_free':pinned('bank_circuits_main.jsonl')}
for old,new in [
    (";parser.add_argument('--continuous',action='store_true')",''),
    ("    if args.dp_free and args.continuous:raise ValueError('Choose one construction')\n",''),
    ("else f'theory_banks_continuous_{args.panel}.jsonl' if args.continuous else",'else'),
    (' if args.dp_free else "_continuous" if args.continuous else ""',' if args.dp_free else ""'),
]:
    if text.count(old)!=1:raise RuntimeError('Observed continuous extension differs')
    text=text.replace(old,new)
def encodings(value):
    value=value.rstrip('\n')
    for newline,ending,bom in itertools.product(['\n','\r\n'],['','\n','\n\n'],[False,True]):
        yield (b'\xef\xbb\xbf' if bom else b'')+(value+ending).replace('\n',newline).encode('utf8')
matches={};attempts=0
def try_candidate(stage,value):
    global attempts
    for candidate in encodings(value):
        attempts+=1
        if hashlib.sha256(candidate).hexdigest()==targets[stage]:
            matches[stage]=candidate;return True
    return False
try_candidate('before_continuous',text)
# Remove exactly the data-source and registry branches added by --dp-free.
older=text.replace(";parser.add_argument('--dp-free',action='store_true')",'')
older=older.replace("source=HERE/('theory_banks_dp_free.jsonl' if args.dp_free else f'theory_banks_{args.panel}.jsonl')", "source=HERE/f'theory_banks_{args.panel}.jsonl'")
start=older.index('    registry=None\n');end=older.index('    output=',start)
older=older[:start]+older[end:]
older=older.replace('f\'bank_circuits_{args.panel}{"_dp_free" if args.dp_free else ""}.jsonl\'',"f'bank_circuits_{args.panel}.jsonl'")
older=older.replace("    if registry:sources[str(registry)]=sha(registry)\n",'')
try_candidate('before_dp_free',older)
try_candidate('before_dp_free',older.replace("choices=['main','core','independent']","choices=['main','core']"))
result=dict(previous_attempt='Only continuous extension reversed but compared with earlier pre-DP-free hash; no snapshot written',
    targets=targets,candidate_byte_encodings_tested=attempts,recovered=[],unresolved=[])
for stage,wanted in targets.items():
    if stage not in matches:result['unresolved'].append(stage);continue
    destination=HERE/f'bank_circuit_experiments_{stage}.py';data=matches[stage]
    if destination.exists() and destination.read_bytes()!=data:raise RuntimeError('Refuse overwrite of different historical snapshot')
    if not destination.exists():destination.write_bytes(data)
    result['recovered'].append(dict(stage=stage,path=str(destination),sha256=wanted))
log=HERE/'historical_bank_driver_recovery_v2.json'
if log.exists():raise RuntimeError('Refuse overwrite log')
log.write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
