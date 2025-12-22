import React, { useState } from 'react';

function LoginButton({ onLogin }) {
  const [username, setUsername] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      onLogin(username.trim());
    }
  };

  return (
    <div className="login-button-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Mock Passkey Login</h2>
        <p>Enter any username to login (mock mode)</p>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username..."
          required
        />
        <button type="submit">🔐 Login with Passkey</button>
      </form>
    </div>
  );
}

export default LoginButton;
