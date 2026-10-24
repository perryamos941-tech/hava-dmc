/* v1.8: network-first for document and CSS/JS; no stale mobile layout after updates. */
const CACHE='hava-dmc-drawings-v2.3';
const CORE=['./','./index.html','./app.js','./style.css','./data/content.js','./assets/icon.svg','./manifest.webmanifest','./units.html','./drawings.html','./assets/units.js','./data/sales.json','./data/sales.js'];
const THUMBS=Array.from({length:11},(_,i)=>`./plans/thumb-${77+i}.webp`);
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll([...CORE,...THUMBS])).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('hava-dmc-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 const req=event.request;const url=new URL(req.url);
 if(req.method!=='GET'||url.origin!==self.location.origin)return;
 const isCritical=req.mode==='navigate'||/\/(?:index\.html|app\.js|style\.css|service-worker\.js|units\.html|drawings\.html|assets\/units\.js|data\/content\.js|data\/sales\.(?:json|js))$/.test(url.pathname);
 if(isCritical){event.respondWith(fetch(req).then(res=>{if(res.ok){let copy=res.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(req,copy)))}return res}).catch(async()=>await caches.match(req)||await caches.match('./index.html')||Response.error()));return;}
 event.respondWith(caches.match(req).then(cached=>cached||fetch(req).then(res=>{if(res.ok){const copy=res.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(req,copy)))}return res})))
});
