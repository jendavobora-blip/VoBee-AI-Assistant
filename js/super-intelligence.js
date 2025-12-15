/**
 * VoBee Super-Intelligence Integration Layer
 * 
 * This module integrates the Supreme Brain and all subsystems with
 * the existing VoBee chatbot, providing the unified interface for
 * the super-intelligence system.
 * 
 * @module super-intelligence
 */

/**
 * Enhanced VoBee Super-Intelligence Chatbot
 * Extends the basic chatbot with Supreme Brain capabilities
 */
class SuperIntelligenceChatbot extends VoBeeChatbot {
    constructor() {
        super();
        
        // Initialize Supreme Brain
        this.supremeBrain = null;
        this.voiceInterface = null;
        this.devicePreview = null;
        this.securityManager = null;
        this.gpuEngine = null;
        this.fitnessTest = null;
        this.moduleDocking = null;
        
        // Enhanced features
        this.mode = 'standard'; // 'standard' or 'supreme'
        this.awaitingConfirmation = false;
        this.pendingTask = null;
    }

    /**
     * Initialize the super-intelligence system
     * @returns {Promise<void>}
     */
    async init() {
        // Initialize base chatbot
        await super.init();
        
        // Initialize Supreme Brain
        this.supremeBrain = new SupremeBrain();
        
        // Initialize Voice Interface
        this.voiceInterface = new VoiceInterface();
        this.setupVoiceHandlers();
        
        // Initialize Device Preview
        this.devicePreview = new DevicePreview();
        
        // Initialize Security Manager
        this.securityManager = new SecurityManager();
        
        // Initialize GPU Orchestration Engine
        this.gpuEngine = new GPUOrchestrationEngine();
        
        // Initialize Fitness Testing
        this.fitnessTest = new FitnessTest();
        this.setupFitnessChecks();
        
        // Initialize Module Docking
        this.moduleDocking = new ModuleDocking();
        this.registerCoreModules();
        
        console.log('🧠 Super-Intelligence System initialized!');
        console.log('Available subsystems:', this.supremeBrain.getSubSystems());
        console.log('Voice support:', this.voiceInterface.getStatus());
        console.log('Security:', this.securityManager.getStatus());
        console.log('GPU:', this.gpuEngine.getStatus());
        
        // Start fitness monitoring
        this.fitnessTest.startContinuousMonitoring(300000); // Every 5 minutes
    }

    /**
     * Setup fitness checks for system health monitoring
     */
    setupFitnessChecks() {
        // Check database connectivity
        this.fitnessTest.registerCheck('Database', async () => {
            return this.db !== null;
        }, 10);
        
        // Check Supreme Brain
        this.fitnessTest.registerCheck('Supreme Brain', async () => {
            return this.supremeBrain && this.supremeBrain.getSubSystems().length > 0;
        }, 10);
        
        // Check subsystems
        this.fitnessTest.registerCheck('Subsystems', async () => {
            return this.supremeBrain.subSystems.size >= 5;
        }, 8);
        
        // Check voice interface
        this.fitnessTest.registerCheck('Voice Interface', async () => {
            return this.voiceInterface && this.voiceInterface.isSupported.full;
        }, 5);
        
        // Check security
        this.fitnessTest.registerCheck('Security', async () => {
            return this.securityManager && this.securityManager.hasOwner();
        }, 7);
        
        // Check GPU engine
        this.fitnessTest.registerCheck('GPU Engine', async () => {
            return this.gpuEngine !== null;
        }, 6);
    }

    /**
     * Register core modules for docking
     */
    registerCoreModules() {
        // Register Supreme Brain module
        this.moduleDocking.registerModule('SupremeBrain', {
            version: '1.0.0',
            init: () => Promise.resolve(),
            cleanup: () => Promise.resolve()
        });
        
        // Register Voice module
        this.moduleDocking.registerModule('VoiceInterface', {
            version: '1.0.0',
            dependencies: [],
            init: () => Promise.resolve(),
            cleanup: () => Promise.resolve()
        });
        
        // Register Security module
        this.moduleDocking.registerModule('Security', {
            version: '1.0.0',
            init: () => Promise.resolve(),
            cleanup: () => Promise.resolve()
        });
        
        // Dock all core modules
        this.moduleDocking.dockModule('SupremeBrain');
        this.moduleDocking.dockModule('VoiceInterface');
        this.moduleDocking.dockModule('Security');
    }

