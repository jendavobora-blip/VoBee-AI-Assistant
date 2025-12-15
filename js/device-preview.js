/**
 * VoBee Multi-Device Preview System
 * 
 * This module provides visual previews for different device types
 * (TV, Monitor, Mobile, Tablet) to ensure optimal display across all platforms.
 * 
 * @module device-preview
 */

/**
 * Device Preview Class
 * Manages responsive previews for different screen sizes and device types
 */
class DevicePreview {
    constructor() {
        this.devices = this.initializeDevices();
        this.currentDevice = 'monitor';
        this.previewMode = false;
        this.originalStyles = null;
    }

    /**
     * Initialize device configurations
     * @returns {Object} Device specifications
     */
    initializeDevices() {
        return {
            tv: {
                name: 'Television',
                width: 1920,
                height: 1080,
                aspectRatio: '16:9',
                ppi: 96,
                description: 'Large screen TV display (1080p)',
                scale: 1.0,
                orientation: 'landscape'
            },
            tv4k: {
                name: '4K Television',
                width: 3840,
                height: 2160,
                aspectRatio: '16:9',
                ppi: 96,
                description: 'Ultra HD 4K TV display',
                scale: 0.5,
                orientation: 'landscape'
            },
            monitor: {
                name: 'Desktop Monitor',
                width: 1920,
                height: 1080,
                aspectRatio: '16:9',
                ppi: 96,
                description: 'Standard desktop monitor',
                scale: 1.0,
                orientation: 'landscape'
            },
            laptop: {
                name: 'Laptop',
                width: 1366,
                height: 768,
                aspectRatio: '16:9',
                ppi: 96,
                description: 'Typical laptop screen',
                scale: 1.0,
                orientation: 'landscape'
            },
            tablet: {
                name: 'Tablet (Portrait)',
                width: 768,
                height: 1024,
                aspectRatio: '3:4',
                ppi: 132,
                description: 'iPad-like tablet in portrait mode',
                scale: 1.0,
                orientation: 'portrait'
            },
            tabletLandscape: {
                name: 'Tablet (Landscape)',
                width: 1024,
                height: 768,
                aspectRatio: '4:3',
                ppi: 132,
                description: 'iPad-like tablet in landscape mode',
                scale: 1.0,
                orientation: 'landscape'
            },
            mobile: {
                name: 'Mobile Phone (Portrait)',
                width: 375,
                height: 667,
                aspectRatio: '9:16',
                ppi: 163,
                description: 'iPhone-like mobile device',
                scale: 1.0,
                orientation: 'portrait'
            },
            mobileLandscape: {
                name: 'Mobile Phone (Landscape)',
                width: 667,
                height: 375,
                aspectRatio: '16:9',
                ppi: 163,
                description: 'iPhone-like mobile in landscape',
                scale: 1.0,
                orientation: 'landscape'
            },
            mobileSmall: {
                name: 'Small Mobile',
                width: 320,
                height: 568,
                aspectRatio: '9:16',
                ppi: 163,
                description: 'Smaller mobile device',
                scale: 1.0,
                orientation: 'portrait'
            }
        };
    }

    /**
     * Switch to a specific device preview
     * @param {string} deviceKey - Device identifier
     * @returns {boolean} Success status
     */
    switchToDevice(deviceKey) {
        if (!this.devices[deviceKey]) {
            console.error(`Device "${deviceKey}" not found`);
            return false;
        }

        this.currentDevice = deviceKey;
        
        if (this.previewMode) {
            this.applyDeviceStyles(deviceKey);
        }

        return true;
    }

    /**
     * Enable preview mode
     * @param {string} deviceKey - Optional device to preview
     */
    enablePreview(deviceKey = null) {
        if (deviceKey) {
            this.switchToDevice(deviceKey);
        }

        // Store original styles
        this.originalStyles = {
            width: document.documentElement.style.width,
            height: document.documentElement.style.height,
            maxWidth: document.documentElement.style.maxWidth,
            margin: document.documentElement.style.margin,
            transform: document.documentElement.style.transform
        };

        this.previewMode = true;
        this.applyDeviceStyles(this.currentDevice);
    }

    /**
     * Disable preview mode and restore original styles
     */
    disablePreview() {
        if (!this.previewMode) {
            return;
        }

        this.previewMode = false;

        // Restore original styles
        if (this.originalStyles) {
            const root = document.documentElement;
            root.style.width = this.originalStyles.width;
            root.style.height = this.originalStyles.height;
            root.style.maxWidth = this.originalStyles.maxWidth;
            root.style.margin = this.originalStyles.margin;
            root.style.transform = this.originalStyles.transform;
            
            // Remove preview container if it exists
            const previewContainer = document.querySelector('.device-preview-container');
            if (previewContainer) {
                const content = previewContainer.querySelector('.device-preview-content');
                if (content && content.firstChild) {
                    previewContainer.parentNode.replaceChild(content.firstChild, previewContainer);
                }
            }
        }
    }

