/**
 * VoBee AI Assistant - Main Application
 * PWA handlers and UI logic
 */

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const quickReplies = document.getElementById('quickReplies');
const clearHistoryBtn = document.getElementById('clearHistory');

// Storage key for conversation history
const STORAGE_KEY = 'vobee_chat_history';

/**
 * Initialize the application
 */
function init() {
    registerServiceWorker();
    loadConversationHistory();
    setupEventListeners();
    showWelcomeMessage();
    setupInstallPrompt();
}

/**
 * Register Service Worker for PWA
 */
async function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js');
            console.log('Service Worker registered:', registration.scope);
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    }
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Form submission
    chatForm.addEventListener('submit', handleSubmit);

    // Menu toggle
    menuBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Topic buttons
    document.querySelectorAll('.topic-btn').forEach(btn => {
        btn.addEventListener('click', handleTopicClick);
    });

    // Quick reply buttons
    document.querySelectorAll('.quick-reply-btn').forEach(btn => {
        btn.addEventListener('click', handleQuickReply);
    });

    // Clear history
    clearHistoryBtn.addEventListener('click', handleClearHistory);

    // Keyboard shortcut for input focus
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== chatInput) {
            e.preventDefault();
            chatInput.focus();
        }
    });
}

/**
 * Handle form submission
 * @param {Event} e - Submit event
 */
function handleSubmit(e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    // Process and respond after delay
    setTimeout(() => {
        hideTypingIndicator();
        const response = chatbot.processMessage(message);
        addMessage(response, 'bot');
        saveConversationHistory();
    }, 500 + Math.random() * 1000);
}

/**
 * Add message to chat
 * @param {string} content - Message content
 * @param {string} type - 'user' or 'bot'
 */
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const avatar = type === 'user' ? '👤' : '🐝';
    const time = new Date().toLocaleTimeString('cs-CZ', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });

    // Parse markdown-like formatting
    const formattedContent = formatMessage(content);

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            ${formattedContent}
            <div class="message-time">${time}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();

    // Add to chatbot history
    chatbot.addToHistory(type, content);
}

/**
 * Format message with markdown-like syntax
 * @param {string} text - Raw text
 * @returns {string} Formatted HTML
 */
