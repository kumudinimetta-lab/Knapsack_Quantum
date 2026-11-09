from pathlib import Path
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'paper-qip'
AUDIT = OUT / 'audit'
AUDIT.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = {str(p.relative_to(ROOT)): sha(p) for p in (ROOT/'paper').rglob('*') if p.is_file()}
(AUDIT/'original_paper_manifest.json').write_text(json.dumps(manifest, indent=2))
for name in ['main.tex', 'references.bib', 'main.pdf']:
    shutil.copy2(ROOT/'paper'/name, AUDIT/('original_'+name))
for name in ['references.bib', 'sn-jnl.cls', 'sn-mathphys-num.bst']:
    shutil.copy2(ROOT/'paper'/name, OUT/name)
old = (ROOT/'paper/main.tex').read_text(encoding='utf8')
lr = old[old.index('\\section{Literature Review}'):old.index('% III. PRELIMINARIES')]
lr = lr[:lr.rfind('% ==============================================================')]
lr = lr.replace('table*', 'table').replace('p{0.20\\textwidth}p{0.32\\textwidth}p{0.38\\textwidth}', 'p{0.20\\textwidth}p{0.30\\textwidth}p{0.38\\textwidth}')
(AUDIT/'retained_literature.tex').write_text(lr, encoding='utf8')
print('Preserved original paper hashes:', len(manifest))
