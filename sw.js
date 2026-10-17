/* Static GitHub Pages-compatible caching, confined to this project's scope. */
self.window = self;
importScripts('./offline/catalog.js');
importScripts('./assets/runtime-manifest.js');
const CATALOG = self.CODELAB_OFFLINE_CATALOG;
const PREFIX = 'codelab-library-v2-'+encodeURIComponent(new URL(self.registration.scope).pathname)+'-';
const CACHE = PREFIX + CATALOG.revision;
const SHELL = ['./', ...self.CODELAB_RUNTIME.shell];
const ALLOWED = new Set([...SHELL, ...CATALOG.files,...self.CODELAB_RUNTIME.files.map(f=>f.path)].map(path => new URL(path, self.registration.scope).href));

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)));
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const name of await caches.keys()) {
      if (name.startsWith(PREFIX) && name !== CACHE) await caches.delete(name);
    }
    await self.clients.claim();
  })());
});
self.addEventListener('message', event => {
  if (event.data?.type !== 'CODELAB_APPLY_UPDATE') return;
  event.waitUntil((async () => {
    const tabs = (await self.clients.matchAll({type:'window',includeUncontrolled:true}))
      .filter(client => client.url.startsWith(self.registration.scope));
    // Another tab may be running an exam, including one on an older app version.
    if (tabs.length > 1) {
      event.ports[0]?.postMessage({ok:false,message:'Close other Study Lab tabs and installed windows before applying the update.'});
      return;
    }
    event.ports[0]?.postMessage({ok:true});
    await self.skipWaiting();
  })());
});
self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  url.search = '';
  url.hash = '';
  if (!ALLOWED.has(url.href)) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const saved = await cache.match(url.href);
    if (saved) return saved;
    const response = await fetch(request);
    if (response.ok) await cache.put(url.href, response.clone());
    return response;
  })());
});
