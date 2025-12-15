/**
 * VoBee Testing & Automation Module
 * 
 * This module provides automated fitness testing and inline module docking
 * for the super-intelligence system.
 * 
 * @module testing-automation
 */

/**
 * Test Suite Class
 * Manages automated testing for the system
 */
class TestSuite {
    constructor() {
        this.tests = [];
        this.results = [];
        this.testModules = new Map();
        this.isRunning = false;
    }

    /**
     * Register a test module
     * @param {string} moduleName - Module name
     * @param {Object} testModule - Test module with test functions
     */
    registerModule(moduleName, testModule) {
        this.testModules.set(moduleName, testModule);
        console.log(`Test module registered: ${moduleName}`);
    }

    /**
     * Add a test case
     * @param {string} name - Test name
     * @param {Function} testFn - Test function
     * @param {string} category - Test category
     */
    addTest(name, testFn, category = 'general') {
        this.tests.push({
            name,
            testFn,
            category,
            status: 'pending'
        });
    }

    /**
     * Run all tests
     * @returns {Promise<Object>} Test results
     */
    async runAllTests() {
        if (this.isRunning) {
            console.warn('Tests are already running');
            return null;
        }

        this.isRunning = true;
        this.results = [];
        const startTime = Date.now();

        console.log(`Running ${this.tests.length} tests...`);

        for (const test of this.tests) {
            const result = await this.runTest(test);
            this.results.push(result);
        }

        const endTime = Date.now();
        const duration = endTime - startTime;

        this.isRunning = false;

        const summary = this.generateSummary(duration);
        console.log('Test Summary:', summary);

        return summary;
    }

    /**
     * Run a single test
     * @param {Object} test - Test to run
     * @returns {Promise<Object>} Test result
     */
    async runTest(test) {
        const result = {
            name: test.name,
            category: test.category,
            status: 'running',
            startTime: Date.now(),
            endTime: null,
            duration: null,
            error: null,
            output: null
        };

        try {
            const output = await test.testFn();
            result.status = 'passed';
            result.output = output;
        } catch (error) {
            result.status = 'failed';
            result.error = error.message;
            console.error(`Test failed: ${test.name}`, error);
        }

        result.endTime = Date.now();
        result.duration = result.endTime - result.startTime;

        return result;
    }

    /**
     * Generate test summary
     * @param {number} totalDuration - Total test duration
     * @returns {Object} Test summary
     */
    generateSummary(totalDuration) {
        const passed = this.results.filter(r => r.status === 'passed').length;
        const failed = this.results.filter(r => r.status === 'failed').length;
        const total = this.results.length;

        return {
            total,
            passed,
            failed,
            passRate: total > 0 ? (passed / total) * 100 : 0,
            duration: totalDuration,
            results: this.results
        };
    }

    /**
     * Get test results
     * @returns {Array} Test results
     */
    getResults() {
        return this.results;
    }

    /**
     * Clear all tests and results
     */
    clear() {
        this.tests = [];
        this.results = [];
    }
}

/**
 * Automated Fitness Testing Class
 * Provides continuous health checks for the system
 */
class FitnessTest {
    constructor() {
        this.checks = [];
        this.fitnessScore = 100;
        this.lastCheck = null;
        this.checkInterval = null;
    }

    /**
     * Register a fitness check
     * @param {string} name - Check name
     * @param {Function} checkFn - Check function (should return boolean)
     * @param {number} weight - Weight of this check (1-10)
     */
    registerCheck(name, checkFn, weight = 5) {
        this.checks.push({
            name,
            checkFn,
            weight,
            lastResult: null,
            lastRun: null
        });
    }

    /**
     * Run all fitness checks
     * @returns {Promise<Object>} Fitness report
     */
    async runFitnessCheck() {
        const results = [];
        let totalWeight = 0;
        let passedWeight = 0;

        for (const check of this.checks) {
            const result = {
                name: check.name,
                weight: check.weight,
                passed: false,
                error: null
            };

            try {
                result.passed = await check.checkFn();
                check.lastResult = result.passed;
                check.lastRun = new Date().toISOString();

                if (result.passed) {
                    passedWeight += check.weight;
                }
            } catch (error) {
                result.error = error.message;
                check.lastResult = false;
            }

            totalWeight += check.weight;
            results.push(result);
        }

        this.fitnessScore = totalWeight > 0 ? (passedWeight / totalWeight) * 100 : 0;
        this.lastCheck = new Date().toISOString();

        return {
            score: this.fitnessScore,
            checks: results,
            timestamp: this.lastCheck,
            passed: this.fitnessScore >= 70
        };
    }

    /**
     * Start continuous fitness monitoring
     * @param {number} interval - Check interval in milliseconds
     */
    startContinuousMonitoring(interval = 60000) {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }

