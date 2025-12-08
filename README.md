# VoBee AI Assistant <img width="480" height="480" alt="image" src="https://github.com/user-attachments/assets/feb0de59-8c3c-4796-8b99-554155982991" />


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
├── scripts/
│   └── fetch_recent_commits.sh # Automation script to fetch recent commits
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

### IndexedDB Stores
1. **conversations**: Stores all chat messages with timestamps
2. **unrecognized_queries**: Logs unknown inputs with occurrence counts

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

## Automation Scripts

### Fetch Recent Commits Script
The repository includes an automation script to fetch commits from the last 2 hours across all your accessible GitHub repositories.

#### Prerequisites
- **jq** - JSON processor (required)
- **curl** - HTTP client (required if not using GitHub CLI)
- **GitHub CLI (gh)** - Optional but recommended

Install prerequisites:
```bash
# On Ubuntu/Debian
sudo apt-get install jq curl

# On macOS
brew install jq curl

# On CentOS/RHEL
sudo yum install jq curl
```

#### Authentication
The script supports two authentication methods:

**Option 1: GitHub CLI (Recommended)**
```bash
gh auth login
```

**Option 2: Personal Access Token**
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

To create a personal access token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Copy the token and set it as an environment variable

#### Usage
```bash
# Run the script
./scripts/fetch_recent_commits.sh

# Enable debug mode for verbose output
DEBUG=1 ./scripts/fetch_recent_commits.sh
```

#### Output
The script will:
1. Authenticate with GitHub
2. Fetch all repositories you have access to (owned, collaborator, organization member)
3. Query each repository for commits from the last 2 hours
4. Display commits grouped by repository with:
   - Commit SHA (short)
   - Author name and email
   - Commit date
   - Commit message

#### Example Output
```
[INFO] Starting to fetch commits from the last 2 hours...
[SUCCESS] Authenticated as: username
[INFO] Fetching commits since: 2024-12-08T20:12:00Z
[SUCCESS] Found 15 accessible repositories

Repository: username/repo-name
Total commits: 2
================================================================================
  Commit: a1b2c3d
  Author: John Doe <john@example.com>
  Date:   2024-12-08T21:30:00Z
  Message: Add new feature

  Commit: e4f5g6h
  Author: Jane Smith <jane@example.com>
  Date:   2024-12-08T20:45:00Z
  Message: Fix bug in component
```

## Browser Support
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## License
MIT License - feel free to use and modify!
