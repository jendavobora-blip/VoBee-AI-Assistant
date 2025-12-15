/**
 * VoBee Security & Privacy Module
 * 
 * This module handles owner authentication, approval workflows,
 * and data encryption for the super-intelligence system.
 * 
 * @module security
 */

/**
 * Security Manager Class
 * Manages authentication, encryption, and privacy controls
 */
class SecurityManager {
    constructor() {
        this.owner = null;
        this.isAuthenticated = false;
        this.sessionToken = null;
        this.encryptionEnabled = true;
        this.approvalQueue = [];
        this.securityLevel = 'high'; // 'low', 'medium', 'high'
        this.accessLog = [];
        
        // Initialize from storage
        this.loadSecuritySettings();
    }

    /**
     * Load security settings from storage
     */
    async loadSecuritySettings() {
        try {
            const settings = localStorage.getItem('vobee_security_settings');
            if (settings) {
                const parsed = JSON.parse(settings);
                this.securityLevel = parsed.securityLevel || 'high';
                this.encryptionEnabled = parsed.encryptionEnabled !== false;
            }
        } catch (error) {
            console.error('Error loading security settings:', error);
        }
    }

    /**
     * Save security settings to storage
     */
    async saveSecuritySettings() {
        try {
            const settings = {
                securityLevel: this.securityLevel,
                encryptionEnabled: this.encryptionEnabled
            };
            localStorage.setItem('vobee_security_settings', JSON.stringify(settings));
        } catch (error) {
            console.error('Error saving security settings:', error);
        }
    }

    /**
     * Initialize owner (first-time setup)
     * @param {string} ownerId - Owner identifier
     * @param {string} passphrase - Owner passphrase
     * @returns {Promise<boolean>} Success status
     */
    async initializeOwner(ownerId, passphrase) {
        try {
            // Hash the passphrase
            const hashedPassphrase = await this.hashPassphrase(passphrase);
            
            // Store owner credentials (encrypted)
            const ownerData = {
                id: ownerId,
                passphraseHash: hashedPassphrase,
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            };
            
            localStorage.setItem('vobee_owner', JSON.stringify(ownerData));
            
            this.owner = {
                id: ownerId,
                createdAt: ownerData.createdAt
            };
            
            this.isAuthenticated = true;
            this.sessionToken = this.generateSessionToken();
            
            this.logAccess('Owner initialized', 'success');
            
            return true;
        } catch (error) {
            console.error('Error initializing owner:', error);
            this.logAccess('Owner initialization failed', 'error');
            return false;
        }
    }

    /**
     * Authenticate owner
     * @param {string} ownerId - Owner identifier
     * @param {string} passphrase - Owner passphrase
     * @returns {Promise<boolean>} Authentication result
     */
    async authenticate(ownerId, passphrase) {
        try {
            const storedOwner = localStorage.getItem('vobee_owner');
            if (!storedOwner) {
                this.logAccess('Authentication failed - no owner', 'warning');
                return false;
            }

            const ownerData = JSON.parse(storedOwner);
            
            // Verify owner ID
            if (ownerData.id !== ownerId) {
                this.logAccess('Authentication failed - invalid owner ID', 'warning');
                return false;
            }

            // Verify passphrase
            const hashedPassphrase = await this.hashPassphrase(passphrase);
            if (ownerData.passphraseHash !== hashedPassphrase) {
                this.logAccess('Authentication failed - invalid passphrase', 'warning');
                return false;
            }

            // Authentication successful
            this.owner = {
                id: ownerData.id,
                createdAt: ownerData.createdAt
            };
            
            this.isAuthenticated = true;
            this.sessionToken = this.generateSessionToken();
            
            // Update last login
            ownerData.lastLogin = new Date().toISOString();
            localStorage.setItem('vobee_owner', JSON.stringify(ownerData));
            
            this.logAccess('Authentication successful', 'success');
            
            return true;
        } catch (error) {
            console.error('Authentication error:', error);
            this.logAccess('Authentication error', 'error');
            return false;
        }
    }

    /**
     * Logout current session
     */
    logout() {
        this.isAuthenticated = false;
        this.sessionToken = null;
        this.owner = null;
        this.logAccess('User logged out', 'info');
    }

    /**
     * Check if owner exists
     * @returns {boolean} Owner exists
     */
    hasOwner() {
        return !!localStorage.getItem('vobee_owner');
    }

    /**
     * Hash passphrase using Web Crypto API
     * @param {string} passphrase - Passphrase to hash
     * @returns {Promise<string>} Hashed passphrase
     */
    async hashPassphrase(passphrase) {
        try {
            const encoder = new TextEncoder();
            const data = encoder.encode(passphrase);
            const hashBuffer = await crypto.subtle.digest('SHA-256', data);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            return hashHex;
        } catch (error) {
            console.error('Hashing error:', error);
            // Fallback to simple hash if Web Crypto API fails
            return btoa(passphrase);
        }
    }

