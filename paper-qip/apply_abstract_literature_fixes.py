from pathlib import Path
import shutil, difflib

p = Path(__file__).resolve().parent
backup = p/'backups/before_abstract_literature_fixes_20261027'
backup.mkdir(exist_ok=False)
for name in ['main.tex', 'main.pdf', 'qip_latex_review_bundle.zip']:
    shutil.copy2(p/name, backup/name)
f = p/'main.tex'
old = f.read_text(encoding='utf8')
s = old
changes = {
    'Quantum tree-search frameworks require reversible bounding predicates': 'Quantum branch-and-bound frameworks use reversible bounding predicates',
    'Separate small-circuit tests report zero gate mismatches': 'Completed small-circuit basis tests report zero gate mismatches',
    r"Grover's algorithm searches an unstructured space of size $N$ using $O(\sqrt{N})$ oracle queries": r"For an unstructured space of size $N$ containing one marked item, Grover's algorithm finds that item with bounded error using $O(\sqrt{N})$ oracle queries",
    r'Searching all binary assignments therefore requires $O(2^{n/2})$ queries before accounting for oracle cost.': r'Treating the $2^n$ binary assignments as an unstructured objective table gives an $O(2^{n/2})$-query minimum-finding baseline at constant success probability, before accounting for oracle cost \cite{ref13}.',
    'distinguish QRAM architectures': 'distinguish quantum random-access memory (QRAM) architectures',
    'present a quantum tree generator with amplitude amplification': 'present a quantum tree generator (QTG) with amplitude amplification',
    r'their quantum B\&B benchmarks': r'their quantum B\&B (QBnB) benchmarks',
    r'with Grover-mixer QAOA \cite{ref23}': r'with the Grover-mixer quantum approximate optimization algorithm (QAOA) \cite{ref23}',
    'the full search tree on the QPU': 'the full search tree on the quantum processing unit (QPU)',
    'compare it with QUBO reformulations': 'compare it with quadratic unconstrained binary optimization (QUBO) reformulations',
}
for a,b in changes.items():
    assert s.count(a)==1, a
    s=s.replace(a,b)
assert s.split(r'\section{Introduction}')[1].split(r'\section{Literature Review}')[0] == old.split(r'\section{Introduction}')[1].split(r'\section{Literature Review}')[0]
assert s.split(r'\section{Problem and pruning contract}')[1] == old.split(r'\section{Problem and pruning contract}')[1]
f.write_text(s,encoding='utf8')
(p/'audit/abstract_literature_fixes_20261027.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='before',tofile='after')),encoding='utf8')