        this.checkInterval = setInterval(async () => {
            const report = await this.runFitnessCheck();
            console.log('Fitness Check:', report);

            if (report.score < 70) {
                console.warn(`Low fitness score: ${report.score}%`);
            }
        }, interval);

        console.log(`Continuous fitness monitoring started (interval: ${interval}ms)`);
    }

    /**
     * Stop continuous monitoring
     */
    stopContinuousMonitoring() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
            console.log('Continuous fitness monitoring stopped');
        }
    }

    /**
     * Get current fitness score
     * @returns {number} Fitness score (0-100)
     */
    getFitnessScore() {
        return this.fitnessScore;
    }

    /**
     * Get fitness status
     * @returns {Object} Fitness status
     */
    getStatus() {
        return {
            score: this.fitnessScore,
            lastCheck: this.lastCheck,
            checks: this.checks.map(c => ({
                name: c.name,
                weight: c.weight,
                lastResult: c.lastResult,
                lastRun: c.lastRun
            })),
            monitoring: !!this.checkInterval
        };
    }
}

/**
 * Module Docking System
 * Allows inline docking and hot-swapping of modules
 */
class ModuleDocking {
    constructor() {
        this.modules = new Map();
        this.dockedModules = new Map();
    }

    /**
     * Register a module for docking
     * @param {string} moduleName - Module name
     * @param {Object} moduleDefinition - Module definition
     */
    registerModule(moduleName, moduleDefinition) {
        this.modules.set(moduleName, {
            name: moduleName,
            definition: moduleDefinition,
            version: moduleDefinition.version || '1.0.0',
            dependencies: moduleDefinition.dependencies || [],
            status: 'registered'
        });

        console.log(`Module registered: ${moduleName} v${moduleDefinition.version || '1.0.0'}`);
    }

    /**
     * Dock a module (activate it)
     * @param {string} moduleName - Module name
     * @returns {Promise<boolean>} Success status
     */
    async dockModule(moduleName) {
        const module = this.modules.get(moduleName);

        if (!module) {
            console.error(`Module not found: ${moduleName}`);
            return false;
        }

        // Check dependencies
        for (const dep of module.dependencies) {
            if (!this.dockedModules.has(dep)) {
                console.error(`Dependency not docked: ${dep}`);
                return false;
            }
        }

        try {
            // Initialize module if it has init function
            if (module.definition.init) {
                await module.definition.init();
            }

            module.status = 'docked';
            this.dockedModules.set(moduleName, module);

            console.log(`Module docked: ${moduleName}`);
            return true;
        } catch (error) {
            console.error(`Failed to dock module ${moduleName}:`, error);
            module.status = 'error';
            return false;
        }
    }

    /**
     * Undock a module (deactivate it)
     * @param {string} moduleName - Module name
     * @returns {Promise<boolean>} Success status
     */
    async undockModule(moduleName) {
        const module = this.dockedModules.get(moduleName);

        if (!module) {
            console.error(`Module not docked: ${moduleName}`);
            return false;
        }

        try {
            // Cleanup module if it has cleanup function
            if (module.definition.cleanup) {
                await module.definition.cleanup();
            }

            module.status = 'registered';
            this.dockedModules.delete(moduleName);

            console.log(`Module undocked: ${moduleName}`);
            return true;
        } catch (error) {
            console.error(`Failed to undock module ${moduleName}:`, error);
            return false;
        }
    }

    /**
     * Hot-swap a module (replace with new version)
     * @param {string} moduleName - Module name
     * @param {Object} newDefinition - New module definition
     * @returns {Promise<boolean>} Success status
     */
    async hotSwapModule(moduleName, newDefinition) {
        const wasDocked = this.dockedModules.has(moduleName);

        // Undock old version
        if (wasDocked) {
            await this.undockModule(moduleName);
        }

        // Register new version
        this.registerModule(moduleName, newDefinition);

        // Dock new version if old was docked
        if (wasDocked) {
            return await this.dockModule(moduleName);
        }

        return true;
    }

    /**
     * Get docked modules
     * @returns {Array} List of docked module names
     */
    getDockedModules() {
        return Array.from(this.dockedModules.keys());
    }

    /**
     * Get all modules
     * @returns {Array} List of all module names
     */
    getAllModules() {
        return Array.from(this.modules.keys());
    }

    /**
     * Get module info
     * @param {string} moduleName - Module name
     * @returns {Object|null} Module information
     */
    getModuleInfo(moduleName) {
        return this.modules.get(moduleName) || null;
    }

    /**
     * Get docking system status
     * @returns {Object} Status information
     */
    getStatus() {
        return {
            totalModules: this.modules.size,
            dockedModules: this.dockedModules.size,
            modules: Array.from(this.modules.values()).map(m => ({
                name: m.name,
                version: m.version,
                status: m.status,
                dependencies: m.dependencies
            }))
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TestSuite, FitnessTest, ModuleDocking };
}
