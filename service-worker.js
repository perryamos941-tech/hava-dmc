/* HAVA v2.6.3: network-first documents, data, CSS and JavaScript; offline cache for reviewed static resources. */
const CACHE='hava-dmc-v2.6.3';
const CORE=['./','./index.html','./app.js','./style.css','./data/content.js',
  './data/quality.js','./data/sales.js','./assets/units.js','./assets/site-nav-v26.css',
  './assets/icon.svg','./manifest.webmanifest','./units.html','./drawings.html',
  './quality.html','./chinese.html'];
const THUMBS=Array.from({length:11},(_,i)=>`./plans/thumb-${77+i}.webp`);
self.addEventListener('install',event=>event.waitUntil(
  caches.open(CACHE).then(c=>c.addAll([...CORE,...THUMBS])).then(()=>self.skipWaiting())
));
self.addEventListener('activate',event=>event.waitUntil(
  caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('hava-dmc-')&&k!==CACHE).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim())
));
self.addEventListener('fetch',event=>{
  const request=event.request;
  const url=new URL(request.url);
  if(request.method!=='GET'||url.origin!==self.location.origin)return;
  // Queries (e.g. ?v=2.6.3) must not return stale ?v=2.5.7 assets.
  const executable=/\.(?:js|css|json|html|webmanifest)$/i.test(url.pathname);
  const critical=request.mode==='navigate'||executable||url.pathname.endsWith('/');
  if(critical){
    event.respondWith(fetch(request).then(response=>{
      if(response.ok){
        const copy=response.clone();
        event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)));
      }
      return response;
    }).catch(async()=>{
      const cache=await caches.open(CACHE);
      const hit=await cache.match(request)||await cache.match(request,{ignoreSearch:true});
      // Never serve index.html as a replacement for a missing script, style or JSON.
      if(hit)return hit;
      if(request.mode==='navigate')return (await cache.match('./index.html'))||Response.error();
      return Response.error();
    }));
    return;
  }
  event.respondWith(caches.match(request).then(cached=>cached||fetch(request).then(response=>{
    if(response.ok){
      const copy=response.clone();
      event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)));
    }
    return response;
  })));
});
