"""Read immutable ledgers, regenerate manuscript tables/figure and provenance."""
from pathlib import Path
import csv, hashlib, json, re, shutil, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
AUDIT = OUT/'audit'
DATA = OUT/'evidence'
DATA.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf8'))
rows = [json.loads(s) for s in (ROOT/'research_log/claim_validation_20261025/root_aware_resource105_rows.jsonl').read_text().splitlines()]
summary = read(ROOT/'research_log/claim_validation_20261025/root_aware_resource105_summary.json')
coverage_rows = [json.loads(s) for s in (ROOT/'research_log/claim_validation_20261025/root_all_reachable_v2_rows.jsonl').read_text().splitlines()]
assert len(rows) == len({r['id'] for r in rows}) == 105
assert all(r['status']=='complete' for r in rows)
assert len(coverage_rows)==1400 and all(r['predicate_floor_mismatches']==0 for r in coverage_rows)
assert sum(r['reachable_states'] for r in coverage_rows)==5204456
assert sum(r['bank_floor_comparisons'] for r in coverage_rows)==20817824
metrics = [('allocated_qubits','Allocated qubits'),('active_qubits','Active qubits'),('cx','CX gates'),('u','Arbitrary-angle $u$ gates'),('depth','Common-basis depth')]
ratios={}
for key,_ in metrics:
    vals=[]
    for r in rows:
        b,c=r['bank_resources'],r['resources']
        if key=='allocated_qubits': x,y=b['qubits'],c['qubits']
        elif key=='active_qubits': x,y=r['bank_active_qubits'],r['interface_plus_touched_qubits']
        elif key=='depth': x,y=b['common_depth'],c['common_depth']
        else:x,y=b['common_counts'][key],c['common_counts'][key]
        vals.append(x/y)
    ratios[key]=vals
    check=dict(n=len(vals),median=statistics.median(vals),minimum=min(vals),maximum=max(vals),lower=sum(x<1 for x in vals),equal=sum(x==1 for x in vals),higher=sum(x>1 for x in vals))
    assert check==summary['ratios'][key], (key,check)
with (DATA/'resource_ratios.csv').open('w',newline='',encoding='utf8') as f:
    writer=csv.writer(f);writer.writerow(['id']+list(ratios))
    for i,r in enumerate(rows):writer.writerow([r['id']]+[ratios[k][i] for k in ratios])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'pdf.fonttype':42,'ps.fonttype':42})
fig,axes=plt.subplots(1,3,figsize=(4.8,2.4),layout='constrained')
for ax,key,title,marker in zip(axes,['cx','active_qubits','depth'],['(a) CX gates','(b) Active qubits','(c) Logical depth'],['o','s','^']):
    ax.plot(range(1,106),sorted(ratios[key]),marker=marker,markersize=2.4,linewidth=0.9,color='#174b70',markevery=3)
    ax.axhline(1,color='#8c3b22',ls='--',lw=0.9)
    ax.set(title=title,xlabel='Sorted instance rank',xlim=(0,106))
    ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Bank / root-aware scan')
fig.savefig(OUT/'resource_ratios.pdf');fig.savefig(AUDIT/'resource_ratios.png',dpi=180);plt.close(fig)

resource = r'''\begin{table}[t]
\caption{Derived paired resource ratios on 105 inputs. Lower/equal/higher compares the bank with the root-aware scan separately on each input}\label{tab:resources}
\centering\small
\begin{tabular}{lrrrr}
\toprule
Resource & Median & Minimum & Maximum & Lower/equal/higher\\
\midrule
'''
for k,label in metrics:
    q=summary['ratios'][k]
    resource += f"{label} & {q['median']:.4f} & {q['minimum']:.4f} & {q['maximum']:.4f} & {q['lower']}/{q['equal']}/{q['higher']}"+r'\\'+'\n'
resource+=r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table}'
coverage=r'''\begin{table}[t]
\caption{Derived exact-arithmetic coverage. Each reachable state is compared with four banks; these are not quantum gate simulations}\label{tab:coverage}
\centering\small
\begin{tabular}{lrrrr}
\toprule
Panel & Inputs & States & Comparisons & Mismatches\\
\midrule
Original & 700 & 3,148,192 & 12,592,768 & 0\\
Reduced cores & 700 & 2,056,264 & 8,225,056 & 0\\
Total & 1,400 & 5,204,456 & 20,817,824 & 0\\
\bottomrule
\end{tabular}
\end{table}'''
for key,value in [('resource_table.tex',resource),('coverage_table.tex',coverage)]:
    (AUDIT/key).write_text(value,encoding='utf8')
