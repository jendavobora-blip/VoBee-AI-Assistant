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
                                .then(cachedResponse => {
                                    if (cachedResponse) {
                                        return cachedResponse;
                                    }
                                    // If index.html is not cached, return a basic offline page
                                    return new Response(
                                        '<!DOCTYPE html><html><head><title>VoBee - Offline</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#1a1a2e;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}h1{color:#ffc107}</style></head><body><div><h1>🐝 VoBee</h1><p>You are currently offline</p><p>Please check your internet connection</p></div></body></html>',
                                        { 
                                            status: 200, 
                                            statusText: 'OK',
                                            headers: { 'Content-Type': 'text/html' }
                                        }
                                    );
                                });
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
                cacheNames
                    .filter(cacheName => cacheName !== CACHE_NAME)
                    .map((cacheName) => {
                        console.log('VoBee: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    })
            );
        }).then(() => {
            // Take control of all clients immediately
            return self.clients.claim();
        })
    );
});
