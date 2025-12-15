#!/usr/bin/env node

/**
 * Optimization Test Runner
 * Tests the AI optimization system
 */

console.log('='.repeat(60));
console.log('🧠 VoBee AI Optimization Test Runner');
console.log('='.repeat(60));
console.log('');

// Simulate browser environment
global.window = {
    caches: {
        open: async () => ({
            match: async () => null,
            put: async () => {},
            keys: async () => [],
            delete: async () => {}
        })
    }
};

global.indexedDB = {
    open: (name, version) => {
        const request = {
            onsuccess: null,
            onerror: null,
            onupgradeneeded: null,
            result: {
                transaction: () => ({
                    objectStore: () => ({
                        get: () => ({ onsuccess: null, onerror: null }),
                        put: async () => {}
                    })
                }),
                objectStoreNames: {
                    contains: () => false
                },
                createObjectStore: () => ({})
            }
        };
        setTimeout(() => {
            if (request.onsuccess) request.onsuccess({ target: request });
        }, 10);
        return request;
    }
};

global.fetch = async (url, options) => {
    // Simulate API response
    return {
        json: async () => ({ success: true, data: 'test' }),
        ok: true
    };
};

global.caches = global.window.caches;

const AIOptimization = require('../js/ai-optimization.js');

async function runOptimizationTests() {
    try {
        const optimizer = new AIOptimization();
        
        console.log('Initializing AI Optimization System...');
        await optimizer.init();
        
        console.log('\n📊 Running optimization tests...\n');
        
        // Test 1: API Call Optimization
        console.log('Test 1: Optimized API Calls');
        const testURL = 'https://api.example.com/data';
        
        const start = Date.now();
        for (let i = 0; i < 5; i++) {
            await optimizer.optimizedAPICall(testURL, { method: 'GET' });
        }
        const duration = Date.now() - start;
        
        console.log(`  ✓ Made 5 API calls in ${duration}ms`);
        
        // Test 2: Get Statistics
        console.log('\nTest 2: Optimization Statistics');
        const stats = optimizer.getStatistics();
        console.log('  Statistics:', JSON.stringify(stats, null, 2));
        
        // Test 3: Learning and Pattern Analysis
        console.log('\nTest 3: Learning and Pattern Analysis');
        const patterns = await optimizer.learnAndOptimize();
        console.log('  Patterns detected:', JSON.stringify(patterns, null, 2));
        
        console.log('\n' + '='.repeat(60));
        console.log('✓ All optimization tests passed!');
        console.log('='.repeat(60));
        console.log('\nOptimization Summary:');
        console.log(`  - Cache Hits: ${stats.cacheHits}`);
        console.log(`  - Deduplication Hits: ${stats.deduplicationHits}`);
        console.log(`  - Total Optimizations: ${stats.totalOptimizations}`);
        console.log(`  - Savings Rate: ${stats.savingsRate.toFixed(2)}%`);
        
        process.exit(0);
    } catch (error) {
        console.error('\n✗ Optimization test failed:', error);
        process.exit(1);
    }
}

runOptimizationTests();
