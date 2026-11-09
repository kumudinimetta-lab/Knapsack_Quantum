from pathlib import Path
import fitz,json,hashlib,zipfile,re
from PIL import Image,ImageOps,ImageDraw
OUT=Path(__file__).resolve().parent
preview=OUT/'audit/preview';preview.mkdir(exist_ok=True)
doc=fitz.open(OUT/'main.pdf');texts=[];bounds=[];thumbs=[]
for i,page in enumerate(doc):
    text=page.get_text();texts.append(text)
    page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(preview/f'page_{i+1:02d}.png')
    im=Image.open(preview/f'page_{i+1:02d}.png').convert('RGB');im.thumbnail((480,650))
    tile=Image.new('RGB',(500,690),'#dddddd');tile.paste(im,((500-im.width)//2,25))
    ImageDraw.Draw(tile).text((15,8),f'Page {i+1}',fill='black');thumbs.append(tile)
    for block in page.get_text('blocks'):
        if block[0]<0 or block[1]<0 or block[2]>page.rect.width+1 or block[3]>page.rect.height+1:
            bounds.append({'page':i+1,'bbox':block[:4]})
for start in range(0,len(thumbs),6):
    sheet=Image.new('RGB',(1500,1380),'white')
    for j,t in enumerate(thumbs[start:start+6]):sheet.paste(t,((j%3)*500,(j//3)*690))
    sheet.save(preview/f'sheet_{start//6+1}.png')
alltext='\n'.join(texts);(OUT/'audit/extracted_pdf.txt').write_text(alltext,encoding='utf8')
log=(OUT/'build/main.log').read_text(errors='replace')
bbl=(OUT/'main.bbl').read_text(errors='replace')
assert '???' not in bbl,'Unfilled publisher metadata'
assert not re.search(r'Citation .*undefined|Reference .*undefined|There were undefined',log)
assert not re.search('Overfull',log),'Layout overflow needs review'
assert not bounds,bounds
result={'pages':len(doc),'out_of_page_text_blocks':bounds,'undefined_citations_or_references':False,'overfull_boxes':0,'placeholder_publisher_locations':0,'visual_review':'Rendered; awaiting visual inspection of all sheets and key pages','pdf_sha256':hashlib.sha256((OUT/'main.pdf').read_bytes()).hexdigest()}
(OUT/'audit/PDF_CHECKS.json').write_text(json.dumps(result,indent=2))
files=['main.tex','references.bib','main.bbl','sn-jnl.cls','sn-mathphys-num.bst','resource_ratios.pdf','integer_coverage_example.pdf','oracle_workflow.pdf','main.pdf','LATEX_SUBMISSION_CHECKLIST.md']
with zipfile.ZipFile(OUT/'qip_latex_review_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in files:
        if (OUT/name).exists():z.write(OUT/name,name)
print(json.dumps(result,indent=2))
