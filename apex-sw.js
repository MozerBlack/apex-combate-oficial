const CACHE_NAME = 'apex-combate-v43';
const APP_SHELL = [
  './',
  './apex-combate.html',
  './manifest.webmanifest',
  './assets/apex-combate-logo-oficial.png',
  './assets/apex-combate-hero.jpg',
  './assets/apex-combate-login-bg.jpg',
  './icons/apex-192.png',
  './icons/apex-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  if (new URL(event.request.url).pathname.startsWith('/api/')) return;

  // Navegações usam a rede primeiro para evitar versões antigas do aplicativo.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(response => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        return response;
      }).catch(() => caches.match(event.request).then(cached => cached || caches.match('./apex-combate.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      return response;
    }).catch(() => new Response('', { status: 503, statusText: 'Offline' })))
  );
});
