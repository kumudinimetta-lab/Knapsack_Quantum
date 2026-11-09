"""Record primary-source checks made during the bibliography/LR audit, not new research results."""
from pathlib import Path
import json,re
out=Path(__file__).resolve().parent
# key | primary source | inspected source location | supported use | limitation
data=r'''
ref8|https://arxiv.org/abs/quant-ph/9605043|Original STOC paper/abstract; ACM DOI10.1145/237814.237866|Unstructured quantum search query scaling|Query count excludes reversible implementation cost; not a structured knapsack lower bound.
ref9|https://arxiv.org/html/quant-ph/9701001v1|Section3.1 and Theorem3.5|Black-box and random-oracle lower-bound context|Theorem3.5 concerns random-oracle NP and time o(2^(n/2)); it does not rule out structure-exploiting knapsack algorithms.
ref11|https://arxiv.org/html/quant-ph/0005055v1|Section2, Theorem3; arXiv journal reference/related DOI; AMS volume305 cover|Amplitude amplification using A and its inverse|Theorem3 assumes measurement-free A, success probability a>0; expected O(1/sqrt(a)); zero-solution handling requires more than that statement. Publisher cover gives Quantum Computation and Information despite arXiv journal-reference title discrepancy.
ref12|https://www.math.canterbury.ac.nz/research/ucdms2000n10.pdf|Author technical-report abstract; author-institution published record https://researchers.mq.edu.au/en/publications/implementing-pure-adaptive-search-with-grovers-quantum-algorithm/|Grover-based implementation of pure adaptive search|Conditional objective/domain assumptions; not unrestricted polynomial knapsack optimization. Published2003JOTA116(3)517--529, DOI10.1023/A:1023061218864.
ref13|https://arxiv.org/abs/quant-ph/9607014|Abstract and original1996 submission/revision history|Quantum minimum finding as optimization background|Cited as original preprint, not an invented journal publication; no theorem transplanted into our oracle.
ref16|https://eprint.iacr.org/2013/199|Author-posted abstract, metadata and official BibTeX|Quantum subset-sum algorithms using Johnson-graph walks and representation methods|The source describes heuristic cost; cite the verified expanded ePrint rather than guessing conference-version details. This is exact-target subset sum, not arbitrary weight/value optimization.
ref17|https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2018.5|Publisher metadata, abstract and paper opening|Quantum subset-sum algorithms under random-instance/heuristic assumptions|No current-best claim and no worst-case general-knapsack exponent. Exact proceedings pagination5:1--5:15.
ref18|https://quantum-journal.org/papers/q-2025-12-02-1922/|Published abstract and official BibTeX|Active/passive QRAM assumptions and costs|Does not prove all quantum-addressable memory impossible; circuit QRAM can help. Updated2023preprint to Quantum9,1922(2025).
ref23|https://arxiv.org/abs/2411.00518v2|Abstract, accepted-at-QCE statement and related DOI|QTG state preparation with Grover-mixer QAOA; finite-depth evidence and eventual optimal-sampling result|Not all QTG uses are QAOA; do not claim no guarantees whatsoever. DOI10.1109/QCE65121.2025.00011; no unverified page range inserted.
ref24|https://arxiv.org/html/1906.10375v1|Statement of results and oracle model|Quantum branch-and-bound query framework|Monotone cost/bounding oracle, depth and precision assumptions matter. The result is not a free-oracle runtime bound and is not simply sqrt(T)*d in all models. Old body theorem remains on hold.
ref25|https://arxiv.org/html/1411.4028v1|Algorithm description and asymptotic-depth discussion|QAOA variational framework|Do not claim all QAOA lacks guarantees; source has specified approximation/limit results.
ref26|https://quantum-journal.org/papers/q-2021-04-08-428/|Abstract and official BibTeX|Grover adaptive search for constrained polynomial binary optimization|Search is not variational QAOA. Source discusses oracle construction and conditional comparison with brute force, not blanket practical advantage. Quantum5,428(2021).
ref31|https://preskill.caltech.edu/pubs/preskill-2018-NISQ.pdf|Author full text; Quantum2,79 metadata|Noise/depth context|No evidence for this project's device experiments, a four-item boundary or its implementation-specific mitigation claims.
ref33|https://raw.githubusercontent.com/Qiskit/qiskit/refs/heads/main/CITATION.bib|Official Qiskit BibTeX; Aer README citation link|Software attribution to Quantum computing with Qiskit,2024|Citation is not evidence for device execution or experiment results. Actual package versions belong in later methods revision.
bonnetain2020improved|https://arxiv.org/html/2002.05276v4|Section3.2 heuristic discussion, Sections4--5 alternative algorithms and memory tradeoffs; publisher DOI metadata|Specific walk-update heuristic issue and subsequent alternatives|Do not label every subset-sum method unsound or every variant QRAQM-dependent. Correct ASIACRYPT2020,LNCS12492,633--666, DOI10.1007/978-3-030-64834-3_22.
ref35|https://theoryofcomputing.org/articles/v014a015/|Publisher full paper, Theorems1.1/1.2|Quantum backtracking query framework|Detection and witness recovery have distinct statements. No full gate-model LP walk follows merely from a citation. ToC14(15)1--24(2018), DOI10.4086/toc.2018.v014a015.
ref36|https://www.mdpi.com/1099-4300/26/4/345|Article title/authors, abstract and hybrid model|Classical B&B with quantum annealing for integer linear problems|Correct authors Sanavio,Tignone,Ercolessi; Entropy26(4),345(2024), DOI10.3390/e26040345. Oldarxiv2403.09560 is a different DFT paper and is removed.
bozejko2026|https://link.springer.com/article/10.1007/s10479-024-06025-1|Sections3.1/4, Eq16--20, floor-pruning rule; Section5 experimental scope; publisher CiteThisArticle|Finite multiplier-set bounds and integer pruning are prior art; quantum annealing hybrid|Their sign convention u<=0 maps to our nonnegative lambda=-u; local residual capacity maps to their subproblem W. No claim their model certifies our bank or circuit. Large instances ran root-bound calculations only. Online2024; actual issue is AnnalsOR364,2111--2126(2026).
gabbassov2025|https://journals.aps.org/prresearch/abstract/10.1103/53gd-2374|Publisher abstract and bibliographic header|Lagrangian duality in constrained quantum optimization, comparison with QUBO|Different adiabatic/fault-tolerant framework; does not establish this bank's correctness or novelty. PRR7,023305(2025), authors EinarGabbassov,GiliRosenberg,ArturScherer.
martiel2019|https://link.springer.com/chapter/10.1007/978-3-030-38919-2_49|Publisher abstract/metadata, arxiv1908.11291 author version|Concrete implementation of quantum backtracking and resource accounting|CSP graph coloring/SAT, not a full implementation of this LP oracle. Updated to SOFSEM2020,LNCS12011,597--606; key retains historical2019identifier only.
'''
rows=[]
for line in data.strip().splitlines():
    key,url,loc,support,limit=line.split('|')
    rows.append({'key':key,'primary_url':url,'source_location':loc,'supports':support,'limits':limit,
                 'identity_status':'VERIFIED_REAL_RECORD','lr_status':'SUPPORTED_WITH_STATED_SCOPE'})
