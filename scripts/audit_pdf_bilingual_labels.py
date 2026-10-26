"""Independent source-to-website bilingual labels audit; requires PyMuPDF.
Reads 2026 uploaded PDF directly. This is a machine geometry cross-check, not certified human review.
"""
from pathlib import Path
import json,re,fitz,bisect,sys
ROOT=Path(__file__).resolve().parents[1]
db=json.loads((ROOT/'data/sales.json').read_text())
pdf=fitz.open(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/SPHA_20260817.pdf')
def norm(x):return re.sub('[^a-z0-9]','',x.lower())
brands=['Siemens','Miele','Philco','Stiebel Eltron','TGC','Panasonic','Ostberg','Toshiba']
checks=0
for pg in range(105,111):
 p=pdf[pg-1];br_left,br_right=(394,550) if pg<=108 else (354,496);cat_right=br_left
 for column in ('brand','category'):
  left,right=(br_left,br_right) if column=='brand' else (76.5,cat_right)
  b={233,735}
  for shape in p.get_drawings():
   for z in shape['items']:
    if z[0]=='l':
     a,q=z[1],z[2]
     if abs(a.y-q.y)<.2 and 225<a.y<735 and abs(a.x-left)<2 and abs(q.x-right)<2:b.add(round(a.y,2))
  boundaries=sorted(b)
  for y,model,brand,category in {(r['rowY'],r['model'],r['brand'],r['category']) for r in db['appliances'] if r['page']==pg}:
   i=bisect.bisect_right(boundaries,y);lo=boundaries[i-1] if i else 233;hi=boundaries[i] if i<len(boundaries) else 735
   txt=p.get_text('text',clip=fitz.Rect(left+1,lo+.1,right-1,hi-.1))
   if column=='brand':
    match=[n for n in brands if re.search(r'(?<![A-Za-z])'+re.escape(n)+r'(?![A-Za-z])',txt,re.I)]
    assert len(match)==1,(pg,y,model,'brand source',match,txt)
    assert match[0].lower() in brand.lower(),(pg,y,model,'brand mismatch',brand,match[0])
   else:
    en=re.search(r'[A-Za-z].*',category).group()
    assert norm(en) in norm(txt),(pg,y,model,'category mismatch',category,txt)
   checks+=1
missing=[];me_ok=0
for pg,y,item in {(r['page'],r['rowY'],r['item']) for r in db['me']}:
 source=pdf[pg-1].get_text('text',clip=fitz.Rect(247,y-13,578,y+17))
 zh=''.join(re.findall(r'[\u3400-\u9fff]+',item))
 actual=''.join(re.findall(r'[\u3400-\u9fff]+',source))
 if not zh or zh not in actual:missing.append((pg,y,item,actual))
 me_ok+=1
assert not missing,missing[:12]
print('PASS: source category + brand: %s checks across 98 unique appliance lines; bilingual M&E labels: %s checked'%(checks,me_ok))