    /**
     * Generate a session token
     * @returns {string} Session token
     */
    generateSessionToken() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Request approval for an action
     * @param {string} action - Action description
     * @param {Object} details - Action details
     * @returns {string} Approval request ID
     */
    requestApproval(action, details) {
        const request = {
            id: Date.now().toString(),
            action: action,
            details: details,
            timestamp: new Date().toISOString(),
            status: 'pending'
        };
        
        this.approvalQueue.push(request);
        this.logAccess(`Approval requested: ${action}`, 'info');
        
        return request.id;
    }

    /**
     * Approve an action
     * @param {string} requestId - Request ID to approve
     * @returns {boolean} Success status
     */
    approveAction(requestId) {
        const request = this.approvalQueue.find(r => r.id === requestId);
        
        if (!request) {
            return false;
        }
        
        request.status = 'approved';
        request.approvedAt = new Date().toISOString();
        
        this.logAccess(`Action approved: ${request.action}`, 'success');
        
        return true;
    }

    /**
     * Reject an action
     * @param {string} requestId - Request ID to reject
     * @returns {boolean} Success status
     */
    rejectAction(requestId) {
        const request = this.approvalQueue.find(r => r.id === requestId);
        
        if (!request) {
            return false;
        }
        
        request.status = 'rejected';
        request.rejectedAt = new Date().toISOString();
        
        this.logAccess(`Action rejected: ${request.action}`, 'warning');
        
        return true;
    }

    /**
     * Get pending approval requests
     * @returns {Array} Pending requests
     */
    getPendingApprovals() {
        return this.approvalQueue.filter(r => r.status === 'pending');
    }

    /**
     * Encrypt data
     * @param {string} data - Data to encrypt
     * @returns {string} Encrypted data
     */
    encrypt(data) {
        if (!this.encryptionEnabled) {
            return data;
        }
        
        try {
            // Simple XOR encryption for demo (use proper encryption in production)
            const key = this.sessionToken || 'default-key';
            let encrypted = '';
            
            for (let i = 0; i < data.length; i++) {
                const charCode = data.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                encrypted += String.fromCharCode(charCode);
            }
            
            return btoa(encrypted);
        } catch (error) {
            console.error('Encryption error:', error);
            return data;
        }
    }

    /**
     * Decrypt data
     * @param {string} encryptedData - Encrypted data
     * @returns {string} Decrypted data
     */
    decrypt(encryptedData) {
        if (!this.encryptionEnabled) {
            return encryptedData;
        }
        
        try {
            const key = this.sessionToken || 'default-key';
            const decoded = atob(encryptedData);
            let decrypted = '';
            
            for (let i = 0; i < decoded.length; i++) {
                const charCode = decoded.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                decrypted += String.fromCharCode(charCode);
            }
            
            return decrypted;
        } catch (error) {
            console.error('Decryption error:', error);
            return encryptedData;
        }
    }

    /**
     * Log access event
     * @param {string} event - Event description
     * @param {string} level - Log level (info, warning, error, success)
     */
    logAccess(event, level = 'info') {
        const logEntry = {
            timestamp: new Date().toISOString(),
            event: event,
            level: level,
            owner: this.owner ? this.owner.id : 'anonymous',
            authenticated: this.isAuthenticated
        };
        
        this.accessLog.push(logEntry);
        
        // Keep only last 1000 entries
        if (this.accessLog.length > 1000) {
            this.accessLog = this.accessLog.slice(-1000);
        }
        
        console.log(`[Security ${level.toUpperCase()}] ${event}`);
    }

    /**
     * Get access log
     * @param {number} limit - Number of entries to return
     * @returns {Array} Access log entries
     */
    getAccessLog(limit = 100) {
        return this.accessLog.slice(-limit);
    }

    /**
     * Set security level
     * @param {string} level - Security level (low, medium, high)
     */
    setSecurityLevel(level) {
        if (['low', 'medium', 'high'].includes(level)) {
            this.securityLevel = level;
            this.saveSecuritySettings();
            this.logAccess(`Security level changed to ${level}`, 'info');
        }
    }

    /**
     * Enable/disable encryption
     * @param {boolean} enabled - Encryption status
     */
    setEncryption(enabled) {
        this.encryptionEnabled = enabled;
        this.saveSecuritySettings();
        this.logAccess(`Encryption ${enabled ? 'enabled' : 'disabled'}`, 'info');
    }

    /**
     * Get security status
     * @returns {Object} Security status
     */
    getStatus() {
        return {
            hasOwner: this.hasOwner(),
            isAuthenticated: this.isAuthenticated,
            owner: this.owner ? this.owner.id : null,
            securityLevel: this.securityLevel,
            encryptionEnabled: this.encryptionEnabled,
            pendingApprovals: this.getPendingApprovals().length,
            accessLogSize: this.accessLog.length
        };
    }

    /**
     * Clear all security data (use with caution!)
     */
    clearSecurityData() {
        if (confirm('Are you sure you want to clear all security data? This action cannot be undone.')) {
            localStorage.removeItem('vobee_owner');
            localStorage.removeItem('vobee_security_settings');
            this.logout();
            this.approvalQueue = [];
            this.accessLog = [];
            this.logAccess('All security data cleared', 'warning');
            return true;
        }
        return false;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SecurityManager };
}
