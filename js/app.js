// VoBee AI Assistant - Main Application
// Hlavní aplikační logika

// Inicializace chatbota
const chatbot = new VoBeeChatbot();

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const topicButtons = document.querySelectorAll('.topic-btn');
const installBtn = document.getElementById('installBtn');
const offlineIndicator = document.getElementById('offlineIndicator');

// PWA Install prompt
let deferredPrompt;

// Registrace Service Workeru
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js');
            console.log('VoBee: Service Worker registrován', registration.scope);
        } catch (error) {
            console.error('VoBee: Service Worker registrace selhala', error);
        }
    });
}

// PWA Install event
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.classList.remove('hidden');
});

// Install button click
installBtn.addEventListener('click', async () => {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log('VoBee: Instalace:', outcome);
        deferredPrompt = null;
        installBtn.classList.add('hidden');
    }
});

// Installed event
window.addEventListener('appinstalled', () => {
    console.log('VoBee: Aplikace nainstalována');
    installBtn.classList.add('hidden');
    addMessage('bot', 'Děkuji za instalaci VoBee! 🐝 Aplikace je nyní dostupná na vaší ploše.');
});

// Online/Offline detection
window.addEventListener('online', () => {
    offlineIndicator.classList.add('hidden');
    console.log('VoBee: Online');
});

window.addEventListener('offline', () => {
    offlineIndicator.classList.remove('hidden');
    console.log('VoBee: Offline');
});

// Check initial online status
if (!navigator.onLine) {
    offlineIndicator.classList.remove('hidden');
}

// Topic selection
topicButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        topicButtons.forEach(btn => btn.classList.remove('active'));
        // Add active class to clicked button
        button.classList.add('active');
        
        // Set topic in chatbot
        const topic = button.dataset.topic;
        const welcomeMessage = chatbot.setTopic(topic);
        
        // Add topic change message
        addMessage('bot', welcomeMessage);
        
        // Scroll to bottom
        scrollToBottom();
    });
});

// Form submission
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Clear input
    messageInput.value = '';
    
    // Add user message
    addMessage('user', message);
    
    // Show typing indicator
    showTypingIndicator();
    
    // Process message with delay for natural feel
    setTimeout(() => {
        hideTypingIndicator();
        
        const response = chatbot.processMessage(message);
        addMessage('bot', response.text, response.quickReplies);
        
        scrollToBottom();
    }, 500 + Math.random() * 500);
});

// Add message to chat
function addMessage(role, text, quickReplies = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'bot' ? '🐝' : '👤';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Parse text and convert newlines to paragraphs
    const paragraphs = text.split('\n\n');
    paragraphs.forEach(para => {
        if (para.trim()) {
            const p = document.createElement('p');
            // Convert single newlines to <br> and basic markdown
            p.innerHTML = formatMessage(para);
            content.appendChild(p);
        }
    });
    
    // Add quick replies if provided
    if (quickReplies && quickReplies.length > 0) {
        const quickRepliesDiv = document.createElement('div');
        quickRepliesDiv.className = 'quick-replies';
        
        quickReplies.forEach(reply => {
            const btn = document.createElement('button');
            btn.className = 'quick-reply-btn';
            btn.textContent = reply;
            btn.addEventListener('click', () => {
                messageInput.value = reply;
                chatForm.dispatchEvent(new Event('submit'));
            });
            quickRepliesDiv.appendChild(btn);
        });
        
        content.appendChild(quickRepliesDiv);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

// Format message with basic markdown
function formatMessage(text) {
    return text
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Line breaks
        .replace(/\n/g, '<br>')
        // Lists (• or -)
        .replace(/^[•\-]\s*/gm, '• ')
        // Numbered lists
        .replace(/^(\d+[\.\)]\s*)/gm, '<strong>$1</strong>');
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🐝';
    
    const indicator = document.createElement('div');
    indicator.className = 'message-content typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);
    
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Focus input on load
messageInput.focus();

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Focus input on any key press if not already focused
    if (document.activeElement !== messageInput && !e.ctrlKey && !e.altKey && !e.metaKey) {
        if (e.key.length === 1) {
            messageInput.focus();
        }
    }
});

// Save state before page unload
window.addEventListener('beforeunload', () => {
    chatbot.saveHistory();
});

// Log initialization
console.log('VoBee AI Assistant inicializován 🐝');
console.log('Stats:', chatbot.getStats());
