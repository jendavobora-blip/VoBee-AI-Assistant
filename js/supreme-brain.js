/**
 * VoBee Supreme Brain - Central Intelligence Coordinator
 * 
 * This module implements the top-level AI coordinator that manages
 * all microsub systems and orchestrates intelligent responses following
 * the standard pattern: Understanding -> Confirmation -> Execution -> Report -> Logs
 * 
 * @module supreme-brain
 */

/**
 * Supreme Brain Class
 * The central AI coordinator that manages all intelligent subsystems
 */
class SupremeBrain {
    constructor() {
        this.name = 'Supreme Brain';
        this.version = '1.0.0';
        this.subSystems = new Map();
        this.taskQueue = [];
        this.activeTask = null;
        this.owner = null;
        this.requiresApproval = true;
        
        // Initialize subsystems
        this.initializeSubSystems();
    }

    /**
     * Initialize all intelligent subsystems
     */
    initializeSubSystems() {
        // Register all subsystems
        this.registerSubSystem(new MarketingIntelligence());
        this.registerSubSystem(new MediaManagementIntelligence());
        this.registerSubSystem(new OrchestrationIntelligence());
        this.registerSubSystem(new AnalyticsIntelligence());
        this.registerSubSystem(new CreativeIntelligence());
        
        console.log(`${this.name} initialized with ${this.subSystems.size} subsystems`);
    }

    /**
     * Register a subsystem with the Supreme Brain
     * @param {Object} subSystem - The subsystem to register
     */
    registerSubSystem(subSystem) {
        if (!subSystem.name) {
            throw new Error('SubSystem must have a name property');
        }
        this.subSystems.set(subSystem.name, subSystem);
        console.log(`Registered subsystem: ${subSystem.name}`);
    }

    /**
     * Analyze user input and determine which subsystem should handle it
     * @param {string} input - User input to analyze
     * @returns {Object} Analysis result with subsystem assignment
     */
    analyzeInput(input) {
        const analysis = {
            input: input,
            intent: this.detectIntent(input),
            assignedSystem: null,
            confidence: 0,
            requiresConfirmation: false
        };

        // Check each subsystem for capability match
        let bestMatch = null;
        let highestConfidence = 0;

        for (const [name, system] of this.subSystems) {
            const confidence = system.canHandle(input);
            if (confidence > highestConfidence) {
                highestConfidence = confidence;
                bestMatch = system;
            }
        }

        if (bestMatch && highestConfidence > 0.3) {
            analysis.assignedSystem = bestMatch.name;
            analysis.confidence = highestConfidence;
            analysis.requiresConfirmation = highestConfidence < 0.8;
        }

        return analysis;
    }

    /**
     * Detect the intent behind user input
     * @param {string} input - User input
     * @returns {string} Detected intent
     */
    detectIntent(input) {
        const lowerInput = input.toLowerCase();
        
        // Intent patterns
        const patterns = {
            create: ['create', 'make', 'generate', 'build', 'design'],
            analyze: ['analyze', 'review', 'examine', 'evaluate', 'assess'],
            manage: ['manage', 'organize', 'schedule', 'plan', 'coordinate'],
            learn: ['learn', 'teach', 'train', 'understand', 'study'],
            execute: ['execute', 'run', 'perform', 'do', 'implement'],
            query: ['what', 'when', 'where', 'who', 'why', 'how']
        };

        for (const [intent, keywords] of Object.entries(patterns)) {
            if (keywords.some(keyword => lowerInput.includes(keyword))) {
                return intent;
            }
        }

        return 'general';
    }

    /**
     * Process a task using the standard response pattern:
     * Understanding -> Confirmation -> Execution -> Report -> Logs
     * 
     * @param {string} userInput - The user's request
     * @returns {Promise<Object>} Processing result
     */
    async processTask(userInput) {
        const task = {
            id: Date.now(),
            input: userInput,
            timestamp: new Date().toISOString(),
            phase: 'understanding',
            status: 'pending'
        };

        this.activeTask = task;

        try {
            // Phase 1: Understanding
            const understanding = await this.understandProblem(userInput);
            task.understanding = understanding;
            task.phase = 'confirmation';

            // Phase 2: Confirmation (if required)
            if (understanding.requiresConfirmation && this.requiresApproval) {
                const confirmationNeeded = {
                    phase: 'confirmation',
                    message: this.formatConfirmationMessage(understanding),
                    understanding: understanding,
                    awaitingApproval: true
                };
                return confirmationNeeded;
            }

            // Phase 3: Execution
            task.phase = 'execution';
            const executionResult = await this.executeTask(understanding);
            task.result = executionResult;
            task.phase = 'reporting';

            // Phase 4: Report
            const report = this.generateReport(task);
            task.phase = 'logging';

            // Phase 5: Persistent Logging
            await this.logTask(task);
            task.status = 'completed';

            return {
                phase: 'completed',
                report: report,
                task: task
            };

        } catch (error) {
            task.status = 'failed';
            task.error = error.message;
            await this.logTask(task);
            
            return {
                phase: 'error',
                error: error.message,
                task: task
            };
        }
    }

    /**
     * Phase 1: Understand the problem
     * @param {string} input - User input
     * @returns {Promise<Object>} Understanding result
     */
    async understandProblem(input) {
        const analysis = this.analyzeInput(input);
        
        return {
            originalInput: input,
            intent: analysis.intent,
            assignedSystem: analysis.assignedSystem,
            confidence: analysis.confidence,
            requiresConfirmation: analysis.requiresConfirmation,
            context: this.extractContext(input),
            parameters: this.extractParameters(input)
        };
    }

