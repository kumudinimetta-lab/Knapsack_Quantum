from pathlib import Path
import shutil,difflib,re
p=Path(__file__).resolve().parent
b=p/'backups/before_sections_7_9_20261027';b.mkdir(exist_ok=False)
for n in ['main.tex','main.pdf','qip_latex_review_bundle.zip']:shutil.copy2(p/n,b/n)
f=p/'main.tex';old=f.read_text(encoding='utf8');s=old
start=s.index(r'\subsection*{Use of generative AI}')
end=s.index(r'\subsection*{Data and code availability}',start)
s=s[:start]+s[end:]
changes={
'Their state count includes 59 states omitted by an earlier all-fit compiler shortcut; the present count enumerates them explicitly. The input registry also contains 15 scaled and 5 tiny auxiliary records, outside the declared main700 panel. Those records are not silently pooled into this experiment.':'All reachable states of these cases are included. The 15 scaled and 5 tiny auxiliary records in the input registry are outside the declared 700-instance panel.',
r'\subsection{Finite gate-validation scope and a retained failure}':r'\subsection{Gate-level checks and initialization discrepancy}',
'The resumed QFT count includes five already completed method-cases and 544 columns from the original run only once.':'Each method-case is counted once; different circuit forms are not independent problem instances.',
'One original coherent test failed and is retained.':'A coherent test using partial-register initialization failed.',
'an opaque partial-register initialization followed by Aer matrix-product-state simulation':'partial-register initialization followed by Aer matrix-product-state simulation',
'Separate investigations reproduced an incorrect prepared state before any oracle gates.':'Preparation-only checks reproduced an incorrect state before any oracle gates.',
'The underlying backend initialization defect remains unresolved; that initialization path is excluded as a trusted validation method, and its failed record remains available. No oracle change or tolerance relaxation was used to resume the tests.':'The cause of the initialization discrepancy remains unresolved, so this preparation path is excluded from the supporting correctness evidence. The failed result is retained; the successful checks use the same oracle and numerical tolerance.',
'These bounded tests support the implementation on their stated inputs; they do not establish exhaustive gate validation of the large cohort.':'These checks cover the stated small inputs; the 105-input resource cohort is not exhaustively gate-simulated.',
'An earlier scan control retained fractional calculations at positions where a split was impossible. Removing those terms strengthens the baseline and changes the comparison. Likewise, excluding truly idle workspace while retaining interface wires changes the qubit accounting. We therefore use the root-aware, active-wire comparison as the principal result; older counts remain in the research record. No comparison here establishes superiority over an optimized released implementation, a fault-tolerant architecture, or a classical knapsack solver.':'The control omits fractional calculations before the earliest possible split, and active-qubit counts exclude unused workspace while retaining all interface wires. The reported ratios apply to this matched comparison, not to an optimal implementation or a classical knapsack solver.',
'The central distinction is semantic: a certified bank preserves the LP rejection decision at integer targets while allowing its fractional value to differ.':'A certified bank preserves the LP rejection decision at integer targets while allowing its fractional value to differ.',
'The contribution supported by these results is the scoped compiler and its reversible resource tradeoff.':'These results support a compiler for the stated prefix predicate and quantify its reversible resource tradeoff.',
'Neither is claimed as new. The minimum-cardinality interval reduction concerns a specific all-prefix predicate contract and does not imply minimum gate count.':'The contribution concerns the all-prefix coverage construction and its implementation; minimum bank cardinality does not imply minimum gate count.',
'The circuit contract excludes arbitrary branching orders, rational objective thresholds, negative profits or weights, and dirty initial workspace.':'The circuit contract requires positive integer weights, nonnegative integer profits, a fixed efficiency-ordered prefix, representable integer thresholds, and clean initial workspace.',
'The large arithmetic coverage experiment proves no general simulator reliability claim; the retained initialization failure illustrates why independent preparation and dense-reference checks matter.':'Arithmetic coverage and gate-level simulation establish different properties; the initialization discrepancy demonstrates the need for preparation-only and independent dense-reference checks.',
'Further work can compare copied-control schedules, tighter arithmetic widths, alternative bank-selection objectives, and rotation-synthesis error budgets on the same predicate contract. Such comparisons may reduce or reverse individual resource advantages. Public release and independent reproduction of the full evidence package remain necessary steps before final submission.':'The resource tradeoff depends on the arithmetic layout and compilation model. Alternative implementations may change the relative gate counts, qubit requirements, and depth.',
'Exact arithmetic audits cover both original and reduced-core instances, while separately scoped small-circuit tests check gate behavior and expose an unreliable initialization path.':'Exact arithmetic checks cover the original and reduced-core instances, and separate small-circuit simulations test the reversible predicate.',
}
for a,z in changes.items():
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,z)
assert not re.search(r'\b(?:AI|OpenAI|ChatGPT|Codex)\b|generative AI|AI-assisted',s,re.I)
assert old.split(r'\section{Results}')[0]==s.split(r'\section{Results}')[0]
f.write_text(s,encoding='utf8')
(p/'audit/sections_7_9.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='before',tofile='after')),encoding='utf8')
