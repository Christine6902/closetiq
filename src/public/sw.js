// ClosetIQ service worker.
//
// On localhost it acts as a KILL SWITCH: a caching SW on a dev server turns
// every server restart into a sticky "You're offline" page, so here the SW
// clears its caches, unregisters itself, and reloads open tabs. On a real
// (production) host it behaves as a normal PWA app-shell cache.

const HOST = self.location.hostname;
const IS_LOCAL =
    HOST === "localhost" || HOST === "127.0.0.1" || HOST === "[::1]" || HOST.endsWith(".localhost");

if (IS_LOCAL) {
    self.addEventListener("install", function () { self.skipWaiting(); });
    self.addEventListener("activate", function (event) {
        event.waitUntil((async function () {
            const keys = await caches.keys();
            await Promise.all(keys.map(function (k) { return caches.delete(k); }));
            await self.registration.unregister();
            const clients = await self.clients.matchAll({ type: "window" });
            clients.forEach(function (c) {
                try { c.navigate(c.url); } catch (e) { /* ignore */ }
            });
        })());
    });
} else {
    // ── Production PWA app-shell cache ────────────────────────────────
    const CACHE = "closetiq-v1";
    const APP_SHELL = [
        "/",
        "/offline.html",
        "/css/tina4.min.css",
        "/css/closetiq.css",
        "/js/tina4.min.js",
        "/js/frond.min.js",
        "/js/closetiq.js",
        "/icons/icon-192.png",
        "/icons/icon-512.png",
    ];

    self.addEventListener("install", function (event) {
        event.waitUntil(
            caches.open(CACHE)
                .then(function (cache) { return Promise.allSettled(APP_SHELL.map(function (u) { return cache.add(u); })); })
                .then(function () { return self.skipWaiting(); })
        );
    });

    self.addEventListener("activate", function (event) {
        event.waitUntil(
            caches.keys()
                .then(function (keys) {
                    return Promise.all(keys.filter(function (k) { return k !== CACHE; })
                        .map(function (k) { return caches.delete(k); }));
                })
                .then(function () { return self.clients.claim(); })
        );
    });

    self.addEventListener("fetch", function (event) {
        const req = event.request;
        if (req.method !== "GET") return;

        const url = new URL(req.url);
        if (url.origin !== self.location.origin) return;
        if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/__dev")) return;

        // Navigations: network-first, fall back to the cached page, then offline.
        if (req.mode === "navigate") {
            event.respondWith(
                fetch(req).catch(function () {
                    return caches.match(req).then(function (r) { return r || caches.match("/offline.html"); });
                })
            );
            return;
        }

        // Static assets: cache-first, then network (and cache the result).
        event.respondWith(
            caches.match(req).then(function (cached) {
                return cached || fetch(req).then(function (resp) {
                    if (resp && resp.ok && resp.type === "basic") {
                        const copy = resp.clone();
                        caches.open(CACHE).then(function (c) { c.put(req, copy); });
                    }
                    return resp;
                });
            })
        );
    });
}