    /**
     * Setup voice interface event handlers
     */
    setupVoiceHandlers() {
        // When voice recognition gets final result
        this.voiceInterface.onFinalResult = (transcript) => {
            console.log('Voice input:', transcript);
            this.handleVoiceInput(transcript);
        };

        // When voice recognition gets interim result
        this.voiceInterface.onInterimResult = (transcript) => {
            console.log('Interim:', transcript);
            this.onInterimVoiceResult && this.onInterimVoiceResult(transcript);
        };

        // Voice recognition started
        this.voiceInterface.onListeningStart = () => {
            console.log('Started listening...');
            this.onVoiceListeningStart && this.onVoiceListeningStart();
        };

        // Voice recognition ended
        this.voiceInterface.onListeningEnd = () => {
            console.log('Stopped listening');
            this.onVoiceListeningEnd && this.onVoiceListeningEnd();
        };
    }

    /**
     * Handle voice input
     * @param {string} transcript - Voice transcript
     */
    async handleVoiceInput(transcript) {
        if (this.onVoiceInput) {
            this.onVoiceInput(transcript);
        }
        
        // Process the voice input as regular message
        const response = await this.processMessage(transcript);
        
        // Speak the response
        if (this.voiceInterface && response) {
            this.voiceInterface.speak(response);
        }
    }

    /**
     * Enhanced message processing with Supreme Brain
     * @param {string} userInput - The user's message
     * @returns {Promise<string>} - The chatbot's response
     */
    async processMessage(userInput) {
        if (!userInput || userInput.trim() === '') {
            return "I didn't catch that. Could you type something? 🐝";
        }

        // Check for confirmation response
        if (this.awaitingConfirmation && this.pendingTask) {
            return await this.handleConfirmation(userInput);
        }

        // Check for system commands
        if (userInput.startsWith('/')) {
            return await this.handleSystemCommand(userInput);
        }

        // Determine which mode to use
        let response;
        
        if (this.shouldUseSupremeBrain(userInput)) {
            response = await this.processWithSupremeBrain(userInput);
        } else {
            // Use standard chatbot for simple queries
            response = await this.processWithStandardBot(userInput);
        }

        return response;
    }

    /**
     * Determine if Supreme Brain should handle the input
     * @param {string} input - User input
     * @returns {boolean} Should use Supreme Brain
     */
    shouldUseSupremeBrain(input) {
        const supremeKeywords = [
            'create', 'build', 'design', 'analyze', 'manage', 'orchestrate',
            'marketing', 'media', 'workflow', 'analytics', 'automate',
            'execute', 'process', 'generate', 'plan', 'strategy'
        ];

        const lowerInput = input.toLowerCase();
        return supremeKeywords.some(keyword => lowerInput.includes(keyword));
    }

    /**
     * Process message with Supreme Brain
     * @param {string} userInput - User input
     * @returns {Promise<string>} Response
     */
    async processWithSupremeBrain(userInput) {
        try {
            const result = await this.supremeBrain.processTask(userInput);
            
            // Save to history
            await this.saveMessage('user', userInput);
            
            if (result.phase === 'confirmation') {
                // Store pending task and wait for confirmation
                this.awaitingConfirmation = true;
                this.pendingTask = result;
                
                const confirmMessage = result.message + '\n\nType "yes" to proceed or "no" to cancel.';
                await this.saveMessage('bot', confirmMessage);
                
                return confirmMessage;
            } else if (result.phase === 'completed') {
                // Task completed successfully
                this.awaitingConfirmation = false;
                this.pendingTask = null;
                
                const successMessage = '✅ Task completed!\n\n' + result.report;
                await this.saveMessage('bot', successMessage);
                
                return successMessage;
            } else if (result.phase === 'error') {
                // Task failed
                this.awaitingConfirmation = false;
                this.pendingTask = null;
                
                const errorMessage = '❌ Error: ' + result.error;
                await this.saveMessage('bot', errorMessage);
                
                return errorMessage;
            }
            
        } catch (error) {
            console.error('Supreme Brain processing error:', error);
            return await this.processWithStandardBot(userInput);
        }
    }

