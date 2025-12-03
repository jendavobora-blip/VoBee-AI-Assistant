# VoBee AI Assistant 🐝

Your Creative AI Assistant - An engaging chatbot Progressive Web App (PWA) that learns and adapts to your preferences.

## Features

- **Creative & Engaging Conversations**: VoBee provides friendly, creative responses with personality
- **Pseudo-Dynamic Learning**: Remembers your name, interests, and conversation history
- **Progressive Web App**: Install on any device for offline access
- **Beautiful UI**: Modern dark theme with smooth animations
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open http://localhost:3000 in your browser

### Files

- `index.html` - Main HTML structure
- `styles.css` - Modern CSS styling with animations
- `chatbot.js` - VoBee chatbot logic with pseudo-dynamic learning
- `sw.js` - Service worker for offline capability
- `manifest.json` - PWA manifest for installability

## How It Works

### Pseudo-Dynamic Learning

VoBee learns from your conversations by:
- Remembering your name when you introduce yourself
- Tracking topics you discuss frequently
- Storing your interests and preferences
- Personalizing responses based on conversation history

All data is stored locally in your browser's localStorage.

### PWA Features

- **Offline Support**: Works without an internet connection
- **Installable**: Add to your home screen on mobile
- **Fast Loading**: Assets are cached for quick access

## License

ISC