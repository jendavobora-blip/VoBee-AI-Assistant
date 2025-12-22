import React from 'react';

function CostAlertModal({ costUsage, onClose }) {
  const hourlyPercent = (costUsage.hourly_usage / costUsage.hourly_limit) * 100;
  const dailyPercent = (costUsage.daily_usage / costUsage.daily_limit) * 100;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>⚠️ Cost Usage Alert</h2>
        <p>You are approaching your usage limits:</p>
        
        <div className="cost-details">
          <div className="cost-item">
            <label>Hourly Usage:</label>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${hourlyPercent}%` }}
              />
            </div>
            <span>
              ${costUsage.hourly_usage.toFixed(2)} / ${costUsage.hourly_limit.toFixed(2)} 
              ({hourlyPercent.toFixed(0)}%)
            </span>
          </div>

          <div className="cost-item">
            <label>Daily Usage:</label>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${dailyPercent}%` }}
              />
            </div>
            <span>
              ${costUsage.daily_usage.toFixed(2)} / ${costUsage.daily_limit.toFixed(2)} 
              ({dailyPercent.toFixed(0)}%)
            </span>
          </div>

          <div className="cost-item">
            <label>Total Usage:</label>
            <span>${costUsage.total_usage.toFixed(2)}</span>
          </div>
        </div>

        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default CostAlertModal;
