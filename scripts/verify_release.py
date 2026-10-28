"""HAVA structured sales brochure preflight; only standard library is required."""
from pathlib import Path
import argparse, json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]

def check(expression, message):
    if not expression: raise AssertionError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pdf',type=Path,help='Optional: uploaded SPHA_20260817.pdf to verify byte-level SHA-256')
    args=ap.parse_args()
    db=json.loads((ROOT/'data/sales.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'data/quality.json').read_text(encoding='utf-8'))
    diff=json.loads((ROOT/'data/version_diff_v2026.json').read_text(encoding='utf-8'))
    check(manifest['siteVersion']==db['source']['version'],'wrong version')
    check(db['source']['file']==manifest['currentBrochure']['filename'],'mixed source names')
    check(db['source']['contentSha256']==manifest['currentBrochure']['sha256'],'source checksum mismatch')
    check(db['source']['pages']==135,'wrong source page count')
    check(db['source']['originalUrl']==manifest['currentBrochure']['url'],'PDF links mismatch')
    check(len(db['units'])==594 and len(db['appliances'])==788 and len(db['me'])==2950,'data size unexpected')
    check(manifest['auditCoverage']['mechanicalSourceNonEmptyCells']==2950,'source grid count mismatch')
    check(len(diff['revisedMechanicalCells'])==5 and len(manifest['revisedMechanicalCells'])==5,'version delta mismatch')
    for collection,lo,hi in [('appliances',105,110),('me',111,119)]:
        for row in db[collection]:
            check(lo<=row['page']<=hi,f'{collection} invalid page {row}')
            check(row['tower'] in ('1A','1B','2'),'invalid tower')
            check(row['auditStatus'] in ('pdf_coordinate_crosschecked','sample_row_reviewed','version_change_reconciled'),f'bad audit status: {row}')
    for key,u in db['units'].items():
        check(50<=u['page']<=64,f'{key} invalid area source page')
        check(u['auditStatus']=='pdf_area_template_crosschecked',f'area wrongly marked verified: {key}')
        check((ROOT/u['unitImage']).exists(),f'{key} missing unit drawing')
    changed_count=0
    for change in diff['revisedMechanicalCells']:
        matching=[r for r in db['me'] if r['tower']==change['tower'] and r['group']==change['floorGroup'] and r['unit']==change['unit'] and r['page']==change['pdfPage'] and r['item']==change['item'] and r['room']==change['room'] and abs(r['rowY']-change['y0'])<0.5]
        check(len(matching)==1,f'changed cell lookup error: {change}')
        row=matching[0]
        check(row['quantity']==change['2026'] and row['priorQuantity']==change['2025'],'changed cell still old value')
        check(row['auditStatus']=='version_change_reconciled','changed cell lacks evidence')
        changed_count+=1
    sampled=[a for a in db['appliances'] if a['auditStatus']=='sample_row_reviewed']
    check(len(sampled)==11,'sample count mismatch')
    check(all(a['tower']=='1A' and a['group']=='standard' and a['unit']=='E' for a in sampled),'audit scope leakage')
    check(len([x for x in db['me'] if x['auditStatus']=='version_change_reconciled'])==changed_count,'5 changes not reconciled')
    check(len([x for x in db['me'] if x['auditStatus']=='pdf_coordinate_crosschecked'])==2945,'unreviewed count incorrect')
    for t in ['index.html','units.html','drawings.html','quality.html','data/quality.js','data/sales.js','data/content.js']:
        check((ROOT/t).is_file(),f'missing {t}')
    for rec in json.loads((ROOT/'data/drawings.json').read_text()):
        for target in (f"brochure/drawing-{rec['page']}.webp",f"brochure/drawing-thumb-{rec['page']}.webp"):
            check((ROOT/target).exists(),f'missing {target}')
    html=(ROOT/'units.html').read_text(encoding='utf-8')
    js=(ROOT/'assets/units.js').read_text(encoding='utf-8')
    check('售樓說明書 · 2025-01-22' not in html,'stale 2025 default source label')
    check('Based on the 22 January 2025 sales brochure' not in js,'stale English disclaimer')
    check('data/quality.js?v='+manifest['siteVersion'] in html,'missing quality metadata')
    if args.pdf:
        check(args.pdf.is_file(),f'PDF not found: {args.pdf}')
        digest=hashlib.sha256(args.pdf.read_bytes()).hexdigest()
        check(digest==manifest['currentBrochure']['sha256'],'uploaded PDF does not match published indexed version')
    print('PASS: 594 units / 788 appliance rows / 2950 M&E rows; all 52 omissions restored / 5 reconciled cells / 11 sampled appliance entries / 26 brochure drawings')
    if args.pdf: print('PASS: official source PDF SHA-256 matches indexed document')

if __name__=='__main__':
    try:main()
    except AssertionError as exc:
        print('FAIL:',exc,file=sys.stderr);raise SystemExit(1)
