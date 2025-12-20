/**
 * Module Manager UI
 * 
 * User interface for managing AI modules (enable/disable, health monitoring, configuration).
 * ⚠️ DOES NOT MODIFY /js/chatbot.js - This is a NEW extension module
 * 
 * @module module-manager-ui
 */

class ModuleManagerUI {
    /**
     * Initialize Module Manager UI
     */
    constructor() {
        this.moduleManagerEndpoint = '/api/module-manager';
        this.modules = [];
        this.refreshInterval = 30000; // 30 seconds
        this.autoRefresh = false;
        
        console.log('Module Manager UI initialized');
    }

    /**
     * Initialize the UI
     * @param {string} containerId - Container element ID
     */
    async init(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        await this.loadModules();
        this.render();
        
        if (this.autoRefresh) {
            this.startAutoRefresh();
        }
    }

    /**
     * Load all modules
     * @returns {Promise<void>}
     */
    async loadModules() {
        try {
            // In a real implementation, this would call the actual API
            // For now, we'll simulate the module list
            this.modules = await this._fetchModules();
            console.log(`Loaded ${this.modules.length} modules`);
        } catch (error) {
            console.error('Error loading modules:', error);
        }
    }

    /**
     * Fetch modules from API
     * @private
     * @returns {Promise<Array>} Modules
     */
    async _fetchModules() {
        // Simulated module data
        // In production, this would fetch from module-manager.py
        return [
            // Business & Marketing
            { name: 'email-ai', category: 'business', enabled: true, health: 'healthy', port: 5100 },
            { name: 'facebook-ai', category: 'business', enabled: true, health: 'healthy', port: 5101 },
            { name: 'marketing-ai', category: 'business', enabled: true, health: 'healthy', port: 5102 },
            { name: 'seo-ai', category: 'business', enabled: true, health: 'healthy', port: 5103 },
            { name: 'content-ai', category: 'business', enabled: true, health: 'healthy', port: 5104 },
            { name: 'analytics-ai', category: 'business', enabled: true, health: 'healthy', port: 5105 },
            
            // Finance
            { name: 'finance-ai', category: 'finance', enabled: true, health: 'healthy', port: 5110, readOnly: true },
            { name: 'invoice-ai', category: 'finance', enabled: true, health: 'healthy', port: 5111 },
            { name: 'budget-ai', category: 'finance', enabled: true, health: 'healthy', port: 5112 },
            { name: 'tax-ai', category: 'finance', enabled: false, health: 'unknown', port: 5113 },
            { name: 'cashflow-ai', category: 'finance', enabled: true, health: 'healthy', port: 5114 },
            
            // Research & Data
            { name: 'research-ai', category: 'research', enabled: true, health: 'healthy', port: 5120 },
            { name: 'web-scraper-ai', category: 'research', enabled: true, health: 'degraded', port: 5121 },
            { name: 'data-mining-ai', category: 'research', enabled: true, health: 'healthy', port: 5122 },
            { name: 'sentiment-ai', category: 'research', enabled: true, health: 'healthy', port: 5123 },
            { name: 'trend-ai', category: 'research', enabled: true, health: 'healthy', port: 5124 },
            
            // Communication
            { name: 'email-response-ai', category: 'communication', enabled: true, health: 'healthy', port: 5130 },
            { name: 'chat-support-ai', category: 'communication', enabled: true, health: 'healthy', port: 5131 },
            { name: 'translation-ai', category: 'communication', enabled: false, health: 'unknown', port: 5132 },
            { name: 'voice-ai', category: 'communication', enabled: false, health: 'unknown', port: 5133 },
            { name: 'meeting-ai', category: 'communication', enabled: true, health: 'healthy', port: 5134 },
            
            // Creative
            { name: 'music-ai', category: 'creative', enabled: false, health: 'unknown', port: 5140 },
            { name: 'design-ai', category: 'creative', enabled: true, health: 'healthy', port: 5141 },
            { name: 'animation-ai', category: 'creative', enabled: false, health: 'unknown', port: 5142 },
            { name: 'presentation-ai', category: 'creative', enabled: true, health: 'healthy', port: 5143 },
            { name: 'podcast-ai', category: 'creative', enabled: false, health: 'unknown', port: 5144 },
            
            // Technical
            { name: 'code-review-ai', category: 'technical', enabled: true, health: 'healthy', port: 5150 },
            { name: 'documentation-ai', category: 'technical', enabled: true, health: 'healthy', port: 5151 },
            { name: 'testing-ai', category: 'technical', enabled: true, health: 'healthy', port: 5152 },
            { name: 'deployment-ai', category: 'technical', enabled: false, health: 'unknown', port: 5153 }
        ];
    }

