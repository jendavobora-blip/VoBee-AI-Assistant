import React, { useState } from 'react';
import './PromptInput.css';

function PromptInput({ onGenerate, disabled }) {
  const [prompt, setPrompt] = useState('');
  const [type, setType] = useState('image');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const params = { prompt };
    if (type === 'image') {
      params.style = 'realistic';
      params.resolution = '1024x1024';
      params.hdr = true;
      params.pbr = true;
    } else {
      params.duration = 5;
      params.resolution = '4K';
      params.fps = 30;
    }

    onGenerate(type, params);
  };

  return (
    <form className="prompt-input-form" onSubmit={handleSubmit}>
      <textarea
        className="prompt-textarea"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe what you want to create..."
        disabled={disabled}
        rows={4}
      />
      
      <div className="type-selector">
        <label className="radio-label">
          <input
            type="radio"
            value="image"
            checked={type === 'image'}
            onChange={(e) => setType(e.target.value)}
            disabled={disabled}
          />
          <span>Image</span>
        </label>
        <label className="radio-label">
          <input
            type="radio"
            value="video"
            checked={type === 'video'}
            onChange={(e) => setType(e.target.value)}
            disabled={disabled}
          />
          <span>Video</span>
        </label>
      </div>

      <button 
        type="submit" 
        className="generate-button"
        disabled={disabled || !prompt.trim()}
      >
        Generate
      </button>
    </form>
  );
}

export default PromptInput;
