const CACHE_NAME = "badminton-coach-v2";
const SHELL_FILES = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_FILES)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

function putInCache(request, response) {
  if (!response || !response.ok) return;
  const copy = response.clone();
  caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
}

// 只处理同源请求；对 DeepSeek API 等跨域请求一律直接放行，不拦截。
// 页面本身（HTML）网络优先，保证发新版后手机能拿到更新，断网时才用缓存；
// 其余静态资源（图标、ffmpeg.wasm 解码引擎等）缓存优先，解码引擎只需下载一次。
self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isPage = req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname.endsWith("/");

  if (isPage) {
    event.respondWith(
      fetch(req)
        .then((resp) => { putInCache(req, resp); return resp; })
        .catch(() => caches.match(req).then((c) => c || caches.match("./index.html")))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) =>
      cached || fetch(req).then((resp) => { putInCache(req, resp); return resp; })
    )
  );
});
