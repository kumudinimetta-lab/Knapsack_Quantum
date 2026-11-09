"""Scientific plots of final derived proxies; no fitted validation curve."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
summary=json.loads((HERE/'paired_summary.json').read_text(encoding='utf8'))
fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
names={'simple':'Profit only','root_dual':'Root dual','bank2':'Bank 2','bank4':'Bank 4'}
colors={'simple':'#777777','root_dual':'#0072B2','bank2':'#009E73','bank4':'#D55E00'}
for ax,cat,title in zip(axes,['main700','core700'],['Original inputs','After exact fixing']):
    for method,label in names.items():
        rows=[r for r in summary['proxy_pairs'] if r['category']==cat and r['group']=='ALL'
            and r['weak']==method and r['metric']=='ccx' and r['target_kind']=='incumbent_plus_one'
            and r['subset']=='requires_detection_complete']
        rows=sorted(rows,key=lambda r:r['overhead_exact_cost_units'])
        if rows:
            ax.plot([r['overhead_exact_cost_units'] for r in rows],[r['median'] for r in rows],
                marker='o',color=colors[method],label=label+' (n='+str(rows[0]['n'])+')')
    ax.axhline(1,color='black',ls='--',lw=1)
    ax.set_xscale('symlog',linthresh=.25);ax.set_yscale('log')
    ax.set_xlim(0,110)
    ax.set_xticks([0,.25,1,10,100],labels=['0','0.25','1','10','100'])
    ax.set_xlabel('Shared overhead h / exact-predicate CCX cost')
    ax.set_title(title);ax.grid(True,axis='y',alpha=.2);ax.legend(fontsize=8)
axes[0].set_ylabel('Median conditional work ratio vs exact LP\n(C + h) sqrt(T) / (C_exact + h) sqrt(T_exact)')
fig.suptitle('DERIVED overhead sensitivity; lower ratios use less modeled work',fontsize=12)
fig.text(.5,.01,'Complete tree/resource pairs only, initial-incumbent + 1; classically resolved and root-rejected pairs excluded.\n'
    'Caps are retained in the ledger. Predicate model only: no full quantum walk, physical runtime, or measured speedup.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.12,1,.94))
for ext in ['png','svg']: fig.savefig(HERE/('overhead_sensitivity.'+ext),dpi=200)
print('saved overhead_sensitivity.png / .svg')
