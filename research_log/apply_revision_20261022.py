"""Apply scoped manuscript replacements to the preserved pre-revision source."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'paper/backups/2026-10-22_before_revision/main.tex'
s=source.read_text(encoding='utf-8')


def block(start,end,replacement):
    global s
    a=s.index(start);b=s.index(end,a)
    s=s[:a]+replacement.rstrip()+'\n\n'+s[b:]


front=r'''\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{algorithm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{needspace}
\usepackage{url}
\raggedbottom
\hypersetup{hypertexnames=false}
\begin{document}

\title{LP-Pruned Quantum Branch-and-Bound for the 0/1 Knapsack Problem: Query Analysis and Spectral Checks}
\author[1]{\fnm{Nagini} \sur{S.}}\email{nagini\_s@vnrvjiet.in}
\author*[1]{\fnm{Madhavi} \sur{A.}}\email{madhavi\_a@vnrvjiet.in}
\author[1]{\fnm{Shiva} \sur{Sai}}\email{venkatashivasai07@gmail.com}
\author[1]{\fnm{Metta} \sur{Kumudini}}\email{kumudini.metta@gmail.com}
\author[1]{\fnm{Purusharth} \sur{Mishra}}\email{purusharthmishra10@gmail.com}
\author[1]{\fnm{Rakshit} \sur{Chaturvedi}}\email{rakshitchaturvedi09@gmail.com}
\author[1]{\fnm{Veerabhadra} \sur{Yerram}}\email{veerabhadrayerram@gmail.com}
\affil[1]{\orgdiv{Department of Computer Science and Engineering}, \orgname{VNR VJIET}, \orgaddress{\city{Hyderabad}, \country{India}}}

\abstract{We study a hybrid algorithm for integer knapsack combining exact linear programming variable fixing with quantum tree detection. We specify witness recovery and account for accumulated decision error under an explicit tree-size bound. A core containment result and an integer counterexample describe the role of efficiency spacing. We derive a safe fixed-point pruning rule and synthesize reversible circuits for it. Classical benchmarks, sparse statevector circuit checks, and simulations of explicit walk operators test distinct components. These results establish neither a complete quantum walk implementation nor a practical quantum speedup.}
\keywords{quantum computing, knapsack problem, branch-and-bound, quantum walk, linear programming, variable fixing}
\maketitle
'''
block(r'\documentclass',r'\section{Introduction}',front)
s=s.replace('the best classical exact algorithm---the Horowitz--Sahni meet-in-the-middle approach---runs',
            'the classical Horowitz--Sahni meet-in-the-middle approach runs')
block('More sophisticated quantum approaches',r'\subsection{Contributions and Novelty}',r'''
Quantum backtracking and branch-and-bound provide oracle-model query bounds for structured search trees~\cite{ref35,ref24}. Their applicability depends on constructing valid branching and bounding predicates and accounting for both detection and solution recovery. We study how exact knapsack LP fixing and finite-precision node bounds fit this framework.
''')
block('Our algorithm uniquely combines',r'\section{Literature Review}',r'''
Our algorithm combines exact LP reduced-cost fixing with quantum tree detection. The contributions are:
\begin{enumerate}
    \item A core containment bound and an integer family showing that the LP gap alone cannot bound the number of unfixed items.
    \item A threshold-search procedure with explicit witness recovery and a query bound conditional on a certified bound for every queried tree.
    \item A finite-precision pruning lemma and reversible node-predicate circuits with clean workspace.
    \item Component checks on specified circuits and seeds, including the 700-instance classical benchmark and the completed subset of a spectral audit.
    \item Classical comparisons with OR-Tools, including a separate large-coefficient benchmark with an independent exact reference.
\end{enumerate}
We do not claim priority for hybrid quantum knapsack search, wall-clock quantum acceleration, or a complete gate-complexity bound for the full walk. The synthesized node predicates and the simulated walk operators are separate components.

The remainder of this paper reviews related work, defines the algorithm and its assumptions, gives the analysis, and reports the component experiments and limitations.
''')
block(r'\section{Literature Review}',r'\section{Preliminaries}',r'''
\section{Literature Review}

\textit{Classical exact methods.} Dantzig's fractional relaxation~\cite{ref1}, meet-in-the-middle~\cite{ref2}, dynamic programming, and core methods~\cite{ref3,ref4} provide the classical context. Pisinger~\cite{ref4} studies core difficulty and credits the earlier core concept to Balas and Zemel. We use exact forced-item LP tests; their validity follows from the relaxation upper bound, not from an assumed small core. Specialized solvers such as COMBO combine dynamic programming and strong bounds~\cite{martello1999combo}.

\textit{Quantum tree search.} Montanaro's backtracking results distinguish detection (Theorem~1.1) from finding an assignment (Theorem~1.2)~\cite{ref35}. His branch-and-bound algorithm additionally controls tree size while searching for an optimal solution~\cite{ref24}. Our binary-search and prefix-recovery procedure uses the detection result with a supplied tree-size bound; it does not implement that adaptive tree-size-estimation algorithm. Grover search and amplitude amplification supply alternative search primitives~\cite{ref8,ref11}.

\textit{Closest quantum knapsack work.} Wilkening et al.~\cite{wilkening2025} combine a Quantum Tree Generator with amplitude amplification and quantum maximum finding, and give resource estimates and classical-solver comparisons. Their method has theoretical guarantees; it is not restricted to a variational QAOA routine. Creemers and P\'erez Armas~\cite{creemers2025} develop quantum binary search and hybrid branch-and-bound for knapsack and other discrete optimization problems. Bo\.{z}ejko et al.~\cite{bozejko2026} study a hybrid branch-and-bound method using a D-Wave annealer. Consequently, hybrid search, thresholding, and knapsack specificity are not by themselves new contributions here. The present focus is the exact fixing/core analysis, safe finite-precision node predicates, and explicit spectral checks under stated oracle-model assumptions.

\begin{table}[t]
\caption{Technical comparison with closely related work. These are differences in method, not claims that the present work dominates prior algorithms.}
\label{tab:related}
\centering\small
\begin{tabular}{lp{0.62\textwidth}}
\toprule
Method & Search mechanism and scope \\
\midrule
Montanaro~\cite{ref24} & Generic quantum branch-and-bound with tree-size estimation and witness search. \\
Wilkening et al.~\cite{wilkening2025} & Feasible-solution superpositions, amplitude amplification, and maximum finding. \\
Creemers--P\'erez Armas~\cite{creemers2025} & Grover-based binary search and hybrid branch-and-bound. \\
Bo\.{z}ejko et al.~\cite{bozejko2026} & Annealer-assisted classical branch-and-bound. \\
Present work & Exact LP fixing, a conditional detection/recovery composition, and reversible pruning components. \\
\bottomrule
\end{tabular}
\end{table}
''')
s=s.replace('and that all efficiencies $e_i = v_i / w_i$ are distinct.',
            'Efficiencies $e_i=v_i/w_i$ may tie; ties are broken deterministically using the original item order. Distinctness is required only for the spacing bound below. If all items fit, the instance is solved directly.')
s=s.replace(r'$e_1 > e_2 > \cdots > e_n$',r'$e_1 \ge e_2 \ge \cdots \ge e_n$')
block('The remaining items are partitioned into',r'\subsection{Amplitude Amplification}',r'''
This efficiency band is an analytical comparison set, not a fixing rule. The actual partition $(F_1,C,F_0)$ is produced by Algorithm~\ref{alg:filter}. The core literature~\cite{ref4} motivates studying the items near the split; it does not guarantee a small core for every instance.
''')
block(r'\textbf{Theorem (Brassard',r'\subsection{Reduced-Cost Variable Fixing}',r'''
Brassard et al.~\cite{ref11}, Theorem~3, give expected $O(1/\sqrt{p})$ uses of a measurement-free preparation algorithm and its inverse to find a good state when its initial success probability is $p>0$. The good-state predicate must be supplied; this statement alone does not give an optimal knapsack witness.

\subsection{Quantum Tree Detection (Montanaro)}

\textbf{Theorem (Montanaro~\cite{ref35}, Theorem 1.1).} Given an upper bound $B$ on the number of vertices of a backtracking tree on $m$ Boolean variables, and coherent access to its predicate and deterministic branching heuristic, existence of a marked vertex can be detected with failure probability at most $\eta$ using
\begin{equation}
O\!\left(\sqrt{B\max(1,m)}\log(1/\eta)\right)
\label{eq:montanaro}
\end{equation}
queries. Here the predicate rejects infeasible prefixes or prefixes with LP bound below the fixed threshold, accepts complete feasible assignments meeting the threshold, and is indeterminate otherwise. The branching heuristic selects the next item in the fixed efficiency order. Montanaro's branching heuristic, also named $h$ in that source, is distinct from our LP bounding predicate $h$.

Detection does not return an assignment. Theorem~1.2 of the same source gives a separate witness-search result; our explicit recovery procedure below instead composes further detections. The bound is in oracle queries, excludes the cost of certifying $B$, and does not establish a gate count or wall-clock improvement.
''')
s=s.replace(r'\STATE Compute efficiencies $e_i \leftarrow v_i / w_i$; sort decreasingly',
            r'\STATE Exclude items with $w_i>W$; return all remaining items if they fit'+ '\n'+r'\STATE Compare efficiencies by exact rational arithmetic; sort decreasingly'+ '\n'+r'\STATE Initialize $F_1,C,F_0\leftarrow\emptyset$')
s=s.replace(r'This technique, due to Pisinger~\cite{ref4}, is exact---no heuristic assumptions are involved.',
            'These are exact relaxation-based tests: the opposite assignment cannot belong to any optimum if its upper bound is below a feasible lower bound.')
s=s.replace('The core contribution of this paper. We construct a classical B\\&B tree over the $m$ core items using LP relaxation bounds at each node, then apply Montanaro\'s quantum walk~\\cite{ref24} to search this tree in $$O\\!\\left(\\sqrt{T_{\\max}}\\,m\\log m\\log V_{\\max}\\right)$$ queries.',
            'We define an implicit B\\&B tree over the $m$ core items, with a fixed threshold and LP pruning. Detection and witness recovery are analyzed in Proposition~1; the explicit matrices used for component simulation are not a full gate-level walk implementation.')
s=s.replace('A node is pruned when its LP bound falls below the current best known integer solution.',
            r'For a detection call at threshold $\tau$, a node is pruned when its LP bound is strictly below $\tau$. The threshold is fixed throughout that call, so the tree does not depend on a changing incumbent.')
block(r'\subsubsection{Reversible LP-Bound Oracle ($h$)}',r'\subsubsection{Quantum Walk Application}',r'''
\subsubsection{Reversible LP-Bound Oracle ($h$)}

For fixed depth $d$, write a node bound as $U=P+r v_s/w_s$, where $P$ includes the already selected and fully packed integer values, and $0\le r<w_s$. Efficiencies are ordered exactly. Precompute the problem constants $q_i=\lfloor 2^k v_i/w_i\rfloor$ and compute
\begin{equation}
A=2^kP+r q_s,\qquad A W_{\max}+2^k\le \tau\,2^kW_{\max}.
\label{eq:robust-node}
\end{equation}
The inequality is the pruning predicate; Lemma~1a specifies sufficient precision. The truncated value $A/2^k$ is not itself treated as an upper bound.

Existing reversible arithmetic includes elementary networks~\cite{vedral1996}, Fourier addition~\cite{draper2000}, and restoring division~\cite{thapliyal2016}. Our new construction uses $X$, CNOT, and Toffoli gates for binary additions, comparisons, multiplexing, and multiplication by the compiled constants. No division of quantum inputs is needed. It computes the prefix weight and value, scans the remaining items in efficiency order, packs full items while they fit, and uses the first fractional item once. Infeasible prefixes are rejected separately. Register widths cover the full weight/value sums and the scaled cross products. Copying the final flag and reversing the computation restores all workspace, giving
\[
|x_{1:d},\tau,b,0\rangle\longmapsto
|x_{1:d},\tau,b\oplus[U(x_{1:d})<\tau],0\rangle.
\]
The coherent wrapper computes each depth-specific flag into a private bit, conditionally flips the output using a binary depth register, and clears the private bit. It reuses the clean work pool between depths. Thus depth is handled coherently; the complete walk remains a separate implementation task.

\begin{table}[t]
\caption{DERIVED gate-list resources on $w=(2,3,4,5)$, $v=(3,4,5,8)$, $W=8$, $k=5$, with a five-bit threshold register. The final row includes coherent depth dispatch. Workspace uncomputation is included.}
\label{tab:h_resources}
\centering
\begin{tabular}{rrrr}
\toprule
Prefix depth $d$ & Qubits & Gates & Gate depth \\
\midrule
0 & 46 & 133 & 57 \\
1 & 545 & 1747 & 257 \\
2 & 404 & 1285 & 211 \\
3 & 287 & 907 & 165 \\
4 & 155 & 475 & 121 \\
Coherent $d$ & 591 & 9228 & 1622 \\
\bottomrule
\end{tabular}
\end{table}

SIMULATED checks on the 700-instance benchmark (seeds and sizes in Section~\ref{sec:experiments}) exhaust all prefix, threshold-register and target-bit basis states at depth $d=3$, with clean initial workspace: 15,859,712 columns, 0 predicate mismatches against exact rational LP bounds, and 0 columns with uncleared workspace. Precision is $k=13$ or $14$, chosen per instance by $2^k>W_{\max}^2$. The $X$/CNOT/Toffoli circuit is a permutation, so sparse statevectors propagate basis labels and amplitudes exactly through every gate. This checks arbitrary superpositions in the tested input subspace by linearity. It is not a check of all depths on those 700 instances.

For $(w,v,W)=((2,3,4,5),(3,4,5,8),8)$, $((3,5,7,8),(3,5,7,8),13)$, and $((4,7,6),(5,6,2),7)$, every prefix depth and every threshold/target input was additionally checked: respectively 1984, 1984, and 480 columns, 0 mismatches and 0 uncleared-workspace columns (SIMULATED). The coherent-depth wrappers on these same instances at $k=5,7,6$ exhaust all prefix, binary-depth, threshold and target encodings: respectively 8192, 8192 and 1024 columns, 0 mismatches and 0 uncleared-workspace columns (SIMULATED). An independent dense Qiskit statevector check on $w=(2)$, $v=(1)$, $W=2$, $d=1$, $k=3$ gave maximum amplitude error $5.56\times10^{-17}$ (SIMULATED).
''')
block(r'\begin{algorithm}[h]'+'\n'+r'\caption{Classical Threshold-Search',r'\subsection{Phase 3: Classical Post-Processing}',r'''
\begin{algorithm}[t]
\caption{Threshold Search and Witness Recovery (Phase 2)}
\label{alg:qbb}
\begin{algorithmic}[1]
\REQUIRE Core $C$, residual capacity $W'$, failure budget $\delta$, certified tree-size bound $B$
\ENSURE Core assignment $x_C^*$, except with probability at most $\delta$
\STATE $S\leftarrow\sum_{i\in C}v_i$, $L\leftarrow\lceil\log_2(S+1)\rceil$, $M\leftarrow L+m$
\STATE Set each detection's failure probability to $\delta/M$; solve $M=0$ directly
\STATE $\ell\leftarrow0$, $u\leftarrow S+1$
\WHILE{$u-\ell>1$}
    \STATE $\tau\leftarrow\lfloor(\ell+u)/2\rfloor$
    \STATE Detect a feasible completion of value $\ge\tau$ in its fixed-threshold tree
    \STATE If detected, set $\ell\leftarrow\tau$; otherwise set $u\leftarrow\tau$
\ENDWHILE
\STATE $Z\leftarrow\ell$; initialize empty prefix with weight/value zero
\FOR{each item in the fixed efficiency order}
    \STATE Test whether extending the prefix by 0 permits a completion of value $\ge Z$
    \STATE Choose 0 if yes and 1 otherwise; update prefix weight and value
\ENDFOR
\STATE Check the final assignment's capacity and value; report failure if invalid
\RETURN $x_C^*$
\end{algorithmic}
\end{algorithm}

Recovery uses the prefix's accrued value and weight to form each residual threshold and capacity; empty or infeasible residual problems are decided classically. At most $L+m$ detections are made. The bound $B$ must cover both value-search and recovery trees, not just the trees encountered during value search. Proposition~1 accounts for these calls and their error allocation.

\subsubsection{Reversible Knapsack Oracle (Answer-Agnostic)}
\label{sec:oracle-impl}

The separate phase predicate $V$ marks $\mathrm{feasible}(x)\wedge\mathrm{value}(x)\ge\tau$ using the problem data and a supplied threshold. The existing Draper-arithmetic construction accumulates weight and value, checks the two signed differences, flips the phase, and uncomputes both accumulators. On $w=(2,3,4,5)$, $v=(3,4,5,8)$, $W=8$, dense statevector checks covered all 16 selection states at each of the 22 thresholds $\tau=0,\ldots,21$: 0 mismatches, with maximum amplitude error below $5.60\times10^{-14}$ (SIMULATED). These are component checks, not executions of Algorithm~\ref{alg:qbb} as a full quantum circuit.
''')
s=s.replace('using a surrogate relaxation: the minimum of $d$ single-constraint Dantzig bounds.',
            'using the minimum of $d$ single-constraint Dantzig bounds.')
s=s.replace('over a strict superset of the full', 'over a superset of the full')
s=s.replace(r'saturating to $\alpha = 1.0$ instantly at $d \ge 2$',
            r'giving $\alpha = 1.0$ in all tested configurations with $d \ge 2$')
s=s.replace('Our framework extends cleanly to', 'The classical fixing rule also applies to')
block(r'\textbf{Lemma 1a',r'\textbf{Lemma 1b',r'''
\textbf{Lemma 1a (Safe fixed-point pruning).}\label{lem:precision}
\textit{For positive integer weights and values, retain the exact efficiency order. Let $\widetilde U=P+r\lfloor 2^kv_s/w_s\rfloor/2^k$ approximate any feasible node or forced-item LP bound $U=P+r v_s/w_s$, with integer $P$, $0\le r<w_s\le W_{\max}$. Then
\[
0\le U-\widetilde U<\varepsilon(k)=W_{\max}2^{-k}.
\]
If $\varepsilon(k)<1/W_{\max}$, the rule $\widetilde U\le\tau-1/W_{\max}$ is equivalent to $U<\tau$ for every integer threshold $\tau$. This sufficient condition preserves both the fixing decisions at $\tau=Z_{LB}$ and the node-pruning decisions in Phase~2.}

\textit{Proof.} Flooring gives $0\le v_s/w_s-\lfloor 2^kv_s/w_s\rfloor/2^k<2^{-k}$; multiplication by $r<W_{\max}$ gives the error bound. Since $P$ and $\tau$ are integers, $U<\tau$ implies $U\le\tau-1/w_s\le\tau-1/W_{\max}$, so the truncated test prunes. If $U\ge\tau$, then $\widetilde U>U-\varepsilon(k)>\tau-1/W_{\max}$, so it does not prune. If there is no fractional item, $U$ is integral and the same argument applies with zero truncation error. Equation~\eqref{eq:robust-node} implements the comparison by exact integer cross multiplication. $\square$

The condition $2^k>W_{\max}^2$ is sufficient, not necessary for every instance: dyadic efficiencies may be represented exactly at lower precision. Pure truncation with the unadjusted test is unsafe even at equality. For example, excluding $(w,v)=(7,6)$ from $w=(4,7,6)$, $v=(5,6,2)$, $W=7$ gives $U=5+3(2/6)=Z_{LB}=6$, but $\widetilde U<6$ at every finite precision. The robust rule avoids this false pruning when the lemma's precision condition holds. It guarantees decisions, not equality of approximate and rational bound values.

\textbf{Theorem 1.} \textit{With exact fixing, valid node predicates, a certified tree-size bound for every detection call, and the error allocation in Algorithm~\ref{alg:qbb}, Algorithm~\ref{alg:hybrid} returns an optimal assignment with probability at least $1-\delta$.}

\textit{Proof.} If forcing the opposite value of a variable yields an LP bound below a feasible lower bound, no optimal assignment has that opposite value. Thus every optimum respects all fixed decisions. Conditional on correct detection answers, binary search maintains an achievable lower threshold and an unachievable upper threshold and ends at the optimal core value. During recovery, the current prefix has a completion attaining that value. If the zero extension has no such completion, the one extension must have one; this preserves the invariant until a complete optimal assignment is obtained. Reconstruction adds the fixed-in items. There are at most $M=L+m$ adaptive calls, each with conditional failure probability at most $\delta/M$; the union bound gives total failure at most $\delta$. The final capacity/value check detects an invalid recovered witness but does not by itself certify optimality after erroneous detections. $\square$
''')
s=s.replace(r"where $\hat{Z}'_i$ is the derived formula assuming no split shift",
            r"where $\hat{Z}'_i$ is the dual upper-bound formula")
needle=r'\textbf{Theorem 2 (Core Containment).}'
proof=r'''\textit{Proof of Lemma 1b.} Set $\lambda=e_s$. The LP dual bound is
$Z_{LP}=\lambda W+\sum_j\max(0,v_j-\lambda w_j)$.
Removing an item before the split deletes its nonnegative term; forcing an item after the split in changes the bound by $v_i-\lambda w_i\le0$. Optimizing the restricted LP cannot exceed either resulting dual bound, giving $Z'_i\le Z_{LP}-w_i|e_i-e_s|$. This proof also covers ties with zero reduced cost. $\square$

'''
s=s.replace(needle,proof+needle)
block(r'\textbf{Lemma 1b',r'\textit{Proof of Lemma 1b.}',r'''
\textbf{Lemma 1b (Dual bound for forced assignments).}\label{lem:monotonicity}
\textit{For any item $i\ne s$, the exact forced-item LP bound satisfies $Z'_i\le Z_{LP}-w_i|e_i-e_s|$. This upper bound does not require the split item to remain unchanged.}
''')
s=s.replace('Assume items are sorted in strictly decreasing efficiency order.',
            'Assume a split item exists and items are sorted in nonincreasing efficiency order.')
s=s.replace("Let $i \\in C_{RC}$, meaning item $i$ was not fixed and $Z'_i \\ge Z_{LB}$.",
            "For $i=s$, containment is immediate. For any other $i \\in C_{RC}$, item $i$ was not fixed and $Z'_i \\ge Z_{LB}$.")
block(r'\textbf{Remark.} The no-split-shift',r'\textbf{Proposition 2',r'''
\textbf{Remark.} The proof uses an upper bound, so a change of split item does not invalidate containment. It also gives the tighter item-dependent bound $|e_i-e_s|\le(Z_{LP}-Z_{LB})/w_i$.
''')
block(r'\textbf{Consequence for $T_{LP}$',r'\subsection{Discussion: Structural Interpretation}',r'''
\textbf{Tree-count consequence.} A full binary tree of depth $m$ contains $2^{m+1}-1$ vertices, so every threshold or recovery tree has at most this many nodes. If $K=\min\{n,\lfloor 2(Z_{LP}-Z_{LB})/(w_{\min}\Delta)\rfloor+1\}$, Proposition~2 gives $m\le K$ and hence $B=2^{K+1}-1$ is a certified bound for Proposition~1. This is a worst-case bound; positive spacing is not guaranteed in general, including tied-efficiency instances.

\textbf{Remark (Gap alone does not bound the core).} For $n\ge2$, set $q=\lfloor n/2\rfloor$, $M_0=2n^2$, $w_i=2(M_0+i)$, $v_i=2$, and
\[
W=\sum_{i=1}^q w_i+(M_0+q+1).
\]
All data are positive integers and $e_i=1/(M_0+i)$ are distinct. Every $q$-item subset fits: the difference between the heaviest and lightest $q$-subsets is $2q(n-q)\le n^2/2<M_0+q+1$. No $(q+1)$-item subset fits, because the lightest such subset adds $w_{q+1}=2(M_0+q+1)$ to the lightest $q$-subset. Thus $Z^*=Z_{LB}=2q$. The LP fills exactly half of item $q+1$, so $Z_{LP}-Z_{LB}=1$ for every $n$. Each item is included in some optimum and excluded from another, so neither forced-item LP test can fix it: $|C_{RC}|=n$. Therefore no finite bound depending on the gap alone holds for this integer problem class. This does not rule out bounds using weights or other structure.

\textbf{Proposition 1 (Detection and witness query complexity).} \textit{Let $S=\sum_{i\in C}v_i$, $L=\lceil\log_2(S+1)\rceil$, $m=|C|$, and $M=L+m>0$. Suppose a supplied certified bound $B$ covers every fixed-threshold tree queried during value search and prefix recovery. Under the assumptions of Montanaro's Theorem~1.1~\cite{ref35}, Algorithm~\ref{alg:qbb} uses}
\begin{equation}
O\!\left(\sqrt{B\max(1,m)}\,(L+m)\log\frac{L+m}{\delta}\right)
\label{eq:totalcomplexity}
\end{equation}
\textit{queries, with failure probability at most $\delta$.}

\textit{Proof.} Value search makes at most $L$ detections and recovery at most $m$. Each call has depth at most $m$ and error at most $\delta/M$. Applying \eqref{eq:montanaro} and summing at most $M$ calls gives \eqref{eq:totalcomplexity}; Theorem~1 gives correctness. $\square$

The safe generic choice is $B=2^{m+1}-1$. A smaller bound requires a certificate; computing it by classical tree enumeration is not free. The simulator explicitly constructs its trees, so its running time is not the query bound. Classical preprocessing, arithmetic bit costs, coherent depth dispatch, and walk-reflection gate costs are also excluded. We make no general claim that this composition inherits Montanaro's adaptive optimal-tree bound~\cite{ref24}.
''')
block(r'\subsection{Comparison with Prior Work}',r'\section{Experimental Results}',r'''
\subsection{Comparison with Prior Work}
Table~\ref{tab:related} compares mechanisms. Equation~\eqref{eq:totalcomplexity} is a conditional oracle-query statement, not a measured runtime or a comparison with the best classical knapsack solver. In particular, an easy first-solution classical search need not traverse the entire threshold tree~\cite{ref35}.
''')
block(r'\subsection{Experimental Setup}',r'\subsection{Variable Fixing Results}',r'''
\subsection{Experimental Setup}
The revised experiments use exact rational efficiency comparisons and LP bounds, with dynamic programming as the classical reference on the small-coefficient benchmark. The value-search simulator now returns a prefix-recovered assignment and includes its detection calls in the scheduled total. It computes analytical acceptance/majority probabilities rather than sampling a physical quantum execution. The empirical phase-estimation constant and fixed repetition count in the simulation are not a universal certification of the error assumptions in Theorem~1.

Numbers are classified as follows: classical solve outcomes, node counts and timings are \texttt{MEASURED}; exact bound calculations, fitted statistics and gate-list resource counts are \texttt{DERIVED}; quantum-operator and statevector outputs are \texttt{SIMULATED}; chosen quantum query budgets are \texttt{SCHEDULED}; manually chosen sizes, cutoffs and precision policies are \texttt{HARDCODED} configurations. No scheduled budget is interpreted as a measured quantum cost.

The classical and node-predicate benchmark has five Pisinger-style classes~\cite{ref4}: uncorrelated, weakly correlated, strongly correlated, subset sum, and inverse strongly correlated. For each class, $n\in\{12,14,16,18,20,22,24\}$ and seeds $1000n+t$, $t=0,\ldots,19$, give 700 instances. The coefficient range parameter is $R=100$, with capacity $\lfloor\sum_iw_i/2\rfloor$; the generators and exact inputs are reproducible from these specifications. Exact fixing plus core solving gave 0 optimum mismatches against dynamic programming on all 700 instances, with 0 node-capped cases (MEASURED). This establishes agreement on this tested set, not a universal empirical proof.

The analytical-majority optimization simulator was separately checked on 135 configurations: five generators, $n=0,\ldots,8$, three seeds $1000n+t$ per size, $R=15$, phase-estimation constant 2, $K=11$, and a 2000-node cap. It returned 0 value/witness mismatches and 0 capped cases (SIMULATED). These small tests do not establish the asymptotic query bound experimentally.
''')
s=s.replace(r'\caption{Average Core Ratio $\alpha = m/n$ by Instance Type}',
            r'\caption{MEASURED mean fixing ratios at $n=24$, 20 seeds per class, from the exact-arithmetic rerun.}')
s=s.replace('Uncorrelated & 0.32 & 0.35 & 0.33 & Tight',
            'Uncorrelated & 0.252 & 0.483 & 0.265 & Positive')
s=s.replace('Weakly correlated & 0.76 & 0.12 & 0.12 & Medium',
            'Weakly correlated & 0.748 & 0.140 & 0.112 & Mixed')
s=s.replace('Strongly correlated & 0.95 & 0.02 & 0.03 & Loose',
            'Strongly correlated & 0.958 & 0.035 & 0.006 & Positive')
s=s.replace(r'Subset-sum & 1.00 & 0.00 & 0.00 & N/A (gap $\equiv 0$)',
            'Subset-sum & 1.000 & 0.000 & 0.000 & Zero in this set')
s=s.replace('Inverse strongly & 0.81 & 0.10 & 0.09 & Medium',
            'Inverse strongly & 0.735 & 0.062 & 0.202 & Positive')
block(r'\subsection{Spectral Validation of the Quantum Walk}',r'\subsection{Classical Runtime and Memory Characterization}',r'''
\subsection{Spectral Checks of the Quantum Walk}
The spectral audit uses $R=50$, $n\in\{8,10,12,14,16,18\}$, and seeds $1000n+t$, $t=0,\ldots,19$, for each of the five classes. Each seed has a marked threshold equal to the exact residual optimum and an unmarked threshold one greater: 1200 scheduled conditions. These answer-known thresholds are used only to audit detection, not to run optimization.

Of these conditions, 889 trees completed with $T\le2000$: 489 marked and 400 unmarked. The remaining conditions are 74 marked tree caps, 74 conditions bypassed at 37 empty-core seeds, and 163 immediately pruned unmarked roots (SIMULATED status counts). None is silently discarded. Median core size is 16 for capped cases and 10 for completed cases (DERIVED), limiting generalization to larger trees.

The fresh audit uses orthogonal real Schur blocks so degenerate eigenspaces do not require treating nonorthogonal eigenvectors as a probability basis. On the 889 completed trees, spectral and direct sparse-walk acceptance calculations differ by at most $9.49\times10^{-12}$ (SIMULATED). We check the effective spectral-gap inequality $\mu(\Phi)\le\Phi^2Tm/4$ for unmarked trees at $\Phi=c/\sqrt{Tm}$, $c\in\{1/8,1/4,1/2,1,2\}$, and phase-zero weight at least $1/2$ for marked trees, with numerical tolerances. These are the conditions in the proof of Montanaro's Lemma~2.4 and effective spectral-gap Lemma~2.1~\cite{ref35}, with eigenphase $\Phi=2\theta$.

The results are 400/400 unmarked trees satisfying all tested inequalities (0 violations), 489/489 marked trees satisfying the phase-zero test (0 violations), and 889/889 analytical-majority decisions agreeing with marked status (0 mismatches), all SIMULATED. The phase-estimation constant is 2 and $K=11$. These are component checks on the completed subset, not measurements of optimization query scaling, minimum spectral gaps, or a speedup.

\begin{table}[t]
\caption{SIMULATED spectral audit status counts. The 1200 conditions include bypassed and capped cases.}
\label{tab:measured}
\centering
\begin{tabular}{lr}
\toprule
Category & Count \\
\midrule
Completed marked & 489 \\
Completed unmarked & 400 \\
Marked tree cap & 74 \\
Immediately pruned unmarked root & 163 \\
Empty-core seed conditions & 74 \\
\midrule
Total & 1200 \\
\bottomrule
\end{tabular}
\end{table}
''')
block(r'\subsection{Classical Runtime and Memory Characterization}',r'\subsection{Comparison Against Google OR-Tools at Scale}',r'''
\subsection{Classical Runtime and Memory Characterization}
Archived instrumentation used \texttt{time.perf\_counter\_ns()} and \texttt{tracemalloc}. Its 1500 method records correspond to 500 matched instance configurations at $n\in\{12,14,16,18,20\}$, with three methods per configuration. The classical baseline already uses LP bounds; the comparison measures the additional cost of fixing. Across the five classes, median paired baseline/fixing runtime ratios range from 0.267 to 0.533, and median fixing-solver peak allocations range from 1384 to 1416 bytes (DERIVED from archived MEASURED records). These timings belong to the archived implementation and were not remeasured for the revised exact arithmetic. Simulation runtime is not physical quantum execution time; no wall-clock quantum speedup is reported.
''')
s=s.replace('We benchmarked the algorithm against Google OR-Tools (version 9.15.6755)',
            'The archived classical benchmark compared LP fixing plus classical B\\&B against Google OR-Tools')
s=s.replace("this supports the correctness of our implementation.",
            'these are value-agreement checks for those completed classical runs.')
s=s.replace('Warning: $n=2$, not a stable avg', 'Only 2 completed pairs')
s=s.replace('Warning: $n=1$, not a stable avg', 'Only 1 completed pair')
s=s.replace(r'\caption{Category (a): Both Solvers Reached Certified Optimal}',
            r'\caption{Archived MEASURED classical timings: both solvers reported certified optimality. Times shown as 0.0000 s are rounded, not zero.}')
s=s.replace(r'\caption{Category (b): Cutoffs Reached}',
            r'\caption{Archived MEASURED cutoff counts; these rows are excluded from solve-time comparisons.}')
block(r'\subsection{Empirical Scaling of $T_{\text{LP}}$',r'\section{Discussion}',r'''
\subsection{Large-Coefficient Benchmark}
An additional MEASURED benchmark uses $R=10^6$, $n\in\{20,24,28\}$, three trials per class, and seeds $20261022+100n+t$, $t=0,1,2$: 45 instances. Meet-in-the-middle supplies an independent exact reference. OR-Tools 9.15.6755 solved all 45 within its one-second limit, with 0 optimum mismatches. Exact LP fixing plus classical B\&B completed 36 with 0 mismatches; the other 9 reached the 100,000-node cap and remain included as capped cases. Dynamic programming was not run on these large-coefficient instances. This small benchmark does not establish a quantum advantage or replace a comparison with a specialized solver such as COMBO~\cite{martello1999combo}.

\subsection{Exploratory Tree-Size Regression}
We fit $\log N_{\mathrm{core}}\sim\log(Z_{LP}-Z^*)+m$ to the exact rerun, where $N_{\mathrm{core}}$ is the actual node count of classical incumbent-based core solving. It is not the maximum fixed-threshold tree size. The response is counted by the solver, not computed from the predictors. Zero gaps are ineligible for this logarithmic model: 141/700 cases (all 140 subset-sum cases and one weakly correlated case) are explicitly excluded; no cases were capped. On the remaining 559 cases, pooled $R^2=0.783$ and five-fold grouped cross-validation mean $R^2=0.776$ (DERIVED). Groups keep equal $(n,\mathrm{seed})$ configurations across classes in one fold.

\begin{table}[t]
\caption{DERIVED exploratory fits for actual classical core-tree node counts; positive-gap cases only.}
\label{tab:tlp_regression}
\centering
\begin{tabular}{lrrr}
\toprule
Class & Included & $R^2$ & CV mean $R^2$ \\
\midrule
Uncorrelated & 140 & 0.872 & 0.861 \\
Weakly correlated & 139 & 0.802 & 0.775 \\
Strongly correlated & 140 & 0.701 & 0.617 \\
Inverse strongly & 140 & 0.770 & 0.688 \\
\bottomrule
\end{tabular}
\end{table}

These fits describe the tested $n\le24$, $R=100$ distributions and provide neither a universal tree-size bound nor independent evidence for quantum query scaling. Regressing a query budget selected from tree size on that same tree size would be circular, so no such validation is used.
''')
block(r'\subsection{Instance-Dependent Query-Complexity Behavior}',r'\section{Conclusion}',r'''
\subsection{Instance-Dependent Behavior}
The exact rerun shows different contributions from classical fixing and residual search. At $n=24$, the uncorrelated mean core contains 6.05 items and its classical core solve visits 24.5 nodes, whereas strongly correlated means are 23 items and 3076.7 nodes (MEASURED). Subset-sum fixing leaves every item in this tested set, yet its mean classical core solve visits only 126.15 nodes: failure to fix variables alone does not imply a hard residual search. Classical incumbent-based node counts and fixed-threshold walk tree sizes are different metrics.

The query theorem gives square-root dependence on a certified size bound, with explicit depth, recovery and error costs. It does not ensure a reduction against the fastest classical solver on each distribution. Nor does a small core ratio establish a constant-size core as $n$ grows.

\subsection{Limitations}
\textbf{Implementation scope.} The reversible circuits implement tested node/threshold predicates, including coherent depth dispatch on the specified small instances. Complete walk reflections and a full optimization circuit have not been composed or executed. Sparse permutation statevectors for the new Boolean circuits and explicit tree-space walk simulations test different objects. The supplied bound $B$ must be justified for every detection tree; classical enumeration to obtain it cannot be hidden as free preprocessing in a runtime claim.

\textbf{Hardware evidence.} No hardware execution of the revised algorithm is reported. Archived IBM count summaries lack retained job identifiers and circuit hashes sufficient to establish that the current answer-agnostic circuit was executed; they are not used as evidence for the present algorithm or a universal hardware size boundary.

\textbf{Resource estimates.} Gate-list counts are component resources, not a full fault-tolerant resource estimate. A controlled-phase gate cannot simply be counted as a Toffoli, and an asymptotic or heuristic rotation-synthesis estimate is not a measured T-count or a certified lower bound. We therefore do not infer a numerical crossover by equating T gates with classical nodes.

\textbf{Classical baselines and scope.} Capacity-based dynamic programming requires $O(nW)$ operations and can use $O(W)$ working storage. It is a strong baseline when coefficients are small. The large-coefficient checks are still small in item count, and COMBO has not been benchmarked here. No general advantage over specialized classical solvers is claimed.

\textbf{Detection reliability and selection.} The simulated phase-estimation constant is calibrated for the reported tests, not proved universal. The 889 completed spectral trees exclude the explicitly counted capped, trivial and bypassed conditions. Their agreement supports those implemented tests on that subset; it does not establish an asymptotic optimization complexity experimentally.
''')
block(r'\section{Conclusion}',r'\section{Data Availability and Reproducibility}',r'''
\section{Conclusion}
We studied exact LP fixing followed by fixed-threshold quantum tree detection for integer knapsack. The revised algorithm explicitly recovers a witness and allocates error across value-search and recovery calls. Its query bound is conditional on a certified bound for all queried trees. The core containment argument identifies the role of efficiency spacing, and the integer counterexample has an unbounded core at the same gap of one.

The finite-precision lemma certifies pruning decisions, including equality cases. The new node circuits had 0 mismatches and 0 uncleared-workspace columns on 15,859,712 sparse statevector columns covering depth-three prefix/threshold/target inputs for the specified 700-instance benchmark at $k\in\{13,14\}$ (SIMULATED). The exact classical rerun had 0 optimum mismatches on all 700 cases (MEASURED). The fresh 889-tree completed spectral subset had 0 tested endpoint violations and 0 analytical detection disagreements (SIMULATED). These scoped component results establish neither a complete gate-level quantum optimization algorithm nor a wall-clock quantum speedup.

Future work includes coherent composition of the predicate circuits with the walk, tighter certified tree-size bounds for structured distributions, and comparisons with specialized classical solvers on larger, hard large-coefficient instances. Any practical quantum advantage requires separate evidence.
''')
block(r'\section{Data Availability and Reproducibility}',r'\section*{Acknowledgment}',r'''
\section{Data Availability and Reproducibility}
The project repository is \url{https://github.com/kumudinimetta-lab/Knapsack_Quantum}. The revision's scripts and separately generated results are supplied with this manuscript source under \texttt{simulation/} and \texttt{research\_log/}; historical raw records are preserved. The revision audit specifies generator parameters, seeds, cutoffs, predicate mismatch counts, workspace checks, and source hashes. New files must be included in the deposited revision; their presence in the public repository is not assumed until that version is published. The reproduction guide distinguishes classical reference solves, sparse/dense statevectors, analytical walk simulation, scheduled query budgets, and archived measurements.

\section*{Statements and Declarations}
\textbf{Funding, competing interests, and author contributions.} These author-supplied declarations require confirmation before submission; no funding status, absence of conflicts, or individual contribution is inferred here.

\textbf{Use of AI tools.} An OpenAI coding assistant assisted with source checking, mathematical revision, code changes, and manuscript editing. The authors must independently review the resulting analysis, code, and text and take responsibility for the submitted version.
''')
s=s.replace("IBM Quantum services were used for the hardware experiments reported in Section~\\ref{sec:experiments}; the views expressed are those of the authors and do not reflect the official policy of IBM or the IBM Quantum team.",
            'The acknowledgment of institutional support does not substitute for the funding declaration required before submission.')
s=s.replace(r'\bibliographystyle{IEEEtran}',r'% Bibliography style is selected by the sn-mathphys-num class option.')
s=s.replace(r'\bibliography{references}',r'\setlength{\bibsep}{3pt}'+ '\n'+r'\bibliography{references}')
s=s.replace(r'\subsection{Phase 3: Classical Post-Processing}',r'\Needspace{11\baselineskip}'+ '\n'+r'\subsection{Phase 3: Classical Post-Processing}')
s=s.replace('(items heavier than the capacity are trivially excluded) Efficiencies',
            '(items heavier than the capacity are trivially excluded). Efficiencies')
s=s.replace(r'Given a parameter $\delta > 0$',r'Given a parameter $\delta \ge 0$')
s=s.replace('Unlike heuristic delta-based filtering, reduced-cost fixing is \\textit{provably exact}: no item in $F_1$ or $F_0$ can change the optimal solution.',
            'Every optimal assignment respects the decisions in $F_1$ and $F_0$.')
s=s.replace(r'\REQUIRE Items $(w_i, v_i)_{i=1}^n$, capacity $W$'+ '\n'+r'\ENSURE Optimal solution $x^*$ and value $Z^*$',
            r'\REQUIRE Items $(w_i, v_i)_{i=1}^n$, capacity $W$, failure budget $\delta$'+ '\n'+r'\ENSURE Optimal solution $x^*$ and value $Z^*$, except with probability $\delta$')
s=s.replace(r'\STATE $m \leftarrow |C|$',r'\STATE $m \leftarrow |C|$; set certified $B\leftarrow 2^{m+1}-1$ unless a smaller certificate is supplied')
s=s.replace(r'\ELSIF{$m \leq m_{\text{thresh}}$}',r'\ELSIF{a configured classical fallback is selected}')
s=s.replace(r'\textsc{Quantum-B\&B}$(C, W\', V_1)$',r'\textsc{Quantum-B\&B}$(C,W\',\delta,B)$')
s=s.replace(r"\textsc{Quantum-B\&B}$(C, W', V_1)$",r"\textsc{Quantum-B\&B}$(C,W',\delta,B)$")
s=s.replace('respectively 1984, 1984, and 480 columns',
            'respectively 1984, 1984, and 480 columns at $k=5,7,6$')
s=s.replace('runs in $O(2^{n/2})$ time and space',
            'runs in $\\widetilde O(2^{n/2})$ time and $O(2^{n/2})$ space')
s=s.replace("applying Grover search directly to knapsack yields $O(2^{n/2})$---no improvement over classical meet-in-the-middle.",
            "applying Grover search directly to knapsack uses $O(2^{n/2})$ threshold-oracle queries; this alone does not improve the classical meet-in-the-middle exponential rate.")
s=s.replace('The total time and space are both $O(2^{n/2})$.',
            'This straightforward implementation uses $O(n2^{\\lceil n/2\\rceil})$ arithmetic operations and $O(2^{\\lceil n/2\\rceil})$ stored pairs; polynomial factors are suppressed in exponential-rate comparisons.')
s=s.replace('in Section VI-B (Table~\\ref{tab:fixing})','in Table~\\ref{tab:fixing}')
# IEEE two-column float notation is unnecessary in the journal layout.
s=s.replace(r'\begin{table*}',r'\begin{table}').replace(r'\end{table*}',r'\end{table}')
# The Springer class already wraps tables in center/threeparttable. Its table
# measurement is incompatible with the inherited resizebox wrappers.
s=re.sub(r'\\resizebox\{\\columnwidth\}\{!\}\{%?\n(.*?)\\end\{tabular\}%?\n\}',
         lambda m:m.group(1)+r'\end{tabular}',s,flags=re.S)
s=s.replace(r'\begin{center}','').replace(r'\end{center}','')
s=s.replace(r'\textbf{Core Ratio $\alpha$ (Mean $\pm$ 95\% CI)}',r'\textbf{Mean core ratio (95\% CI)}')
s=s.replace(r'\begin{tabular}{lcccccc}',r'\begin{tabular}{@{}lrrrrr@{}}')
s=s.replace(r' & \textbf{Notes}', '')
s=re.sub(r'(Uncorrelated|Weakly correlated|Subset sum|Strongly correlated|Inverse strongly)( & [^\n]+?) & (?:Only [12] completed pairs?)? ?\\\\',r'\1\2 \\\\',s)
# Remove excessive inherited empty lines without changing paragraph content.
s=re.sub(r'\n{4,}','\n\n\n',s)
s='\n'.join(line.rstrip() for line in s.splitlines())+'\n'
(ROOT/'paper/main.tex').write_text(s,encoding='utf-8')
abstract=re.search(r'\\abstract\{(.*?)\}\n',s,re.S).group(1)
print('Abstract words:',len(abstract.split()))
print('Manuscript lines:',len(s.splitlines()))
print('Citations:',sorted(set(k for group in re.findall(r'\\cite\{([^}]+)\}',s)for k in group.split(','))))
