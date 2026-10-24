import fitz, json, math,collections,re
from pathlib import Path
import sys
PDF=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/SPHA_20260817.pdf')
ROOT=Path(__file__).resolve().parents[1]
pdf=fitz.open(PDF);d=json.load(open(ROOT/'data/sales.json'))
G={'1A':['ABCDEFGHIJ'.replace('I','') , 'ABCDEFGHIJ'.replace('I',''),'ABC'], '1B':['ABCDEFGH','ABCDEFGH','ABC'],'2':['ABCDEFGHJK','ABCDEFGHJK','ABCD']}
def head(page,tower):
 ws=pdf[page-1].get_text('words'); a=[z for z in ws if z[4] in 'ABCDEFGHJK' and 215<=z[1]<=240 and z[0]>550]
 a.sort(key=lambda x:x[0]); expected=''.join(G[tower]); h=''.join(z[4] for z in a);
 if h!=expected:print('HEADER MISMATCH',page,h,expected)
 n=[len(z) for z in G[tower]]; i=0;mp={}
 for group,units in zip(['2','standard','28' if tower!='2' else '27'],G[tower]):
  for char in units:
   if i>=len(a):break
   q=a[i];mp[(group,char)]=(q[0]+q[2])/2;i+=1
 return mp, ws

def ck(kind,lo,hi):
 arr=d[kind]; results=collections.Counter(); failures=[]; marks_total=0; captured=set(); unsourced=[]
 for p in range(lo,hi+1):
  rows=[r for r in arr if r['page']==p];tower=rows[0]['tower']; mp,ws=head(p,tower)
  minx,maxx=min(mp.values()),max(mp.values());
  marks=[]
  for w in ws:
   cx=(w[0]+w[2])/2; y=w[1]; v=w[4]
   if y>229 and y<770 and minx-10<cx<maxx+10 and (v=='\uf0fc' if kind=='appliances' else v.isdigit()):marks.append((cx,y,v,w))
  marks_total+=len(marks)
  for j,r in enumerate(rows):
   try:x=mp[(r['group'],r['unit'])]
   except KeyError:
    results['bad-key']+=1;failures.append(('bad-key',p,r));continue
   y=r['rowY'];
   candidates=[(k,math.hypot((w[0]+w[2])/2-x, (w[1]-y)*2)) for k,(_,_,_,w) in enumerate(marks) if abs((w[0]+w[2])/2-x)<9 and abs(w[1]-y)<5]
   candidates.sort(key=lambda a:a[1]);
   if not candidates:results['not-found']+=1;failures.append(('not-found',p,r['group'],r['unit'],y,r.get('quantity') or r.get('model')));continue
   k,dist=candidates[0];mark=marks[k];actual=mark[2];want='\uf0fc' if kind=='appliances' else str(r['quantity'])
   if actual!=want:
    results['mismatch']+=1;failures.append(('mismatch',p,r['group'],r['unit'],y,want,actual));continue
   results['matched']+=1;captured.add((p,k))
  missing=[(p,round(x,1),round(y,1),v) for i,(x,y,v,w) in enumerate(marks) if (p,i) not in captured]
  unsourced+=missing
  print(kind,p,'db',len(rows),'marks',len(marks),'missing',len(missing))
 print('SUMMARY',kind,'data',len(arr),'matched',results,'marks_total',marks_total,'missing marks',len(unsourced))
 print('FAILURES',failures[:30]);print('MISSING MARKS',unsourced[:30]);
 return results,failures,unsourced
if __name__=='__main__':
 a,fa,ma=ck('appliances',105,110)
 m,fm,mm=ck('me',111,119)
 assert a['matched']==788 and not fa and not ma,(a,fa[:5],ma[:5])
 assert m['matched']==2950 and not fm and not mm,(m,fm[:5],mm[:5])
 print('PASS: 788 appliance checkmarks + 2,950 M&E numeric cells checked in both directions')
