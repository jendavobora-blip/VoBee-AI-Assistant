/**
 * VoBee AI Assistant - Main Chatbot Logic
 * 
 * This module handles the core chatbot functionality including:
 * - Pattern matching for user input
 * - IndexedDB integration for conversation history and learning
 * - UI interactions and message rendering
 * 
 * @module chatbot
 */

/**
 * VoBee Chatbot Class
 * Manages all chatbot operations including message processing,
 * conversation history, and pseudo-learning features
 */
class VoBeeChatbot {
    /**
     * Initialize the chatbot with default settings
     */
    constructor() {
        this.dbName = 'VoBeeDB';
        this.dbVersion = 1;
        this.db = null;
        this.conversationHistory = [];
        this.isInitialized = false;
        
        // Store names for IndexedDB
        this.stores = {
            conversations: 'conversations',
            unrecognized: 'unrecognized_queries'
        };
    }

    /**
     * Initialize the chatbot - set up IndexedDB and load conversation history
     * @returns {Promise<void>}
     */
    async init() {
        try {
            await this.initDatabase();
            await this.loadConversationHistory();
            this.isInitialized = true;
            console.log('VoBee Chatbot initialized successfully! 🐝');
        } catch (error) {
            console.error('Failed to initialize VoBee Chatbot:', error);
            // Continue without persistence if IndexedDB fails
            this.isInitialized = true;
        }
    }

    /**
     * Initialize IndexedDB for storing conversation history and unrecognized queries
     * @returns {Promise<IDBDatabase>}
     */
    initDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onerror = () => {
                console.error('IndexedDB error:', request.error);
                reject(request.error);
            };

            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Create conversations store if it doesn't exist
                if (!db.objectStoreNames.contains(this.stores.conversations)) {
                    const conversationStore = db.createObjectStore(this.stores.conversations, {
                        keyPath: 'id',
                        autoIncrement: true
                    });
                    conversationStore.createIndex('timestamp', 'timestamp', { unique: false });
                }

                // Create unrecognized queries store for pseudo-learning
                if (!db.objectStoreNames.contains(this.stores.unrecognized)) {
                    const unrecognizedStore = db.createObjectStore(this.stores.unrecognized, {
                        keyPath: 'id',
                        autoIncrement: true
                    });
                    unrecognizedStore.createIndex('query', 'query', { unique: false });
                    unrecognizedStore.createIndex('timestamp', 'timestamp', { unique: false });
                    unrecognizedStore.createIndex('count', 'count', { unique: false });
                }
            };
        });
    }

    /**
     * Load conversation history from IndexedDB
     * @returns {Promise<Array>}
     */
    async loadConversationHistory() {
        if (!this.db) return [];

        return new Promise((resolve, reject) => {
            try {
                const transaction = this.db.transaction([this.stores.conversations], 'readonly');
                const store = transaction.objectStore(this.stores.conversations);
                const request = store.getAll();

                request.onsuccess = () => {
                    this.conversationHistory = request.result || [];
                    resolve(this.conversationHistory);
                };

                request.onerror = () => {
                    console.error('Error loading conversation history:', request.error);
                    reject(request.error);
                };
            } catch (error) {
                console.error('Transaction error:', error);
                reject(error);
            }
        });
    }

    /**
     * Save a message to conversation history
     * @param {string} sender - 'user' or 'bot'
     * @param {string} message - The message content
     * @returns {Promise<void>}
     */
    async saveMessage(sender, message) {
        const messageObj = {
            sender,
            message,
            timestamp: new Date().toISOString()
        };

        this.conversationHistory.push(messageObj);

        if (this.db) {
            return new Promise((resolve, reject) => {
                try {
                    const transaction = this.db.transaction([this.stores.conversations], 'readwrite');
                    const store = transaction.objectStore(this.stores.conversations);
                    const request = store.add(messageObj);

                    request.onsuccess = () => resolve();
                    request.onerror = () => {
                        console.error('Error saving message:', request.error);
                        reject(request.error);
                    };
                } catch (error) {
                    console.error('Transaction error:', error);
                    reject(error);
                }
            });
        }
    }

    /**
     * Log an unrecognized query for pseudo-learning
     * @param {string} query - The unrecognized user input
     * @returns {Promise<void>}
     */
    async logUnrecognizedQuery(query) {
        if (!this.db) return;

        const normalizedQuery = query.toLowerCase().trim();

        return new Promise((resolve, reject) => {
            try {
                const transaction = this.db.transaction([this.stores.unrecognized], 'readwrite');
                const store = transaction.objectStore(this.stores.unrecognized);
                const index = store.index('query');
                const request = index.get(normalizedQuery);

                request.onsuccess = () => {
                    if (request.result) {
                        // Update existing entry
                        const entry = request.result;
                        entry.count++;
                        entry.lastSeen = new Date().toISOString();
                        store.put(entry);
                    } else {
                        // Add new entry
                        store.add({
                            query: normalizedQuery,
                            originalQuery: query,
                            count: 1,
                            timestamp: new Date().toISOString(),
                            lastSeen: new Date().toISOString()
                        });
                    }
                    resolve();
                };

                request.onerror = () => {
                    console.error('Error logging unrecognized query:', request.error);
                    reject(request.error);
                };
            } catch (error) {
                console.error('Transaction error:', error);
                reject(error);
            }
        });
    }

    /**
     * Get all unrecognized queries for analysis
     * @returns {Promise<Array>}
     */
    async getUnrecognizedQueries() {
        if (!this.db) return [];

        return new Promise((resolve, reject) => {
            try {
                const transaction = this.db.transaction([this.stores.unrecognized], 'readonly');
                const store = transaction.objectStore(this.stores.unrecognized);
                const request = store.getAll();

                request.onsuccess = () => {
                    resolve(request.result || []);
                };

                request.onerror = () => {
                    console.error('Error getting unrecognized queries:', request.error);
                    reject(request.error);
                };
            } catch (error) {
                console.error('Transaction error:', error);
                reject(error);
            }
        });
    }

    /**
     * Clear conversation history
     * @returns {Promise<void>}
     */
    async clearHistory() {
        this.conversationHistory = [];

        if (this.db) {
            return new Promise((resolve, reject) => {
                try {
                    const transaction = this.db.transaction([this.stores.conversations], 'readwrite');
                    const store = transaction.objectStore(this.stores.conversations);
                    const request = store.clear();

                    request.onsuccess = () => resolve();
                    request.onerror = () => {
                        console.error('Error clearing history:', request.error);
                        reject(request.error);
                    };
                } catch (error) {
                    console.error('Transaction error:', error);
                    reject(error);
                }
            });
        }
    }

    /**
     * Find the matching category for user input
     * @param {string} input - User's message
     * @returns {string|null} - Matched category name or null
     */
    findMatchingCategory(input) {
        const normalizedInput = input.toLowerCase().trim();

        // Check each category's keywords
        for (const [category, keywords] of Object.entries(KeywordMappings)) {
            for (const keyword of keywords) {
                if (normalizedInput.includes(keyword)) {
                    return category;
                }
            }
        }

        return null;
    }

    /**
     * Get a random response from a category
     * @param {string} category - The response category
     * @returns {string} - Random response from the category
     */
    getRandomResponse(category) {
        const responses = ResponsePatterns[category];
        if (!responses || responses.length === 0) {
            return this.getFallbackResponse();
        }
        return responses[Math.floor(Math.random() * responses.length)];
    }

    /**
     * Get a random fallback response
     * @returns {string} - Random fallback response
     */
    getFallbackResponse() {
        const fallbacks = ResponsePatterns.fallbacks;
        return fallbacks[Math.floor(Math.random() * fallbacks.length)];
    }

    /**
     * Process user input and generate a response
     * @param {string} userInput - The user's message
     * @returns {Promise<string>} - The chatbot's response
     */
    async processMessage(userInput) {
        if (!userInput || userInput.trim() === '') {
            return "I didn't catch that. Could you type something? 🐝";
        }

        // Find matching category
        const category = this.findMatchingCategory(userInput);
        let response;

        if (category) {
            response = this.getRandomResponse(category);
        } else {
            // Log unrecognized query for learning
            await this.logUnrecognizedQuery(userInput);
            response = this.getFallbackResponse();
        }

        // Save both messages to history
        await this.saveMessage('user', userInput);
        await this.saveMessage('bot', response);

        return response;
    }

    /**
     * Get conversation history
     * @returns {Array} - Array of conversation messages
     */
    getHistory() {
        return this.conversationHistory;
    }
}

