/**
 * VoBee Enhanced UI Controller
 * 
 * Enhanced UI controller for the Super-Intelligence system
 * with voice controls and device preview support.
 * 
 * @module enhanced-ui
 */

/**
 * Enhanced Chat UI Class
 * Extends the basic ChatUI with super-intelligence features
 */
class EnhancedChatUI extends ChatUI {
    constructor(chatbot) {
        super(chatbot);
        this.voiceButton = null;
        this.previewButton = null;
        this.systemStatus = null;
        this.isVoiceActive = false;
        this.isPreviewActive = false;
    }

    /**
     * Initialize the enhanced UI
     */
    async init() {
        // Call parent init
        await super.init();
        
        // Get additional elements
        this.voiceButton = document.getElementById('voice-button');
        this.previewButton = document.getElementById('preview-button');
        this.systemStatus = document.getElementById('system-status');
        
        // Setup additional event listeners
        this.setupEnhancedEventListeners();
        
        // Setup voice callbacks
        this.setupVoiceCallbacks();
        
        // Display enhanced welcome message
        if (this.chatbot.getHistory().length === 0) {
            this.displayEnhancedWelcomeMessage();
        }
        
        console.log('Enhanced Chat UI initialized! 🧠');
    }

    /**
     * Setup enhanced event listeners
     */
    setupEnhancedEventListeners() {
        // Voice button
        if (this.voiceButton) {
            this.voiceButton.addEventListener('click', () => this.toggleVoice());
        }
        
        // Preview button
        if (this.previewButton) {
            this.previewButton.addEventListener('click', () => this.togglePreview());
        }
    }

    /**
     * Setup voice interface callbacks
     */
    setupVoiceCallbacks() {
        if (!this.chatbot.voiceInterface) return;
        
        // Voice input handler
        this.chatbot.onVoiceInput = (transcript) => {
            this.displayMessage('user', transcript);
        };
        
        // Interim results
        this.chatbot.onInterimVoiceResult = (transcript) => {
            this.showInterimVoice(transcript);
        };
        
        // Listening state changes
        this.chatbot.onVoiceListeningStart = () => {
            this.updateVoiceButtonState(true);
        };
        
        this.chatbot.onVoiceListeningEnd = () => {
            this.updateVoiceButtonState(false);
            this.hideInterimVoice();
        };
    }

    /**
     * Toggle voice input
     */
    toggleVoice() {
        if (!this.chatbot.voiceInterface) {
            this.displaySystemMessage('❌ Voice input not supported in your browser');
            return;
        }
        
        this.chatbot.voiceInterface.toggleListening();
    }

    /**
     * Update voice button state
     * @param {boolean} isActive - Whether voice is active
     */
    updateVoiceButtonState(isActive) {
        if (!this.voiceButton) return;
        
        this.isVoiceActive = isActive;
        
        if (isActive) {
            this.voiceButton.classList.add('active');
            this.voiceButton.innerHTML = '🎙️';
            this.voiceButton.title = 'Listening... Click to stop';
        } else {
            this.voiceButton.classList.remove('active');
            this.voiceButton.innerHTML = '🎤';
            this.voiceButton.title = 'Click to start voice input';
        }
    }

    /**
     * Show interim voice recognition results
     * @param {string} text - Interim text
     */
    showInterimVoice(text) {
        let interimDiv = document.getElementById('interim-voice');
        
        if (!interimDiv) {
            interimDiv = document.createElement('div');
            interimDiv.id = 'interim-voice';
            interimDiv.className = 'interim-voice';
            this.chatMessages.appendChild(interimDiv);
        }
        
        interimDiv.textContent = `🎤 ${text}...`;
        this.scrollToBottom();
    }

    /**
     * Hide interim voice display
     */
    hideInterimVoice() {
        const interimDiv = document.getElementById('interim-voice');
        if (interimDiv) {
            interimDiv.remove();
        }
    }

    /**
     * Toggle device preview
     */
    togglePreview() {
        if (!this.chatbot.devicePreview) {
            return;
        }
        
        if (this.isPreviewActive) {
            this.chatbot.devicePreview.disablePreview();
            this.isPreviewActive = false;
            this.previewButton.classList.remove('active');
            this.displaySystemMessage('📱 Device preview disabled');
        } else {
            this.showPreviewSelector();
        }
    }

    /**
     * Show device preview selector
     */
    showPreviewSelector() {
        const selector = this.chatbot.devicePreview.createDeviceSelector();
        document.body.appendChild(selector);
        
        // Add close handler
        const closeBtn = selector.querySelector('.close-preview-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.isPreviewActive = false;
                this.previewButton.classList.remove('active');
            });
        }
        
        this.isPreviewActive = true;
        this.previewButton.classList.add('active');
    }

    /**
     * Display enhanced welcome message
     */
    displayEnhancedWelcomeMessage() {
        const messages = [
            "🧠 Welcome to VoBee Super-Intelligence System!",
            "I'm powered by a hierarchical AI architecture with specialized subsystems.",
            "I can help with marketing, media management, orchestration, analytics, and creative tasks!",
            "Try saying: 'Create a marketing campaign' or 'Analyze my data'",
            "Type /help to see all available commands and features."
        ];

        messages.forEach((msg, index) => {
            setTimeout(() => {
                this.displayMessage('bot', msg);
            }, index * 400);
        });
    }

    /**
     * Display system message (info/status)
     * @param {string} message - System message
     */
    displaySystemMessage(message) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    /**
     * Enhanced handle send with voice support
     */
    async handleSend() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Clear input
        this.userInput.value = '';

        // Display user message
        this.displayMessage('user', message);

        // Show typing indicator
        this.showTypingIndicator();

        // Get and display bot response
        setTimeout(async () => {
            const response = await this.chatbot.processMessage(message);
            this.hideTypingIndicator();
            
            // Display response
            this.displayMessage('bot', response);
            
            // Optionally speak the response if voice was used
            if (this.isVoiceActive && this.chatbot.voiceInterface) {
                this.chatbot.voiceInterface.speak(response);
            }
        }, 500 + Math.random() * 500);
    }

    /**
     * Update system status display
     */
    updateSystemStatus() {
        if (!this.systemStatus) return;
        
        const info = this.chatbot.getSystemInfo();
        const statusText = this.systemStatus.querySelector('.status-text');
        
        if (statusText) {
            statusText.textContent = `Supreme Brain Active - ${info.supremeBrain.subSystems.length} subsystems`;
        }
    }

    /**
     * Enhanced message display with formatting
     * @param {string} sender - 'user', 'bot', or 'system'
     * @param {string} message - Message content
     */
    displayMessage(sender, message) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format message (preserve newlines)
        const formattedMessage = message.split('\n').map(line => {
            const span = document.createElement('span');
            span.textContent = line;
            return span;
        });
        
        formattedMessage.forEach((span, index) => {
            contentDiv.appendChild(span);
            if (index < formattedMessage.length - 1) {
                contentDiv.appendChild(document.createElement('br'));
            }
        });

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
}

// Initialize enhanced UI when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    const enhancedUI = new EnhancedChatUI(vobee);
    await enhancedUI.init();
    
    // Update status periodically
    setInterval(() => {
        enhancedUI.updateSystemStatus();
    }, 5000);
});
