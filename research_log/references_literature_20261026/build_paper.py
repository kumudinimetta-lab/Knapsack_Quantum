from pathlib import Path
import subprocess,json,shutil
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
results=[]
work=out/'latex_build'
work.mkdir(exist_ok=True)
for filename in ['main.tex','references.bib']:
    shutil.copy2(root/'paper'/filename,work/filename)
shutil.copytree(root/'paper/figures',work/'figures',dirs_exist_ok=True)
for i,command in enumerate([
 ['pdflatex','--disable-installer','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],
 ['bibtex','main'],
 ['pdflatex','--disable-installer','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],
 ['pdflatex','--disable-installer','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],
 ['pdflatex','--disable-installer','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],
],1):
    command[0]=shutil.which(command[0])
    result=subprocess.run(command,cwd=work,capture_output=True,timeout=120)
    (out/f'build_{i}.log').write_bytes(result.stdout+b'\n'+result.stderr)
    results.append({'pass':i,'command':command,'returncode':result.returncode})
    print(f'pass {i}: exit {result.returncode}',flush=True)
    if result.returncode: break
(out/'BUILD_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if results[-1]['returncode']==0 and len(results)==5:
    shutil.copy2(work/'main.pdf',root/'paper/main.pdf')
raise SystemExit(results[-1]['returncode'])
