import React from 'react';
import './ProgressDisplay.css';

function ProgressDisplay({ progress, stage, onCancel }) {
  return (
    <div className="progress-display">
      <h3>Generating...</h3>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="progress-text">{progress}% - {stage}</p>
      <button className="cancel-button" onClick={onCancel}>Cancel</button>
    </div>
  );
}

export default ProgressDisplay;
