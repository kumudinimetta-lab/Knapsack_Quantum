"""Keep only cited, source-checked entries; preserve the old file in backups."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
old=(ROOT/'paper/backups/2026-10-22_before_revision/references.bib').read_text(encoding='utf-8')
entries={}
for chunk in re.split(r'(?=^@)',old,flags=re.M):
    match=re.match(r'@\w+\{([^,]+),',chunk)
    if match:
        entries[match.group(1)]=chunk.strip()
keep=['ref1','ref2','ref3','ref4','ref8','ref11','ref24','ref35',
      'draper2000','vedral1996','thapliyal2016','martello1999combo']
dois={'ref1':'10.1287/opre.5.2.266','ref2':'10.1145/321812.321823',
      'ref3':'10.1007/978-3-540-24777-7','ref4':'10.1287/opre.47.4.570',
      'ref8':'10.1145/237814.237866','ref24':'10.1103/PhysRevResearch.2.013056',
      'ref35':'10.4086/toc.2018.v014a015','vedral1996':'10.1103/PhysRevA.54.147',
      'martello1999combo':'10.1287/mnsc.45.3.414'}
result=[]
for key in keep:
    entry=entries[key]
    if key in dois:
        entry=entry[:-1].rstrip()+',\n  doi = {'+dois[key]+'}\n}'
    if key=='ref24':
        entry=entry[:-1].rstrip()+',\n  pages = {013056}\n}'
    if key=='thapliyal2016':
        entry=r'''@misc{thapliyal2016,
  author = {Himanshu Thapliyal and T. S. S. Varun and Edgard Munoz-Coreas},
  title = {Quantum Circuit Design of Integer Division Optimizing Ancillary Qubits and {T}-Count},
  year = {2016},
  eprint = {1609.01241},
  archivePrefix = {arXiv},
  url = {https://arxiv.org/abs/1609.01241}
}'''
    if key=='draper2000':
        entry=r'''@misc{draper2000,
  author = {Thomas G. Draper},
  title = {Addition on a Quantum Computer},
  year = {2000},
  eprint = {quant-ph/0008033},
  archivePrefix = {arXiv},
  url = {https://arxiv.org/abs/quant-ph/0008033}
}'''
    result.append(entry)
result.append(r'''@article{wilkening2025,
  author = {S{\"o}ren Wilkening and Andreea-Iulia Lefterovici and Lennart Binkowski and Michael Perk and S{\'a}ndor P. Fekete and Tobias J. Osborne},
  title = {A quantum algorithm for solving 0-1 Knapsack problems},
  journal = {npj Quantum Information},
  volume = {11},
  pages = {146},
  year = {2025},
  doi = {10.1038/s41534-025-01097-8}
}''')
result.append(r'''@article{creemers2025,
  author = {Stefan Creemers and Luis Fernando P{\'e}rez Armas},
  title = {Discrete optimization: A quantum revolution?},
  journal = {European Journal of Operational Research},
  volume = {323},
  number = {2},
  pages = {378--408},
  year = {2025},
  doi = {10.1016/j.ejor.2024.12.016}
}''')
result.append(r'''@article{bozejko2026,
  author = {Wojciech Bo{\.z}ejko and Anna Burduk and Jaros{\l}aw Pempera and Mariusz Uchro{\'n}ski and Mieczys{\l}aw Wodecki},
  title = {Optimal solving of a binary knapsack problem on a {D-Wave} quantum machine and its implementation in production systems},
  journal = {Annals of Operations Research},
  volume = {364},
  pages = {2111--2126},
  year = {2026},
  note = {First published online 13 May 2024},
  doi = {10.1007/s10479-024-06025-1}
}''')
# Raw strings above intentionally contain ordinary LaTeX accent commands.
text='\n\n'.join(result)+'\n'
text=text.replace('\\\\','\\')
(ROOT/'paper/references.bib').write_text(text,encoding='utf-8')
print('Retained verified cited entries:',len(result))


if __name__=='__main__':
    pass