main=(OUT/'main.tex').read_text(encoding='utf8')
for key,value in [('RETAINED_LITERATURE',(AUDIT/'retained_literature.tex').read_text()),('COVERAGE_TABLE',coverage),('RESOURCE_TABLE',resource)]:
    marker='% '+key
    if marker in main:main=main.replace(marker,value)
(OUT/'main.tex').write_text(main,encoding='utf8')
paths=[
 'research_log/claim_validation_20261025/VALIDATION_VERDICT.md',
 'research_log/claim_validation_20261025/theory_claim_audit.md',
 'research_log/claim_validation_20261025/theory_adversarial_audit_v2.json',
 'research_log/claim_validation_20261025/root_all_reachable_v2_summary.json',
 'research_log/claim_validation_20261025/root_all_reachable_v2_rows.jsonl',
 'research_log/claim_validation_20261025/root_aware_resource105_summary.json',
 'research_log/claim_validation_20261025/root_aware_resource105_rows.jsonl',
 'research_log/claim_validation_20261025/root_aware_validation.json',
 'research_log/claim_validation_20261025/final_crosscheck.json',
 'research_log/claim_validation_20261025/circuit_vertex_adversarial.json',
 'research_log/claim_validation_20261025/circuit_vertex_adversarial_resume.json',
 'research_log/claim_validation_20261025/theory_phase_preparation_triage_v2.json',
 'research_log/pruning_study_20261023/inputs.json',
 'research_log/pruning_study_20261023/inputs_core700.json',
 'research_log/source_faithful_20261024/qft_bank_full105_manifest.json',
 'research_log/references_literature_20261026/COMPLETE_REFERENCE_AUDIT.json',
 'research_log/references_literature_20261026/FINAL_AUDIT.md',
]
manifest={}
for rel in paths:
    p=ROOT/rel;dest=DATA/p.name
    shutil.copy2(p,dest);manifest[rel]={'sha256':sha(p),'local_copy':str(dest.relative_to(OUT))}
source_paths=[
 'simulation/source_faithful_20261024/qft_bank.py',
 'simulation/source_faithful_20261024/compressed_bank.py',
 'simulation/source_faithful_20261024/continuous_bank.py',
 'simulation/source_faithful_20261024/resource_profile.py',
 'simulation/source_faithful_20261024/qft_normal_form.py',
 'simulation/source_faithful_20261024/qft_reconstruction.py',
 'research_log/claim_validation_20261025/root_aware_control.py',
 'research_log/claim_validation_20261025/root_aware_experiments.py',
 'research_log/claim_validation_20261025/root_all_reachable_coverage.py',
 'research_log/claim_validation_20261025/theory_adversarial_audit.py',
 'research_log/claim_validation_20261025/circuit_vertex_adversarial.py',
 'research_log/claim_validation_20261025/circuit_vertex_adversarial_resume.py',
 'research_log/pruning_study_20261023/tree_experiments.py',
 'research_log/pruning_study_20261023/make_core_inputs.py',
 'simulation/exact_knapsack.py',
 'simulation/benchmark_v5.py',
]
for rel in source_paths:
    p=ROOT/rel;dest=DATA/'source_snapshots'/rel
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    manifest[rel]={'sha256':sha(p),'local_copy':str(dest.relative_to(OUT)),'note':'Source snapshot; imports use original project tree'}
(DATA/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
abstract=re.search(r'\\abstract\{(.*?)\}\s*\\keywords',main,re.S).group(1)
count=len(abstract.split());assert 150<=count<=250,count
keys=set(re.findall(r'@\w+\s*\{([^,]+),',(OUT/'references.bib').read_text()))
cites=set(k.strip() for m in re.findall(r'\\cite\w*\{([^}]+)\}',main) for k in m.split(','))
assert not cites-keys,cites-keys
(AUDIT/'ASSEMBLY_CHECKS.json').write_text(json.dumps({'abstract_words_whitespace':count,'bib_entries':len(keys),'cited':len(cites),'uncited':sorted(keys-cites),'resource_rows':len(rows),'arithmetic_states':5204456,'ratio_reaggregation_conflicts':0},indent=2))
print('Abstract words:',count,'References:',len(keys),'Cited:',len(cites),'Uncited:',sorted(keys-cites))
