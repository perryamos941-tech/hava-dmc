"""Check model and M&E English item labels against on-page source text; PyMuPDF needed.
These are machine comparisons, NOT human product-certification or legal checks.
Usage: python scripts/audit_pdf_labels.py /path/to/SPHA_20260817.pdf
"""
import json,fitz,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/sales.json').read_text(encoding='utf-8'))
P=fitz.open(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/SPHA_20260817.pdf')
text_cache={n:P[n-1].get_text('words') for n in list(range(105,111))+list(range(111,120))}
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
models={(r['page'],r['rowY'],r['model']) for r in D['appliances']}
for page,y,model in models:
 words=text_cache[page];line=' '.join(v[4] for v in sorted(words,key=lambda x:x[0]) if 480<v[0]<702 and abs(v[1]-y)<2.8)
 if not all(norm(x) in norm(line) for x in model.split('/')):raise AssertionError(f'Appliance model differs: {page}, {y}, {model}, {line}')
items={(r['page'],r['rowY'],r['item']) for r in D['me']}
for page,y,item in items:
 words=text_cache[page];line=' '.join(v[4] for v in sorted(words,key=lambda x:(x[1],x[0])) if 250<=v[0]<555 and y-7<=v[1]<=y+6)
 match=re.search(r'(?<!\S)[A-Z][a-z].*',item)
 if not match or norm(match.group()) not in norm(line):raise AssertionError(f'M&E item differs: {page}, {y}, {item}, {line}')
print(f'PASS: {len(models)} unique appliance model rows and {len(items)} unique M&E English item lines (including wrapped labels) match the source PDF')
