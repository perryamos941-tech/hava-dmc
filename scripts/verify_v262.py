"""HAVA v2.6.2 release integrity checks. Python 3 stdlib only.
Checks version consistency, data copies, source attribution, evidence and static links;
NOT a substitute for legal sentence-by-sentence or actual installation verification.
"""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]

def require(condition,message):
    if not condition:raise AssertionError(message)

def get(path):return (ROOT/path).read_text(encoding='utf-8')
def decode_js(path,name):
    s=get(path).strip()
    prefix='window.'+name+' = '
    require(s.startswith(prefix) and s.endswith(';'),f'malformed wrapper: {path}')
    return json.loads(s[len(prefix):-1])

def main():
    release=json.loads(get('data/release_manifest.json'))
    v=release['siteVersion'];require(v=='2.6.2','unexpected site version')
    sales=json.loads(get('data/sales.json'));quality=json.loads(get('data/quality.json'))
    require(sales==decode_js('data/sales.js','HAVA_SALES'),'sales.js differs from sales.json')
    require(quality==decode_js('data/quality.js','HAVA_QUALITY'),'quality.js differs from quality.json')
    require(sales['source']['version']==quality['siteVersion']==v,'site versions inconsistent')
    require(sales['source']['originalUrl']==quality['currentBrochure']['url']==release['brochurePdf'],'sales brochure source URL mismatch')
    require(quality['dmc']['url']==release['dmcEnglishPdf'],'DMC English PDF URL mismatch')
    require(len(sales['units'])==594 and len(sales['appliances'])==788 and len(sales['me'])==2950,'record count mismatch')
    require(quality['currentBrochure']['sha256']==sales['source']['contentSha256'],'brochure hash mismatch')
    require(sales['source']['pages']==135,'wrong brochure page count')
    require('user_provided' in quality['dmc']['translationStatus'],'Chinese source status changed')
    for path in ['index.html','units.html','drawings.html','quality.html','chinese.html']:
        s=get(path)
        all_versions=re.findall(r'(?:(?:\?|&)v=)(\d+\.\d+(?:\.\d+)?)',s)
        require(all_versions and set(all_versions)=={v},f'{path} contains inconsistent revision strings {all_versions}')
        require('assets/site-nav-v26.css?v='+v in s,f'{path} missing shared navigation stylesheet')
        require('href="chinese.html"' in s and 'href="units.html"' in s,f'{path} missing unified navigation')
        require('SPH%20Site%20A%20DMC' not in s,f'{path} contains non-public Chinese PDF link')
    require('HAVA v2.5.7 · 非官方業主資訊索引' not in get('quality.html'),'quality page footer shows stale version')
    sw=get('service-worker.js')
    require("const CACHE='hava-dmc-v"+v+"'" in sw,'SW cache is outdated')
    require("if(request.mode==='navigate')" in sw and "if(hit)return hit;" in sw,'offline fallback logic absent')
    require("if(request.mode==='navigate')return (await cache.match('./index.html'))||Response.error();" in sw,'uncontrolled fallback for code')
    require("/\\.(?:js|css|json|html|webmanifest)$/" in sw,'network-first rule does not include scripts/styles')
    # Markers below are independent editorial notes, not proof every other clause is valid.
    chinese=get('chinese.html')
    for part in ['8(c)','8(e)','10','13(a)','62']:
        require(part in chinese,f'missing known discrepancy note {part}')
    require('未完成全文逐句' in chinese or '尚未完成全文逐句' in chinese,'missing non-certification limitation')
    dmc=get('data/content.js');require('window.HAVA_DATA = ' in dmc,'DMC source index missing')
    dmc_data=json.loads(dmc.split(' = ',1)[1].rstrip().rstrip(';'))
    require(len(dmc_data['translations'])==85,'DMC 85 sections truncated')
    # PDF anchors on the unified Chinese reader must resolve to the English deed.
    hrefs=re.findall(r'href="([^"]+\.pdf(?:#page=\\d+)?)"',chinese)
    require(not hrefs or all(release['dmcEnglishPdf'] in url for url in hrefs),'Chinese reader links a different PDF')
    for page in range(77,88):require((ROOT/f'plans/plan-{page}.jpg').exists(),f'missing DMC plan {page}')
    require('downloadDrawing' in get('app.js') and 'download=' in get('app.js'),'DMC download UI missing')
    require('id="vdownload"' in get('drawings.html'),'Sales viewer download UI missing')
    require('downloadCrop' in get('assets/units.js'),'Unit image download UI missing')
    require(len(list((ROOT/'plans').glob('plan-*.jpg')))==11,'DMC plan image count incorrect')
    draw=json.loads(get('data/drawings.json'))
    require(len(draw)==26,'sales brochure drawing count changed')
    for row in draw:require(f'HAVA_SalesBrochure_20260817_P'+str(row['page']) in get('drawings.html') or 'HAVA_SalesBrochure_20260817_P${r.page}' in get('drawings.html'),'sales high-resolution download attribute missing')
    for row in draw:
        for kind in ['drawing-','drawing-thumb-']:
            require((ROOT/f"brochure/{kind}{row['page']}.webp").exists(),f"missing brochure image {row['page']}")
    for target in ['index.html','units.html','drawings.html','quality.html','chinese.html','app.js','assets/units.js','assets/site-nav-v26.css','manifest.webmanifest','.nojekyll']:
        require((ROOT/target).is_file(),f'missing required file {target}')
    print('PASS v2.6.2 | version and five page revisions | JSON/JS synchronized | DMC 85 blocks | 594 units | 788 appliances | 2950 M&E | 26 brochure + 11 DMC drawings | 5 known discrepancy labels')
    print('LIMIT: these are structural checks, not independent legal certification or real-device deployment verification')

if __name__=='__main__':
    try: main()
    except (AssertionError,KeyError,ValueError) as e:
        print('FAIL:',str(e),file=sys.stderr);raise SystemExit(1)