function formatMessage(text) {
    return text
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Lists
        .replace(/^• /gm, '<br>• ')
        // Numbered items
        .replace(/^(\d️⃣|\d\.|📌)/gm, '<br>$1')
        // Line breaks
        .replace(/\n/g, '<br>')
        // Links
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
        // Tables (simple)
        .replace(/\|/g, ' | ');
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🐝</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Toggle sidebar visibility
 */
function toggleSidebar() {
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    menuBtn.classList.toggle('active');
}

/**
 * Close sidebar
 */
function closeSidebar() {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    menuBtn.classList.remove('active');
}

/**
 * Handle topic button click
 * @param {Event} e - Click event
 */
function handleTopicClick(e) {
    const topic = e.currentTarget.dataset.topic;
    
    // Update active state
    document.querySelectorAll('.topic-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    // Get topic intro
    const intro = chatbot.getTopicIntro(topic);
    
    // Add as user selection and bot response
    addMessage(`Chci se dozvědět více o: ${e.currentTarget.textContent.trim()}`, 'user');
    
    setTimeout(() => {
        addMessage(intro, 'bot');
        updateQuickReplies(topic);
        saveConversationHistory();
    }, 300);

    closeSidebar();
}

/**
 * Update quick replies based on topic
 * @param {string} topic - Current topic
 */
function updateQuickReplies(topic) {
    const replies = {
        crypto: ['Co je Bitcoin?', 'Jak funguje Ethereum?', 'Jakou peněženku použít?', 'Jak investovat do krypta?'],
        stocks: ['Co jsou akcie?', 'Jak začít s akciemi?', 'Co jsou dividendy?', 'Co je P/E ratio?'],
        etf: ['Co je ETF?', 'Jak vybrat ETF?', 'Co je TER?', 'Nejlepší ETF pro začátečníky'],
        literacy: ['Jak sestavit rozpočet?', 'Co je inflace?', 'Kolik mít v nouzovém fondu?', 'Pravidlo 50/30/20'],
        insolvency: ['Co je insolvence?', 'Jak funguje oddlužení?', 'Co může exekutor zabavit?', 'Jak zastavit exekuci?'],
        savings: ['Jak šetřit peníze?', 'Kam uložit peníze?', 'Stavební spoření', 'Penzijní spoření']
    };

    const topicReplies = replies[topic] || replies.literacy;
    quickReplies.innerHTML = topicReplies
        .map(reply => `<button class="quick-reply-btn" data-message="${reply}">${reply}</button>`)
        .join('');

    // Re-attach event listeners
    document.querySelectorAll('.quick-reply-btn').forEach(btn => {
        btn.addEventListener('click', handleQuickReply);
    });
}

/**
 * Handle quick reply click
 * @param {Event} e - Click event
 */
function handleQuickReply(e) {
    const message = e.currentTarget.dataset.message;
    chatInput.value = message;
    handleSubmit(new Event('submit'));
}

/**
 * Handle clear history button
 */
function handleClearHistory() {
    if (confirm('Opravdu chcete vymazat historii konverzace?')) {
        chatMessages.innerHTML = '';
        chatbot.clearHistory();
        localStorage.removeItem(STORAGE_KEY);
        showWelcomeMessage();
        closeSidebar();
    }
}

/**
 * Show welcome message
 */
function showWelcomeMessage() {
    if (chatMessages.children.length === 0) {
        const welcomeContent = `Ahoj! 🐝 Jsem **VoBee**, váš osobní finanční asistent.

Mohu vám pomoci s tématy jako:
• Kryptoměny (Bitcoin, Ethereum, peněženky)
• Akcie a investování
• ETF fondy
• Finanční gramotnost a rozpočtování
• Insolvence a oddlužení
• Šetření a spoření

Zeptejte se mě na cokoliv nebo vyberte téma z menu!`;
        
        addMessage(welcomeContent, 'bot');
    }
}

/**
 * Save conversation history to localStorage
 */
function saveConversationHistory() {
    const history = chatbot.getHistory();
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch (e) {
        console.warn('Could not save conversation history:', e);
    }
}

/**
 * Load conversation history from localStorage
 */
function loadConversationHistory() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            const history = JSON.parse(saved);
            history.forEach(msg => {
                addMessage(msg.content, msg.role);
            });
        }
    } catch (e) {
        console.warn('Could not load conversation history:', e);
    }
}

/**
 * Setup PWA install prompt
 */
let deferredPrompt;

function setupInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        showInstallPrompt();
    });

    window.addEventListener('appinstalled', () => {
        hideInstallPrompt();
        console.log('PWA installed');
    });
}

/**
 * Show install prompt
 */
function showInstallPrompt() {
    // Check if already installed or prompt dismissed
    if (localStorage.getItem('installPromptDismissed')) return;

    const promptHTML = `
        <div class="install-prompt show" id="installPrompt">
            <span>🐝</span>
            <div class="install-prompt-text">
                <h3>Nainstalovat VoBee AI</h3>
                <p>Přidejte aplikaci na plochu pro rychlý přístup</p>
            </div>
            <button class="install-btn" id="installBtn">Nainstalovat</button>
            <button class="install-dismiss" id="dismissInstall">×</button>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', promptHTML);

    document.getElementById('installBtn').addEventListener('click', async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const result = await deferredPrompt.userChoice;
            console.log('Install prompt result:', result);
            deferredPrompt = null;
        }
        hideInstallPrompt();
    });

    document.getElementById('dismissInstall').addEventListener('click', () => {
        localStorage.setItem('installPromptDismissed', 'true');
        hideInstallPrompt();
    });
}

/**
 * Hide install prompt
 */
function hideInstallPrompt() {
    const prompt = document.getElementById('installPrompt');
    if (prompt) {
        prompt.remove();
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
