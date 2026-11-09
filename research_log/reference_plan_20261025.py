"""Read-only paper inventory; write a separate reference plan and CSV."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'paper'
hashes={n:hashlib.sha256((PAPER/n).read_bytes()).hexdigest() for n in ['main.tex','references.bib','main.pdf']}
bib=(PAPER/'references.bib').read_text(encoding='utf8')
tex=(PAPER/'main.tex').read_text(encoding='utf8')
def field(block,name):
    match=re.search(r'\b'+name+r'\s*=\s*\{',block,re.I)
    if not match:return ''
    start=match.end();depth=1;end=start
    while depth:
        c=block[end]
        if c=='{' and (end==0 or block[end-1]!='\\'):depth+=1
        elif c=='}' and (end==0 or block[end-1]!='\\'):depth-=1
        end+=1
    return block[start:end-1]
notes={
'ref1':('KEEP','Fractional-knapsack LP bound; foundational attribution.'),
'ref2':('KEEP','Meet-in-the-middle reference; qualify model and worst-case comparisons.'),
'ref3':('KEEP','Knapsack definitions, exact methods, benchmark classes and preprocessing.'),
'ref4':('KEEP','Core methods; verify exact attribution of any specific fixing lemma.'),
'ref5':('OPTIONAL','Subset-sum representation background; retain if discussing that comparison.'),
'ref6':('HOLD_VERIFY','Exact title/authors/ESA2021 metadata not established. Do not treat as a verified Helm-May paper or delete merely for being unverified.'),
'ref7':('HOLD_VERIFY','Exact packing-tree title/venue/pages need verification; related real Plateau-Elkihel hybrid-knapsack work is not an automatic substitute.'),
'ref8':('KEEP','Quantum search foundation.'),
'ref9':('KEEP','Black-box lower-bound context; does not prove an unrestricted lower bound for structured knapsack.'),
'ref10':('OPTIONAL','Exact Grover variant; remove only if that discussion is omitted and this method is not used.'),
'ref11':('KEEP','Amplitude amplification; assumptions and success probabilities must be stated.'),
'ref12':('OPTIONAL','Pure adaptive search background; not the implemented main construction.'),
'ref13':('KEEP','Quantum optimization/minimum finding background if retained.'),
'ref14':('OPTIONAL','Element distinctness is background rather than the backtracking theorem used.'),
'ref15':('OPTIONAL','Generic walk-search framework; retain only for a meaningful comparison or theorem use.'),
'ref16':('KEEP','Closest subset-sum quantum algorithm background; distinguish subset sum from general knapsack.'),
'ref17':('KEEP','Quantum subset-sum comparison; qualify heuristic assumptions and memory model.'),
'ref18':('KEEP','QRAM model discussion; a critique is not proof that every hardware proposal is impossible.'),
'ref19':('HOLD_VERIFY','Saved Jaques-Schanck lattice-sieving title/venue was not verified. Their real RAM-model cryptanalysis paper is a different work.'),
'ref20':('REPAIR_OR_REPLACE','CONFIRMED wrong arXiv identifier:2006.09838 is Xin Xu, LSTM Networks for Music Generation. Do not cite as knapsack; identify intended paper or replace with verified Hou-Perkowski, without inventing a Shi record.'),
'ref21':('KEEP_SCOPE','Real small-device speedup work; do not describe it as a verified Grover-knapsack solver without source support.'),
'ref22':('HOLD_VERIFY','Exact quantum-search/JTAIT record not verified. Same authors have real quantum-INSPIRED evolutionary papers; do not conflate them with gate-model search.'),
'ref23':('KEEP_UPDATE','Keep QTG/QAOA comparison; primary now lists QCE2025 DOI10.1109/QCE65121.2025.00011. Saved extra author initial should be checked against official export.'),
'ref24':('KEEP_UPDATE','Central B&B framework; complete article013056/DOI10.1103/PhysRevResearch.2.013056 and verify exact theorem use.'),
'ref25':('OPTIONAL','QAOA context if retained; not the algorithm used by the new oracle.'),
'ref26':('KEEP_SCOPE','Relevant constrained adaptive-search comparison; check published citation and avoid claiming it is our algorithm.'),
'ref27':('OPTIONAL_VERIFY','Energy application is peripheral; saved title/year/venue appear conflated. Author group lists Energy179(2019)76-89 for the energy-systems review, and a different fault-diagnosis title in C&CE143(2020).'),
'ref28':('OPTIONAL_VERIFY','Peripheral genetic-method comparison. Saved Norambuena/ESWA223 record not verified; verified Ballinas-Montiel2022 is different, not an automatic repair.'),
'ref29':('OPTIONAL_VERIFY','Peripheral quantum-inspired wolf-pack method; saved authors/title/venue/year need primary verification.'),
'ref30':('OPTIONAL_VERIFY','Peripheral harmonic-oscillator method; likely metadata mismatch. Related real record has Genetic Operator in title, DOI10.1109/ACCESS.2019.2942340; publisher confirmation pending.'),
'ref31':('OPTIONAL','Retain for an explicit limitations paragraph; not evidence of device execution or knapsack advantage.'),
'ref32':('OPTIONAL','Unrelated shallow-circuit separation; not support for advantages of this oracle.'),
'ref33':('KEEP_UPDATE','Use official Quantum computing with Qiskit citation (Javadi-Abhari etal.,2024,arXiv2405.08810), and state actual Qiskit2.4.2/Aer0.17.2 versions.'),
'ref34':('OPTIONAL','Generic adversary-method lower bounds; retain only if actually used, without an unrestricted NP/knapsack conclusion.'),
'bonnetain2020improved':('KEEP','Needed if discussing subset-sum walk assumptions; avoid a blanket claim that all quantum subset-sum algorithms are unsound.'),
'ref35':('KEEP','Backtracking/detection versus witness-search theorem attribution; not interchangeable with the B&B theorem.'),
'ref36':('REPAIR','CONFIRMED wrong identifier and author list. Real intended-topic paper:Sanavio,Tignone,Ercolessi, Hybrid Classical-Quantum Branch-and-Bound Algorithm for Solving Integer Linear Problems, Entropy26(4),345(2024), DOI10.3390/e26040345.'),
'beier2004random':('KEEP_SCOPE','Currently uncited. Useful random-instance context only if distribution assumptions are mapped; not a theorem about our correlated panels.'),
'pisinger1997minimal':('KEEP','Currently uncited. Strong exact-solver/MINKNAP context, useful for fair classical comparisons.'),
'martello1999combo':('KEEP','Currently uncited. Essential COMBO/strong-bound comparison if that baseline is discussed.'),
'martello1988mtm':('OPTIONAL','Currently uncited. Retain for actual historical/exact-algorithm comparison; do not delete simply because uncited.'),
'draper2000':('KEEP','Already present: QFT addition used in reconstruction. Do not add a duplicate.'),
'vedral1996':('KEEP','Already present: elementary reversible arithmetic. Attribute the construction actually used.'),
'thapliyal2016':('OPTIONAL','Real divider paper, but new circuits compile classical rational constants and do not execute this divider. Drop only if divider discussion is removed; do not call it fabricated.'),
'barenco1995':('KEEP_SCOPE','Elementary gate decomposition background if used; does not by itself justify Ross-Selinger T-synthesis numbers.'),
}
starts=list(re.finditer(r'(?m)^@(\w+)\{([^,]+),',bib));records=[]
locations={}
for lineno,line in enumerate(tex.splitlines(),1):
    for match in re.finditer(r'\\cite\w*\s*(?:\[[^]]*\]\s*)?\{([^}]+)\}',line):
        for key in match.group(1).split(','):locations.setdefault(key.strip(),[]).append(lineno)
for index,m in enumerate(starts):
    key=m.group(2);block=bib[m.start():starts[index+1].start() if index+1<len(starts) else len(bib)]
    action,reason=notes[key]
    records.append(dict(key=key,type=m.group(1),author_as_saved=field(block,'author'),title_as_saved=field(block,'title'),year_as_saved=field(block,'year'),venue_as_saved=field(block,'journal') or field(block,'booktitle') or field(block,'publisher'),cited_lines=locations.get(key,[]),recommendation=action,reason=reason))
assert len(records)==len(notes)==45
assert set(locations)<=set(notes)
adds=[
('ADD','Wilkening et al. (2025)','A quantum algorithm for solving 0-1 Knapsack problems','https://doi.org/10.1038/s41534-025-01097-8','Closest fractional-greedy quantum-knapsack work and arithmetic comparison; distinct from existing QTG-QAOA ref23.'),
('ADD','Cuccaro, Draper, Kutin and Moulton (2004)','A new quantum ripple-carry addition circuit','https://arxiv.org/abs/quant-ph/0410184','Actual ripple/MAJ-UMA arithmetic comparator used in the research; cite the simple versus optimized variant accurately.'),
('ADD','Dey, Dubey and Molinaro (2020; revised2021v4)','Branch-and-Bound Solves Random Binary IPs in Polytime','https://arxiv.org/abs/2007.15192','Section3 LP dual/reduced-cost framework; do not transfer its random-IP polynomial result to our benchmarks.'),
('ADD','Bozejko, Burduk, Pempera, Uchronski and Wodecki (2024)','Optimal solving of a binary knapsack problem on a D-Wave quantum machine and its implementation in production systems','https://doi.org/10.1007/s10479-024-06025-1','Required prior art for affine Lagrangian multiplier sets and integer-floor pruning; not our clean reversible compiler.'),
('ADD_OR_REPLACE_REF20','Hou and Perkowski (2020)','Quantum-based algorithm and circuit design for bounded Knapsack optimization problem','https://doi.org/10.26421/QIC20.9-10-4','Verified gate-model knapsack feasibility oracle, Quantum Information and Computation20(9-10),766-786; relevant comparison rather than the incorrect ref20.'),
('ADD','Gabbassov, Rosenberg and Scherer (2025)','Lagrangian duality in quantum optimization: Overcoming QUBO limitations for constrained problems','https://doi.org/10.1103/53gd-2374','Physical Review Research7,023305; distinguish established quantum/Lagrangian optimization from our scoped bank compiler.'),
('ADD','Erickson (2019)','Algorithms, Chapter4: Greedy Algorithms','https://jeffe.cs.illinois.edu/teaching/algorithms/book/04-greedy.pdf','Credit standard interval-stabbing subproblem; keep our strict open-endpoint proof self-contained. No invented exercise/theorem number.'),
('RECOMMENDED_CLOSEST_CONTEXT','Hamitouche, Hnaien and Menacer (2025)','Towards a Quantum Resolution of the Knapsack Problem','https://www.cs.auckland.ac.nz/research/groups/CDMTCS/researchreports/download.php?selected-id=904','Workshop contribution in CDMTCS-586; compare quantum feasibility oracle versus separate classical fractional bound. Cite as workshop/report, not QIP journal article.'),
('SOFTWARE_ARTIFACT','Wilkening et al. released R1 software archive','Version-specific source artifact DOI10.5281/zenodo.16895828','https://doi.org/10.5281/zenodo.16895828','Reproducibility citation when reporting our source audit; import official archive metadata rather than inventing the artifact title.'),
('UPDATE_EXISTING_REF33','Javadi-Abhari et al. (2024)','Quantum computing with Qiskit','https://github.com/Qiskit/qiskit/blob/main/CITATION.bib','Official Qiskit/Aer recommendation. Do not add redundant citations merely to inflate counts. Report actual package versions and link Aer documentation for simulator options.'),
('CONDITIONAL','Martiel and Remaud (2019)','Practical implementation of a quantum backtracking algorithm','https://arxiv.org/abs/1908.11291','Add if retaining circuit-space/backtracking implementation comparisons; no full-walk implementation claim is implied.'),
]
result=dict(current_entries=45,distinct_cited_keys=len(locations),uncited=[r['key'] for r in records if not r['cited_lines']],current=records,proposed_additions=adds,paper_sha256_before=hashes)
dest=ROOT/'research_log/REFERENCE_PLAN_2026-10-26.json';assert not dest.exists();dest.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader()
for r in records:writer.writerow({**r,'cited_lines':';'.join(map(str,r['cited_lines']))})
(ROOT/'research_log/REFERENCE_INVENTORY_2026-10-26.csv').write_text(stream.getvalue(),encoding='utf-8-sig')
lines=['# Reference plan before manuscript editing','', 'Prepared 25–26 October 2026. No manuscript changes.', '',
'No paper or bibliography changes. There are **45 saved entries**, **41 distinct cited keys**, and **4 uncited saved entries**. Keys below are BibTeX identifiers, not necessarily the numbers printed in the PDF.',
'', 'Current titles/authors/years are reproduced **as saved**, including suspect metadata. KEEP is a relevance recommendation, not certification of every field or every sentence currently citing it. Unverified does not mean fake and does not justify automatic removal.',
'', '## All current entries','', '| Key | Current entry as saved | Cited? | Proposed action | Reason |','|---|---|---|---|---|']
for r in records:
    title=r['title_as_saved'].replace('{','').replace('}','')
    lines.append(f"| `{r['key']}` | {r['author_as_saved']} ({r['year_as_saved']}). {title} | {'Yes' if r['cited_lines'] else 'No'} | {r['recommendation']} | {r['reason']} |")
lines+=['','## Proposed additions / updates','','| Priority | Work | Why |','|---|---|---|']
for priority,author,title,url,why in adds:lines.append(f'| {priority} | {author}. [{title}]({url}) | {why} |')
lines+=['','## Confirmed repairs versus optional pruning','',
'**Confirmed identifier errors: ref20 and ref36.** Their supplied arXiv links point to [music generation](https://arxiv.org/abs/2006.09838) and [DFT Hamiltonian prediction](https://arxiv.org/abs/2403.09560), respectively. Those identifiers cannot support the current claims. Repair the intended source, or replace the citation with a verified relevant source; preserve the old record in the audit. The real Sanavio paper has [Tignone and Ercolessi as coauthors](https://doi.org/10.3390/e26040345).',
'', '**Potential removals on relevance only:** ref10, ref12, ref14, ref15, ref25, ref27, ref28, ref29, ref30, ref32, ref34 and thapliyal2016, but only if their related discussion is actually removed from the revised paper. These are candidates, not an instruction to delete all twelve. ref5, ref21, ref31 and martello1988mtm are also conditional background. Keep substantive closest-work comparisons even when they weaken our novelty position.',
'', '**Hold pending exact-source checks:** ref6, ref7, ref19, ref22, ref27, ref28, ref29, ref30. Search returned related but different papers for several of them; do not silently substitute authors/titles or declare the saved paper nonexistent from a failed search. In particular, the verified Ballinas-Montiel2022 genetic paper is not the saved Norambuena2023 record.',
'', '**Keep the four uncited classical entries available.** MINKNAP and COMBO are directly relevant to baseline credibility. Whether they appear in the final rendered bibliography depends on adding a supported citation in the revised text, not merely keeping a BibTeX entry.',
'', 'Draper, VBE, Barenco, Montanaro2020 and Montanaro2018 are already present; additions must not duplicate them. Do not add game-theory, Zeno, IBM-hardware or rotation-synthesis papers just to imply experiments or methods that were not performed.',
'', '## Evidence and limitations','',
'Read the restored bibliography and every citation location in main.tex. Graph-tool discovery returned no available graph tools, so targeted reads were used. Previously verified primary sources and the new audit supplied the construction-related additions. Fresh primary checks reconfirmed ref20/ref36 identifiers, ref23 QCE publication metadata, Cuccaro, Hou-Perkowski, Gabbassov, Dey, interval-stabbing source and official Qiskit citation. Author-group publications flag the conflated ref27 metadata. Several publisher URLs were inaccessible, so those fields remain pending rather than guessed.',
'', 'Read-only identifier mismatches remain research-integrity holds on claims depending on them; this inventory does not approve those claims. No compilation or manuscript revision was attempted. An invalid exploratory arXiv URL1898.11291 was rejected as a typo; the verified Martiel-Remaud identifier is1908.11291. A guessed Aer-local CITATION.bib URL404 was replaced by following the official README link to Qiskit/CITATION.bib.',
'', 'The final bibliography size is intentionally undecided. Relevance, accurate attribution and direct support for the final manuscript determine the count.']
(ROOT/'research_log/REFERENCE_PLAN_2026-10-26.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
after={n:hashlib.sha256((PAPER/n).read_bytes()).hexdigest() for n in hashes}
assert after==hashes
print(json.dumps(dict(entries=45,cited=len(locations),uncited=result['uncited'],paper_unchanged=True,outputs=[dest.name,'REFERENCE_PLAN_2026-10-26.md','REFERENCE_INVENTORY_2026-10-26.csv']),indent=2))

if __name__=='__main__':pass
