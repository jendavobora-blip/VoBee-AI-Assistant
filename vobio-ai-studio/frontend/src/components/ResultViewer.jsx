import React from 'react';

function ResultViewer({ result, type }) {
  if (!result) return null;

  if (result.status === 'error') {
    return (
      <div className="result error">
        <h3>❌ Error</h3>
        <p>{result.error}</p>
      </div>
    );
  }

  return (
    <div className="result success">
      {type === 'chat' && (
        <>
          <h3>💬 AI Response</h3>
          <p>{result.message}</p>
          <small>Model: {result.model} | Cost: ${result.cost.toFixed(4)}</small>
        </>
      )}

      {type === 'image' && (
        <>
          <h3>🖼️ Generated Image</h3>
          <img src={result.url} alt={result.prompt} />
          <p><strong>Prompt:</strong> {result.prompt}</p>
          <p><strong>Style:</strong> {result.style}</p>
          <small>Model: {result.model} | Cost: ${result.cost.toFixed(4)}</small>
        </>
      )}

      {type === 'video' && (
        <>
          <h3>🎥 Generated Video</h3>
          <div className="video-placeholder">
            <p>Video Preview: {result.url}</p>
          </div>
          <p><strong>Prompt:</strong> {result.prompt}</p>
          <p><strong>Duration:</strong> {result.duration}s</p>
          <small>Model: {result.model} | Cost: ${result.cost.toFixed(4)}</small>
        </>
      )}

      {type === 'lifesync' && (
        <>
          <h3>🎯 LifeSync Recommendation</h3>
          <div className="lifesync-result">
            <div className="recommendation">
              <h4>Recommended: {result.recommendation}</h4>
              <div className="confidence">
                Confidence: {(result.confidence * 100).toFixed(0)}%
              </div>
            </div>
            
            <div className="reasoning">
              <h4>Reasoning:</h4>
              <p>{result.reasoning}</p>
            </div>

            {result.all_options && (
              <div className="all-options">
                <h4>All Options Analysis:</h4>
                {result.all_options.map((option, index) => (
                  <div key={index} className="option-card">
                    <h5>{option.name}</h5>
                    <p>Score: {option.total_score.toFixed(2)}/10</p>
                    <div className="factors">
                      {option.factors.map((factor, fIndex) => (
                        <div key={fIndex} className="factor">
                          <span>{factor.name}:</span>
                          <div className="factor-bar">
                            <div 
                              className="factor-fill" 
                              style={{ width: `${factor.value * 100}%` }}
                            />
                          </div>
                          <span>{(factor.score * 10).toFixed(1)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default ResultViewer;
