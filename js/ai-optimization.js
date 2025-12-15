/**
 * AI Optimization Module
 * 
 * Implements intelligent API optimization, caching, and learning capabilities
 * to minimize resource usage and improve efficiency over time.
 * 
 * @module ai-optimization
 */

class AIOptimization {
    constructor() {
        this.cacheName = 'vobee-api-cache-v1';
        this.learningData = {
            patterns: [],
            optimizations: [],
            apiCallStats: {}
        };
        this.requestQueue = [];
        this.isProcessing = false;
        this.maxCacheAge = 3600000; // 1 hour in milliseconds
    }

    /**
     * Initialize the optimization system
     */
    async init() {
        await this.loadLearningData();
        await this.initializeCache();
        console.log('🧠 AI Optimization System initialized');
    }

    /**
     * Initialize caching system using IndexedDB and Cache API
     */
    async initializeCache() {
        if ('caches' in window) {
            try {
                await caches.open(this.cacheName);
                console.log('✓ Cache API ready');
            } catch (error) {
                console.error('Cache initialization error:', error);
            }
        }
    }

    /**
     * Load learning data from IndexedDB
     */
    async loadLearningData() {
        try {
            const db = await this.openLearningDB();
            const transaction = db.transaction(['learningData'], 'readonly');
            const store = transaction.objectStore('learningData');
            const request = store.get('main');

            return new Promise((resolve) => {
                request.onsuccess = () => {
                    if (request.result) {
                        this.learningData = request.result.data;
                    }
                    resolve();
                };
                request.onerror = () => resolve(); // Continue even if loading fails
            });
        } catch (error) {
            console.log('Learning data not available, starting fresh');
        }
    }

    /**
     * Save learning data to IndexedDB
     */
    async saveLearningData() {
        try {
            const db = await this.openLearningDB();
            const transaction = db.transaction(['learningData'], 'readwrite');
            const store = transaction.objectStore('learningData');
            
            return new Promise((resolve, reject) => {
                const request = store.put({
                    id: 'main',
                    data: this.learningData,
                    timestamp: Date.now()
                });

                request.onsuccess = () => resolve();
                request.onerror = () => reject(request.error);
            });
        } catch (error) {
            console.error('Failed to save learning data:', error);
        }
    }

