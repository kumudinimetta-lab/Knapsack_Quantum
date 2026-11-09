"""Verified publisher locations and Springer numeric-style compatibility."""
from pathlib import Path
import re,json
OUT=Path(__file__).resolve().parent
p=OUT/'references.bib';s=p.read_text()
updates={
 'ref5':('Berlin, Heidelberg','https://link.springer.com/chapter/10.1007/978-3-642-20465-4_21'),
 'ref11':('Providence, RI','https://userpages.cs.umbc.edu/lomonaco/ams/Special.html'),
 'ref17':('Dagstuhl, Germany','https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2018.5'),
 'bonnetain2020improved':('Cham','https://link.springer.com/chapter/10.1007/978-3-030-64834-3_22'),
 'hamitouche2025':('Auckland, New Zealand','https://www.cs.auckland.ac.nz/research/groups/CDMTCS/researchreports/download.php?selected-id=904'),
 'martiel2019':('Cham','https://link.springer.com/chapter/10.1007/978-3-030-38919-2_49'),
}
for key,(place,url) in updates.items():
    pat=rf'(@\w+\{{{key},)(.*?)(?=\n@|\Z)'
    m=re.search(pat,s,re.S);assert m
    block=m.group(0)
    if not re.search(r'\baddress\s*=',block):block=block.replace(m.group(1),m.group(1)+'\n address={'+place+'},',1)
    if key=='ref17':
        block=block.replace('pages={5:1--5:15}', 'note={Article 5, pp. 5:1--5:15}')
    s=s[:m.start()]+block+s[m.end():]
# Do not invent a publisher city for an author-hosted self-published ebook.
s=s.replace('@book{erickson2019algorithms,','@misc{erickson2019algorithms,')
start=s.index('@misc{erickson2019algorithms,');end=s.index('\n@',start+1)
block=s[start:end].replace('publisher = {Self-published}', 'howpublished = {Self-published textbook, first edition}')
s=s[:start]+block+s[end:]
p.write_text(s,encoding='utf8')
(OUT/'audit/BIBLIOGRAPHY_FORMAT_CHANGES.json').write_text(json.dumps({'checked':'2026-10-27','publisher_locations':updates,'ref17':'Keep exact article/page identifiers in note; stock BST otherwise strips colons into false page range 5--1515.','erickson2019algorithms':'Author-hosted electronic textbook formatted as misc; no publication city invented. All 40 works retained.','erickson_source':'https://jeffe.web.engr.illinois.edu/teaching/algorithms/','class_and_bst':'Official files unmodified.'},indent=2))
