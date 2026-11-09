from pathlib import Path
import hashlib,json,re
import fitz
out=Path(__file__).resolve().parent
root=out.parents[1]
back=root/'paper/backups/2026-10-26_before_references_literature'
src=(root/'paper/main.tex').read_bytes()
old=(back/'main.tex').read_bytes()
def span(b):
    a=b.index(b'\\section{Literature Review}')
    z=b.index(b'% ==============================================================',a)
    return a,z
a,z=span(src);oa,oz=span(old)
assert src[:a]==old[:oa] and src[z:]==old[oz:]
back_checks=[]
for r in json.loads((back/'MANIFEST.json').read_text(encoding='utf-8-sig')):
    actual=hashlib.sha256((back/r['file']).read_bytes()).hexdigest()
    assert actual==r['sha256']
    back_checks.append({'file':r['file'],'sha256':actual,'matches':True})
bib=(root/'paper/references.bib').read_text(encoding='utf-8-sig')
keys=re.findall(r'(?m)^@\w+\s*\{\s*([^,]+),',bib)
assert len(keys)==len(set(keys))==40
cited={k.strip() for group in re.findall(rb'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',src) for k in group.decode().split(',')}
assert cited==set(keys)
ledgers=[json.loads((out/'theory_reference_audit.json').read_text(encoding='utf-8-sig'))['rows'],
         json.loads((out/'circuit_reference_audit.json').read_text(encoding='utf-8-sig'))['references'],
         json.loads((out/'root_reference_audit.json').read_text(encoding='utf-8-sig'))['references']]
source_map={}
for filename,rows in zip(['theory_reference_audit.json','circuit_reference_audit.json','root_reference_audit.json'],ledgers):
    for row in rows:
        if row['key'] in keys:
            assert row['key'] not in source_map
            source_map[row['key']]={'ledger':filename,'source':row}
assert set(source_map)==set(keys),set(keys)-set(source_map)
locations=json.loads((out/'CITATION_LOCATIONS.json').read_text(encoding='utf-8-sig'))
lr_first=src[:a].count(b'\n')+1;lr_last=src[:z].count(b'\n')
for key,row in source_map.items():
    row['literature_lines']=sorted({loc['line'] for loc in locations if key in loc['keys'] and lr_first<=loc['line']<=lr_last})
    row['other_lines']=sorted({loc['line'] for loc in locations if key in loc['keys'] and not lr_first<=loc['line']<=lr_last})
    assert row['literature_lines'],key
(out/'COMPLETE_REFERENCE_AUDIT.json').write_text(json.dumps(source_map,indent=2)+'\n',encoding='utf-8')
log=(out/'latex_build/main.log').read_text(encoding='utf-8',errors='replace')
blg=(out/'latex_build/main.blg').read_text(encoding='utf-8',errors='replace')
assert not re.search(r'(Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references)',log)
assert 'Warning--' not in blg
bbl=(out/'latex_build/main.bbl').read_text(encoding='utf-8',errors='replace')
assert set(re.findall(r'\\bibitem\{([^}]+)\}',bbl))==set(keys)
pdf=root/'paper/main.pdf';doc=fitz.open(pdf)
assert len(doc)==13
alltext='\n'.join(p.get_text() for p in doc)
assert 'LITERATURE REVIEW' in alltext and 'REFERENCES' in alltext
assert (out/'latex_build/main.pdf').read_bytes()==pdf.read_bytes()
result={'date':'2026-10-26','metric_class':'DERIVED document inventory/checks; no research measurements',
 'entries':40,'distinct_cited_keys':len(cited),'missing_citation_keys':0,'uncited_entries':0,'duplicate_keys':0,
 'source_identity_records':len(source_map),'all_remaining_references_have_scoped_lr_source_records':True,
 'prefix_and_suffix_outside_lr_byte_identical':True,'backup_hash_checks':back_checks,
 'undefined_citations':0,'undefined_references':0,'bibtex_warnings':0,'pdf_pages':len(doc),
 'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
 'tex_sha256':hashlib.sha256(src).hexdigest(),'bib_sha256':hashlib.sha256((root/'paper/references.bib').read_bytes()).hexdigest(),
 'visual_review_pages':[2,3,4,12,13],
 'whole_paper_status':'NOT_CERTIFIED: outside-scope claim/citation integrity holds remain',
 'warnings':[line.strip() for line in log.splitlines() if 'Warning' in line or 'Overfull' in line]}
(out/'FINAL_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['backup_hash_checks']},indent=2))
