"""Preserve all audit evidence and the complete prior checkpoint, without overwrites."""
import hashlib
import json
from pathlib import Path
import platform
import zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DEST=ROOT/'research_log/claim_validation_20261025_checkpoint.zip'
MANIFEST=HERE/'CHECKPOINT_MANIFEST.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not DEST.exists()
prior=ROOT/'research_log/source_faithful_20261025_checkpoint.zip'
assert sha(prior)=='53705a8a624d5d79a23fd789ac57d2198faa2f6416f390b4d854af53ac709bc8'
frozen=json.loads((ROOT/'research_log/source_faithful_20261024/CHECKPOINT_MANIFEST.json').read_text())
for entry in frozen['files']:
    assert sha(ROOT/entry['path'])==entry['sha256'],entry['path']
for name in ['main.tex','references.bib','main.pdf']:
    assert (ROOT/'paper'/name).read_bytes()==(ROOT/'paper/backups/2026-10-22_before_revision'/name).read_bytes()
files={p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=MANIFEST}
files.add(prior)
for name in ['claim_validation_dwave_knapsack2024.md','draper-full.md','theory_search_dey_0.md','circuit_wilkening_arxiv_full.md','circuit_wilkening2025_supplement.txt','circuit_cuccaro_full.md']:
    p=ROOT/'.firecrawl'/name
    assert p.exists(),p
    files.add(p)
manifest=dict(date='2026-10-25',python_version=platform.python_version(),
    scope='Fresh adversarial validation; failed initialization tests retained, all-state bank coverage, gate reruns, stronger LP resource control; previous checkpoint included intact',
    previous_workspace_files_rechecked=len(frozen['files']),previous_checkpoint_sha256=sha(prior),
    restored_paper_unchanged=True,bibliography_entries=45,
    restoration='Extract this archive at project root. If restoring from scratch, extract nested source_faithful_20261025_checkpoint.zip there, then its earlier nested checkpoints as needed. Preserve versioned raw evidence.',
    files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)])
MANIFEST.write_text(json.dumps(manifest,indent=2));files.add(MANIFEST)
with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix(),compress_type=zipfile.ZIP_STORED if p==prior else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(DEST) as z:
    assert z.testzip() is None
    for entry in manifest['files']:assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256'],entry['path']
result=dict(path=str(DEST),bytes=DEST.stat().st_size,sha256=sha(DEST),files=len(files),crc='PASS',member_sha256='ALL PASS',previous_workspace_files_unchanged=len(frozen['files']),paper='unchanged',bibliography_entries=45)
(DEST.parent/'claim_validation_20261025_checkpoint_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
