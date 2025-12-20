/**
 * AI Orchestration Interface
 * 
 * Interface to the orchestrator brain for task submission and monitoring.
 * ⚠️ DOES NOT MODIFY /js/chatbot.js - This is a NEW extension module
 * 
 * @module ai-orchestration
 */

class AIOrchestration {
    /**
     * Initialize AI Orchestration interface
     */
    constructor() {
        this.orchestratorEndpoint = '/api/orchestrator';
        this.activeTasks = new Map();
        this.taskHistory = [];
        this.maxHistorySize = 100;
        
        console.log('AI Orchestration initialized');
    }

    /**
     * Submit a task to the orchestrator
     * @param {Object} task - Task configuration
     * @param {string} task.type - Task type (email, content, analytics, etc.)
     * @param {string} task.priority - Priority level (low, normal, high, critical)
     * @param {Object} task.data - Task-specific data
     * @returns {Promise<Object>} Task result
     */
    async submitTask(task) {
        try {
            const taskId = this._generateTaskId();
            
            const taskRequest = {
                id: taskId,
                type: task.type,
                priority: task.priority || 'normal',
                data: task.data || {},
                submittedAt: new Date().toISOString()
            };

            // Store task as active
            this.activeTasks.set(taskId, {
                ...taskRequest,
                status: 'pending'
            });

            // Submit to orchestrator
            const response = await fetch(`${this.orchestratorEndpoint}/orchestrate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tasks: [taskRequest],
                    priority: task.priority || 'normal'
                })
            });

            if (!response.ok) {
                throw new Error(`Orchestrator error: ${response.statusText}`);
            }

            const result = await response.json();
            
            // Update task status
            this.activeTasks.get(taskId).status = 'completed';
            this.activeTasks.get(taskId).result = result;
            
            // Move to history
            this._moveToHistory(taskId);

            return result;

        } catch (error) {
            console.error('Error submitting task:', error);
            throw error;
        }
    }

    /**
     * Submit multiple tasks as a workflow
     * @param {Array<Object>} tasks - Array of tasks
     * @param {string} priority - Workflow priority
     * @returns {Promise<Object>} Workflow result
     */
    async submitWorkflow(tasks, priority = 'normal') {
        try {
            const workflowId = this._generateTaskId();
            
            const workflow = {
                workflow_id: workflowId,
                tasks: tasks.map(task => ({
                    type: task.type,
                    params: task.data || {}
                })),
                priority: priority,
                submittedAt: new Date().toISOString()
            };

            const response = await fetch(`${this.orchestratorEndpoint}/orchestrate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(workflow)
            });

            if (!response.ok) {
                throw new Error(`Workflow error: ${response.statusText}`);
            }

            return await response.json();

        } catch (error) {
            console.error('Error submitting workflow:', error);
            throw error;
        }
    }

    /**
     * Get task status by ID
     * @param {string} taskId - Task identifier
     * @returns {Promise<Object>} Task status
     */
    async getTaskStatus(taskId) {
        try {
            // Check active tasks first
            if (this.activeTasks.has(taskId)) {
                return this.activeTasks.get(taskId);
            }

            // Check history
            const historical = this.taskHistory.find(t => t.id === taskId);
            if (historical) {
                return historical;
            }

            // Query orchestrator
            const response = await fetch(`${this.orchestratorEndpoint}/task/${taskId}`);
            
            if (!response.ok) {
                throw new Error(`Task not found: ${taskId}`);
            }

            return await response.json();

        } catch (error) {
            console.error('Error getting task status:', error);
            throw error;
        }
    }

    /**
     * Get list of available AI services
     * @returns {Promise<Array>} List of services
     */
    async getAvailableServices() {
        try {
            const response = await fetch(`${this.orchestratorEndpoint}/services`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch services');
            }

            const data = await response.json();
            return data.services || [];

        } catch (error) {
            console.error('Error fetching services:', error);
            return [];
        }
    }

    /**
     * Get active tasks
     * @returns {Array<Object>} Active tasks
     */
    getActiveTasks() {
        return Array.from(this.activeTasks.values());
    }

    /**
     * Get task history
     * @param {number} limit - Max number of tasks to return
     * @returns {Array<Object>} Task history
     */
    getTaskHistory(limit = 50) {
        return this.taskHistory.slice(0, limit);
    }

    /**
     * Cancel a task
     * @param {string} taskId - Task to cancel
     * @returns {boolean} Success status
     */
    async cancelTask(taskId) {
        try {
            if (!this.activeTasks.has(taskId)) {
                return false;
            }

            // Update status
            this.activeTasks.get(taskId).status = 'cancelled';
            this._moveToHistory(taskId);

            return true;

        } catch (error) {
            console.error('Error cancelling task:', error);
            return false;
        }
    }

    /**
     * Clear task history
     */
    clearHistory() {
        this.taskHistory = [];
        console.log('Task history cleared');
    }

    /**
     * Generate unique task ID
     * @private
     * @returns {string} Task ID
     */
    _generateTaskId() {
        return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Move task from active to history
     * @private
     * @param {string} taskId - Task ID
     */
    _moveToHistory(taskId) {
        if (this.activeTasks.has(taskId)) {
            const task = this.activeTasks.get(taskId);
            this.activeTasks.delete(taskId);
            
            // Add to history
            this.taskHistory.unshift(task);
            
            // Maintain max history size
            if (this.taskHistory.length > this.maxHistorySize) {
                this.taskHistory = this.taskHistory.slice(0, this.maxHistorySize);
            }
        }
    }

    /**
     * Get orchestrator statistics
     * @returns {Object} Statistics
     */
    getStatistics() {
        const completed = this.taskHistory.filter(t => t.status === 'completed').length;
        const failed = this.taskHistory.filter(t => t.status === 'failed').length;
        const cancelled = this.taskHistory.filter(t => t.status === 'cancelled').length;

        return {
            active: this.activeTasks.size,
            completed: completed,
            failed: failed,
            cancelled: cancelled,
            total: this.taskHistory.length,
            successRate: this.taskHistory.length > 0 
                ? (completed / this.taskHistory.length * 100).toFixed(2) + '%'
                : '0%'
        };
    }
}

// Create global instance
const aiOrchestration = new AIOrchestration();

// Example usage functions
window.AIOrchestration = {
    /**
     * Submit an email campaign task
     * @param {Object} campaign - Campaign data
     * @returns {Promise<Object>} Result
     */
    async createEmailCampaign(campaign) {
        return await aiOrchestration.submitTask({
            type: 'email_campaign',
            priority: 'normal',
            data: campaign
        });
    },

    /**
     * Generate content
     * @param {Object} contentRequest - Content request data
     * @returns {Promise<Object>} Result
     */
    async generateContent(contentRequest) {
        return await aiOrchestration.submitTask({
            type: 'content_generation',
            priority: 'normal',
            data: contentRequest
        });
    },

    /**
     * Run analytics
     * @param {Object} analyticsRequest - Analytics request
     * @returns {Promise<Object>} Result
     */
    async runAnalytics(analyticsRequest) {
        return await aiOrchestration.submitTask({
            type: 'analytics',
            priority: 'high',
            data: analyticsRequest
        });
    },

    /**
     * Get task status
     * @param {string} taskId - Task ID
     * @returns {Promise<Object>} Status
     */
    async getTaskStatus(taskId) {
        return await aiOrchestration.getTaskStatus(taskId);
    },

    /**
     * Get statistics
     * @returns {Object} Statistics
     */
    getStats() {
        return aiOrchestration.getStatistics();
    }
};

console.log('AI Orchestration module loaded');
