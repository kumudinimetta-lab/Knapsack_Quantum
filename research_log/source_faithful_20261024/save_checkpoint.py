"""Freeze new research + sources and preserve verified previous checkpoints."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT / 'research_log/source_faithful_20261025_checkpoint.zip'
MANIFEST = HERE / 'CHECKPOINT_MANIFEST.json'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not DEST.exists(), 'Refuse to overwrite a prior checkpoint'
paper = {}
for name in ['main.tex', 'references.bib', 'main.pdf']:
    p = ROOT / 'paper' / name
    old = ROOT / 'paper/backups/2026-10-22_before_revision' / name
    assert p.read_bytes() == old.read_bytes(), name
    paper[name] = sha(p)
bib = (ROOT / 'paper/references.bib').read_text(encoding='utf8')
assert len(re.findall(r'^\s*@\w+\s*\{', bib, re.M)) == 45

prior = {
    'pruning_study_20261024_checkpoint.zip': '05a7ec81069f45b8bbd67593fabd0bbab6a61c1287e1f403ef524704978c5108',
    'advance_comparison_20261024_checkpoint.zip': 'e3243187c646d42ee0bbdb418d9e73ed4449df958cdf4e7207d26f9789af3524',
}
files = set()
for base in [HERE, ROOT / 'simulation']:
    files.update(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p != MANIFEST)
for name, expected in prior.items():
    p = ROOT / 'research_log' / name
    assert sha(p) == expected, name
    files.add(p)
for name in paper:
    files.add(ROOT / 'paper' / name)
    files.add(ROOT / 'paper/backups/2026-10-22_before_revision' / name)

manifest = {
    'date': '2026-10-25',
    'scope': 'New construction, both arithmetic engines, raw ledgers, failures, independent audits, all simulation sources, two verified prior checkpoints',
    'paper_byte_identical_to_restored_backup': paper,
    'bibliography_entries': 45,
    'previous_checkpoints_sha256': prior,
    'restoration': 'Extract outer archive at project root; if needed extract each nested earlier checkpoint at that same root for earlier raw dependencies. Nothing should be discarded or silently overwritten.',
    'files': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)],
}
MANIFEST.write_text(json.dumps(manifest, indent=2), encoding='utf8')
files.add(MANIFEST)
with zipfile.ZipFile(DEST, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in sorted(files):
        z.write(p, p.relative_to(ROOT).as_posix(), compress_type=zipfile.ZIP_STORED if p.name in prior else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(DEST) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(files)
    for entry in manifest['files']:
        assert hashlib.sha256(z.read(entry['path'])).hexdigest() == entry['sha256'], entry['path']
result = dict(path=str(DEST), bytes=DEST.stat().st_size, files=len(files), sha256=sha(DEST), crc='PASS', member_sha256='ALL PASS', paper='unchanged', bibliography_entries=45)
(DEST.parent / 'source_faithful_20261025_checkpoint_verification.json').write_text(json.dumps(result, indent=2), encoding='utf8')
print(json.dumps(result, indent=2))
