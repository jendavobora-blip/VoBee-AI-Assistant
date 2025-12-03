// VoBee AI Assistant - Chatbot Logic
// Logika chatbota v češtině

class VoBeeChatbot {
    constructor() {
        this.currentTopic = 'general';
        this.conversationHistory = this.loadHistory();
        this.userName = localStorage.getItem('vobee_userName') || null;
    }

    // Načtení historie konverzace z localStorage
    loadHistory() {
        try {
            const history = localStorage.getItem('vobee_history');
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Chyba při načítání historie:', error);
            return [];
        }
    }

    // Uložení historie konverzace do localStorage
    saveHistory() {
        try {
            // Uchovat max 100 zpráv
            const historyToSave = this.conversationHistory.slice(-100);
            localStorage.setItem('vobee_history', JSON.stringify(historyToSave));
        } catch (error) {
            console.error('Chyba při ukládání historie:', error);
        }
    }

    // Vyčištění historie
    clearHistory() {
        this.conversationHistory = [];
        localStorage.removeItem('vobee_history');
    }

    // Nastavení aktuálního tématu
    setTopic(topic) {
        this.currentTopic = topic;
        return this.getTopicWelcome(topic);
    }

    // Uvítací zpráva pro téma
    getTopicWelcome(topic) {
        const welcomes = {
            general: "Jsem připraven odpovídat na všechny vaše finanční dotazy. 🐝",
            crypto: "Téma: Kryptoměny 💰 Zeptejte se mě na Bitcoin, Ethereum, peněženky nebo jak nakupovat krypto!",
            stocks: "Téma: Akcie 📈 Mohu vám poradit s investováním do akcií, výběrem brokera nebo dividendami.",
            etf: "Téma: ETF fondy 📊 Pomohu vám pochopit ETF, vybrat vhodný fond nebo vysvětlit rozdíly.",
            literacy: "Téma: Finanční gramotnost 📚 Naučím vás základy osobních financí, rozpočtu a složeného úročení.",
            insolvency: "Téma: Insolvence ⚖️ Pomohu vám porozumět oddlužení, procesu insolvence a prevenci dluhů.",
            savings: "Téma: Šetření 💵 Poradím vám jak efektivně šetřit, stavební spoření nebo penzijko."
        };
        return welcomes[topic] || welcomes.general;
    }

    // Hlavní metoda pro zpracování zprávy
    processMessage(userMessage) {
        // Uložení zprávy uživatele
        this.addToHistory('user', userMessage);

        // Normalizace zprávy pro porovnání
        const normalizedMessage = this.normalizeText(userMessage);

        // Kontrola speciálních příkazů
        const specialResponse = this.checkSpecialCommands(normalizedMessage);
        if (specialResponse) {
            this.addToHistory('bot', specialResponse.text);
            return specialResponse;
        }

        // Hledání odpovědi v knowledge base
        let response = this.findAnswer(normalizedMessage);

        // Přidání quick replies pokud existují
        const quickReplies = this.getQuickReplies(normalizedMessage, response);

        // Uložení odpovědi bota
        this.addToHistory('bot', response);

        return {
            text: response,
            quickReplies: quickReplies
        };
    }

    // Normalizace textu pro porovnání
    normalizeText(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Odstranění diakritiky
            .replace(/[^\w\s]/g, '') // Odstranění speciálních znaků
            .trim();
    }

    // Kontrola speciálních příkazů
    checkSpecialCommands(message) {
        // Pozdravy
        if (this.matchesAny(message, ['ahoj', 'cau', 'nazdar', 'dobry den', 'zdravim', 'hey', 'hi', 'hello'])) {
            const greetings = KnowledgeBase.general.greeting;
            return { text: greetings[Math.floor(Math.random() * greetings.length)] };
        }

        // Rozloučení
        if (this.matchesAny(message, ['nashledanou', 'na shledanou', 'cau', 'bye', 'papa', 'ahoj', 'sbohem'])) {
            const farewellPatterns = ['nashle', 'shle', 'bye', 'papa', 'sbohem'];
            if (farewellPatterns.some(pattern => message.includes(pattern))) {
                const farewells = KnowledgeBase.general.farewell;
                return { text: farewells[Math.floor(Math.random() * farewells.length)] };
            }
        }

        // Poděkování
        if (this.matchesAny(message, ['dekuji', 'dekuju', 'diky', 'dik', 'thanks', 'thank you'])) {
            const thanks = KnowledgeBase.general.thanks;
            return { text: thanks[Math.floor(Math.random() * thanks.length)] };
        }

        // Vymazání historie
        if (this.matchesAny(message, ['vymaz historii', 'smazat historii', 'clear history', 'reset'])) {
            this.clearHistory();
            return { text: "Historie konverzace byla vymazána. 🗑️ Jak vám mohu pomoci?" };
        }

        // Nápověda
        if (this.matchesAny(message, ['napoveda', 'help', 'pomoc', 'jak funguje', 'co umi'])) {
            return { 
                text: "Jsem VoBee, váš finanční asistent! 🐝\n\nMohu vám pomoci s:\n• 💰 Kryptoměnami (Bitcoin, Ethereum...)\n• 📈 Akciemi a investováním\n• 📊 ETF fondy\n• 📚 Finanční gramotností\n• ⚖️ Insolvencí a dluhy\n• 💵 Šetřením a spořením\n\nVyberte téma nahoře nebo se mě prostě zeptejte!",
                quickReplies: ["Co je Bitcoin?", "Jak šetřit?", "Co jsou ETF?"]
            };
        }

        return null;
    }

