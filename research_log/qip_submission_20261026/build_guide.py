from pathlib import Path
import hashlib,json,re,shutil
from zipfile import ZipFile
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'paper/QIP_SUBMISSION_GUIDE_2026-10-26.md'
PDF=SOURCE.with_suffix('.pdf')
for name,filename in [('Guide','arial.ttf'),('Guide-Bold','arialbd.ttf'),('Guide-Italic','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/filename)))
pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='Guide-Bold',italic='Guide-Italic',boldItalic='Guide-Bold')
style=getSampleStyleSheet()
style.add(ParagraphStyle(name='BodyGuide',fontName='Guide',fontSize=9.2,leading=13,spaceAfter=6))
style.add(ParagraphStyle(name='TableGuide',fontName='Guide',fontSize=8.0,leading=10.5))
style.add(ParagraphStyle(name='TitleGuide',fontName='Guide-Bold',fontSize=19,leading=23,spaceAfter=13))
style.add(ParagraphStyle(name='H2Guide',fontName='Guide-Bold',fontSize=12.2,leading=16,spaceBefore=12,spaceAfter=7,keepWithNext=True))
style.add(ParagraphStyle(name='H3Guide',fontName='Guide-Bold',fontSize=10.2,leading=14,spaceBefore=9,spaceAfter=5,keepWithNext=True))
style.add(ParagraphStyle(name='BulletGuide',parent=style['BodyGuide'],leftIndent=10,firstLineIndent=-8))
style.add(ParagraphStyle(name='CodeGuide',fontName='Courier',fontSize=8,leading=10,spaceAfter=8))
def inline(s):
    s=escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2" color="#17608b">\1</link>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Courier" size="8">\1</font>',s)
    return s
lines=SOURCE.read_text(encoding='utf-8').splitlines()
story=[];i=0
while i<len(lines):
    line=lines[i]
    if not line.strip(): i+=1;continue
    if line.startswith('```'):
        code=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]);i+=1
        story.append(Preformatted('\n'.join(code),style['CodeGuide']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            raw=[s.strip() for s in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',s) for s in raw):
                rows.append([Paragraph(inline(s),style['TableGuide']) for s in raw])
            i+=1
        width=487
        widths=[110,width-110] if len(rows[0])==2 else [115,150,width-265]
        t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9f0f5')),
            ('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#69879a')),
            ('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d6dfe5')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.extend([t,Spacer(1,8)]);continue
    st='BodyGuide'
    if line.startswith('# '): line=line[2:];st='TitleGuide'
    elif line.startswith('## '): line=line[3:];st='H2Guide'
    elif line.startswith('### '): line=line[4:];st='H3Guide'
    elif line.startswith('- '): line='- '+line[2:];st='BulletGuide'
    story.append(Paragraph(inline(line),style[st]));i+=1
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#cbd5df'));c.line(54,40,541,40)
    c.setFont('Guide',8);c.setFillColor(colors.HexColor('#596b78'))
    c.drawString(54,27,'QIP submission preparation | Checked 26 October 2026')
    c.drawRightString(541,27,str(d.page));c.restoreState()
doc=SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),leftMargin=54,rightMargin=54,
                      topMargin=48,bottomMargin=54,title='Quantum Information Processing: revision and submission guide',author='Project preparation document')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# Preserve the publisher package already downloaded in the previous research stage.
zpath=ROOT/'.firecrawl/springer-template.zip'
with ZipFile(zpath) as z:
    for name in ['user-manual.pdf','sn-article.tex','sn-jnl.cls']:
        (OUT/name).write_bytes(z.read('sn-article-template/'+name))
    (OUT/'sn-mathphys-num.bst').write_bytes(z.read('sn-article-template/bst/sn-mathphys-num.bst'))
pdfdoc=fitz.open(PDF)
for n,p in enumerate(pdfdoc):
    p.get_pixmap(matrix=fitz.Matrix(1.05,1.05)).save(OUT/f'guide_page_{n+1}.png')
checks={'date':'2026-10-26','pdf_pages':len(pdfdoc),'markdown_words_approx':len(SOURCE.read_text(encoding='utf-8').split()),
 'main_tex_sha256':hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest(),
 'main_bib_sha256':hashlib.sha256((ROOT/'paper/references.bib').read_bytes()).hexdigest(),
 'main_pdf_sha256':hashlib.sha256((ROOT/'paper/main.pdf').read_bytes()).hexdigest(),
 'unchanged_paper_expected_sha256':'0fd2c3494dc74383403e2e8673731134ebbe1aea94e8e1399bb87929f3e8dd9d',
 'guide_pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
 'template_archive_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),
 'template_sample_version':'3.1 December 2024; local cached official package',
 'main_class_matches_cached_package':(ROOT/'paper/sn-jnl.cls').read_bytes()==(OUT/'sn-jnl.cls').read_bytes(),
 'source_file_unchanged':True,'submitted':False,
 'source_access_notes':['Fresh official web checks; existing Firecrawl cache read as supporting context. Earlier Firecrawl insufficient-credit result not retried.',
 'Live template page links December2024package; ZIP re-download unavailable through web tool. Local matching package/manual inspected instead.',
 'Portal itself not inspected behind login. No form was submitted.','Abstract limit conflict is recorded, not resolved by inference.']}
assert checks['main_tex_sha256']==checks['unchanged_paper_expected_sha256']
prior=json.loads((ROOT/'research_log/references_literature_20261026/FINAL_CHECKS.json').read_text())
assert checks['main_bib_sha256']==prior['bib_sha256'] and checks['main_pdf_sha256']==prior['pdf_sha256']
alltext='\n'.join(p.get_text() for p in pdfdoc)
for token in ['80','150','383','Madhavi','Contributions','Completion gates']:
    assert token in alltext,token
assert '\ufffd' not in alltext
(OUT/'DOCUMENT_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