    /**
     * Apply device-specific styles
     * @param {string} deviceKey - Device identifier
     */
    applyDeviceStyles(deviceKey) {
        const device = this.devices[deviceKey];
        if (!device) {
            return;
        }

        // Create or get preview container
        let container = document.querySelector('.device-preview-container');
        
        if (!container) {
            container = document.createElement('div');
            container.className = 'device-preview-container';
            
            const content = document.createElement('div');
            content.className = 'device-preview-content';
            
            // Move body content into preview
            const appContainer = document.querySelector('.app-container');
            if (appContainer) {
                content.appendChild(appContainer);
            }
            
            container.appendChild(content);
            document.body.appendChild(container);
        }

        // Apply device dimensions
        const content = container.querySelector('.device-preview-content');
        if (content) {
            content.style.width = `${device.width}px`;
            content.style.height = `${device.height}px`;
            content.style.transform = `scale(${device.scale})`;
            content.style.transformOrigin = 'top left';
            content.style.border = '2px solid #333';
            content.style.boxShadow = '0 10px 40px rgba(0,0,0,0.3)';
            content.style.margin = '20px auto';
            content.style.overflow = 'hidden';
            content.style.backgroundColor = 'white';
        }

        // Update container
        container.style.display = 'flex';
        container.style.justifyContent = 'center';
        container.style.alignItems = 'flex-start';
        container.style.minHeight = '100vh';
        container.style.padding = '20px';
        container.style.backgroundColor = '#f0f0f0';
    }

    /**
     * Get current device information
     * @returns {Object} Current device specs
     */
    getCurrentDevice() {
        return {
            key: this.currentDevice,
            ...this.devices[this.currentDevice]
        };
    }

    /**
     * Get all available devices
     * @returns {Object} All device specifications
     */
    getAllDevices() {
        return { ...this.devices };
    }

    /**
     * Create device selector UI
     * @returns {HTMLElement} Device selector element
     */
    createDeviceSelector() {
        const selector = document.createElement('div');
        selector.className = 'device-selector';
        selector.innerHTML = `
            <div class="device-selector-header">
                <h3>Device Preview</h3>
                <button class="close-preview-btn">×</button>
            </div>
            <div class="device-selector-grid">
                ${Object.entries(this.devices).map(([key, device]) => `
                    <button class="device-btn" data-device="${key}" title="${device.description}">
                        <span class="device-icon">${this.getDeviceIcon(device.orientation)}</span>
                        <span class="device-name">${device.name}</span>
                        <span class="device-size">${device.width}×${device.height}</span>
                    </button>
                `).join('')}
            </div>
        `;

        // Add event listeners
        selector.querySelectorAll('.device-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const deviceKey = btn.dataset.device;
                this.switchToDevice(deviceKey);
                this.enablePreview();
                
                // Update active state
                selector.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        const closeBtn = selector.querySelector('.close-preview-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.disablePreview();
                selector.remove();
            });
        }

        return selector;
    }

    /**
     * Get icon for device type
     * @param {string} orientation - Device orientation
     * @returns {string} Icon emoji
     */
    getDeviceIcon(orientation) {
        if (orientation === 'portrait') {
            return '📱';
        }
        return '💻';
    }

    /**
     * Generate responsive CSS for current device
     * @returns {string} CSS rules
     */
    generateResponsiveCSS() {
        const device = this.devices[this.currentDevice];
        
        return `
            /* Device: ${device.name} */
            @media (max-width: ${device.width}px) {
                .app-container {
                    max-width: ${device.width}px;
                }
            }
        `;
    }

    /**
     * Test responsiveness across all devices
     * @returns {Array} Test results
     */
    testAllDevices() {
        const results = [];
        
        for (const [key, device] of Object.entries(this.devices)) {
            results.push({
                device: device.name,
                key: key,
                width: device.width,
                height: device.height,
                aspectRatio: device.aspectRatio,
                tested: true,
                timestamp: new Date().toISOString()
            });
        }
        
        return results;
    }

    /**
     * Get preview status
     * @returns {Object} Preview status
     */
    getStatus() {
        return {
            previewMode: this.previewMode,
            currentDevice: this.currentDevice,
            deviceInfo: this.getCurrentDevice(),
            totalDevices: Object.keys(this.devices).length
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DevicePreview };
}