    // Hledání odpovědi v knowledge base
    findAnswer(normalizedMessage) {
        // Nejprve hledáme v aktuálním tématu
        let answer = this.searchInTopic(normalizedMessage, this.currentTopic);
        
        // Pokud nenalezeno, hledáme ve všech tématech
        if (!answer) {
            const topics = ['crypto', 'stocks', 'etf', 'literacy', 'insolvency', 'savings'];
            for (const topic of topics) {
                answer = this.searchInTopic(normalizedMessage, topic);
                if (answer) break;
            }
        }

        // Pokud stále nenalezeno, vrátíme default odpověď
        if (!answer) {
            const unknowns = KnowledgeBase.general.unknown;
            answer = unknowns[Math.floor(Math.random() * unknowns.length)];
        }

        return answer;
    }

    // Hledání v konkrétním tématu
    searchInTopic(normalizedMessage, topic) {
        const topicData = KnowledgeBase[topic];
        if (!topicData) return null;

        let bestMatch = null;
        let bestScore = 0;

        for (const key in topicData) {
            const item = topicData[key];
            if (item.question && item.answer) {
                const score = this.calculateMatchScore(normalizedMessage, item.question);
                if (score > bestScore && score >= 0.5) {
                    bestScore = score;
                    bestMatch = item.answer;
                }
            }
        }

        return bestMatch;
    }

    // Výpočet skóre shody
    calculateMatchScore(userMessage, questions) {
        const userWords = userMessage.split(/\s+/);
        let maxScore = 0;

        for (const question of questions) {
            const normalizedQuestion = this.normalizeText(question);
            const questionWords = normalizedQuestion.split(/\s+/);

            // Přesná shoda
            if (userMessage.includes(normalizedQuestion) || normalizedQuestion.includes(userMessage)) {
                return 1.0;
            }

            // Počet shodných slov
            let matchingWords = 0;
            for (const userWord of userWords) {
                if (userWord.length < 2) continue;
                for (const questionWord of questionWords) {
                    if (questionWord.includes(userWord) || userWord.includes(questionWord)) {
                        matchingWords++;
                        break;
                    }
                }
            }

            const score = matchingWords / Math.max(userWords.length, questionWords.length);
            if (score > maxScore) {
                maxScore = score;
            }
        }

        return maxScore;
    }

    // Kontrola shody s polem vzorů
    matchesAny(text, patterns) {
        for (const pattern of patterns) {
            if (text.includes(pattern)) {
                return true;
            }
        }
        return false;
    }

    // Získání quick replies na základě kontextu
    getQuickReplies(message, response) {
        const topicQuickReplies = {
            crypto: ["Co je Bitcoin?", "Rizika krypto", "Kde koupit?"],
            stocks: ["Jak začít?", "Jaký broker?", "Co jsou dividendy?"],
            etf: ["Co je ETF?", "Typy ETF", "Jak koupit ETF?"],
            literacy: ["Rozpočet", "Složené úročení", "Finanční rezerva"],
            insolvency: ["Co je insolvence?", "Proces oddlužení", "Kde hledat pomoc?"],
            savings: ["Jak šetřit?", "Stavební spoření", "Pravidlo 50/30/20"]
        };

        // Vrátit quick replies pro aktuální téma
        return topicQuickReplies[this.currentTopic] || ["Kryptoměny", "Akcie", "Šetření"];
    }

    // Přidání zprávy do historie
    addToHistory(role, message) {
        this.conversationHistory.push({
            role: role,
            message: message,
            timestamp: new Date().toISOString()
        });
        this.saveHistory();
    }

    // Získání statistik
    getStats() {
        return {
            totalMessages: this.conversationHistory.length,
            userMessages: this.conversationHistory.filter(m => m.role === 'user').length,
            botMessages: this.conversationHistory.filter(m => m.role === 'bot').length,
            currentTopic: this.currentTopic
        };
    }
}

// Export pro použití v jiných modulech
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoBeeChatbot;
}
