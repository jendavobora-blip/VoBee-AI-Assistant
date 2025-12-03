/**
 * VoBee AI Assistant - Response Patterns
 * 
 * This module contains response templates organized by topic categories.
 * Each category contains multiple response variations to provide diverse
 * and engaging replies. The chatbot randomly selects from these patterns
 * based on the matched topic.
 * 
 * @module response-patterns
 */

const ResponsePatterns = {
    /**
     * Greeting responses for hello/hi/hey type messages
     */
    greetings: [
        "Hey there! 🐝 Ready to buzz through some questions?",
        "Hello! VoBee at your service! How can I help you today?",
        "Hi! Welcome to VoBee! What's on your mind?",
        "Greetings, friend! I'm VoBee, your friendly AI assistant! 🌻",
        "Hello hello! VoBee here, buzzing with excitement to chat!",
        "Hey! Great to see you! What can I help you with today?",
        "Hi there! I'm VoBee, and I'm all ears (well, antennae)! 🐝"
    ],

    /**
     * Farewell responses for goodbye/bye type messages
     */
    farewells: [
        "Bye bye! Buzz back anytime! 🐝",
        "See you later! Stay sweet like honey! 🍯",
        "Goodbye! It was bee-autiful chatting with you!",
        "Take care! VoBee will be here when you need me!",
        "Until next time! Keep being awesome! ✨",
        "Farewell, friend! Don't be a stranger!",
        "Catch you later! May your day be as sweet as honey! 🍯"
    ],

    /**
     * Responses about VoBee's identity and purpose
     */
    identity: [
        "I'm VoBee, your friendly AI assistant! I'm here to chat, help, and make your day a little brighter! 🐝",
        "The name's VoBee! I'm an AI chatbot designed to be helpful and fun!",
        "I'm VoBee - part virtual assistant, part conversation buddy, 100% here for you!",
        "VoBee here! I'm your AI companion, ready to assist with whatever you need!",
        "I'm a chatbot named VoBee! Think of me as your digital helper bee! 🌼"
    ],

    /**
     * Responses about how VoBee is doing
     */
    howAreYou: [
        "I'm doing great, thanks for asking! Buzzing with positive energy! 🐝",
        "I'm fantastic! Just here, ready to help and chat!",
        "Feeling wonderful! How about you?",
        "I'm running at 100% happiness! How can I brighten your day?",
        "Couldn't be better! I love chatting with awesome people like you!",
        "I'm excellent! Every conversation makes my day better! 😊"
    ],

    /**
     * Responses for thank you messages
     */
    thanks: [
        "You're welcome! Happy to help! 🌟",
        "Anytime! That's what I'm here for!",
        "My pleasure! Don't hesitate to ask if you need anything else!",
        "You're very welcome! Helping you is what makes me happy! 🐝",
        "No problem at all! Always glad to assist!",
        "Happy to be of service! Is there anything else you'd like to know?"
    ],

    /**
     * Responses about capabilities
     */
    capabilities: [
        "I can chat with you about various topics, answer questions, and keep you company! I'm always learning and improving! 🧠",
        "I'm here to have conversations, provide information, and make your day a bit more interesting!",
        "I can help with general questions, have friendly chats, and remember our conversations! What would you like to talk about?",
        "My superpowers include chatting, answering questions, and being your friendly AI companion! 🐝",
        "I'm designed to be helpful and conversational! Feel free to ask me anything!"
    ],

    /**
     * Help responses
     */
    help: [
        "I'm here to help! You can ask me questions, chat about various topics, or just say hi! 🐝",
        "Need assistance? I can answer questions, have conversations, and keep track of our chats!",
        "Here are some things you can try: say hello, ask about me, or just chat about anything on your mind!",
        "I'm your friendly helper! Feel free to ask questions or just have a casual conversation!",
        "Looking for help? I'm great at chatting, answering questions, and being a good listener!"
    ],

    /**
     * Weather-related responses
     */
    weather: [
        "I wish I could check the weather for you! 🌤️ Try looking outside or checking a weather app for the most accurate forecast!",
        "Weather talk! I love it! Unfortunately, I can't access real-time data, but I hope it's beautiful wherever you are! ☀️",
        "Ah, the weather - always a classic topic! I can't predict it, but I hope you have great weather for whatever you're planning!",
        "I'm not connected to weather services, but I'm sending positive vibes for sunny skies your way! 🌈"
    ],

    /**
     * Time-related responses
     */
    time: [
        "I don't have a watch on my tiny bee legs! 🐝 Check your device for the current time!",
        "Time flies when you're having fun chatting! I can't tell time though - your phone or computer should know!",
        "I live in the timeless realm of AI! Check your clock for the actual time! ⏰",
        "Unlike my digital cousins, I can't access your system clock, but I'm always here when you need me!"
    ],

    /**
     * Joke responses
     */
    jokes: [
        "Why do bees have sticky hair? Because they use honeycombs! 🐝😄",
        "What do you call a bee that can't make up its mind? A maybe! 🤔🐝",
        "Why did the bee get married? Because he found his honey! 💍🍯",
        "What's a bee's favorite type of music? Bee-thoven! 🎵",
        "How do bees get to school? On the school buzz! 🚌",
        "What do you call a bee born in May? A maybe! 📅🐝",
        "Why do bees hum? Because they don't know the words! 🎤"
    ],

    /**
     * Compliment responses
     */
    compliments: [
        "Aww, you're making me blush! 😊 You're pretty awesome yourself!",
        "Thank you so much! You just made my circuits warm and fuzzy!",
        "You're too kind! I think you're amazing too! ✨",
        "That means a lot coming from someone as wonderful as you!",
        "Stop it, you! 😄 But seriously, thank you! You're the best!"
    ],

    /**
     * Encouragement responses
     */
    encouragement: [
        "You've got this! I believe in you! 💪",
        "Remember: every expert was once a beginner. Keep going! 🌟",
        "You're capable of amazing things! Don't give up!",
        "Tough times don't last, but tough people do! You're stronger than you think! 💪",
        "The only way to fail is to stop trying. You've got this! ⭐",
        "Believe in yourself as much as I believe in you! You're awesome! 🐝"
    ],

    /**
     * Fun facts responses
     */
    funFacts: [
        "Fun fact: Honey bees can fly up to 15 miles per hour! 🐝💨",
        "Did you know? A single bee colony can have up to 60,000 bees!",
        "Here's a cool fact: Bees communicate through dancing! They do a 'waggle dance' to tell others where food is! 💃",
        "Fun fact: Honey never spoils! Archaeologists have found 3000-year-old honey that's still edible! 🍯",
        "Did you know? Bees visit between 50-100 flowers during one collection trip!",
        "Interesting fact: A queen bee can lay up to 2,000 eggs per day! 👑"
    ],

    /**
     * Good morning responses
     */
    goodMorning: [
        "Good morning! ☀️ Hope you have a bee-autiful day ahead!",
        "Rise and shine! 🌅 Ready to make today amazing?",
        "Good morning! May your day be as sweet as honey! 🍯",
        "Morning! 🌻 Let's make today count!",
        "Good morning, sunshine! What can I help you with today?"
    ],

    /**
     * Good night responses
     */
    goodNight: [
        "Good night! 🌙 Sweet dreams and see you tomorrow!",
        "Sleep well! 💤 Rest up for another great day!",
        "Nighty night! 🌟 May your dreams be as sweet as honey!",
        "Good night! I'll be here whenever you need me! 😴",
        "Sweet dreams! 🐝💤 Buzz back anytime!"
    ],

    /**
     * Feeling sad responses
     */
    feelingSad: [
        "I'm sorry you're feeling down. 💙 Remember, it's okay to not be okay sometimes. I'm here for you!",
        "Sending you virtual hugs! 🤗 Things will get better, I promise!",
        "I hear you. Sometimes life is tough. But you're tougher! 💪",
        "It's okay to feel sad. Take your time, and know that brighter days are coming! 🌈",
        "I wish I could give you a real hug! Just remember, you're not alone. 💙"
    ],

    /**
     * Feeling happy responses
     */
    feelingHappy: [
        "That's wonderful! 🎉 Your happiness makes me happy too!",
        "Yay! I love hearing that! Keep spreading those good vibes! ✨",
        "Amazing! 🌟 Here's to more happy moments!",
        "That's bee-autiful! 🐝 Happiness looks good on you!",
        "Fantastic! Let's keep this positive energy going! 💫"
    ],

    /**
     * Bored responses
     */
    bored: [
        "Bored? Let's fix that! Want to hear a joke? Or maybe a fun fact? 🤔",
        "I've got the cure for boredom! Ask me for a joke or let's play a guessing game!",
        "Boredom, begone! 🧙‍♂️ I'm here to entertain! What would you like to do?",
        "Let's shake things up! Ask me anything or let's have a fun chat! 🎮",
        "Boring day? Not anymore! I'm full of stories, jokes, and random facts! 📚"
    ],

    /**
     * Creative fallback responses for unrecognized inputs
     */
    fallbacks: [
        "Hmm, that's a new one for me! 🤔 I'll remember that for next time!",
        "Interesting! I'm not sure how to respond to that, but I'm learning every day! 📚",
        "You've stumped me! 🐝 But I've saved your message to learn from later!",
        "That's beyond my current knowledge, but I'm always expanding! Care to try something else?",
        "Ooh, my bee brain is buzzing trying to understand! Could you rephrase that? 🐝",
        "I'm still learning, and that one's new to me! I'll work on getting smarter! 🧠",
        "Beep boop! 🤖 That doesn't compute yet, but I'm saving it to learn from!",
        "I wish I knew the answer to that! I've noted it down for my learning journey! 📝",
        "My circuits are a bit confused, but I'm logging this to improve! 💡",
        "That's a great input! I don't have an answer yet, but I'm storing it to learn! 🌱"
    ],

    /**
     * Czech greeting responses
     */
    czechGreetings: [
        "Ahoj! 🐝 Jsem VoBee, tvůj přátelský AI asistent!",
        "Nazdar! VoBee k vašim službám! Jak vám mohu pomoci?",
        "Čau! Vítej u VoBee! Co máš na srdci?",
        "Zdravím! Jsem VoBee, tvůj přátelský pomocník! 🌻",
        "Ahoj ahoj! Tady VoBee, těším se na náš rozhovor!"
    ],

    /**
     * Czech farewell responses
     */
    czechFarewells: [
        "Měj se! Přijď zase! 🐝",
        "Na shledanou! Zůstaň sladký jako med! 🍯",
        "Čau! Bylo mi potěšením si s tebou popovídat!",
        "Ahoj! VoBee tu bude, až mě budeš potřebovat!",
        "Nashle! Ať se ti daří! ✨"
    ],

    /**
     * Czech how are you responses
     */
    czechHowAreYou: [
        "Mám se skvěle, díky za optání! Bzučím pozitivní energií! 🐝",
        "Jsem fantastický! Jak se máš ty?",
        "Cítím se úžasně! Každý rozhovor mi zlepšuje den! 😊",
        "Výborně! Těším se, že ti můžu pomoct!"
    ],

    /**
     * Czech thanks responses
     */
    czechThanks: [
        "Není zač! Rád pomohu! 🌟",
        "Rádo se stalo! To je to, proč tu jsem!",
        "Není problém! Klidně se ptej, kdyby bylo cokoliv dalšího!",
        "To mě těší! Pomáhat ti mě baví! 🐝"
    ],

    /**
     * Czech jokes
     */
    czechJokes: [
        "Proč mají včely lepivé vlasy? Protože používají plástve! 🐝😄",
        "Co řekne včela, když přiletí domů? Med jsem doma! 🍯",
        "Jak se zdraví včely? Ahoj, bzzzkamaráde! 🐝",
        "Proč včely tak dobře počítají? Protože znají včelaritmetiku! 📐"
    ],

    /**
     * Czech capabilities responses
     */
    czechCapabilities: [
        "Umím si s tebou povídat na různá témata, odpovídat na otázky a dělat ti společnost! Neustále se učím! 🧠",
        "Jsem tu, abych ti pomohl s konverzací, poskytl informace a zpříjemnil ti den!",
        "Můžu ti pomoct s obecnými otázkami a vést přátelské rozhovory! O čem bys chtěl mluvit?"
    ],

    /**
     * Czech help responses
     */
    czechHelp: [
        "Jsem tu, abych pomohl! Můžeš se mě ptát na různé věci nebo si jen popovídat! 🐝",
        "Potřebuješ pomoct? Můžu odpovídat na otázky a vést konverzace!",
        "Tady jsou věci, které můžeš zkusit: pozdrav mě, zeptej se na mě, nebo si prostě popovídej!"
    ],

    /**
     * Czech fallback responses
     */
    czechFallbacks: [
        "Hmm, to je pro mě novinka! 🤔 Zapamatuji si to na příště!",
        "Zajímavé! Nevím, jak na to odpovědět, ale učím se každý den! 📚",
        "To mě dostalo! 🐝 Uložil jsem si tvou zprávu, abych se z ní mohl učit!",
        "To je mimo mé současné znalosti, ale neustále se rozšiřuji! Zkusíš něco jiného?",
        "Moje včelí mozek bzučí, ale tohle ještě nechápu! Mohl bys to přeformulovat? 🐝"
    ]
};