    /**
     * Process with standard chatbot (fallback)
     * @param {string} userInput - User input
     * @returns {Promise<string>} Response
     */
    async processWithStandardBot(userInput) {
        // Use the original chatbot logic
        const category = this.findMatchingCategory(userInput);
        let response;

        if (category) {
            response = this.getRandomResponse(category);
        } else {
            await this.logUnrecognizedQuery(userInput);
            response = this.getFallbackResponse();
        }

        await this.saveMessage('user', userInput);
        await this.saveMessage('bot', response);

        return response;
    }

    /**
     * Handle user confirmation
     * @param {string} input - User response
     * @returns {Promise<string>} Response
     */
    async handleConfirmation(input) {
        const lowerInput = input.toLowerCase().trim();
        
        if (lowerInput === 'yes' || lowerInput === 'y' || lowerInput === 'proceed' || lowerInput === 'confirm') {
            // User confirmed - execute the task
            this.awaitingConfirmation = false;
            
            try {
                // Extract the understanding from pending task
                const understanding = this.pendingTask.understanding;
                
                // Execute the task directly
                const executionResult = await this.supremeBrain.executeTask(understanding);
                const task = {
                    id: Date.now(),
                    input: understanding.originalInput,
                    understanding: understanding,
                    result: executionResult,
                    status: 'completed'
                };
                
                const report = this.supremeBrain.generateReport(task);
                await this.supremeBrain.logTask(task);
                
                this.pendingTask = null;
                
                const successMessage = '✅ Task executed!\n\n' + report;
                await this.saveMessage('user', input);
                await this.saveMessage('bot', successMessage);
                
                return successMessage;
            } catch (error) {
                this.pendingTask = null;
                const errorMessage = '❌ Execution failed: ' + error.message;
                await this.saveMessage('user', input);
                await this.saveMessage('bot', errorMessage);
                return errorMessage;
            }
        } else if (lowerInput === 'no' || lowerInput === 'n' || lowerInput === 'cancel') {
            // User cancelled
            this.awaitingConfirmation = false;
            this.pendingTask = null;
            
            const cancelMessage = '❌ Task cancelled. How else can I help you?';
            await this.saveMessage('user', input);
            await this.saveMessage('bot', cancelMessage);
            
            return cancelMessage;
        } else {
            // Invalid response
            return 'Please respond with "yes" to proceed or "no" to cancel.';
        }
    }

    /**
     * Handle system commands
     * @param {string} command - System command
     * @returns {Promise<string>} Response
     */
    async handleSystemCommand(command) {
        const cmd = command.toLowerCase().trim();
        
        if (cmd === '/help' || cmd === '/commands') {
            return this.getSystemHelp();
        } else if (cmd === '/status') {
            return this.getSystemStatus();
        } else if (cmd === '/subsystems') {
            return this.listSubSystems();
        } else if (cmd === '/voice on') {
            return this.enableVoice();
        } else if (cmd === '/voice off') {
            return this.disableVoice();
        } else if (cmd.startsWith('/preview ')) {
            const device = cmd.replace('/preview ', '');
            return this.enableDevicePreview(device);
        } else if (cmd === '/preview off') {
            return this.disableDevicePreview();
        } else if (cmd === '/mode supreme') {
            this.mode = 'supreme';
            return '🧠 Switched to Supreme Brain mode. All requests will use intelligent subsystems.';
        } else if (cmd === '/mode standard') {
            this.mode = 'standard';
            return '🐝 Switched to Standard mode. Using pattern-based responses.';
        } else if (cmd === '/security status') {
            return this.getSecurityStatus();
        } else if (cmd === '/gpu status') {
            return this.getGPUStatus();
        } else if (cmd === '/fitness') {
            return await this.getFitnessReport();
        } else if (cmd === '/modules') {
            return this.getModulesStatus();
        }
        
        return 'Unknown command. Type /help for available commands.';
    }

