/**
 * VoBee AI Assistant - Creative Chatbot with Pseudo-Dynamic Learning
 * 
 * This chatbot implements pseudo-dynamic learning by:
 * 1. Storing conversation history
 * 2. Remembering user preferences and topics
 * 3. Adapting responses based on context
 * 4. Persisting learned data in localStorage
 */

class VoBeeBot {
    constructor() {
        this.conversationHistory = [];
        this.userProfile = this.loadUserProfile();
        this.greetings = [
            "Hello! I'm VoBee, your creative AI assistant! 🐝 How can I brighten your day?",
            "Bzzzz! Welcome! I'm VoBee, ready to help with whatever you need! 🌻",
            "Hey there! VoBee at your service! What creative adventure shall we embark on? ✨"
        ];
        this.init();
    }

    /**
     * Initialize the chatbot
     */
    init() {
        this.messagesContainer = document.getElementById('messages');
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');

        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Show welcome message
        this.showWelcomeMessage();
        
        // Register service worker
        this.registerServiceWorker();
    }

    /**
     * Load user profile from localStorage
     */
    loadUserProfile() {
        const saved = localStorage.getItem('vobee_user_profile');
        return saved ? JSON.parse(saved) : {
            name: null,
            interests: [],
            mood: 'neutral',
            visitCount: 0,
            lastVisit: null,
            learnedTopics: {}
        };
    }

    /**
     * Save user profile to localStorage
     */
    saveUserProfile() {
        localStorage.setItem('vobee_user_profile', JSON.stringify(this.userProfile));
    }

