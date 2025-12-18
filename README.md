# VoBee AI Assistant

**VoBee** is a Progressive Web App (PWA) that serves as your friendly AI chatbot assistant. It's designed to work seamlessly on any device - mobile, tablet, or desktop - and can be installed for an app-like experience.

## 🌟 Release 1.0 Features

- 🐝 **Interactive Chat Interface**: Clean, mobile-first chat UI with real-time responses
- 💬 **Intelligent Responses**: Pattern-based conversation system with diverse response categories
- 💾 **Conversation Memory**: Uses IndexedDB to remember your chat history
- 📱 **Progressive Web App**: Install on iOS, Android, or Desktop for native app experience
- 🌐 **Offline Support**: Service worker enables offline functionality
- 🎨 **Responsive Design**: Optimized for all screen sizes from mobile to desktop
- ⚡ **No Backend Required**: Runs entirely client-side with no server dependencies
- 🔒 **Privacy First**: All data stored locally on your device

## 📱 Installation Instructions

### iOS (Safari)

1. Open [VoBee](https://jendavobora-blip.github.io/VoBee-AI-Assistant/) in Safari
2. Tap the **Share** button (square with arrow pointing up)
3. Scroll down and tap **"Add to Home Screen"**
4. Name it "VoBee" and tap **Add**
5. The app icon will appear on your home screen - tap to launch!

**Note for iOS**: The app will behave like a native iOS app with full-screen mode and no browser UI.

### Android (Chrome)

1. Open [VoBee](https://jendavobora-blip.github.io/VoBee-AI-Assistant/) in Chrome
2. Look for the **"Install App"** prompt at the bottom of the screen, or
3. Tap the menu (⋮) and select **"Add to Home Screen"** or **"Install app"**
4. Confirm the installation
5. Launch VoBee from your app drawer or home screen!

**Note for Android**: You'll get a native app experience with push notification support (future feature).

### Desktop (Chrome/Edge)

1. Open [VoBee](https://jendavobora-blip.github.io/VoBee-AI-Assistant/) in Chrome or Edge
2. Look for the install icon (⊕) in the address bar, or
3. Click the menu (⋮) and select **"Install VoBee"**
4. The app will open in its own window
5. Access it from your desktop or start menu!

**Note for Desktop**: The PWA runs in a standalone window without browser tabs or address bar.

### Manual Access (Any Browser)

Simply visit [https://jendavobora-blip.github.io/VoBee-AI-Assistant/](https://jendavobora-blip.github.io/VoBee-AI-Assistant/) in any modern web browser. No installation required!

## 🚀 How It Works

VoBee is built as a **Progressive Web App** hosted on **GitHub Pages**. Here's why this setup works perfectly:

### GitHub Pages Compatibility

- **Static Hosting**: GitHub Pages serves static files (HTML, CSS, JS) - perfect for PWAs
- **HTTPS by Default**: GitHub Pages provides HTTPS, which is required for Service Workers
- **Custom Domain Support**: Can be mapped to custom domains (future enhancement)
- **CDN Distribution**: Fast global access through GitHub's infrastructure

### PWA Architecture

1. **index.html**: Entry point served from repository root (GitHub Pages requirement)
2. **manifest.json**: Defines app metadata for installation
   - Name: "VoBee"
   - Standalone display mode for app-like experience
   - Start URL: "./" for GitHub Pages subdirectory compatibility
3. **service-worker.js**: Enables offline functionality
   - Caches app shell (HTML, CSS, JS)
   - Provides offline fallback
   - All paths are relative (`./`) for GitHub Pages compatibility
4. **Resource Paths**: All resources use relative paths (`./path`) to work in GitHub Pages subdirectory environment

### Offline Functionality

The service worker caches all essential resources:
- HTML structure
- CSS styles  
- JavaScript logic
- App icons
- Manifest file

Once cached, VoBee works completely offline! The chat functionality continues without internet since no backend calls are made.

### Chat System

VoBee uses a **client-side pattern matching system**:
- Keywords trigger specific response categories
- Multiple response variations prevent repetition
- IndexedDB stores conversation history locally
- Unrecognized queries are logged for future improvements
- No API calls or backend services needed

## 🔧 Technical Stack

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS variables and animations
- **Vanilla JavaScript**: No frameworks - just pure JS
- **IndexedDB**: Client-side database for persistence
- **Service Workers**: Offline support and caching
- **Web App Manifest**: PWA installation metadata

## 📂 Project Structure

```
VoBee-AI-Assistant/
├── index.html              # Main app entry point
├── manifest.json           # PWA manifest
├── service-worker.js       # Service worker for offline support
├── css/
│   └── styles.css         # All application styles
├── js/
│   ├── chatbot.js         # Main chatbot logic and UI
│   └── response-patterns.js # Response templates and keywords
└── icons/
    └── icon-192.svg       # App icons
```

## 🎯 Release 1.0 Scope

### ✅ Included in Release 1.0

- Functional PWA installable on all platforms
- Working chat interface with pattern-based responses
- Offline support via Service Worker
- Local conversation history
- Mobile-first responsive design
- GitHub Pages deployment
- Basic accessibility features

### 🔮 Future Enhancements (Post-1.0)

- Voice input/output capabilities
- Advanced NLP with actual AI integration
- Cloud sync for conversation history
- User accounts and personalization
- Multi-language support
- Enhanced financial advice features
- Cryptocurrency price tracking
- Push notifications
- Theme customization

## 🛠️ Development

Since VoBee uses no build tools, development is simple:

1. Clone the repository
2. Open `index.html` in a browser
3. Edit files and refresh to see changes
4. Test Service Worker using Chrome DevTools → Application tab

To test PWA features locally:
- Use `python -m http.server` or similar to serve over HTTP
- Service Workers require HTTPS (or localhost)

## 🌐 Deployment

VoBee is automatically deployed to GitHub Pages. Any push to the main branch updates the live app at:
https://jendavobora-blip.github.io/VoBee-AI-Assistant/

## 🔒 Privacy & Security

- **No Data Collection**: VoBee doesn't send any data to external servers
- **Local Storage Only**: All conversations stored in browser's IndexedDB
- **No Tracking**: No analytics, cookies, or tracking scripts
- **No Authentication**: No login required, no user data collected

## 📄 License

This project is part of VoBee AI Assistant initiative.

## 👤 Author

**Jan Vobora**  
VoBee Project

## 🐝 Why "VoBee"?

VoBee combines "Vo" (from Vobora) with "Bee" - symbolizing hard work, community, and sweet results (like honey!). Just as bees work efficiently to create value, VoBee aims to be your efficient digital assistant.

---

**Ready to buzz? [Install VoBee now!](https://jendavobora-blip.github.io/VoBee-AI-Assistant/)**
