from pathlib import Path
import shutil,difflib,re
p=Path(__file__).resolve().parent
b=p/'backups/before_requested_small_fixes_20261027';b.mkdir(exist_ok=False)
for n in ['main.tex','main.pdf','qip_latex_review_bundle.zip']:shutil.copy2(p/n,b/n)
f=p/'main.tex';old=f.read_text(encoding='utf8');s=old
changes={
r'We maximize $\sum_i v_i x_i$ subject to $\sum_i w_i x_i\leq W$ and':r'We maximize $\sum_{i=1}^{n} v_i x_i$ subject to $\sum_{i=1}^{n} w_i x_i\leq W$ and',
r'q=\max\left(1,1+\operatorname{bitlength}\left(\max_{\lambda\in B}\{C_\lambda,M_\lambda\}\right)\right).':r'q=\max\Bigl\{1,\,1+\operatorname{bitlength}\!\left(\max_{\lambda\in B}\{C_\lambda,M_\lambda\}\right)\Bigr\}.',
'The all-zero full leaf adds $[0,1/W)$, disjoint from all of them because their smallest lower endpoint is 2.':r'The all-zero full leaf adds $[0,1/W)$, disjoint from all of them: $\rho_m=5/2$ gives the lowest interval $(2,3)$, whose lower endpoint $5/2-1/2=2$ exceeds $1/W$.',
'Integrating them into a quantum search requires coherent node handling and tree reflections, which are outside this implementation.':r'Integrating them into a quantum search requires coherent node handling and tree reflections, which are outside this implementation. An extension to superpositions of depths would also require depth-controlled prefix arithmetic; its synthesis costs are not included here.',
'Thus fewer gates do not imply a shallower circuit.':'The bank reuses one accumulator for successive compute--flag--uncompute evaluations, creating dependencies between multipliers. The scan instead uses separate weight, profit, residual-capacity, and comparison registers in a single suffix pass. These layouts permit different degrees of parallelism, so fewer gates need not imply a shallower circuit.',
}
for a,z in changes.items():
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,z)
# Natural prose keeps the metric semantics established in Section 6.1.
sec=s.index(r'\section{Results}');end=s.index(r'\section{Discussion',sec)
before,body,after=s[:sec],s[sec:end],s[end:]
body=body.replace(r' (\textsc{Derived})','').replace(r' (\textsc{Simulated})','')
body=body.replace(r' (\textsc{Simulated}; tolerance \textsc{Hardcoded})','')
body=body.replace(r'These errors are \textsc{Derived} comparisons of \textsc{Simulated} amplitudes.','These errors compare simulated complex amplitudes with the expected states.')
body=body.replace(r'All numbers in this comparison are \textsc{Derived} logical resources.','These quantities are logical resources derived from the compiled gate lists.')
a=body.index('A coherent test using partial-register initialization failed.')
z=body.index('\n\n',a)
oldpara=body[a:z]
main=r'''For $w=(2,4,1)$, $v=(1,2,0)$, $W=3$, and $d=1$, dense statevector simulations of the raw and inverse-cancelled 22-qubit oracle gave maximum complex-amplitude errors approximately $4.77\times10^{-15}$ and $1.94\times10^{-15}$, respectively. Explicit primitive-gate or decomposed unitary preparation also passed on the matrix-product-state backend at tolerance $10^{-8}$.\footnote{A test using partial-register initialization on the same layout produced amplitude error approximately 0.2154. Preparation-only checks reproduced an incorrect state before any oracle gates. Its cause remains unresolved, and this preparation path is excluded from the supporting correctness evidence. The failed record is retained; the successful checks use the same oracle and tolerance.}'''
body=body[:a]+main+body[z:]
s=before+body+after
start=s.index('The input registries, circuit sources, raw result ledgers, and audit scripts are retained')
end=s.index('\n\n',start)
s=s[:start]+'The input registries, circuit sources, numerical result ledgers, and verification scripts are retained in the research archive.'+s[end:]
start=s.index('The local reproducibility map accompanying this draft')
end=s.index('\n\n',start)
s=s[:start]+'The reproducibility records identify the input registries, circuit-test conditions, failed initialization test, source hashes, and numerical resource records. Tables and resource plots are generated from these records.'+s[end:]
# Add explicit intercolumn space only to the requested fixture table.
start=s.index(r'\caption{Fixed QFT bank fixtures;')
end=s.index(r'\end{table}',start)
block=s[start:end].replace(r'\begin{tabular}{lllll}',r'\begin{tabular}{llr@{\hspace{1.5em}}rl}')
s=s[:start]+block+s[end:]
assert r'\orgname{VNR VJIET}' in s and not re.search(r'[\u0400-\u04ff]',s)
assert 'agree. ee.' not in s
assert 'Common-basis depth &' in s and '$(3,5)$ & $(2,4)$' in s
assert 'Pending author confirmation before submission.' in s
f.write_text(s,encoding='utf8')
(p/'audit/requested_small_fixes.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='before',tofile='after')),encoding='utf8')
