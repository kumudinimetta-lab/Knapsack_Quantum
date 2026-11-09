"""Apply the authorized bibliography/LR-only revision, preserving original bytes elsewhere."""
from pathlib import Path
import hashlib,json,re,difflib

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BACK=ROOT/'paper/backups/2026-10-26_before_references_literature'

def entries(text):
    starts=list(re.finditer(r'(?m)^@\w+\s*\{\s*([^,]+),',text))
    return {m[1].strip():text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)].strip() for i,m in enumerate(starts)}

old=(BACK/'main.tex').read_bytes()
origbib=(BACK/'references.bib').read_text(encoding='utf-8-sig')
original=entries(origbib)
removed=['ref6','ref7','ref10','ref14','ref15','ref19','ref20','ref21','ref22','ref27','ref28','ref29','ref30','ref32','ref34','martello1988mtm']
new={}
for f in ['theory_proposed_classical_entries.bib','circuit_proposed_entries.bib','quantum_proposed_entries.bib']:
    for k,v in entries((OUT/f).read_text(encoding='utf-8-sig')).items():
        if k not in removed:
            assert k not in new,k
            new[k]=v
assert (set(original)-set(removed)) <= set(new), set(original)-set(removed)-set(new)
start=old.index(b'\\section{Literature Review}')
end=old.index(b'% ==============================================================',start)
replacement=(OUT/'literature_replacement.tex').read_text(encoding='utf-8').strip()+'\n\n'
replacement=replacement.replace('\n','\r\n').encode('utf-8')
updated=old[:start]+replacement+old[end:]
# Never alter anything outside the approved section.
assert updated[:start]==old[:start]
assert updated[start+len(replacement):]==old[end:]
keys=set(k.strip() for grp in re.findall(rb'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',updated) for k in grp.decode().split(','))
assert keys==set(new), {'missing':sorted(keys-set(new)), 'uncited':sorted(set(new)-keys)}
for k in removed:
    assert k not in keys,k
order=[k for k in original if k in new]+[k for k in new if k not in original]
bib='% Bibliography audited 26 October 2026. See research_log/references_literature_20261026/.\n\n'+'\n\n'.join(new[k] for k in order)+'\n'
(ROOT/'paper/main.tex').write_bytes(updated)
(ROOT/'paper/references.bib').write_bytes(bib.replace('\n','\r\n').encode('utf-8'))
(OUT/'removed_entries.bib').write_text('% Archived removals; the original files also remain in the dated backup.\n\n'+'\n\n'.join(original[k] for k in removed)+'\n',encoding='utf-8')
reasons={k:'Peripheral discussion omitted; no claim that the work is nonexistent.' for k in removed}
for k in ['ref6','ref7','ref19','ref22']:
    reasons[k]='Exact saved record remains unverified; background discussion omitted in favor of direct primary sources. Quarantined, not declared fake.'
for k in ['ref27','ref28','ref29','ref30']:
    reasons[k]='Peripheral application/metaheuristic discussion omitted; saved metadata also remains unresolved. No invented replacement.'
reasons['ref20']='Confirmed wrong identifier: arXiv:2006.09838 is music generation. Removed unsupported record and replaced the substantive comparison with verified Hou--Perkowski.'
reasons['ref21']='Real small-device speedup work concerns 3-SAT, not a knapsack oracle; peripheral context omitted.'
reasons['martello1988mtm']='Real historical exact solver; MINKNAP and COMBO retained as the more focused classical solver context.'
ledger={'date':'2026-10-26','before_entries':len(original),'after_entries':len(new),'cited_keys':len(keys),
 'removed':[{'key':k,'reason':reasons[k]} for k in removed],
 'added':sorted(set(new)-set(original)),
 'optional_background_retained':['ref12','ref25','ref31','thapliyal2016'],
 'scope_prefix_identical':True,'scope_suffix_identical':True,
 'original_sha256':hashlib.sha256(old).hexdigest(),'updated_sha256':hashlib.sha256(updated).hexdigest()}
(OUT/'CHANGE_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
(OUT/'manuscript.diff').write_text(''.join(difflib.unified_diff(old.decode('utf-8-sig').splitlines(True),updated.decode('utf-8-sig').splitlines(True),fromfile='backup/main.tex',tofile='paper/main.tex')),encoding='utf-8')
locations=[]
for line_no,line in enumerate(updated.decode('utf-8-sig').splitlines(),1):
    for grp in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',line):
        locations.append({'line':line_no,'keys':grp.split(','),'text':line})
(OUT/'CITATION_LOCATIONS.json').write_text(json.dumps(locations,indent=2)+'\n',encoding='utf-8')
print(json.dumps(ledger,indent=2))