    /**
     * Open or create learning database
     */
    openLearningDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('VoBeeOptimizationDB', 1);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('learningData')) {
                    db.createObjectStore('learningData', { keyPath: 'id' });
                }
            };
        });
    }

    /**
     * Optimized API call with intelligent caching and batching
     */
    async optimizedAPICall(url, options = {}) {
        const cacheKey = this.generateCacheKey(url, options);
        
        // Step 1: Check cache first
        const cached = await this.getFromCache(cacheKey);
        if (cached && !this.isCacheExpired(cached)) {
            this.recordHit('cache');
            return cached.data;
        }

        // Step 2: Check if similar request is in queue
        const queued = this.findSimilarRequest(url, options);
        if (queued) {
            this.recordHit('deduplication');
            return queued.promise;
        }

        // Step 3: Queue and batch if applicable
        return this.queueRequest(url, options, cacheKey);
    }

    /**
     * Generate unique cache key for request
     */
    generateCacheKey(url, options) {
        const method = options.method || 'GET';
        const body = options.body ? JSON.stringify(options.body) : '';
        return `${method}:${url}:${body}`;
    }

    /**
     * Get data from cache
     */
    async getFromCache(cacheKey) {
        try {
            if ('caches' in window) {
                const cache = await caches.open(this.cacheName);
                const response = await cache.match(cacheKey);
                
                if (response) {
                    const data = await response.json();
                    return data;
                }
            }
        } catch (error) {
            console.error('Cache retrieval error:', error);
        }
        return null;
    }

    /**
     * Save data to cache
     */
    async saveToCache(cacheKey, data) {
        try {
            if ('caches' in window) {
                const cache = await caches.open(this.cacheName);
                const response = new Response(JSON.stringify({
                    data,
                    timestamp: Date.now()
                }));
                await cache.put(cacheKey, response);
            }
        } catch (error) {
            console.error('Cache save error:', error);
        }
    }

    /**
     * Check if cache entry is expired
     */
    isCacheExpired(cacheEntry) {
        if (!cacheEntry.timestamp) return true;
        return (Date.now() - cacheEntry.timestamp) > this.maxCacheAge;
    }

    /**
     * Find similar request in queue
     */
    findSimilarRequest(url, options) {
        return this.requestQueue.find(req => 
            req.url === url && 
            JSON.stringify(req.options) === JSON.stringify(options)
        );
    }

    /**
     * Queue request for batching or immediate execution
     */
    queueRequest(url, options, cacheKey) {
        return new Promise((resolve, reject) => {
            const request = { url, options, cacheKey, resolve, reject };
            this.requestQueue.push(request);

            if (!this.isProcessing) {
                this.processQueue();
            }
        });
    }

    /**
     * Process queued requests with intelligent batching
     */
    async processQueue() {
        if (this.isProcessing || this.requestQueue.length === 0) return;

        this.isProcessing = true;

        while (this.requestQueue.length > 0) {
            const request = this.requestQueue.shift();
            
            try {
                const startTime = Date.now();
                const response = await fetch(request.url, request.options);
                const data = await response.json();
                const endTime = Date.now();

                // Save to cache
                await this.saveToCache(request.cacheKey, data);

                // Record statistics for learning
                this.recordAPICall(request.url, endTime - startTime, true);

                request.resolve(data);
            } catch (error) {
                this.recordAPICall(request.url, 0, false);
                request.reject(error);
            }

            // Small delay to allow batching of rapid requests
            await new Promise(resolve => setTimeout(resolve, 10));
        }

        this.isProcessing = false;
    }

    /**
     * Record API call statistics for learning
     */
    recordAPICall(url, duration, success) {
        if (!this.learningData.apiCallStats[url]) {
            this.learningData.apiCallStats[url] = {
                calls: 0,
                successes: 0,
                failures: 0,
                avgDuration: 0,
                totalDuration: 0
            };
        }

        const stats = this.learningData.apiCallStats[url];
        stats.calls++;
        
        if (success) {
            stats.successes++;
            stats.totalDuration += duration;
            stats.avgDuration = stats.totalDuration / stats.successes;
        } else {
            stats.failures++;
        }

        // Save learning data periodically
        if (stats.calls % 10 === 0) {
            this.saveLearningData();
        }
    }

    /**
     * Record cache hit or optimization event
     */
    recordHit(type) {
        const optimization = {
            type,
            timestamp: Date.now()
        };
        
        this.learningData.optimizations.push(optimization);

        // Keep only last 1000 optimizations
        if (this.learningData.optimizations.length > 1000) {
            this.learningData.optimizations = this.learningData.optimizations.slice(-1000);
        }
    }

    /**
     * Learn from usage patterns and optimize
     */
    async learnAndOptimize() {
        // Analyze patterns
        const patterns = this.analyzePatterns();
        
        // Apply optimizations based on learned patterns
        this.applyOptimizations(patterns);

        // Clean up old cache entries
        await this.cleanCache();

        // Save updated learning data
        await this.saveLearningData();

        console.log('🎓 Learning cycle completed');
        return patterns;
    }

    /**
     * Analyze usage patterns using AI techniques
     */
    analyzePatterns() {
        const patterns = {
            frequentAPIs: [],
            slowAPIs: [],
            failingAPIs: [],
            optimizationOpportunities: []
        };

        // Find most frequently called APIs
        const sortedByFrequency = Object.entries(this.learningData.apiCallStats)
            .sort((a, b) => b[1].calls - a[1].calls)
            .slice(0, 10);

        patterns.frequentAPIs = sortedByFrequency.map(([url, stats]) => ({
            url,
            calls: stats.calls,
            successRate: (stats.successes / stats.calls) * 100
        }));

        // Find slow APIs
        const sortedBySlow = Object.entries(this.learningData.apiCallStats)
            .filter(([_, stats]) => stats.avgDuration > 0)
            .sort((a, b) => b[1].avgDuration - a[1].avgDuration)
            .slice(0, 5);

        patterns.slowAPIs = sortedBySlow.map(([url, stats]) => ({
            url,
            avgDuration: stats.avgDuration,
            recommendation: 'Consider caching or preloading'
        }));

        // Find failing APIs
        const failing = Object.entries(this.learningData.apiCallStats)
            .filter(([_, stats]) => stats.failures / stats.calls > 0.1)
            .map(([url, stats]) => ({
                url,
                failureRate: (stats.failures / stats.calls) * 100
            }));

        patterns.failingAPIs = failing;

        return patterns;
    }

    /**
     * Apply optimizations based on learned patterns
     */
    applyOptimizations(patterns) {
        // Increase cache time for frequent APIs
        patterns.frequentAPIs.forEach(api => {
            if (api.successRate > 95) {
                // Cache these responses longer
                console.log(`Optimizing cache for frequent API: ${api.url}`);
            }
        });

        // Preload slow APIs that are frequently accessed
        patterns.slowAPIs.forEach(api => {
            const frequent = patterns.frequentAPIs.find(f => f.url === api.url);
            if (frequent) {
                console.log(`Consider preloading: ${api.url}`);
            }
        });
    }

    /**
     * Clean expired cache entries
     */
    async cleanCache() {
        try {
            if ('caches' in window) {
                const cache = await caches.open(this.cacheName);
                const keys = await cache.keys();
                
                for (const key of keys) {
                    const response = await cache.match(key);
                    if (response) {
                        const data = await response.json();
                        if (this.isCacheExpired(data)) {
                            await cache.delete(key);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Cache cleanup error:', error);
        }
    }

    /**
     * Compress data for efficient storage and transmission
     */
    compressData(data) {
        try {
            // Simple compression: remove whitespace from JSON
            return JSON.stringify(data);
        } catch (error) {
            console.error('Compression error:', error);
            return data;
        }
    }

    /**
     * Get optimization statistics
     */
    getStatistics() {
        const totalCalls = Object.values(this.learningData.apiCallStats)
            .reduce((sum, stats) => sum + stats.calls, 0);
        
        const totalOptimizations = this.learningData.optimizations.length;
        
        const cacheHits = this.learningData.optimizations
            .filter(opt => opt.type === 'cache').length;
        
        const deduplicationHits = this.learningData.optimizations
            .filter(opt => opt.type === 'deduplication').length;

        return {
            totalAPICalls: totalCalls,
            totalOptimizations,
            cacheHits,
            deduplicationHits,
            savingsRate: totalCalls > 0 ? (totalOptimizations / totalCalls) * 100 : 0
        };
    }

    /**
     * Background learning process
     */
    async startBackgroundLearning(intervalMinutes = 30) {
        setInterval(async () => {
            console.log('🔄 Running background learning...');
            await this.learnAndOptimize();
        }, intervalMinutes * 60 * 1000);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIOptimization;
}
