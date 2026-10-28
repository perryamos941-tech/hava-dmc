#!/usr/bin/env python3
"""HAVA 2.6.3: check formal brochure drawings use lossless VP8L.
Optional: pass source PDF path to verify pixel-equality against independently
rendered PDF pages at 1.55x (1846 x 1305 RGB).
"""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/lossless_drawings_v263.json').read_text(encoding='utf-8'))
assert len(rows)==26
for r in rows:
 p=ROOT/'brochure'/f"drawing-{r['page']}.webp"
 b=p.read_bytes()
 assert b[:4]==b'RIFF' and b[8:16]==b'WEBPVP8L',str(p)
 assert hashlib.sha256(b).hexdigest()==r['new_sha256']
try: from PIL import Image
except ImportError: Image=None
if Image:
 for r in rows:
  with Image.open(ROOT/'brochure'/f"drawing-{r['page']}.webp") as im:
   assert im.size==(1846,1305),r['page']
if len(sys.argv)>1:
 if not Image: raise RuntimeError('Pillow required for source PDF pixel comparison')
 import fitz
 src=Path(sys.argv[1]); assert hashlib.sha256(src.read_bytes()).hexdigest()=='ce837689896a123ff95ad331ec1358173e5373b883f03d317c3db7fee1890bdc'
 with fitz.open(src) as doc:
  for r in rows:
   p=doc[r['page']-1].get_pixmap(matrix=fitz.Matrix(1.55,1.55),colorspace=fitz.csRGB,alpha=False)
   with Image.open(ROOT/'brochure'/f"drawing-{r['page']}.webp") as im:
    assert im.convert('RGB').tobytes()==p.samples,r['page']
print('PASS: 26 drawing images are lossless WebP VP8L; SHA256 checks pass'+(' and PDF pixels match' if len(sys.argv)>1 else ''))
