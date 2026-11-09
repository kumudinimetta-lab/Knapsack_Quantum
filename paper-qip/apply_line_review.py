from pathlib import Path
p=Path(__file__).resolve().parent
f=p/'main.tex'
s=f.read_text(encoding='utf8')
s=s.replace('prove eventual optimal sampling at sufficiently large depth','establish arbitrarily high optimal-solution sampling probability at sufficiently large depth with suitable parameters')
s=s.replace('If $R=0$, the largest suffix density attains zero.','If $R=0$ and the suffix is nonempty, its largest density attains zero; an empty suffix is covered by $\\lambda=0$.')
s=s.replace('the residual fraction has denominator dividing $b$','the residual LP value has denominator dividing $b$')
start=s.index('No IBM hardware jobs, physical noise experiments,')
end=s.index('\n\n',start)
s=s[:start]+r'''The resource comparison assumes ideal arbitrary-angle gates and all-to-all connectivity. Hardware costs would additionally depend on routing, rotation synthesis, and error management. A complete search implementation would still need coherent node handling, branching and marking operations, reflections, error allocation, witness recovery, and preprocessing. Quantum-query frameworks \cite{ref35,ref24} provide context, but do not supply the missing implementation costs. The reported oracle resource reductions therefore do not establish an end-to-end runtime advantage.'''+s[end:]
anchor=r'\subsection{A sufficient bank without reachability enumeration}'
example=r'''For a concrete example, take $w=v=(1,1)$ and $W=1$. The singleton bank $B=\{1/2\}$ gives root bound $3/2$, whereas the LP value is $1$. Nevertheless, it intersects the coverage intervals of all five reachable $(d,R)$ states and preserves their integer-target decisions (Fig.~\ref{fig:coverage-example}). This is a derived illustration, separate from the benchmark cohorts.
\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{integer_coverage_example.pdf}
\caption{Illustration of integer-threshold coverage. The root dual bound can differ from the LP value while retaining its floor. Below, one rational multiplier intersects all five state coverage intervals; open circles exclude endpoints, filled circles include them, and arrows denote unbounded intervals}\label{fig:coverage-example}
\end{figure}

'''
s=s.replace(anchor,example+anchor)
anchor=r'\subsection{A stronger fractional-scan control}'
figure=r'''Figure~\ref{fig:workflow} separates instance-dependent classical preparation from reversible predicate evaluation.
\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{oracle_workflow.pdf}
\caption{Conceptual workflow, rather than a literal gate diagram. For a fixed instance and depth, the predicate $f$ combines capacity rejection with the bank's bound flags. Copying their OR into the target and reversing the work preserves the inputs and restores clean workspace}\label{fig:workflow}
\end{figure}

'''
s=s.replace(anchor,figure+anchor)
f.write_text(s,encoding='utf8')
for name in ['build_pdf.py','render_and_package.py','finalize_review.py']:
    f=p/name;s=f.read_text();s=s.replace("'resource_ratios.pdf'","'resource_ratios.pdf','integer_coverage_example.pdf','oracle_workflow.pdf'")
    s=s.replace('All 31 pages inspected','All rendered pages inspected')
    f.write_text(s)
