/**
 * VoBee AI Assistant - Service Worker
 * 
 * Enables PWA functionality with offline support and caching
 */

const CACHE_NAME = 'vobee-cache-v1';
const urlsToCache = [
    './',
    './index.html',
    './css/styles.css',
    './js/chatbot.js',
    './js/response-patterns.js',
    './manifest.json',
    './icons/icon-192.svg'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('VoBee: Caching app shell');
                return cache.addAll(urlsToCache);
            })
            .catch((error) => {
                console.error('VoBee: Cache failed during install', error);
                // Re-throw to prevent installation with incomplete cache
                throw error;
            })
    );
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    // Return cached version if available
                    return response;
                }
                
                // Clone the request because it can only be used once
                return fetch(event.request.clone())
                    .catch(() => {
                        // Network failed (offline), try to serve cached index.html for navigation requests
                        const acceptHeader = event.request.headers.get('accept');
                        if (acceptHeader && acceptHeader.includes('text/html')) {
                            return caches.match('./index.html')
                                .then(cachedResponse => cachedResponse || new Response('Offline'));
                        }
                        // For non-HTML requests, return a simple offline response
                        return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
                    });
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('VoBee: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Take control of all clients immediately
    return self.clients.claim();
});
