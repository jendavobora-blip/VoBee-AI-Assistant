import React, { useState, useEffect } from 'react';
import LoginButton from './components/LoginButton';
import CostAlertModal from './components/CostAlertModal';
import ResultViewer from './components/ResultViewer';

const API_URL = 'http://localhost:8000';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState(null);
  const [token, setToken] = useState(null);
  const [costUsage, setCostUsage] = useState(null);
  const [showCostAlert, setShowCostAlert] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Form states
  const [chatMessage, setChatMessage] = useState('');
  const [imagePrompt, setImagePrompt] = useState('');
  const [videoPrompt, setVideoPrompt] = useState('');
  const [lifeSyncScenario, setLifeSyncScenario] = useState('');
  const [lifeSyncOptions, setLifeSyncOptions] = useState(['', '']);

  // Check cost usage periodically
  useEffect(() => {
    if (isLoggedIn && userId) {
      const interval = setInterval(fetchCostUsage, 30000); // Every 30 seconds
      fetchCostUsage(); // Initial fetch
      return () => clearInterval(interval);
    }
  }, [isLoggedIn, userId]);

  const fetchCostUsage = async () => {
    try {
      const response = await fetch(`${API_URL}/api/costs/usage`, {
        headers: {
          'X-User-ID': userId,
        },
      });
      const data = await response.json();
      setCostUsage(data);

      // Show alert if approaching limits
      if (data.hourly_usage / data.hourly_limit > 0.8 || data.daily_usage / data.daily_limit > 0.8) {
        setShowCostAlert(true);
      }
    } catch (error) {
      console.error('Failed to fetch cost usage:', error);
    }
  };

  const handleLogin = async (username) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });
      const data = await response.json();
      
      if (data.status === 'success') {
        setIsLoggedIn(true);
        setUserId(data.user.user_id);
        setToken(data.token);
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please try again.');
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserId(null);
    setToken(null);
    setCostUsage(null);
  };

  const makeRequest = async (endpoint, body) => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
      }

      const data = await response.json();
      setResult(data);
      fetchCostUsage(); // Update cost usage
    } catch (error) {
      setResult({ status: 'error', error: error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async (e) => {
    e.preventDefault();
    await makeRequest('/api/chat', { message: chatMessage });
    setChatMessage('');
  };

  const handleImageGeneration = async (e) => {
    e.preventDefault();
    await makeRequest('/api/generate/image', { prompt: imagePrompt, style: 'realistic' });
  };

  const handleVideoGeneration = async (e) => {
    e.preventDefault();
    await makeRequest('/api/generate/video', { prompt: videoPrompt, duration: 5 });
  };

  const handleLifeSync = async (e) => {
    e.preventDefault();
    const validOptions = lifeSyncOptions.filter(opt => opt.trim() !== '');
    await makeRequest('/api/lifesync/decision', {
      scenario: lifeSyncScenario,
      options: validOptions,
    });
  };

  if (!isLoggedIn) {
    return (
      <div className="app">
        <div className="login-screen">
          <h1>🐝 Vobio AI Studio</h1>
          <p>Production-ready AI orchestration platform</p>
          <LoginButton onLogin={handleLogin} />
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🐝 Vobio AI Studio</h1>
        <div className="user-info">
          <span>User: {userId}</span>
          {costUsage && (
            <span className="cost-badge">
              Daily: ${costUsage.daily_usage.toFixed(2)} / ${costUsage.daily_limit.toFixed(2)}
            </span>
          )}
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="main-content">
        <nav className="tabs">
          <button 
            className={activeTab === 'chat' ? 'active' : ''} 
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button 
            className={activeTab === 'image' ? 'active' : ''} 
            onClick={() => setActiveTab('image')}
          >
            Image
          </button>
          <button 
            className={activeTab === 'video' ? 'active' : ''} 
            onClick={() => setActiveTab('video')}
          >
            Video
          </button>
          <button 
            className={activeTab === 'lifesync' ? 'active' : ''} 
            onClick={() => setActiveTab('lifesync')}
          >
            LifeSync
          </button>
        </nav>

        <div className="tab-content">
          {activeTab === 'chat' && (
            <form onSubmit={handleChat} className="form">
              <h2>Chat Assistant</h2>
              <input
                type="text"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder="Type your message..."
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Sending...' : 'Send'}
              </button>
            </form>
          )}

          {activeTab === 'image' && (
            <form onSubmit={handleImageGeneration} className="form">
              <h2>Image Generation</h2>
              <input
                type="text"
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
                placeholder="Describe the image you want..."
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Generating...' : 'Generate Image'}
              </button>
            </form>
          )}

          {activeTab === 'video' && (
            <form onSubmit={handleVideoGeneration} className="form">
              <h2>Video Generation</h2>
              <input
                type="text"
                value={videoPrompt}
                onChange={(e) => setVideoPrompt(e.target.value)}
                placeholder="Describe the video you want..."
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Generating...' : 'Generate Video'}
              </button>
            </form>
          )}

          {activeTab === 'lifesync' && (
            <form onSubmit={handleLifeSync} className="form">
              <h2>LifeSync Decision Assistant</h2>
              <textarea
                value={lifeSyncScenario}
                onChange={(e) => setLifeSyncScenario(e.target.value)}
                placeholder="Describe your decision scenario..."
                rows="3"
                required
              />
              <div className="options-list">
                <label>Options:</label>
                {lifeSyncOptions.map((option, index) => (
                  <input
                    key={index}
                    type="text"
                    value={option}
                    onChange={(e) => {
                      const newOptions = [...lifeSyncOptions];
                      newOptions[index] = e.target.value;
                      setLifeSyncOptions(newOptions);
                    }}
                    placeholder={`Option ${index + 1}`}
                  />
                ))}
                <button
                  type="button"
                  onClick={() => setLifeSyncOptions([...lifeSyncOptions, ''])}
                >
                  + Add Option
                </button>
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Analyzing...' : 'Get Recommendation'}
              </button>
            </form>
          )}

          {result && <ResultViewer result={result} type={activeTab} />}
        </div>
      </div>

      {showCostAlert && costUsage && (
        <CostAlertModal
          costUsage={costUsage}
          onClose={() => setShowCostAlert(false)}
        />
      )}
    </div>
  );
}

export default App;