    /**
     * Extract contextual information from input
     * @param {string} input - User input
     * @returns {Object} Context information
     */
    extractContext(input) {
        return {
            length: input.length,
            hasQuestion: input.includes('?'),
            sentiment: this.detectSentiment(input),
            complexity: this.assessComplexity(input)
        };
    }

    /**
     * Extract parameters from user input
     * @param {string} input - User input
     * @returns {Object} Extracted parameters
     */
    extractParameters(input) {
        // Simple parameter extraction - can be enhanced
        const params = {};
        
        // Extract numbers
        const numbers = input.match(/\d+/g);
        if (numbers) {
            params.numbers = numbers.map(n => parseInt(n));
        }
        
        // Extract quoted strings
        const quotes = input.match(/"([^"]+)"/g);
        if (quotes) {
            params.quotedText = quotes.map(q => q.replace(/"/g, ''));
        }
        
        return params;
    }

    /**
     * Detect sentiment in user input
     * @param {string} input - User input
     * @returns {string} Detected sentiment
     */
    detectSentiment(input) {
        const positive = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful'];
        const negative = ['bad', 'terrible', 'sad', 'hate', 'awful', 'poor'];
        
        const lowerInput = input.toLowerCase();
        const hasPositive = positive.some(word => lowerInput.includes(word));
        const hasNegative = negative.some(word => lowerInput.includes(word));
        
        if (hasPositive && !hasNegative) return 'positive';
        if (hasNegative && !hasPositive) return 'negative';
        return 'neutral';
    }

    /**
     * Assess input complexity
     * @param {string} input - User input
     * @returns {string} Complexity level
     */
    assessComplexity(input) {
        const wordCount = input.split(/\s+/).length;
        if (wordCount < 5) return 'simple';
        if (wordCount < 15) return 'moderate';
        return 'complex';
    }

    /**
     * Format confirmation message for user
     * @param {Object} understanding - Understanding result
     * @returns {string} Confirmation message
     */
    formatConfirmationMessage(understanding) {
        const systemName = understanding.assignedSystem || 'General Intelligence';
        return `I understand you want to ${understanding.intent} something. ` +
               `I'll use the ${systemName} system to handle this (${Math.round(understanding.confidence * 100)}% confidence). ` +
               `May I proceed?`;
    }

    /**
     * Execute the task with appropriate subsystem
     * @param {Object} understanding - Understanding result
     * @returns {Promise<Object>} Execution result
     */
    async executeTask(understanding) {
        const systemName = understanding.assignedSystem;
        
        if (systemName && this.subSystems.has(systemName)) {
            const system = this.subSystems.get(systemName);
            return await system.execute(understanding);
        }
        
        // Fallback to general processing
        return {
            success: true,
            system: 'Supreme Brain (Direct)',
            message: 'Task processed successfully',
            data: understanding
        };
    }

    /**
     * Generate task report
     * @param {Object} task - Task object
     * @returns {string} Report
     */
    generateReport(task) {
        const report = [
            `Task #${task.id} Report:`,
            `Input: "${task.input}"`,
            `Intent: ${task.understanding.intent}`,
            `System: ${task.understanding.assignedSystem || 'Supreme Brain'}`,
            `Status: ${task.status}`,
            `Result: ${JSON.stringify(task.result)}`
        ];
        
        return report.join('\n');
    }

    /**
     * Log task for persistence
     * @param {Object} task - Task to log
     * @returns {Promise<void>}
     */
    async logTask(task) {
        // Store in IndexedDB or similar
        const logEntry = {
            taskId: task.id,
            timestamp: task.timestamp,
            input: task.input,
            understanding: task.understanding,
            result: task.result,
            status: task.status,
            error: task.error || null
        };
        
        console.log('Task logged:', logEntry);
        // This will be integrated with the existing VoBee DB
        return Promise.resolve();
    }

    /**
     * Confirm and execute a pending task
     * @param {string} taskId - Task ID to confirm
     * @returns {Promise<Object>} Execution result
     */
    async confirmAndExecute(taskId) {
        if (!this.activeTask || this.activeTask.id !== taskId) {
            throw new Error('No pending task to confirm');
        }

        const understanding = this.activeTask.understanding;
        this.activeTask.phase = 'execution';
        
        const executionResult = await this.executeTask(understanding);
        this.activeTask.result = executionResult;
        this.activeTask.phase = 'reporting';

        const report = this.generateReport(this.activeTask);
        this.activeTask.phase = 'logging';

        await this.logTask(this.activeTask);
        this.activeTask.status = 'completed';

        return {
            phase: 'completed',
            report: report,
            task: this.activeTask
        };
    }

    /**
     * Get all available subsystems
     * @returns {Array} List of subsystem names
     */
    getSubSystems() {
        return Array.from(this.subSystems.keys());
    }

    /**
     * Set owner for approval workflow
     * @param {string} ownerId - Owner identifier
     */
    setOwner(ownerId) {
        this.owner = ownerId;
    }

    /**
     * Get system status
     * @returns {Object} System status
     */
    getStatus() {
        return {
            name: this.name,
            version: this.version,
            subSystems: this.getSubSystems(),
            activeTask: this.activeTask ? this.activeTask.id : null,
            queueLength: this.taskQueue.length,
            owner: this.owner,
            requiresApproval: this.requiresApproval
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SupremeBrain };
}
