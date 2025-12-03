# VoBee AI Assistant 🐝

A creative, friendly AI chatbot Progressive Web App (PWA) with pseudo-learning capabilities and persistent conversation history.

## Features

### 🎨 High Creativity in Responses
- Diverse and engaging replies to user queries
- Multiple response variations for each topic category
- Dynamic and unpredictable responses based on pattern matching

### 📚 Response Patterns
- Organized response templates in `js/response-patterns.js`
- 18+ topic categories including:
  - Greetings & Farewells
  - Identity & Capabilities
  - Emotional responses (happy, sad, bored)
  - Fun facts & Jokes
  - Time-specific greetings
  - And more!

### 🧠 Pseudo-Learning Capability
- Logs unrecognized queries to IndexedDB
- Tracks frequency of unknown queries
- Data available for future analysis and improvement

### 💾 Conversation History
- Persistent storage using IndexedDB
- Survives browser reloads and closures
- Clear history option available

### 📱 PWA Integration
- Installable on mobile and desktop
- Offline support via Service Worker
- Responsive design for all screen sizes

### 🎭 Creative Fallback Responses
- 10+ entertaining fallback messages
- Informs users that their input is being logged for learning

### 📷 Custom Avatar Upload
- Upload your own photo for the avatar
- Click the avatar or camera icon to select an image
- Avatar is saved persistently in IndexedDB
- Supports common image formats (JPEG, PNG, GIF, etc.)

### 🎤 Voice Recording
- Record voice messages directly in the chat
- Click the microphone button to start/stop recording
- Voice messages are displayed with playback controls
- Requires microphone permission

## Project Structure

```
VoBee-AI-Assistant/
├── index.html              # Main HTML entry point
├── manifest.json           # PWA manifest
├── sw.js                   # Service Worker for offline support
├── css/
│   └── styles.css          # Responsive styles
├── js/
│   ├── chatbot.js          # Main chatbot logic and UI controller
│   └── response-patterns.js # Response templates and keyword mappings
└── icons/
    └── icon-192.svg        # App icon
```

## Architecture

### VoBeeChatbot Class
The main chatbot engine that handles:
- Pattern matching via keyword mappings
- Random response selection for variety
- IndexedDB management for persistence
- Message processing pipeline

### ChatUI Class
Manages the user interface:
- Message display and animations
- Event handling (send, clear)
- Typing indicators
- Welcome messages
- Avatar upload and display
- Voice recording and playback

### IndexedDB Stores
1. **conversations**: Stores all chat messages with timestamps
2. **unrecognized_queries**: Logs unknown inputs with occurrence counts
3. **user_settings**: Stores user preferences including avatar image

## Usage

### Running Locally
1. Clone the repository
2. Serve the files using any HTTP server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve
   ```
3. Open `http://localhost:8080` in your browser

### Interacting with VoBee
- Type messages in the input field and press Enter or click Send
- Try greetings like "Hello" or "Hi there"
- Ask "Tell me a joke" or "Fun fact"
- Express emotions: "I'm feeling sad" or "I'm so happy!"
- Ask for help with "Help" or "What can you do?"

### Customizing Your Avatar
- Click on the bee emoji avatar in the header, or click the camera (📷) button
- Select an image file from your device (JPEG, PNG, GIF supported)
- Your avatar will be saved and displayed on future visits

### Recording Voice Messages
- Click the microphone (🎤) button to start recording
- Speak your message (grant microphone permission if prompted)
- Click the stop (⏹️) button to end recording
- Your voice message will appear in the chat with playback controls

## Extending the Chatbot

### Adding New Response Categories
1. Add responses to `ResponsePatterns` in `response-patterns.js`:
   ```javascript
   newCategory: [
       "Response 1",
       "Response 2",
       // ...
   ]
   ```

2. Add keywords to `KeywordMappings`:
   ```javascript
   newCategory: ['keyword1', 'keyword2', 'phrase to match']
   ```

### Analyzing Unrecognized Queries
Access logged queries programmatically:
```javascript
const queries = await vobee.getUnrecognizedQueries();
console.log(queries);
```

## Browser Support
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## License
MIT License - feel free to use and modify!