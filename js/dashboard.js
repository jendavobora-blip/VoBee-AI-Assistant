/**
 * AI Activity Dashboard
 * 
 * Dashboard for monitoring AI activity, performance metrics, and task history.
 * ⚠️ DOES NOT MODIFY /js/chatbot.js - This is a NEW extension module
 * 
 * @module dashboard
 */

class AIDashboard {
    /**
     * Initialize AI Dashboard
     */
    constructor() {
        this.dashboardEndpoint = '/api/dashboard';
        this.metrics = {
            tasks: {
                total: 0,
                completed: 0,
                failed: 0,
                active: 0
            },
            performance: {
                avgResponseTime: 0,
                successRate: 0,
                throughput: 0
            },
            modules: {
                total: 30,
                enabled: 0,
                healthy: 0
            }
        };
        this.recentActivity = [];
        this.charts = {};
        
        console.log('AI Dashboard initialized');
    }

    /**
     * Initialize the dashboard
     * @param {string} containerId - Container element ID
     */
    async init(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        await this.loadMetrics();
        this.render();
        this.startLiveUpdates();
    }

    /**
     * Load metrics from orchestrator
     * @returns {Promise<void>}
     */
    async loadMetrics() {
        try {
            // Simulated metrics - in production would fetch from APIs
            this.metrics = {
                tasks: {
                    total: 1247,
                    completed: 1185,
                    failed: 42,
                    active: 20
                },
                performance: {
                    avgResponseTime: 2.3,
                    successRate: 95.0,
                    throughput: 42
                },
                modules: {
                    total: 30,
                    enabled: 26,
                    healthy: 24,
                    degraded: 2
                }
            };

            this.recentActivity = [
                { time: '2 min ago', task: 'Email Campaign Created', module: 'email-ai', status: 'completed' },
                { time: '5 min ago', task: 'Content Generated', module: 'content-ai', status: 'completed' },
                { time: '8 min ago', task: 'Analytics Report', module: 'analytics-ai', status: 'completed' },
                { time: '12 min ago', task: 'SEO Analysis', module: 'seo-ai', status: 'completed' },
                { time: '15 min ago', task: 'Social Post Scheduled', module: 'facebook-ai', status: 'completed' }
            ];

            console.log('Metrics loaded');
        } catch (error) {
            console.error('Error loading metrics:', error);
        }
    }

    /**
     * Render the dashboard
     */
    render() {
        if (!this.container) return;

        const html = `
            <div class="ai-dashboard">
                <div class="dashboard-header">
                    <h2>📊 AI Orchestration Dashboard</h2>
                    <div class="dashboard-time">
                        Last updated: ${new Date().toLocaleTimeString()}
                    </div>
                </div>

                <!-- Metrics Cards -->
                <div class="metrics-grid">
                    ${this._renderMetricsCards()}
                </div>

                <!-- Performance Charts -->
                <div class="charts-section">
                    <h3>📈 Performance</h3>
                    <div class="charts-grid">
                        ${this._renderPerformanceCharts()}
                    </div>
                </div>

                <!-- Recent Activity -->
                <div class="activity-section">
                    <h3>⚡ Recent Activity</h3>
                    ${this._renderRecentActivity()}
                </div>

                <!-- Module Status -->
                <div class="module-status-section">
                    <h3>🔌 Module Status</h3>
                    ${this._renderModuleStatus()}
                </div>

                <!-- Quick Actions -->
                <div class="quick-actions">
                    <h3>⚡ Quick Actions</h3>
                    ${this._renderQuickActions()}
                </div>
            </div>
        `;

        this.container.innerHTML = html;
        this._initializeCharts();
    }