    /**
     * Render the UI
     */
    render() {
        if (!this.container) return;

        const categories = this._groupByCategory();
        
        let html = `
            <div class="module-manager">
                <div class="module-manager-header">
                    <h2>🧠 AI Module Manager</h2>
                    <div class="module-manager-controls">
                        <button onclick="moduleManagerUI.refresh()" class="btn-refresh">🔄 Refresh</button>
                        <button onclick="moduleManagerUI.toggleAutoRefresh()" class="btn-auto">
                            ${this.autoRefresh ? '⏸️ Stop Auto' : '▶️ Auto Refresh'}
                        </button>
                    </div>
                </div>
                <div class="module-manager-summary">
                    ${this._renderSummary()}
                </div>
                <div class="module-manager-categories">
                    ${Object.keys(categories).map(cat => this._renderCategory(cat, categories[cat])).join('')}
                </div>
            </div>
        `;

        this.container.innerHTML = html;
        this._attachEventListeners();
    }

    /**
     * Render summary statistics
     * @private
     * @returns {string} HTML
     */
    _renderSummary() {
        const total = this.modules.length;
        const enabled = this.modules.filter(m => m.enabled).length;
        const healthy = this.modules.filter(m => m.health === 'healthy').length;
        const degraded = this.modules.filter(m => m.health === 'degraded').length;

        return `
            <div class="summary-stats">
                <div class="stat">
                    <span class="stat-label">Total Modules</span>
                    <span class="stat-value">${total}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Enabled</span>
                    <span class="stat-value stat-enabled">${enabled}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Healthy</span>
                    <span class="stat-value stat-healthy">${healthy}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Degraded</span>
                    <span class="stat-value stat-degraded">${degraded}</span>
                </div>
            </div>
        `;
    }

    /**
     * Group modules by category
     * @private
     * @returns {Object} Grouped modules
     */
    _groupByCategory() {
        const groups = {};
        this.modules.forEach(module => {
            if (!groups[module.category]) {
                groups[module.category] = [];
            }
            groups[module.category].push(module);
        });
        return groups;
    }

