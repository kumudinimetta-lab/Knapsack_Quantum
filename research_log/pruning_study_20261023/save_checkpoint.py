"""Pin completed research, check source inputs, and save a recoverable archive."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

summary=json.loads((HERE/'paired_summary.json').read_text(encoding='utf8'))
for name,sha in summary['source_sha256'].items():
    if digest(HERE/name)!=sha: raise RuntimeError('Research source changed: '+name)
paper={}
for name in ['main.tex','references.bib','main.pdf']:
    path=ROOT/'paper'/name
    if path.read_bytes()!=(ROOT/'paper/backups/2026-10-22_before_revision'/name).read_bytes():
        raise RuntimeError('Restored manuscript differs: '+name)
    paper[name]=digest(path)
files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='CHECKPOINT_MANIFEST.json']
files += [p for p in (ROOT/'simulation/pruning_study_20261023').rglob('*.py') if '__pycache__' not in p.parts]
files += [ROOT/'simulation/oracle_h/node_bound_reversible.py',ROOT/'simulation/exact_knapsack.py']
files += [p for p in (ROOT/'research_log/deep_research_20261023').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
for name in ['circuit_wilkening2025_supplement_firecrawl.md','circuit_wilkening_arxiv_full.md','vbe-full.md','backtracking2018-full.md','circuit_circuit_search_cost_0.md']:
    path=ROOT/'.firecrawl'/name
    if path.exists(): files.append(path)
files=sorted(set(files))
manifest=dict(completed_date='2026-10-24 Asia/Calcutta',
    scope='Bounded predicate/pruning research; manuscript unchanged; full walk and QPU execution absent; historical priority unresolved',
    primary_report='research_log/pruning_study_20261023/RESEARCH_RESULTS.md',
    manuscript_sha256=paper,bibliography_entries=45,
    resource_attempts=summary['total_build_records'],
    file_sha256={str(p.relative_to(ROOT)):digest(p) for p in files})
path=HERE/'CHECKPOINT_MANIFEST.json'
path.write_text(json.dumps(manifest,indent=2),encoding='utf8')
archive=ROOT/'research_log/pruning_study_20261024_checkpoint.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[path]: z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    bad=z.testzip()
    if bad: raise RuntimeError('Archive CRC failure: '+bad)
print(json.dumps(dict(archive=str(archive),files=len(files)+1,bytes=archive.stat().st_size,
    sha256=digest(archive),restored_manuscript_matches=True,resource_attempts=summary['total_build_records'])))
