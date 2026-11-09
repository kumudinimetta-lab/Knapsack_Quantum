"""Read-only comparison of manuscripts; writes inventory and exact text diffs."""
from pathlib import Path
import difflib
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'paper/backups/2026-10-22_before_revision'
NEW = ROOT / 'paper'
OUT = ROOT / 'research_log'

def entries(text):
    result = {}
    for chunk in re.split(r'(?=^@)', text, flags=re.M):
        match = re.match(r'@\w+\{([^,]+),', chunk)
        if match:
            result[match[1]] = chunk.strip()
    return result

def cited(text):
    return {key.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}', text)
            for key in group.split(',')}

old_tex = (OLD / 'main.tex').read_text(encoding='utf-8')
new_tex = (NEW / 'main.tex').read_text(encoding='utf-8')
old_bib = (OLD / 'references.bib').read_text(encoding='utf-8')
new_bib = (NEW / 'references.bib').read_text(encoding='utf-8')
old_entries, new_entries = entries(old_bib), entries(new_bib)
diff = []
for filename, before, after in [('main.tex', old_tex, new_tex),
                                 ('references.bib', old_bib, new_bib)]:
    diff.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                fromfile='before_revision/' + filename,
                tofile='current/' + filename, n=3))
(OUT / 'MANUSCRIPT_EXACT_CHANGES_2026-10-23.diff').write_text(''.join(diff), encoding='utf-8')

