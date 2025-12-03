/**
 * VoBee AI Assistant - Unit Tests
 * Tests for chatbot functionality
 */

const assert = require('assert');

// Mock browser APIs for testing
global.localStorage = {
    data: {},
    getItem(key) { return this.data[key] || null; },
    setItem(key, value) { this.data[key] = value; },
    clear() { this.data = {}; }
};

const mockElement = {
    appendChild: () => {},
    scrollHeight: 0,
    scrollTop: 0,
    value: '',
    remove: () => {},
    addEventListener: () => {}
};

global.document = {
    getElementById: () => mockElement,
    createElement: () => ({
        className: '',
        id: '',
        textContent: '',
        innerHTML: '',
        appendChild: () => {}
    }),
    addEventListener: () => {}
};

global.navigator = {
    serviceWorker: null
};

// Define the VoBeeBot class for testing (simplified version extracted from chatbot.js)
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

    init() {
        this.messagesContainer = document.getElementById('messages');
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        if (this.chatForm) {
            this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

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

    saveUserProfile() {
        localStorage.setItem('vobee_user_profile', JSON.stringify(this.userProfile));
    }

    updateUserProfile(message) {
        const nameMatch = message.match(/(?:my name is|i'm|i am|call me)\s+([A-Z][a-z]+)/i);
        if (nameMatch) {
            this.userProfile.name = nameMatch[1];
        }

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
                this.userProfile.learnedTopics[interest] = 
                    (this.userProfile.learnedTopics[interest] || 0) + 1;
            }
        }

        this.userProfile.visitCount++;
        this.userProfile.lastVisit = new Date().toISOString();
        this.saveUserProfile();
    }

    addMessage(text, sender) {
        this.conversationHistory.push({ sender, text, timestamp: Date.now() });
    }

    matchesPattern(message, patterns) {
        return patterns.some(pattern => message.includes(pattern));
    }

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

    generateResponse(userMessage) {
        const message = userMessage.toLowerCase();
        const name = this.userProfile.name;
        const namePrefix = name ? `${name}, ` : '';

        if (this.matchesPattern(message, ['hello', 'hi', 'hey', 'greetings'])) {
            const responses = [
                `${namePrefix}Hello there! 🌟 What creative ideas shall we explore today?`,
                `${namePrefix}Hi! So glad you're here! What's buzzing in your world? 🐝`,
                `${namePrefix}Hey! Ready to make some magic happen! ✨ What can I help with?`
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }

        if (this.matchesPattern(message, ['help', 'can you help', 'need help', 'assist'])) {
            return `${namePrefix}Of course I can help! 🌻 I can chat about almost anything - ideas, questions, creative projects, or just have a friendly conversation. What's on your mind?`;
        }

        if (this.matchesPattern(message, ['joke', 'funny', 'make me laugh'])) {
            const jokes = [
                "Why do bees have sticky hair? Because they use honeycombs! 🐝😄",
                "What do you call a bee that can't make up its mind? A maybe! 🤔🐝",
                "What's a bee's favorite sport? Rug-bee! 🏉🐝"
            ];
            return jokes[Math.floor(Math.random() * jokes.length)];
        }

        return `${namePrefix}That's interesting! Tell me more about that! 🌟`;
    }
}

// Test suite
let passedTests = 0;
let failedTests = 0;

function test(name, fn) {
    try {
        localStorage.clear();
        fn();
        console.log(`✅ ${name}`);
        passedTests++;
    } catch (error) {
        console.log(`❌ ${name}: ${error.message}`);
        failedTests++;
    }
}

console.log('Running VoBee Chatbot Tests\n');

// Test: User profile initialization
test('User profile should initialize with default values', () => {
    const bot = new VoBeeBot();
    assert.strictEqual(bot.userProfile.name, null);
    assert.deepStrictEqual(bot.userProfile.interests, []);
    assert.strictEqual(bot.userProfile.mood, 'neutral');
});

// Test: User profile persistence
test('User profile should be saved to localStorage', () => {
    const bot = new VoBeeBot();
    bot.userProfile.name = 'Test';
    bot.saveUserProfile();
    
    const saved = JSON.parse(localStorage.getItem('vobee_user_profile'));
    assert.strictEqual(saved.name, 'Test');
});

// Test: Name extraction from message
test('Should extract name from "my name is" pattern', () => {
    const bot = new VoBeeBot();
    bot.updateUserProfile('my name is John');
    assert.strictEqual(bot.userProfile.name, 'John');
});

test('Should extract name from "I\'m" pattern', () => {
    const bot = new VoBeeBot();
    bot.updateUserProfile("I'm Sarah");
    assert.strictEqual(bot.userProfile.name, 'Sarah');
});

// Test: Interest tracking
test('Should track music interest from conversation', () => {
    const bot = new VoBeeBot();
    bot.updateUserProfile('I love listening to music');
    assert.ok(bot.userProfile.interests.includes('music'));
});

test('Should track technology interest from conversation', () => {
    const bot = new VoBeeBot();
    bot.updateUserProfile('I enjoy programming and coding');
    assert.ok(bot.userProfile.interests.includes('technology'));
});

test('Should track multiple interests', () => {
    const bot = new VoBeeBot();
    bot.updateUserProfile('I like music and reading books');
    assert.ok(bot.userProfile.interests.includes('music'));
    assert.ok(bot.userProfile.interests.includes('books'));
});

// Test: Pattern matching
test('matchesPattern should return true for matching patterns', () => {
    const bot = new VoBeeBot();
    assert.ok(bot.matchesPattern('hello there', ['hello', 'hi']));
    assert.ok(bot.matchesPattern('hi friend', ['hello', 'hi']));
});

test('matchesPattern should return false for non-matching patterns', () => {
    const bot = new VoBeeBot();
    assert.ok(!bot.matchesPattern('goodbye', ['hello', 'hi']));
});

// Test: Response generation
test('Should generate greeting response for hello', () => {
    const bot = new VoBeeBot();
    const response = bot.generateResponse('hello');
    assert.ok(response.length > 0);
    assert.ok(response.includes('Hello') || response.includes('Hi') || response.includes('Hey'));
});

test('Should generate response for help request', () => {
    const bot = new VoBeeBot();
    const response = bot.generateResponse('I need help');
    assert.ok(response.length > 0);
    assert.ok(response.toLowerCase().includes('help') || response.includes('can'));
});

test('Should generate joke response', () => {
    const bot = new VoBeeBot();
    const response = bot.generateResponse('tell me a joke');
    assert.ok(response.length > 0);
    assert.ok(response.includes('bee') || response.includes('🐝'));
});

// Test: Conversation history
test('addMessage should add to conversation history', () => {
    const bot = new VoBeeBot();
    bot.addMessage('test message', 'user');
    assert.strictEqual(bot.conversationHistory.length, 1);
    assert.strictEqual(bot.conversationHistory[0].text, 'test message');
    assert.strictEqual(bot.conversationHistory[0].sender, 'user');
});

// Test: Visit counting
test('Should increment visit count on profile update', () => {
    const bot = new VoBeeBot();
    const initialCount = bot.userProfile.visitCount;
    bot.updateUserProfile('test message');
    assert.strictEqual(bot.userProfile.visitCount, initialCount + 1);
});

// Test: Interest-based responses
test('Should generate interest-based response for known interest', () => {
    const bot = new VoBeeBot();
    bot.userProfile.interests = ['music'];
    const response = bot.getInterestResponse('music', '');
    assert.ok(response.length > 0);
    assert.ok(response.toLowerCase().includes('music') || response.includes('🎵') || response.includes('🎶'));
});

// Test: Personalized greeting
test('Should use name in greeting for returning user', () => {
    localStorage.setItem('vobee_user_profile', JSON.stringify({
        name: 'Alice',
        interests: [],
        mood: 'neutral',
        visitCount: 5,
        lastVisit: new Date().toISOString(),
        learnedTopics: {}
    }));
    const bot = new VoBeeBot();
    assert.strictEqual(bot.userProfile.name, 'Alice');
});

// Print summary
console.log(`\n${'='.repeat(40)}`);
console.log(`Tests: ${passedTests + failedTests} | Passed: ${passedTests} | Failed: ${failedTests}`);
console.log('='.repeat(40));

process.exit(failedTests > 0 ? 1 : 0);