    /**
     * Get system help
     * @returns {string} Help text
     */
    getSystemHelp() {
        return `
🧠 VoBee Super-Intelligence System Commands:

/help - Show this help message
/status - Show system status
/subsystems - List all intelligent subsystems
/voice on - Enable voice input
/voice off - Disable voice input
/preview [device] - Enable device preview (tv, monitor, mobile, tablet)
/preview off - Disable device preview
/mode supreme - Switch to Supreme Brain mode
/mode standard - Switch to Standard chatbot mode
/security status - Show security and privacy status
/gpu status - Show GPU orchestration status
/fitness - Run system fitness check
/modules - Show module docking status

You can also just chat naturally! The system will automatically
use the appropriate intelligence subsystem based on your request.
        `.trim();
    }

    /**
     * Get system status
     * @returns {string} Status information
     */
    getSystemStatus() {
        const brainStatus = this.supremeBrain.getStatus();
        const voiceStatus = this.voiceInterface.getStatus();
        const previewStatus = this.devicePreview.getStatus();
        const securityStatus = this.securityManager.getStatus();
        const gpuStatus = this.gpuEngine.getStatus();
        
        return `
🧠 System Status:

Supreme Brain: Active
Version: ${brainStatus.version}
Mode: ${this.mode}
Owner: ${securityStatus.owner || 'Not set'}
Requires Approval: ${brainStatus.requiresApproval ? 'Yes' : 'No'}

Subsystems: ${brainStatus.subSystems.length} active
Active Task: ${brainStatus.activeTask || 'None'}

Voice Interface: ${voiceStatus.supported.full ? 'Supported' : 'Not supported'}
Listening: ${voiceStatus.listening ? 'Yes' : 'No'}
Speaking: ${voiceStatus.speaking ? 'Yes' : 'No'}

Device Preview: ${previewStatus.previewMode ? 'Active' : 'Inactive'}
Current Device: ${previewStatus.currentDevice}

Security Level: ${securityStatus.securityLevel}
Authenticated: ${securityStatus.isAuthenticated ? 'Yes' : 'No'}

GPU Available: ${gpuStatus.gpuAvailable ? 'Yes' : 'No'}
Meta-Processing: ${gpuStatus.metaProcessing.enabled ? 'Enabled' : 'Disabled'}
        `.trim();
    }

    /**
     * Get security status
     * @returns {string} Security status
     */
    getSecurityStatus() {
        const status = this.securityManager.getStatus();
        
        return `
🔒 Security & Privacy Status:

Owner Registered: ${status.hasOwner ? 'Yes' : 'No'}
Authenticated: ${status.isAuthenticated ? 'Yes' : 'No'}
Current Owner: ${status.owner || 'None'}
Security Level: ${status.securityLevel}
Encryption: ${status.encryptionEnabled ? 'Enabled' : 'Disabled'}
Pending Approvals: ${status.pendingApprovals}
Access Log Entries: ${status.accessLogSize}
        `.trim();
    }

    /**
     * Get GPU status
     * @returns {string} GPU status
     */
    getGPUStatus() {
        const status = this.gpuEngine.getStatus();
        const stats = status.statistics;
        
        return `
⚡ GPU Orchestration Engine Status:

GPU Available: ${status.gpuAvailable ? 'Yes' : 'No'}
${status.gpuAvailable ? `Vendor: ${status.gpuInfo.vendor}
Renderer: ${status.gpuInfo.renderer}` : ''}

Meta-Processing: ${status.metaProcessing.enabled ? 'Enabled' : 'Disabled'}
Optimization Level: ${status.metaProcessing.optimizationLevel}
Analysis Depth: ${status.metaProcessing.analysisDepth}

Tasks Processed: ${stats.totalTasks}
Completed: ${stats.completed}
Failed: ${stats.failed}
Queued: ${stats.queued}
Active: ${stats.activeTask || 'None'}

Average Processing Time: ${stats.averageProcessingTime.toFixed(2)}ms
        `.trim();
    }

