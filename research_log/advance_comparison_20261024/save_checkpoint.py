import hashlib
import json
from pathlib import Path
import zipfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paper={}
for name in ['main.tex','references.bib','main.pdf']:
    p=ROOT/'paper'/name
    assert p.read_bytes()==(ROOT/'paper/backups/2026-10-22_before_revision'/name).read_bytes()
    paper[name]=sha(p)
files=[p for p in HERE.iterdir() if p.is_file() and p.name!='CHECKPOINT_MANIFEST.json']
source=ROOT/'.firecrawl/circuit_qtg_R1.zip'
assert hashlib.md5(source.read_bytes()).hexdigest()=='02d7becb556d26f3e4a6f898b69530b7'
manifest=dict(date='2026-10-24 Asia/Calcutta',scope='Additional comparison; no substantial cross-source performance advance established',
    manuscript_unchanged_sha256=paper,source_archive_sha256=sha(source),
    file_sha256={p.name:sha(p) for p in files})
p=HERE/'CHECKPOINT_MANIFEST.json';p.write_text(json.dumps(manifest,indent=2),encoding='utf8')
archive=ROOT/'research_log/advance_comparison_20261024_checkpoint.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+[p]:z.write(f,f.relative_to(ROOT))
    z.write(source,'reference_sources/circuit_qtg_R1.zip',compress_type=zipfile.ZIP_STORED)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(dict(archive=str(archive),bytes=archive.stat().st_size,sha256=sha(archive),paper_unchanged=True)))