    /**
     * Render metrics cards
     * @private
     * @returns {string} HTML
     */
    _renderMetricsCards() {
        return `
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-content">
                    <div class="metric-label">Total Tasks</div>
                    <div class="metric-value">${this.metrics.tasks.total}</div>
                    <div class="metric-subtext">${this.metrics.tasks.active} active</div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon">✅</div>
                <div class="metric-content">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">${this.metrics.performance.successRate}%</div>
                    <div class="metric-subtext">${this.metrics.tasks.completed} completed</div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon">⚡</div>
                <div class="metric-content">
                    <div class="metric-label">Avg Response</div>
                    <div class="metric-value">${this.metrics.performance.avgResponseTime}s</div>
                    <div class="metric-subtext">${this.metrics.performance.throughput}/hr throughput</div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon">🔌</div>
                <div class="metric-content">
                    <div class="metric-label">Active Modules</div>
                    <div class="metric-value">${this.metrics.modules.enabled}/${this.metrics.modules.total}</div>
                    <div class="metric-subtext">${this.metrics.modules.healthy} healthy</div>
                </div>
            </div>
        `;
    }

    /**
     * Render performance charts
     * @private
     * @returns {string} HTML
     */
    _renderPerformanceCharts() {
        return `
            <div class="chart-card">
                <h4>Task Completion Rate</h4>
                <div id="task-completion-chart" class="chart-container">
                    <div class="chart-placeholder">
                        📊 Chart visualization would go here
                        <div class="chart-stats">
                            <div>Completed: ${this.metrics.tasks.completed}</div>
                            <div>Failed: ${this.metrics.tasks.failed}</div>
                            <div>Success: ${this.metrics.performance.successRate}%</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-card">
                <h4>Response Time Trend</h4>
                <div id="response-time-chart" class="chart-container">
                    <div class="chart-placeholder">
                        📈 Chart visualization would go here
                        <div class="chart-stats">
                            <div>Current: ${this.metrics.performance.avgResponseTime}s</div>
                            <div>Target: <2.5s</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render recent activity
     * @private
     * @returns {string} HTML
     */
    _renderRecentActivity() {
        return `
            <div class="activity-list">
                ${this.recentActivity.map(activity => `
                    <div class="activity-item">
                        <div class="activity-status status-${activity.status}">
                            ${activity.status === 'completed' ? '✅' : '❌'}
                        </div>
                        <div class="activity-details">
                            <div class="activity-task">${activity.task}</div>
                            <div class="activity-meta">
                                <span class="activity-module">${activity.module}</span>
                                <span class="activity-time">${activity.time}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Render module status
     * @private
     * @returns {string} HTML
     */
    _renderModuleStatus() {
        const categories = ['Business', 'Finance', 'Research', 'Communication', 'Creative', 'Technical'];
        const statusData = [
            { category: 'Business', enabled: 6, total: 6, healthy: 6 },
            { category: 'Finance', enabled: 4, total: 5, healthy: 4 },
            { category: 'Research', enabled: 5, total: 5, healthy: 4 },
            { category: 'Communication', enabled: 3, total: 5, healthy: 3 },
            { category: 'Creative', enabled: 2, total: 5, healthy: 2 },
            { category: 'Technical', enabled: 3, total: 4, healthy: 3 }
        ];

        return `
            <div class="module-status-grid">
                ${statusData.map(cat => `
                    <div class="status-card">
                        <div class="status-category">${cat.category}</div>
                        <div class="status-bar">
                            <div class="status-bar-fill" style="width: ${(cat.enabled/cat.total)*100}%"></div>
                        </div>
                        <div class="status-numbers">
                            ${cat.enabled}/${cat.total} enabled · ${cat.healthy} healthy
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Render quick actions
     * @private
     * @returns {string} HTML
     */
    _renderQuickActions() {
        return `
            <div class="quick-actions-grid">
                <button class="action-btn" onclick="aiDashboard.createEmailCampaign()">
                    ✉️ Create Email Campaign
                </button>
                <button class="action-btn" onclick="aiDashboard.generateContent()">
                    ✍️ Generate Content
                </button>
                <button class="action-btn" onclick="aiDashboard.runAnalytics()">
                    📊 Run Analytics
                </button>
                <button class="action-btn" onclick="aiDashboard.checkAllModules()">
                    🏥 Check All Modules
                </button>
            </div>
        `;
    }

    /**
     * Initialize charts
     * @private
     */
    _initializeCharts() {
        // In a production app, you'd initialize actual charting libraries here
        // Like Chart.js, D3.js, etc.
        console.log('Charts initialized');
    }

    /**
     * Start live updates
     */
    startLiveUpdates() {
        this.updateInterval = setInterval(async () => {
            await this.loadMetrics();
            this.render();
        }, 5000); // Update every 5 seconds

        console.log('Live updates started');
    }

    /**
     * Stop live updates
     */
    stopLiveUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        console.log('Live updates stopped');
    }

    /**
     * Quick action: Create email campaign
     */
    async createEmailCampaign() {
        console.log('Creating email campaign...');
        if (window.AIOrchestration) {
            await window.AIOrchestration.createEmailCampaign({
                subject: 'Quick Campaign',
                content: 'Dashboard created campaign'
            });
        }
    }

    /**
     * Quick action: Generate content
     */
    async generateContent() {
        console.log('Generating content...');
        if (window.AIOrchestration) {
            await window.AIOrchestration.generateContent({
                type: 'blog',
                topic: 'AI Trends'
            });
        }
    }

    /**
     * Quick action: Run analytics
     */
    async runAnalytics() {
        console.log('Running analytics...');
        if (window.AIOrchestration) {
            await window.AIOrchestration.runAnalytics({
                period: 'week'
            });
        }
    }

    /**
     * Quick action: Check all modules
     */
    async checkAllModules() {
        console.log('Checking all modules...');
        await this.loadMetrics();
        this.render();
    }

    /**
     * Destroy dashboard
     */
    destroy() {
        this.stopLiveUpdates();
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// Create global instance
const aiDashboard = new AIDashboard();

// Add CSS styles
const dashboardStyle = document.createElement('style');
dashboardStyle.textContent = `
    .ai-dashboard {
        font-family: Arial, sans-serif;
        padding: 20px;
        background: #f5f5f5;
    }
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .dashboard-time {
        color: #666;
        font-size: 14px;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .metric-icon {
        font-size: 36px;
    }
    .metric-content {
        flex: 1;
    }
    .metric-label {
        font-size: 12px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        margin: 5px 0;
    }
    .metric-subtext {
        font-size: 12px;
        color: #999;
    }
    .charts-section, .activity-section, .module-status-section, .quick-actions {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .charts-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .chart-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
    }
    .chart-container {
        height: 200px;
        margin-top: 10px;
    }
    .chart-placeholder {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #f9f9f9;
        border-radius: 4px;
        color: #666;
    }
    .chart-stats {
        margin-top: 10px;
        font-size: 12px;
        text-align: center;
    }
    .activity-list {
        margin-top: 15px;
    }
    .activity-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
    }
    .activity-item:last-child {
        border-bottom: none;
    }
    .activity-status {
        font-size: 20px;
    }
    .activity-details {
        flex: 1;
    }
    .activity-task {
        font-weight: 500;
        margin-bottom: 4px;
    }
    .activity-meta {
        font-size: 12px;
        color: #666;
        display: flex;
        gap: 15px;
    }
    .module-status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    .status-card {
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    .status-category {
        font-weight: bold;
        margin-bottom: 10px;
    }
    .status-bar {
        height: 8px;
        background: #f0f0f0;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .status-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        transition: width 0.3s;
    }
    .status-numbers {
        font-size: 12px;
        color: #666;
    }
    .quick-actions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    .action-btn {
        padding: 15px;
        border: 2px solid #007bff;
        background: white;
        color: #007bff;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .action-btn:hover {
        background: #007bff;
        color: white;
    }
`;
document.head.appendChild(dashboardStyle);

console.log('AI Dashboard loaded');