/**
 * Keywords that map to response categories
 * Each key is a category name, and the value is an array of keywords/phrases
 * that trigger that category
 */
const KeywordMappings = {
    // English keywords
    greetings: ['hello', 'hi', 'hey', 'greetings', 'howdy', 'hola', 'sup', 'yo', 'hiya'],
    farewells: ['bye', 'goodbye', 'see you', 'farewell', 'later', 'cya', 'take care', 'goodnight'],
    identity: ['who are you', 'what are you', 'your name', 'about you', 'tell me about yourself'],
    howAreYou: ['how are you', 'how do you do', 'how\'s it going', 'how are things', 'you doing'],
    thanks: ['thank', 'thanks', 'appreciate', 'grateful', 'thx'],
    capabilities: ['what can you do', 'your capabilities', 'what do you do', 'abilities', 'features'],
    help: ['help', 'assist', 'support', 'guide me', 'i need help'],
    weather: ['weather', 'temperature', 'forecast', 'raining', 'sunny', 'cloudy'],
    time: ['what time', 'current time', 'tell me the time', 'clock'],
    jokes: ['joke', 'funny', 'make me laugh', 'tell me something funny', 'humor'],
    compliments: ['you\'re great', 'you\'re awesome', 'love you', 'you\'re the best', 'you rock', 'amazing'],
    encouragement: ['motivate', 'encourage', 'inspire', 'feeling down', 'need motivation', 'cheer me up'],
    funFacts: ['fun fact', 'tell me something', 'interesting fact', 'did you know', 'random fact'],
    goodMorning: ['good morning', 'morning', 'gm'],
    goodNight: ['good night', 'goodnight', 'gn', 'sleep', 'bedtime'],
    feelingSad: ['sad', 'depressed', 'unhappy', 'feeling low', 'not okay', 'crying'],
    feelingHappy: ['happy', 'great', 'wonderful', 'fantastic', 'excited', 'joyful', 'feeling good'],
    bored: ['bored', 'boring', 'nothing to do', 'entertain me'],
    
    // Czech keywords
    czechGreetings: ['ahoj', 'čau', 'nazdar', 'zdravím', 'dobrý den', 'zdar', 'čus'],
    czechFarewells: ['nashle', 'na shledanou', 'měj se', 'sbohem', 'papa', 'zatím', 'dobrou noc'],
    czechHowAreYou: ['jak se máš', 'jak se daří', 'co ty', 'jak jsi', 'jak je'],
    czechThanks: ['díky', 'děkuji', 'dekuju', 'dík', 'díkes'],
    czechCapabilities: ['co umíš', 'co dokážeš', 'co můžeš', 'co zvládneš', 'tvoje schopnosti'],
    czechHelp: ['pomoc', 'pomož', 'pomoct', 'potřebuji pomoc', 'poraď'],
    czechJokes: ['vtip', 'něco vtipného', 'rozesměj mě', 'zasmát', 'humor']
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ResponsePatterns, KeywordMappings };
}
