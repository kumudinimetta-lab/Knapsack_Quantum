from pathlib import Path
import difflib,hashlib,json,zipfile
OUT=Path(__file__).resolve().parent
checks=json.loads((OUT/'audit/PDF_CHECKS.json').read_text())
checks['visual_review']='All rendered pages inspected in contact sheets; Figure 1 inspected at full page size after its legend correction. Figures 1-3 and Tables 1-4 have unique sequential numbers and resolved references. No clipping or overflow observed.'
(OUT/'audit/PDF_CHECKS.json').write_text(json.dumps(checks,indent=2))
old=(OUT/'audit/original_main.tex').read_text().splitlines(True)
new=(OUT/'main.tex').read_text().splitlines(True)
(OUT/'audit/manuscript.diff').write_text(''.join(difflib.unified_diff(old,new,fromfile='paper/main.tex (preserved)',tofile='paper-qip/main.tex')),encoding='utf8')
files=['main.tex','references.bib','main.bbl','sn-jnl.cls','sn-mathphys-num.bst','resource_ratios.pdf','integer_coverage_example.pdf','oracle_workflow.pdf','main.pdf','LATEX_SUBMISSION_CHECKLIST.md']
with zipfile.ZipFile(OUT/'qip_latex_review_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in files:z.write(OUT/name,name)
with zipfile.ZipFile(OUT/'qip_latex_review_bundle.zip') as z:
    assert set(z.namelist())==set(files)
    assert all(z.read(name)==(OUT/name).read_bytes() for name in files)
manifest={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in files+['qip_latex_review_bundle.zip']}
(OUT/'audit/DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print('Final PDF:',checks['pages'],'pages; ZIP members checked:',len(files))
