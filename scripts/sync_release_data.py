#!/usr/bin/env python3
"""Synchronize derived .js copies of the JSON datasets; run after editing JSON source.
Set the release version in data/release_manifest.json first; this script syncs embedded release
metadata and derived data files without changing any DMC legal text or source record values.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'data/release_manifest.json').read_text(encoding='utf-8'))
ver=meta['siteVersion']
assert re.fullmatch(r'\d+\.\d+\.\d+',ver)
for file,variable in [('sales','HAVA_SALES'),('quality','HAVA_QUALITY')]:
 source=ROOT/f'data/{file}.json'
 data=json.loads(source.read_text(encoding='utf-8'))
 if file=='sales':data['source']['version']=ver
 else:data['siteVersion']=ver
 source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/f'data/{file}.js').write_text('window.'+variable+' = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('Synchronized derived sales.js, quality.js and JSON versions:',ver)