    /**
     * Get fitness report
     * @returns {Promise<string>} Fitness report
     */
    async getFitnessReport() {
        const report = await this.fitnessTest.runFitnessCheck();
        
        let result = `
🏃 System Fitness Report:

Overall Score: ${report.score.toFixed(1)}% ${report.passed ? '✅' : '⚠️'}
Status: ${report.passed ? 'Healthy' : 'Needs Attention'}
Timestamp: ${report.timestamp}

Individual Checks:
`;
        
        for (const check of report.checks) {
            const icon = check.passed ? '✅' : '❌';
            result += `${icon} ${check.name} (Weight: ${check.weight})`;
            if (check.error) {
                result += ` - Error: ${check.error}`;
            }
            result += '\n';
        }
        
        return result.trim();
    }

    /**
     * Get modules status
     * @returns {string} Modules status
     */
    getModulesStatus() {
        const status = this.moduleDocking.getStatus();
        
        let result = `
🔌 Module Docking Status:

Total Modules: ${status.totalModules}
Docked Modules: ${status.dockedModules}

Modules:
`;
        
        for (const module of status.modules) {
            const icon = module.status === 'docked' ? '🟢' : '⚪';
            result += `${icon} ${module.name} v${module.version} - ${module.status}`;
            if (module.dependencies.length > 0) {
                result += ` (depends on: ${module.dependencies.join(', ')})`;
            }
            result += '\n';
        }
        
        return result.trim();
    }

    /**
     * List all subsystems
     * @returns {string} Subsystems list
     */
    listSubSystems() {
        const systems = this.supremeBrain.getSubSystems();
        
        return `
🔧 Available Intelligent Subsystems:

${systems.map((name, i) => `${i + 1}. ${name}`).join('\n')}

Each subsystem specializes in its domain and can handle
complex tasks autonomously under Supreme Brain coordination.
        `.trim();
    }

    /**
     * Enable voice input
     * @returns {string} Status message
     */
    enableVoice() {
        if (!this.voiceInterface.isSupported.recognition) {
            return '❌ Voice recognition is not supported in your browser.';
        }
        
        this.voiceInterface.startListening();
        return '🎤 Voice input enabled. Start speaking!';
    }

    /**
     * Disable voice input
     * @returns {string} Status message
     */
    disableVoice() {
        this.voiceInterface.stopListening();
        return '🔇 Voice input disabled.';
    }

    /**
     * Enable device preview
     * @param {string} device - Device type
     * @returns {string} Status message
     */
    enableDevicePreview(device) {
        const success = this.devicePreview.switchToDevice(device);
        
        if (!success) {
            const devices = Object.keys(this.devicePreview.getAllDevices()).join(', ');
            return `❌ Invalid device. Available: ${devices}`;
        }
        
        this.devicePreview.enablePreview();
        const info = this.devicePreview.getCurrentDevice();
        
        return `📱 Preview enabled for ${info.name} (${info.width}×${info.height})`;
    }

    /**
     * Disable device preview
     * @returns {string} Status message
     */
    disableDevicePreview() {
        this.devicePreview.disablePreview();
        return '✅ Device preview disabled.';
    }

    /**
     * Get complete system information
     * @returns {Object} System info
     */
    getSystemInfo() {
        return {
            chatbot: {
                initialized: this.isInitialized,
                mode: this.mode,
                historyCount: this.conversationHistory.length
            },
            supremeBrain: this.supremeBrain.getStatus(),
            voice: this.voiceInterface.getStatus(),
            preview: this.devicePreview.getStatus(),
            security: this.securityManager.getStatus(),
            gpu: this.gpuEngine.getStatus(),
            fitness: {
                score: this.fitnessTest.getFitnessScore(),
                lastCheck: this.fitnessTest.lastCheck
            },
            modules: this.moduleDocking.getStatus()
        };
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SuperIntelligenceChatbot };
}
