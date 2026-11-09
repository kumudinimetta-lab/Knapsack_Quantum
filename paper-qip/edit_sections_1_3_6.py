from pathlib import Path
import shutil,difflib
p=Path(__file__).resolve().parent
b=p/'backups/before_sections_1_3_6_20261027';b.mkdir(exist_ok=False)
for n in ['main.tex','main.pdf','qip_latex_review_bundle.zip']:shutil.copy2(p/n,b/n)
f=p/'main.tex';old=f.read_text(encoding='utf8');s=old
changes={
'The 0/1 knapsack problem is one of the most studied problems in combinatorial optimization: given items with weights and values and a capacity, find the subset of greatest total value whose weight does not exceed the capacity.':'The 0/1 knapsack problem asks for a subset of maximum total value whose total weight does not exceed a given capacity.',
'The contribution examined here is their specific combination with coverage certificates for the integer LP predicate and a matched reversible-resource comparison. We do not assert historical priority for the general use of LP or Lagrangian bounds in quantum optimization.':'The contribution is a construction combining these techniques with coverage certificates for the integer LP predicate and a matched reversible-resource comparison.',
'Fourth, it separates exhaustive arithmetic coverage, small-circuit simulation, and large-instance logical resource estimates. The strongest comparison includes a root-aware scan control and shows a depth penalty despite lower gate counts and qubit requirements.':'Fourth, it evaluates arithmetic coverage, small-circuit behavior, and logical resources separately. The comparison with a root-aware scan control shows lower gate counts and qubit requirements alongside increased median depth.',
r'Let $w_i\in\mathbb Z_{>0}$, $v_i\in\mathbb Z_{\geq0}$, and $W\in\mathbb Z_{\geq0}$.':r'Consider $n$ items with weights $w_i\in\mathbb Z_{>0}$, profits $v_i\in\mathbb Z_{\geq0}$, and capacity $W\in\mathbb Z_{\geq0}$.',
'This oracle excludes an improving completion; it does not certify that a surviving prefix has an integer feasible completion.':r'Rejection rules out every feasible completion reaching $\tau$; nonrejection does not guarantee such a completion.',
'A variable is fixed only when the LP bound under the opposite assignment is strictly below $L$.':r'A variable is fixed only when the opposite assignment is infeasible or its LP bound is strictly below $L$.',
'Reference optima are used only to audit the saved transformations, not to select bank entries.':'Exact reference optima are used only to check the transformations, not to select bank entries.',
'Between consecutive endpoints choose a rational representative. Membership is constant within each such cell.':'Choose a rational representative between each pair of consecutive endpoints and one above the greatest endpoint. Membership is constant within each such cell.',
'This is a derived illustration, separate from the benchmark cohorts.':'This analytical example is separate from the benchmark cohorts.',
'We do not treat this preprocessing as free, or claim that minimum-cardinality banks imply an end-to-end acceleration. Saved work budgets retain a root-tail fallback if a compilation cap is reached; such a fallback preserves the predicate but carries no minimum-cardinality claim.':'Preprocessing costs must therefore be included in any end-to-end performance assessment. If a compilation budget is exceeded, the constructors return the root-tail bank; its coverage is preserved, but minimality is not certified.',
'Use one-based indices $i=1,\\ldots,m$ and take':r'For $i=1,\ldots,m$, take',
'This is a cardinality limitation on an easy optimization family, not a knapsack hardness or quantum-query lower bound.':'The lower bound concerns bank cardinality; the family itself is easy to optimize.',
'All coefficients are compiled from the classical instance and bank; no division of quantum data or truncation of item efficiencies is performed. This construction concerns a decision predicate, rather than a fixed-point approximation to the numerical LP value.':'All coefficients are compiled from the classical instance and bank. The circuit evaluates the decision predicate using integer coefficients, without quantum division or efficiency truncation.',
r'Let $t=\max(1,\operatorname{bitlength}(1+\sum_i v_i))$':r'Write $\operatorname{bitlength}(u)=\lceil\log_2(u+1)\rceil$ for nonnegative integers $u$. Let $t=\max(1,\operatorname{bitlength}(1+\sum_i v_i))$',
'and the inspected arithmetic primitives in Wilkening et al., Supplement':'and the arithmetic primitives described by Wilkening et al., Supplement',
'Its existing input validator requires strictly positive profits, whereas the QFT bank accepts zero profits. Their test domains are reported separately.':'The Boolean implementation requires strictly positive profits, whereas the QFT implementation accepts zero profits; their test domains are reported separately.',
'The combination is OR, not parity: two true rejection conditions must still reject.':'Logical OR ensures that simultaneous rejection conditions still produce rejection.',
"The fixed-depth QFT interface does not implement a coherent depth register, tree reflections, or a full quantum walk. The Boolean builder's separately tested depth encoding does not establish those missing QFT or walk operations. Thus the resource comparison below is for fixed-depth bounding predicates, not for a complete quantum B\\&B algorithm.":r'The resource comparison concerns fixed-depth bounding predicates. Integrating them into a quantum search requires coherent node handling and tree reflections, which are outside this implementation.',
r'\subsection{A stronger fractional-scan control}':r'\subsection{Root-aware fractional-scan control}',
r'This is our root-aware reconstruction, not a released LP-oracle netlist from Wilkening et al.\ \cite{wilkening2025,wilkening2025code}. Both sides use serial shared workspace and the same local inverse-cancellation rule. Copied-control parallel schedules, further arithmetic rewrites, and classical-threshold specialization could change the comparison. Minimum-bank cardinality is not used as a claim of optimal circuit cost.':r'The root-aware control is reconstructed from the published arithmetic primitives, rather than taken from a released LP-oracle netlist \cite{wilkening2025,wilkening2025code}. Both implementations use serial shared workspace and the same local inverse-cancellation rule. The comparison is specific to these implementations and does not establish optimal circuit cost.',
'The main arithmetic panel contains 700 saved instances':'The main arithmetic panel contains 700 instances',
"These are the project's saved generator definitions, not a claim of using an external solver's benchmark implementation. Exact arrays and seeds are retained in the input registries.":'Exact arrays and seeds are retained in the input registries.',
'It is not selected by observed resource savings.':'This selection is independent of the observed resource ratios.',
r'We classify exact rational coverage and logical netlist counts as \textsc{Derived}; actual propagation through gates as \textsc{Simulated}; host elapsed times as \textsc{Measured}; fixed tolerances and budgets as \textsc{Hardcoded}; and planned but unexecuted work as \textsc{Scheduled}. No scheduled test is included in a completed count. Derived gate counts, arbitrary-angle rotations, and logical depth are not hardware measurements, fault-tolerant T counts, or device execution times.':r'Exact rational coverage and logical netlist counts are classified as \textsc{Derived}, propagation through gates as \textsc{Simulated}, and host elapsed times as \textsc{Measured}. Tolerances and computational budgets are fixed settings (\textsc{Hardcoded}). Logical gate counts and depth exclude physical routing, rotation synthesis, and device execution time.',
'96 new-seed instances of size 3--7':'96 additional instances of size 3--7',
'Deliberate counterexamples to extensions of the assumptions are retained rather than counted as failures of the scoped theorem.':'Counterexamples delimiting the assumptions are given in Appendix~\\ref{app:counterexamples}.',
r"For resources, each native gate is expanded into Qiskit's $\{u,\mathrm{CX}\}$ basis at optimization level zero, with all-to-all connectivity. Depth is obtained by dependency scheduling of that expanded gate list.":r"For resource accounting, Qiskit generates a $\{u,\mathrm{CX}\}$ decomposition template for each native gate type at optimization level zero. The profiler applies these templates to the circuit gate list, assuming all-to-all connectivity, and computes depth by dependency scheduling.",
'The common inverse-cancellation pass removes literal inverses across disjoint gates; it is not a claim of globally optimal compilation.':'The common inverse-cancellation pass removes literal inverses separated only by gates acting on disjoint wires.',
'Caps and errors are retained as statuses, not silently omitted.':'Capped and failed runs are retained with explicit status labels.',
}
for a,z in changes.items():
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,z)
start=s.index(r'\subsection{AI-assisted research and manuscript preparation}')
end=s.index(r'\section{Results}',start)
s=s[:start]+s[end:]
declaration=r'''\subsection*{Use of generative AI}
OpenAI ChatGPT/Codex assisted with literature searches, mathematical drafting, counterexample exploration, code development, experiment orchestration, source checks, and manuscript preparation.
'''
s=s.replace(r'\subsection*{Data and code availability}',declaration+r'\subsection*{Data and code availability}')
assert old.split(r'\section{Literature Review}')[1].split(r'\section{Problem and pruning contract}')[0]==s.split(r'\section{Literature Review}')[1].split(r'\section{Problem and pruning contract}')[0]
assert old.split(r'\abstract{')[1].split(r'\keywords')[0]==s.split(r'\abstract{')[1].split(r'\keywords')[0]
f.write_text(s,encoding='utf8')
(p/'audit/sections_1_3_6.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='before',tofile='after')),encoding='utf8')
