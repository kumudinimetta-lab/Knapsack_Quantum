"""Vector explanatory figures; worked-example numbers checked exactly first."""
from pathlib import Path
from fractions import Fraction as Q
import itertools,json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'paper-qip'
sys.path.insert(0,str(ROOT))
from research_log.claim_validation_20261025.theory_adversarial_audit import vertices,all_subset_interval

w=[1,1];v=[1,1];W=1;lam=Q(1,2);states={};checks=0
for d in range(3):
 for x in itertools.product((0,1),repeat=d):
  R=W-sum(x);P=sum(x)
  if R<0:continue
  U=vertices(w[d:],v[d:],R)
  F=lam*R+sum(max(Q(vi)-lam*wi,0) for wi,vi in zip(w[d:],v[d:]))
  assert U.numerator//U.denominator==F.numerator//F.denominator
  for tau in range(4):assert (P+U<tau)==(P+F<tau);checks+=1
  interval=all_subset_interval(w[d:],v[d:],R,U.numerator//U.denominator+1)
  states[d,R]=(U,F,interval)
expected={(0,1):(Q(0),True,Q(2)),(1,1):(Q(0),False,Q(2)),(1,0):(Q(0),True,None),(2,1):(Q(0),False,Q(1)),(2,0):(Q(0),False,None)}
assert {k:r[2] for k,r in states.items()}==expected
assert len(states)==5
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,1,figsize=(4.8,4.4),layout='constrained',gridspec_kw={'height_ratios':[1,1.1]})
ax=axes[0];xs=[i/100 for i in range(221)];ys=[x+2*max(1-x,0) for x in xs]
ax.fill_between([0,2.2],[1,1],[2,2],color='#e9eef3',label=r'Equal-floor band $[1,2)$')
ax.plot(xs,ys,color='#174b70',lw=1.7,label=r'Root dual bound $F_0(1,\lambda)$')
ax.axhline(1,color='#45535d',ls=':',lw=1.2,label=r'Root LP value $U_0(1)=1$')
ax.axhline(2,color='#8c3b22',ls='--',lw=1)
ax.scatter([.5],[1.5],marker='D',s=27,color='#8c3b22',zorder=4)
ax.annotate(r'$\lambda=1/2$: bound $3/2$, floor $1$',xy=(.5,1.5),xytext=(.7,1.73),fontsize=8,arrowprops={'arrowstyle':'-','lw':.6})
ax.set(xlim=(-.04,2.2),ylim=(.85,2.25),ylabel='Residual upper bound',title='(a) Same floor, different fractional values')
ax.set_xticks([0,.5,1,1.5,2]);ax.grid(alpha=.18);ax.legend(loc='lower right',fontsize=7.2,frameon=True,facecolor='white',edgecolor='none',framealpha=1)
ax=axes[1]
ordered=[(0,1),(1,1),(1,0),(2,1),(2,0)]
for y,key in enumerate(ordered):
 lo,opened,hi=expected[key];right=float(hi) if hi is not None else 2.15
 ax.plot([float(lo),right],[y,y],color='#174b70',lw=2)
 ax.scatter([float(lo)],[y],s=24,facecolors='white' if opened else '#174b70',edgecolors='#174b70',zorder=3)
 if hi is not None:ax.scatter([right],[y],s=24,facecolors='white',edgecolors='#174b70',zorder=3)
 else:ax.annotate('',xy=(2.2,y),xytext=(2.05,y),arrowprops={'arrowstyle':'->','color':'#174b70','lw':1.3})
ax.axvline(.5,color='#8c3b22',ls='--',lw=1.2,label=r'One bank point: $B=\{1/2\}$')
ax.set_yticks(range(5),[rf'$d={d},\ R={r}$' for d,r in ordered]);ax.invert_yaxis()
ax.set(xlim=(-.04,2.25),ylim=(4.8,-.65),xlabel=r'Multiplier $\lambda$',title='(b) One rational multiplier covers all five states')
ax.set_xticks([0,.5,1,1.5,2]);ax.grid(axis='x',alpha=.15);ax.legend(loc='lower right',fontsize=8,frameon=False)
fig.savefig(OUT/'integer_coverage_example.pdf');fig.savefig(OUT/'audit/integer_coverage_example.png',dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(4.8,3.5));fig.subplots_adjust(left=.015,right=.985,top=.97,bottom=.02)
ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
def box(x,y,width,height,label,fill):
 ax.add_patch(FancyBboxPatch((x,y),width,height,boxstyle='round,pad=0.08,rounding_size=0.08',linewidth=.8,edgecolor='#354957',facecolor=fill))
 ax.text(x+width/2,y+height/2,label,ha='center',va='center',fontsize=8.4,linespacing=1.4)
def arrow(x1,y1,x2,y2):ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'->','lw':1,'color':'#354957'})
ax.text(.15,7.55,'(a) Classical preparation for a fixed instance',fontsize=9,weight='bold')
box(.15,5.8,2.65,1.15,'Integer instance\nFixed efficiency order','#e9eef3')
box(3.65,5.8,2.65,1.15,'Construct bank\nCertify coverage','#e9eef3')
box(7.15,5.8,2.65,1.15,'Compile constants\nand register widths','#e9eef3')
arrow(2.9,6.37,3.5,6.37);arrow(6.4,6.37,7,6.37)
ax.text(.15,4.75,'(b) Reversible evaluation at fixed depth',fontsize=9,weight='bold')
ax.text(5,4.12,r'Input: $|x\rangle\,|\tau\rangle\,|z\rangle\,|0^a\rangle$',ha='center',fontsize=9)
box(.15,2.35,2.65,1.25,'Compute capacity\nand bound flags;\nform their OR','#edf3ed')
box(3.65,2.35,2.65,1.25,'XOR the OR flag\ninto output $z$','#edf3ed')
box(7.15,2.35,2.65,1.25,'Reverse all\nwork computation','#edf3ed')
arrow(2.9,2.97,3.5,2.97);arrow(6.4,2.97,7,2.97)
ax.text(5,1.45,r'Output: $|x\rangle\,|\tau\rangle\,|z\oplus f(x,\tau)\rangle\,|0^a\rangle$',ha='center',fontsize=9)
ax.text(5,.55,'Inputs preserved; workspace restored to zero',ha='center',fontsize=8.5)
fig.savefig(OUT/'oracle_workflow.pdf');fig.savefig(OUT/'audit/oracle_workflow.png',dpi=180);plt.close(fig)
result={'classification':'DERIVED exact illustrative example; schematic is explanatory, not an experiment','weights':w,'profits':v,'capacity':W,'bank':[[1,2]],'reachable_states':len(states),'integer_threshold_comparisons':checks,'mismatches':0,'state_data':[{ 'depth':d,'R':r,'LP':str(a),'bank_bound':str(b),'interval':[str(c[0]),c[1],None if c[2] is None else str(c[2])]} for (d,r),(a,b,c) in states.items()]}
(OUT/'audit/FIGURE_EXAMPLE_CHECKS.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
