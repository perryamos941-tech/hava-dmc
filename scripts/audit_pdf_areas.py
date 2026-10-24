import json,fitz,re,collections
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
src=R/'data/sales.json'; d=json.load(open(src));doc=fitz.open(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/SPHA_20260817.pdf')
unique={(v['page'],v['tower'],v['group'],v['unit']):v for v in d['units'].values()}
problems=[]; ok=0
for key,r in unique.items():
 p=doc[r['page']-1];w=p.get_text('words');unit=r['unit'];anchors=[q for q in w if q[4]==unit and 250<=q[0]<=300 and 210<=q[1]<=700]
 if len(anchors)!=1:problems.append((key,'unit anchor',len(anchors)));continue
 y=anchors[0][1]
 # numeric helpers: find token in fixed area columns by line, not only membership check
 def tokens(xlo,xhi,ylo,yhi):return [(q[4],q[0],q[1]) for q in w if xlo<=q[0]<=xhi and y+ylo<=q[1]<=y+yhi]
 sqm=tokens(395,424,-16,-11);sqft=tokens(430,455,-16,-11)
 balcony=tokens(442,475,-1,3);utility=tokens(470,508,13,17)
 def simple(z):return [x[0] for x in z if re.fullmatch(r'\d+\.\d+|\(\d+\)|--|\(--\)',x[0])]
 s=simple(sqm);f=simple(sqft);b=simple(balcony);u=simple(utility)
 # choose patterns numeric
 sm=next((x for x in s if re.fullmatch(r'\d+\.\d+',x)),None)
 ft=next((int(x[1:-1]) for x in f if re.fullmatch(r'\(\d+\)',x)),None)
 bm=next((x for x in b if re.fullmatch(r'\d+\.\d+',x)),None);bs=next((int(x[1:-1]) for x in b if re.fullmatch(r'\(\d+\)',x)),None)
 um=next((x for x in u if re.fullmatch(r'\d+\.\d+',x)),None);us=next((int(x[1:-1]) for x in u if re.fullmatch(r'\(\d+\)',x)),None)
 want=[r['sqm'],r['sqft'],r['balconySqm'],r['balconySqft'],r['utilitySqm'],r['utilitySqft']]
 got=[sm,ft,bm,bs,um,us]
 if got!=want: problems.append((key,'mismatch',want,got,{'sqft':sqft,'bal':balcony,'utl':utility}))
 else:ok+=1
print('AREA TEMPLATES CHECKED',len(unique),'OK',ok,'PROBLEMS',len(problems))
for x in problems[:40]:print(x)

assert ok==64 and not problems,problems[:10]
