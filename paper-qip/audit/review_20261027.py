"""Preserve the starting draft; line inventory is completed after review."""
from pathlib import Path
import hashlib,json,shutil
OUT=Path(__file__).resolve().parents[1]
backup=OUT/'backups/before_line_audit_20261027'
backup.mkdir(parents=True,exist_ok=True)
files=['main.tex','main.pdf','references.bib','main.bbl','resource_ratios.pdf','qip_latex_review_bundle.zip','audit/PDF_CHECKS.json','audit/REVISION_VERIFICATION.json','audit/DELIVERY_MANIFEST.json']
manifest={}
for name in files:
    p=OUT/name;dest=backup/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():assert dest.read_bytes()==p.read_bytes(),'Do not overwrite an earlier draft backup'
    else:shutil.copy2(p,dest)
    manifest[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(backup/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print('Backed up',len(files),'files')