report={'date':'2026-10-26','scope':'Root quantum/theory-context source audit; not whole-paper validation',
 'references':rows,'rejected_mappings':[
  'Cached .firecrawl/grover1996.md is actually BBHT Tight bounds on quantum searching, quant-ph/9605034; rejected for ref8. Correct Grover is quant-ph/9605043.',
  'Exploratory arxiv1802.07240 is CobaltBFT, not Preskill; rejected. Correct Preskill identifier1801.00862.',
  'Exploratory arxiv1898.11291 typo rejected in the preceding reference plan; correct Martiel1908.11291.',
  'Official AMS volume305 cover says Quantum Computation and Information; arXiv journal-reference field contains a different volume-title wording. Publisher title prevails.',
  'Firecrawl default network resolution failed; escalated scrape returned insufficient credits. No purchase/repeated credit retry; verified cached sources and web fallback used.',
  'Fresh primary metadata changes Bozejko from advance-online2024 to issue2026; original online date retained as note.'
 ],'no_new_experiments':True,'priority_status':'UNRESOLVED; no first/unique or acceptance guarantee asserted'}
(out/'root_reference_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
text=['# Root primary-source audit\n','26 October 2026. Identity and scoped literature-use checks, not whole-paper correctness.\n']
for row in rows:
    text.append(f"## {row['key']}\n\n[Primary source]({row['primary_url']}). {row['source_location']}.\n\nSupports: {row['supports']}.\n\nLimits: {row['limits']}\n")
text.append('## Rejected mappings and limitations\n\n'+'\n'.join('- '+x for x in report['rejected_mappings'])+'\n')
(out/'root_reference_audit.md').write_text('\n'.join(text),encoding='utf-8')
print(f'Recorded {len(rows)} root-audited references.')