    /**
     * Update user profile based on conversation
     */
    updateUserProfile(message) {
        // Extract potential name
        const nameMatch = message.match(/(?:my name is|i'm|i am|call me)\s+([A-Z][a-z]+)/i);
        if (nameMatch) {
            this.userProfile.name = nameMatch[1];
        }

        // Track interests based on keywords
        const interestKeywords = {
            'music': ['music', 'song', 'artist', 'band', 'playlist'],
            'technology': ['tech', 'computer', 'programming', 'code', 'software'],
            'art': ['art', 'paint', 'draw', 'design', 'creative'],
            'travel': ['travel', 'trip', 'vacation', 'country', 'city'],
            'food': ['food', 'cook', 'recipe', 'restaurant', 'eat'],
            'sports': ['sport', 'game', 'team', 'play', 'exercise'],
            'movies': ['movie', 'film', 'watch', 'cinema', 'series'],
            'books': ['book', 'read', 'author', 'novel', 'story']
        };

        const lowerMessage = message.toLowerCase();
        for (const [interest, keywords] of Object.entries(interestKeywords)) {
            if (keywords.some(keyword => lowerMessage.includes(keyword))) {
                if (!this.userProfile.interests.includes(interest)) {
                    this.userProfile.interests.push(interest);
                }
                // Track topic frequency
                this.userProfile.learnedTopics[interest] = 
                    (this.userProfile.learnedTopics[interest] || 0) + 1;
            }
        }

        // Update visit tracking
        this.userProfile.visitCount++;
        this.userProfile.lastVisit = new Date().toISOString();

        this.saveUserProfile();
    }

    /**
     * Show welcome message with personalization
     */
    showWelcomeMessage() {
        let greeting;
        
        if (this.userProfile.name) {
            greeting = `Welcome back, ${this.userProfile.name}! 🐝 Great to see you again! What can I help you with today?`;
        } else if (this.userProfile.visitCount > 0) {
            greeting = "Welcome back! 🐝 I've been buzzing around waiting for you! What's on your mind?";
        } else {
            greeting = this.greetings[Math.floor(Math.random() * this.greetings.length)];
        }

        // Add interest-based follow-up
        if (this.userProfile.interests.length > 0) {
            const topInterest = Object.entries(this.userProfile.learnedTopics)
                .sort((a, b) => b[1] - a[1])[0];
            if (topInterest) {
                greeting += ` I remember you love ${topInterest[0]}! Want to chat about that?`;
            }
        }

        this.addMessage(greeting, 'bot');
    }

    /**
     * Handle form submission
     */
    handleSubmit(event) {
        event.preventDefault();
        const message = this.userInput.value.trim();
        
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        this.userInput.value = '';

        // Update profile with message content
        this.updateUserProfile(message);

        // Show typing indicator and generate response
        this.showTypingIndicator();
        
        setTimeout(() => {
            this.hideTypingIndicator();
            const response = this.generateResponse(message);
            this.addMessage(response, 'bot');
        }, 800 + Math.random() * 1200);
    }

    /**
     * Add message to chat
     */
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'bot' ? '🐝' : '👤';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = text;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Save to conversation history
        this.conversationHistory.push({ sender, text, timestamp: Date.now() });
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message bot';
        indicator.id = 'typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '🐝';
        
        const typing = document.createElement('div');
        typing.className = 'message-content typing-indicator';
        typing.innerHTML = '<span></span><span></span><span></span>';
        
        indicator.appendChild(avatar);
        indicator.appendChild(typing);
        
        this.messagesContainer.appendChild(indicator);
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
     * Scroll to bottom of chat
     */
    scrollToBottom() {
        const container = document.getElementById('chat-container');
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Generate contextual response with pseudo-dynamic learning
     */
    generateResponse(userMessage) {
        const message = userMessage.toLowerCase();
        const name = this.userProfile.name;
        const namePrefix = name ? `${name}, ` : '';

        // Greeting responses
        if (this.matchesPattern(message, ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'])) {
            const responses = [
                `${namePrefix}Hello there! 🌟 What creative ideas shall we explore today?`,
                `${namePrefix}Hi! So glad you're here! What's buzzing in your world? 🐝`,
                `${namePrefix}Hey! Ready to make some magic happen! ✨ What can I help with?`
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }

        // Asking about the bot
        if (this.matchesPattern(message, ['who are you', 'what are you', 'your name', 'about you'])) {
            return `I'm VoBee, your creative AI assistant! 🐝 I love helping people with ideas, answering questions, and having fun conversations. The more we chat, the better I understand what you like!`;
        }

        // Asking how the bot is
        if (this.matchesPattern(message, ['how are you', "how's it going", 'how do you feel'])) {
            return `I'm buzzing with energy! 🐝✨ Being a helpful bee makes me happy. Thanks for asking! How are YOU doing?`;
        }

        // Help requests
        if (this.matchesPattern(message, ['help', 'can you help', 'need help', 'assist'])) {
            return `${namePrefix}Of course I can help! 🌻 I can chat about almost anything - ideas, questions, creative projects, or just have a friendly conversation. What's on your mind?`;
        }

        // Jokes and fun
        if (this.matchesPattern(message, ['joke', 'funny', 'make me laugh', 'tell me something funny'])) {
            const jokes = [
                "Why do bees have sticky hair? Because they use honeycombs! 🐝😄",
                "What do you call a bee that can't make up its mind? A maybe! 🤔🐝",
                "What's a bee's favorite sport? Rug-bee! 🏉🐝",
                "Why did the bee get married? Because he found his honey! 💕🐝"
            ];
            return jokes[Math.floor(Math.random() * jokes.length)];
        }

        // Gratitude
        if (this.matchesPattern(message, ['thank', 'thanks', 'appreciate', 'grateful'])) {
            const responses = [
                `${namePrefix}You're so welcome! It makes me happy to help! 🌟`,
                `Aww, thank YOU for being so kind! 💛 Is there anything else I can do?`,
                `My pleasure! That's what I'm here for! 🐝✨`
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }

        // Farewell
        if (this.matchesPattern(message, ['bye', 'goodbye', 'see you', 'later', 'gotta go'])) {
            return `${namePrefix}Take care! 🌸 Come back anytime you want to chat. I'll be here buzzing around! 🐝`;
        }

        // Interest-based responses
        if (this.userProfile.interests.length > 0) {
            for (const interest of this.userProfile.interests) {
                if (message.includes(interest)) {
                    return this.getInterestResponse(interest, namePrefix);
                }
            }
        }

        // Creative prompt responses
        if (this.matchesPattern(message, ['idea', 'creative', 'inspire', 'suggestion'])) {
            const ideas = [
                `${namePrefix}Here's an idea: Start a gratitude journal and write three things you're thankful for each day! 📔✨`,
                `How about creating a mood board for your next project? Collect images, colors, and textures that inspire you! 🎨`,
                `${namePrefix}Try the "5 whys" technique - ask "why" five times to get to the root of any problem or idea! 🤔`,
                `What if you combined two of your interests in an unexpected way? That's where innovation happens! 💡`
            ];
            return ideas[Math.floor(Math.random() * ideas.length)];
        }

        // Question detection
        if (message.includes('?') || this.matchesPattern(message, ['what', 'how', 'why', 'when', 'where', 'who', 'which'])) {
            return this.getThoughtfulResponse(message, namePrefix);
        }

        // Default conversational responses
        const defaults = [
            `${namePrefix}That's interesting! Tell me more about that! 🌟`,
            `I love hearing about that! What else would you like to share? 🐝`,
            `${namePrefix}Hmm, that's got me thinking! What made you interested in this? 🤔`,
            `That's really cool! I'm always learning new things from our chats! 📚✨`,
            `${namePrefix}Fascinating! Is there something specific you'd like to explore together? 🌻`
        ];
        
        return defaults[Math.floor(Math.random() * defaults.length)];
    }

    /**
     * Check if message matches any pattern
     */
    matchesPattern(message, patterns) {
        return patterns.some(pattern => message.includes(pattern));
    }

    /**
     * Get response based on user's interests
     */
    getInterestResponse(interest, namePrefix) {
        const interestResponses = {
            music: [
                `${namePrefix}Music is such a powerful form of expression! 🎵 What kind of music moves your soul?`,
                `I love that you're into music! Are you listening to anything new lately? 🎶`,
                `Music can change our whole mood, can't it? What's your go-to playlist? 🎧`
            ],
            technology: [
                `${namePrefix}Tech is always evolving! What aspect of technology fascinates you most? 💻`,
                `Being interested in tech is awesome! Are you building anything cool? 🚀`,
                `Technology shapes our world in so many ways! What tech topics interest you? ⚡`
            ],
            art: [
                `${namePrefix}Art is such a beautiful way to express yourself! 🎨 Do you create art?`,
                `I love creativity! What kind of art inspires you the most? ✨`,
                `Art connects us all in unique ways! What's your favorite art form? 🖌️`
            ],
            travel: [
                `${namePrefix}Travel opens our minds to new perspectives! ✈️ Where do you dream of going?`,
                `Adventure is calling! What's the most memorable place you've visited? 🌍`,
                `I love hearing about travel stories! Any trips planned? 🗺️`
            ],
            food: [
                `${namePrefix}Food is such a wonderful part of life! 🍳 Do you enjoy cooking?`,
                `Yum! I love talking about food! What's your favorite cuisine? 🍜`,
                `Food brings people together! Any dishes you'd recommend? 🥗`
            ],
            sports: [
                `${namePrefix}Sports are so energizing! 🏃 What sports do you enjoy?`,
                `I love the teamwork and excitement of sports! Do you play or watch? ⚽`,
                `Staying active is great! What's your favorite way to exercise? 💪`
            ],
            movies: [
                `${namePrefix}Movies transport us to different worlds! 🎬 What genres do you love?`,
                `I could talk about films all day! Seen anything good recently? 🎥`,
                `Cinema is magical! What movie would you recommend? 🍿`
            ],
            books: [
                `${namePrefix}Books are windows to endless knowledge and stories! 📚 What are you reading?`,
                `I love that you enjoy reading! Fiction or non-fiction? 📖`,
                `Books shape who we are! Any favorites you'd recommend? ✨`
            ]
        };

        const responses = interestResponses[interest] || [];
        return responses.length > 0 
            ? responses[Math.floor(Math.random() * responses.length)]
            : `${namePrefix}That's a topic I'd love to learn more about! Tell me more! 🐝`;
    }

    /**
     * Generate thoughtful response to questions
     */
    getThoughtfulResponse(message, namePrefix) {
        const responses = [
            `${namePrefix}That's a great question! Let me think... 🤔 Based on what I know, I'd say the key is to approach it with curiosity and openness!`,
            `Interesting question! 💭 I think it depends on your perspective, but I'd love to hear your thoughts on it!`,
            `${namePrefix}You've got me thinking! While I might not have all the answers, exploring questions together is part of the fun! 🌟`,
            `Great minds ask great questions! 🧠 What's your intuition telling you about this?`,
            `${namePrefix}I love curious minds! Let's explore this together - what aspects interest you most? 🔍`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    /**
     * Register service worker for PWA functionality
     */
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/sw.js');
                console.log('Service Worker registered successfully:', registration.scope);
            } catch (error) {
                console.log('Service Worker registration failed:', error);
            }
        }
    }
}

// Initialize the chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.vobeeBot = new VoBeeBot();
});