rows = [
('Title, abstract, contributions', 'Replaced the long abstract, shortened the contribution list, changed “Spectral Validation” to “Spectral Checks”, and removed broad uniqueness, general advantage and hardware-validation statements.', 'A short abstract and a more limited contribution list remain. This was more extensive rewriting than minimal word changes.'),
('Introduction and literature review', 'Removed the paragraph about subset-sum exponents, Heuristic 2 and QRAQM; replaced most of the literature review, including classical subset-sum work, quantum search limits, quantum walks, other quantum optimization methods, and quantum-inspired methods.', 'A shorter classical/tree-search review and three newly added close quantum knapsack comparisons remain. This substantially reduced literature coverage; removal is not evidence a source is false.'),
('Prior-work tables', 'Removed the capability checklist and the separate table of knapsack/subset-sum algorithm complexities.', 'A narrower method-comparison table remains. Original table content is in the saved source and exact diff.'),
('Preliminaries', 'Replaced the Montanaro theorem statement/attribution; revised amplitude amplification assumptions, core interpretation and meet-in-the-middle cost wording.', 'The concepts remain, with different statements and qualifications.'),
('LP bounding oracle h', 'Replaced the old fixed-precision formula, resource table and claims about the earlier small circuit, including the old 96-qubit result.', 'A new safe pruning formula, Boolean circuit construction, gate-list resources and explicitly scoped simulations replace them.'),
('Threshold predicate V', 'Removed the old logical-resource and analytical T-count table and its associated discussion.', 'The predicate construction and a scoped dense-statevector check remain. Full original resource discussion is recoverable.'),
('Optimization and correctness', 'Replaced the threshold-search pseudocode, repetition-based correctness statement/proof and composed query bound.', 'Explicit witness recovery, allocation of decision error and a certified-tree-bound assumption replace the earlier statements.'),
('Core analysis', 'Replaced the marginal-loss lemma explanation/proof and rational-valued spacing counterexample; corrected the full binary-tree vertex count.', 'Core containment and spacing bounds remain, with a dual proof and an integer fixed-gap counterexample.'),
('Experimental setup and fixing results', 'Replaced the setup description and mean fixing-ratio values in the old table.', 'Exact-arithmetic rerun results and metric classifications replace them; historical data were retained.'),
('Spectral experiment', 'Replaced the original spectral-validation narrative and taxonomy table.', 'A fresh Schur-based audit, capped/trivial/bypassed status counts and explicitly scoped acceptance checks replace them.'),
('Runtime and memory', 'Condensed the old runtime/memory discussion and revised interpretation of the baseline.', 'Archived timings are still reported as archived implementation results; the OR-Tools timing and cutoff tables remain with revised captions/wording.'),
('Regression', 'Removed the old fitted coefficients/statistics and the interpretation of the response as a reduced-core threshold tree.', 'A new exploratory regression of actual classical core-solver nodes replaces it, with explicit zero-gap exclusions.'),
('Instance-dependent discussion', 'Replaced the original discussion of near-constant cores, instance-dependent query behavior and hard regimes.', 'A shorter discussion based on revised data and conditional query costs remains.'),
('IBM hardware', 'Removed the Hardware Validation Insights subsection, IBM-versus-simulator success-probability table, noise-boundary conclusions and corresponding IBM acknowledgment sentence.', 'A limitations paragraph states that archived summaries do not establish execution provenance for the revised algorithm. The old table/text remain in backups; no new hardware run was performed.'),
('Fault-tolerant crossover', 'Removed the Resource-Estimation Crossover Analysis subsection, per-query T-cost/crossover table and numerical hardware-crossover conclusions.', 'A limitation explains why component estimates are not full algorithm costs or a demonstrated crossover.'),
('Conclusion, availability and limitations', 'Rewrote the conclusion and availability statement, replaced parts of the limitations, and added pending declarations and AI-use disclosure.', 'These reflect the revised claims and reproducibility scope.'),
('Journal layout', 'Replaced IEEE conference formatting with the Springer Nature class, reformatted authors/affiliation and reduced keywords.', 'Author order was preserved; Madhavi is provisional corresponding author.'),
]
lines = [
'# Inventory of manuscript removals and replacements', '',
'Prepared 23 October 2026 at the user’s request. Restoration is paused. This report changes neither manuscript nor bibliography.', '',
'The before-revision LaTeX and bibliography preserve the exact prior text. The saved PDF is the PDF present when that backup was made; its build correspondence to the saved LaTeX has not been re-established.', '',
'## Saved files', '',
f'- Earlier source: `{OLD / "main.tex"}`',
f'- Earlier bibliography: `{OLD / "references.bib"}`',
f'- Earlier PDF: `{OLD / "main.pdf"}`',
f'- Current source: `{NEW / "main.tex"}`',
f'- Full line-by-line source and bibliography diff: `{OUT / "MANUSCRIPT_EXACT_CHANGES_2026-10-23.diff"}`', '',
'## Substantive changes', '',
'“Replaced” means the earlier wording/numbers were removed from the current manuscript and different content was inserted. It does not mean the entire subject disappeared. Reasons below describe the revision; this inventory is not a new independent verification of every technical conclusion.', '',
'| Area | Removed or replaced | Current treatment |',
'|---|---|---|',
]
lines += ['| ' + ' | '.join(row) + ' |' for row in rows]
lines += ['', '## Bibliography accounting', '',
f'- Earlier bibliography: {len(old_entries)} entries; earlier manuscript: {len(cited(old_tex))} unique cited keys.',
f'- Current bibliography: {len(new_entries)} entries; current manuscript: {len(cited(new_tex))} unique cited keys.',
f'- Old entries retained: {len(old_entries.keys() & new_entries.keys())}. Old entries omitted: {len(old_entries.keys() - new_entries.keys())}. New entries added: {len(new_entries.keys() - old_entries.keys())}.', '',
'The omitted sources were not all individually established to be false. Blanket exclusion of unverified sources was not a substitute for an individual citation audit.', '',
'### Every omitted bibliography entry', '',
'Titles below are transcribed from the earlier bibliography; they are not certified bibliographic metadata.', '',
'| Old key | Old title | Cited in earlier manuscript? |', '|---|---|---|']
for key in old_entries:
    if key in new_entries:
        continue
    title_match = re.search(r'(?mi)^\s*title\s*=\s*\{(.*)\},?\s*$', old_entries[key])
    title = title_match[1] if title_match else '(see saved entry)'
    lines.append(f'| `{key}` | {title} | {"Yes" if key in cited(old_tex) else "No"} |')
lines += ['', '### Added bibliography keys', '', ', '.join(f'`{key}`' for key in new_entries if key not in old_entries), '',
'## Snapshot hashes', '', 'SHA-256 hashes identify the exact versions compared.']
for base in (OLD, NEW):
    for filename in ('main.tex', 'references.bib', 'main.pdf'):
        path = base / filename
        lines.append(f'- `{path}`: `{hashlib.sha256(path.read_bytes()).hexdigest()}`')
(OUT / 'MANUSCRIPT_REMOVAL_INVENTORY_2026-10-23.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Inventory and exact diff written; manuscript and bibliography unchanged.')
print(f'Old bibliography {len(old_entries)}, current {len(new_entries)}, omitted {len(old_entries.keys() - new_entries.keys())}.')