// Don't create global instance here - will be created in index.html
// const vobee = new VoBeeChatbot();

/**
 * UI Controller for the chatbot interface
 */
class ChatUI {
    constructor(chatbot) {
        this.chatbot = chatbot;
        this.chatMessages = null;
        this.userInput = null;
        this.sendButton = null;
        this.clearButton = null;
    }

    /**
     * Initialize the UI components
     */
    async init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
        }

        // Get DOM elements
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.clearButton = document.getElementById('clear-button');

        // Initialize chatbot
        await this.chatbot.init();

        // Set up event listeners
        this.setupEventListeners();

        // Load and display existing conversation history
        this.displayHistory();

        // Display welcome message if no history
        if (this.chatbot.getHistory().length === 0) {
            this.displayWelcomeMessage();
        }

        console.log('Chat UI initialized! 🐝');
    }

    /**
     * Set up event listeners for UI interactions
     */
    setupEventListeners() {
        // Send button click
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.handleSend());
        }

        // Enter key press
        if (this.userInput) {
            this.userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSend();
                }
            });
        }

        // Clear button click
        if (this.clearButton) {
            this.clearButton.addEventListener('click', () => this.handleClear());
        }
    }

    /**
     * Handle sending a message
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

        // Get and display bot response with a small delay for effect
        setTimeout(async () => {
            const response = await this.chatbot.processMessage(message);
            this.hideTypingIndicator();
            this.displayMessage('bot', response);
        }, 500 + Math.random() * 500);
    }

    /**
     * Handle clearing the chat history
     */
    async handleClear() {
        await this.chatbot.clearHistory();
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
        }
        this.displayWelcomeMessage();
    }

    /**
     * Display a message in the chat window
     * @param {string} sender - 'user' or 'bot'
     * @param {string} message - The message content
     */
    displayMessage(sender, message) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    /**
     * Display welcome message
     */
    displayWelcomeMessage() {
        const welcomeMessages = [
            "Hello! I'm VoBee, your friendly AI assistant! 🐝",
            "Feel free to ask me anything or just say hi!",
            "I'm here to help and have fun conversations with you!"
        ];

        welcomeMessages.forEach((msg, index) => {
            setTimeout(() => {
                this.displayMessage('bot', msg);
            }, index * 300);
        });
    }

    /**
     * Display conversation history
     */
    displayHistory() {
        const history = this.chatbot.getHistory();
        history.forEach(msg => {
            this.displayMessage(msg.sender, msg.message);
        });
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        if (!this.chatMessages) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;

        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    /**
     * Scroll chat to bottom
     */
    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }
}

// Don't auto-initialize - will be handled by enhanced-ui.js
// document.addEventListener('DOMContentLoaded', async () => {
//     const chatUI = new ChatUI(vobee);
//     await chatUI.init();
// });

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VoBeeChatbot, ChatUI };
}
