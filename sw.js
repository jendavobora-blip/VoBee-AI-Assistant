/**
 * VoBee AI Assistant - Service Worker
 * 
 * Enables PWA functionality with offline support and caching
 */

const CACHE_NAME = 'vobee-cache-v2';
const STATIC_CACHE = 'vobee-static-v2';
const DYNAMIC_CACHE = 'vobee-dynamic-v2';

const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/css/styles.css',
    '/js/chatbot.js',
    '/js/response-patterns.js',
    '/manifest.json',
    '/icons/icon-192.png',
    '/icons/icon-512.png',
    '/icons/apple-touch-icon.png',
    '/favicon.ico'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
    console.log('[SW] Installing VoBee service worker...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[SW] Caching app shell and static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((error) => {
                console.error('[SW] Cache failed during install:', error);
            })
    );
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating VoBee service worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Claim all clients immediately
    return self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip cross-origin requests
    if (url.origin !== location.origin) {
        return;
    }
    
    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    // Return cached response and update cache in background
                    updateCache(request);
                    return cachedResponse;
                }
                
                // Not in cache, fetch from network
                return fetch(request)
                    .then((networkResponse) => {
                        // Cache successful responses
                        if (networkResponse && networkResponse.status === 200) {
                            const responseToCache = networkResponse.clone();
                            caches.open(DYNAMIC_CACHE)
                                .then((cache) => {
                                    cache.put(request, responseToCache);
                                });
                        }
                        return networkResponse;
                    })
                    .catch((error) => {
                        console.error('[SW] Fetch failed:', error);
                        // Return offline page for navigation requests
                        if (request.mode === 'navigate') {
                            return caches.match('/index.html');
                        }
                        throw error;
                    });
            })
    );
});

// Background cache update function
function updateCache(request) {
    fetch(request)
        .then((response) => {
            if (response && response.status === 200) {
                const responseToCache = response.clone();
                caches.open(DYNAMIC_CACHE)
                    .then((cache) => {
                        cache.put(request, responseToCache);
                    });
            }
        })
        .catch(() => {
            // Silently fail - we already have cached version
        });
}

// Handle messages from clients
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(DYNAMIC_CACHE)
                .then((cache) => {
                    return cache.addAll(event.data.urls);
                })
        );
    }
});

// Background sync for offline functionality
self.addEventListener('sync', (event) => {
    console.log('[SW] Background sync event:', event.tag);
    
    if (event.tag === 'sync-messages') {
        event.waitUntil(
            // Sync logic can be added here for offline message queue
            Promise.resolve()
        );
    }
});

// Push notifications support (for future enhancements)
self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : {};
    const title = data.title || 'VoBee Notification';
    const options = {
        body: data.body || 'You have a new message!',
        icon: '/icons/icon-192.png',
        badge: '/icons/icon-96.png',
        vibrate: [200, 100, 200],
        data: data.data || {}
    };
    
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

console.log('[SW] VoBee service worker loaded');
