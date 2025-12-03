/**
 * VoBee AI Assistant - Chatbot Engine
 * Message processing and pattern matching
 */

class VoBeeChatbot {
    constructor() {
        this.kb = KnowledgeBase;
        this.conversationHistory = [];
    }

    /**
     * Process user message and generate response
     * @param {string} message - User input message
     * @returns {string} Bot response
     */
    processMessage(message) {
        const normalizedMessage = this.normalizeText(message);
        
        // Check for greetings
        if (this.matchPatterns(normalizedMessage, this.kb.greetings.patterns)) {
            return this.getRandomResponse(this.kb.greetings.responses);
        }

        // Check for farewells
        if (this.matchPatterns(normalizedMessage, this.kb.farewells.patterns)) {
            return this.getRandomResponse(this.kb.farewells.responses);
        }

        // Check for thanks
        if (this.matchPatterns(normalizedMessage, this.kb.thanks.patterns)) {
            return this.getRandomResponse(this.kb.thanks.responses);
        }

        // Search in knowledge base topics
        const response = this.searchKnowledgeBase(normalizedMessage);
        if (response) {
            return response;
        }

        // Default response
        return this.getRandomResponse(this.kb.defaults);
    }

    /**
     * Normalize text for matching
     * @param {string} text - Input text
     * @returns {string} Normalized text
     */
    normalizeText(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Remove diacritics for matching
            .replace(/[^\w\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    /**
     * Check if message matches any patterns
     * @param {string} message - Normalized message
     * @param {string[]} patterns - Patterns to match
     * @returns {boolean} Match found
     */
    matchPatterns(message, patterns) {
        const normalizedPatterns = patterns.map(p => this.normalizeText(p));
        return normalizedPatterns.some(pattern => {
            const words = message.split(' ');
            return words.some(word => word.includes(pattern) || pattern.includes(word));
        });
    }

    /**
     * Search knowledge base for relevant answer
     * @param {string} message - Normalized message
     * @returns {string|null} Answer or null
     */
    searchKnowledgeBase(message) {
        const categories = ['crypto', 'stocks', 'etf', 'literacy', 'insolvency', 'savings'];
        let bestMatch = null;
        let bestScore = 0;

        for (const category of categories) {
            const categoryData = this.kb[category];
            
            // Check category keywords first
            const keywordMatch = categoryData.keywords.some(keyword => 
                message.includes(this.normalizeText(keyword))
            );

            if (keywordMatch) {
                // Search within category topics
                for (const [topicKey, topicData] of Object.entries(categoryData.topics)) {
                    const score = this.calculateMatchScore(message, topicData.question);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMatch = topicData.answer;
                    }
                }
            }
        }

        // Also search all topics regardless of keyword match
        if (!bestMatch || bestScore < 0.3) {
            for (const category of categories) {
                for (const [topicKey, topicData] of Object.entries(this.kb[category].topics)) {
                    const score = this.calculateMatchScore(message, topicData.question);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMatch = topicData.answer;
                    }
                }
            }
        }

        return bestScore > 0.2 ? bestMatch : null;
    }

    /**
     * Calculate match score between message and question patterns
     * @param {string} message - Normalized user message
     * @param {string[]} questions - Question patterns
     * @returns {number} Match score 0-1
     */
    calculateMatchScore(message, questions) {
        const messageWords = message.split(' ').filter(w => w.length > 2);
        let maxScore = 0;

        for (const question of questions) {
            const questionNormalized = this.normalizeText(question);
            const questionWords = questionNormalized.split(' ').filter(w => w.length > 2);

            // Exact match
            if (message === questionNormalized) {
                return 1;
            }

            // Contains full question
            if (message.includes(questionNormalized)) {
                maxScore = Math.max(maxScore, 0.9);
                continue;
            }

            // Word overlap score
            let matchedWords = 0;
            for (const qWord of questionWords) {
                if (messageWords.some(mWord => 
                    mWord.includes(qWord) || qWord.includes(mWord)
                )) {
                    matchedWords++;
                }
            }

            const score = questionWords.length > 0 
                ? matchedWords / questionWords.length 
                : 0;
            maxScore = Math.max(maxScore, score);
        }

        return maxScore;
    }

    /**
     * Get random response from array
     * @param {string[]} responses - Response options
     * @returns {string} Random response
     */
    getRandomResponse(responses) {
        const index = Math.floor(Math.random() * responses.length);
        return responses[index];
    }

    /**
     * Get quick topic introduction
     * @param {string} topic - Topic identifier
     * @returns {string} Topic introduction
     */
    getTopicIntro(topic) {
        const intros = {
            crypto: 'Zajímá vás svět kryptoměn? 🔐 Zeptejte se na Bitcoin, Ethereum, peněženky nebo jak začít investovat.',
            stocks: 'Chcete se dozvědět o akciích? 📈 Mohu vysvětlit základy, dividendy, P/E ratio nebo jak začít obchodovat.',
            etf: 'ETF fondy jsou skvělý způsob diverzifikace. 📊 Zeptejte se, co je ETF, jak vybrat, nebo jaké jsou náklady.',
            literacy: 'Finanční gramotnost je základ. 📚 Pomohu s rozpočtem, nouzovým fondem nebo pochopením inflace.',
            insolvency: 'Máte dotazy ohledně dluhů? ⚖️ Vysvětlím insolvenci, oddlužení nebo jak funguje exekuce.',
            savings: 'Chcete šetřit chytřeji? 💰 Poradím s metodami spoření, stavebním spořením nebo penzijním připojištěním.'
        };
        return intros[topic] || 'Jak vám mohu pomoci?';
    }

    /**
     * Add message to conversation history
     * @param {string} role - 'user' or 'bot'
     * @param {string} content - Message content
     */
    addToHistory(role, content) {
        this.conversationHistory.push({
            role,
            content,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Clear conversation history
     */
    clearHistory() {
        this.conversationHistory = [];
    }

    /**
     * Get conversation history
     * @returns {Array} Conversation history
     */
    getHistory() {
        return this.conversationHistory;
    }
}

// Create global instance
const chatbot = new VoBeeChatbot();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoBeeChatbot;
}
