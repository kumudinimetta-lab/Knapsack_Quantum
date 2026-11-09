"""Build only the copied QIP manuscript; never writes to paper/."""
from pathlib import Path
import json,shutil,subprocess
OUT=Path(__file__).resolve().parent
work=OUT/'build';work.mkdir(exist_ok=True)
for name in ['main.tex','references.bib','sn-jnl.cls','sn-mathphys-num.bst','resource_ratios.pdf','integer_coverage_example.pdf','oracle_workflow.pdf']:
    shutil.copy2(OUT/name,work/name)
results=[]
commands=[['pdflatex','--disable-installer','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],['bibtex','main']]
commands += [commands[0].copy() for _ in range(3)]
for i,cmd in enumerate(commands,1):
    cmd[0]=shutil.which(cmd[0]);r=subprocess.run(cmd,cwd=work,capture_output=True,timeout=150)
    (work/f'pass_{i}.txt').write_bytes(r.stdout+b'\n'+r.stderr)
    results.append({'command':cmd,'exit':r.returncode});print('Pass',i,'exit',r.returncode,flush=True)
    if r.returncode:break
(OUT/'audit/BUILD_RESULTS.json').write_text(json.dumps(results,indent=2))
if len(results)==5 and results[-1]['exit']==0:
    for name in ['main.pdf','main.bbl']:shutil.copy2(work/name,OUT/name)
raise SystemExit(results[-1]['exit'])
