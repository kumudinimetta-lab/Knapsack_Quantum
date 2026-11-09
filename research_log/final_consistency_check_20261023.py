"""Cross-check reported counts and archived table values against actual files."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def main():
    tex=(ROOT/'paper/main.tex').read_text(encoding='utf-8')
    bib=(ROOT/'paper/references.bib').read_text(encoding='utf-8')
    abstract=re.search(r'\\abstract\{(.*?)\}\n',tex,re.S).group(1)
    keywords=re.search(r'\\keywords\{(.*?)\}',tex).group(1).split(',')
    citations={key for group in re.findall(r'\\cite\{([^}]+)\}',tex) for key in group.split(',')}
    entries=set(re.findall(r'@\w+\{([^,]+),',bib))
    assert citations==entries
    assert 80<=len(abstract.split())<=100 and 4<=len(keywords)<=6
    assert not any(ord(c)<32 and c not in '\n\r' for c in tex)
    ref=json.loads((ROOT/'research_log/revision_20261022_reference_results.json').read_text())['reference']
    oracle=json.loads((ROOT/'research_log/revision_20261022_oracle_results.json').read_text())['oracle']['rows']
    spectral=json.loads((ROOT/'research_log/revision_20261022_spectral_results.json').read_text())['summary']
    recovery=json.loads((ROOT/'research_log/revision_20261022_recovery_results.json').read_text())['recovery']
    coherent=json.loads((ROOT/'research_log/revision_20261023_coherent_h_results.json').read_text())['rows']
    assert ref['instances']==700 and ref['fixing_mismatches']==ref['bb_mismatches']==ref['capped']==0
    assert len(oracle)==700 and sum(r['statevector_columns'] for r in oracle)==15859712
    assert all(r['depth']==3 and r['predicate_mismatches']==r['dirty_columns']==0 for r in oracle)
    assert spectral['conditions']==1200 and spectral['completed']==889
    assert spectral['endpoint_violations']==spectral['predicate_disagreements']==0
    assert len(recovery['rows'])==135 and recovery['mismatches']==recovery['capped']==0
    assert [r['statevector_columns'] for r in coherent]==[8192,8192,1024]
    assert all(r['predicate_mismatches']==r['dirty_columns']==0 for r in coherent)
    archive=json.loads((ROOT/'simulation/classical_benchmark/raw_results/benchmark_data.json').read_text())
    groups=defaultdict(list)
    for row in archive:
        if row['or_opt'] and not row['bb_hit_limit']:
            groups[(row['type'],row['n'])].append(row)
    labels={'Uncorrelated':'uncorrelated','Weakly correlated':'weakly_correlated',
            'Subset sum':'subset_sum','Strongly correlated':'strongly_correlated',
            'Inverse strongly':'inverse_strongly'}
    table=tex[tex.index(r'\label{tab:ortools_cat_a}'):tex.index(r'\label{tab:ortools_cat_b}')]
    table_checks=[]
    for line in table.splitlines():
        cells=[c.strip() for c in line.replace('\\\\','').split('&')]
        if len(cells)!=6 or cells[0] not in labels:
            continue
        key=(labels[cells[0]],int(cells[1]))
        rows=groups[key]
        expected=[format(float(np.mean([r['m'] for r in rows])),'.1f'),
                  format(float(np.mean([r['or_time'] for r in rows])),'.4f'),
                  format(float(np.mean([r['total_our_time'] for r in rows])),'.4f')]
        assert cells[2]==str(len(rows))+'/5'
        assert cells[3:]==expected,(key,cells[3:],expected)
        table_checks.append({'class':key[0],'n':key[1],'pairs':len(rows),'values':expected})
    assert len(table_checks)==16
    result={'date':'2026-10-23','abstract_words':len(abstract.split()),
            'keywords':len(keywords),'verified_cited_entries':len(entries),
            'archived_table_rows_checked':len(table_checks),'table_values':table_checks,
            'reference_instances':ref['instances'],'reference_mismatches':0,
            'oracle_columns':sum(r['statevector_columns'] for r in oracle),
            'oracle_mismatches':0,'oracle_dirty_columns':0,
            'spectral_completed':spectral['completed'],'spectral_mismatches':0,
            'recovery_instances':len(recovery['rows']),'recovery_mismatches':0,
            'coherent_h_columns':sum(r['statevector_columns'] for r in coherent),
            'coherent_h_mismatches':0,
            'manuscript_sha256':hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest()}
    (ROOT/'research_log/revision_20261023_final_consistency.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items()if k!='table_values'},indent=2))


if __name__=='__main__':
    main()