    /**
     * Render a category
     * @private
     * @param {string} category - Category name
     * @param {Array} modules - Modules in category
     * @returns {string} HTML
     */
    _renderCategory(category, modules) {
        const categoryIcons = {
            business: '📈',
            finance: '💰',
            research: '🔬',
            communication: '💬',
            creative: '🎨',
            technical: '💻'
        };

        return `
            <div class="module-category">
                <h3 class="category-title">
                    ${categoryIcons[category] || '📦'} ${this._capitalize(category)} 
                    <span class="category-count">(${modules.length})</span>
                </h3>
                <div class="module-list">
                    ${modules.map(m => this._renderModule(m)).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Render a single module
     * @private
     * @param {Object} module - Module data
     * @returns {string} HTML
     */
    _renderModule(module) {
        const healthIcon = {
            healthy: '✅',
            degraded: '⚠️',
            unhealthy: '❌',
            unknown: '❓'
        };

        const healthClass = `health-${module.health}`;
        const enabledClass = module.enabled ? 'enabled' : 'disabled';

        return `
            <div class="module-card ${enabledClass}" data-module="${module.name}">
                <div class="module-header">
                    <span class="module-name">${module.name}</span>
                    ${module.readOnly ? '<span class="module-badge">READ-ONLY</span>' : ''}
                </div>
                <div class="module-info">
                    <span class="module-port">Port: ${module.port}</span>
                    <span class="module-health ${healthClass}">
                        ${healthIcon[module.health]} ${module.health}
                    </span>
                </div>
                <div class="module-actions">
                    <button class="btn-toggle" onclick="moduleManagerUI.toggleModule('${module.name}')">
                        ${module.enabled ? '⏸️ Disable' : '▶️ Enable'}
                    </button>
                    <button class="btn-health" onclick="moduleManagerUI.checkHealth('${module.name}')">
                        🏥 Check
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Toggle module enabled state
     * @param {string} moduleName - Module name
     */
    async toggleModule(moduleName) {
        const module = this.modules.find(m => m.name === moduleName);
        if (!module) return;

        try {
            // In production, this would call the module manager API
            module.enabled = !module.enabled;
            console.log(`Module ${moduleName} ${module.enabled ? 'enabled' : 'disabled'}`);
            this.render();
        } catch (error) {
            console.error('Error toggling module:', error);
        }
    }

    /**
     * Check module health
     * @param {string} moduleName - Module name
     */
    async checkHealth(moduleName) {
        const module = this.modules.find(m => m.name === moduleName);
        if (!module) return;

        try {
            console.log(`Checking health for ${moduleName}...`);
            // In production, this would call the health endpoint
            // Simulate health check
            const healthStates = ['healthy', 'degraded', 'unhealthy'];
            module.health = healthStates[Math.floor(Math.random() * healthStates.length)];
            this.render();
        } catch (error) {
            console.error('Error checking health:', error);
        }
    }

    /**
     * Refresh module list
     */
    async refresh() {
        console.log('Refreshing modules...');
        await this.loadModules();
        this.render();
    }

    /**
     * Toggle auto-refresh
     */
    toggleAutoRefresh() {
        this.autoRefresh = !this.autoRefresh;
        
        if (this.autoRefresh) {
            this.startAutoRefresh();
        } else {
            this.stopAutoRefresh();
        }
        
        this.render();
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        this.refreshTimer = setInterval(() => {
            this.refresh();
        }, this.refreshInterval);
        
        console.log('Auto-refresh started');
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
        
        console.log('Auto-refresh stopped');
    }

    /**
     * Capitalize first letter
     * @private
     * @param {string} str - String to capitalize
     * @returns {string} Capitalized string
     */
    _capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * Attach event listeners
     * @private
     */
    _attachEventListeners() {
        // Event listeners are attached via onclick in the HTML
        // In a production app, you'd want to use proper event delegation
    }
}

// Create global instance
const moduleManagerUI = new ModuleManagerUI();

// Add CSS styles
const style = document.createElement('style');
style.textContent = `
    .module-manager {
        font-family: Arial, sans-serif;
        padding: 20px;
    }
    .module-manager-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .module-manager-controls button {
        margin-left: 10px;
        padding: 8px 16px;
        cursor: pointer;
        border: none;
        border-radius: 4px;
        background: #007bff;
        color: white;
    }
    .summary-stats {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    .stat {
        flex: 1;
        padding: 15px;
        background: #f5f5f5;
        border-radius: 8px;
        text-align: center;
    }
    .stat-label {
        display: block;
        font-size: 12px;
        color: #666;
        margin-bottom: 5px;
    }
    .stat-value {
        display: block;
        font-size: 24px;
        font-weight: bold;
    }
    .stat-enabled { color: #28a745; }
    .stat-healthy { color: #28a745; }
    .stat-degraded { color: #ffc107; }
    .module-category {
        margin-bottom: 30px;
    }
    .category-title {
        margin-bottom: 15px;
        color: #333;
    }
    .module-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 15px;
    }
    .module-card {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        background: white;
    }
    .module-card.enabled {
        border-color: #28a745;
    }
    .module-card.disabled {
        opacity: 0.6;
    }
    .module-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .module-name {
        font-weight: bold;
        font-size: 14px;
    }
    .module-badge {
        font-size: 10px;
        background: #ffc107;
        color: #000;
        padding: 2px 6px;
        border-radius: 3px;
    }
    .module-info {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        margin-bottom: 10px;
        color: #666;
    }
    .health-healthy { color: #28a745; }
    .health-degraded { color: #ffc107; }
    .health-unhealthy { color: #dc3545; }
    .health-unknown { color: #6c757d; }
    .module-actions {
        display: flex;
        gap: 5px;
    }
    .module-actions button {
        flex: 1;
        padding: 6px;
        font-size: 12px;
        cursor: pointer;
        border: 1px solid #ddd;
        border-radius: 4px;
        background: white;
    }
    .module-actions button:hover {
        background: #f0f0f0;
    }
`;
document.head.appendChild(style);

console.log('Module Manager UI loaded');
