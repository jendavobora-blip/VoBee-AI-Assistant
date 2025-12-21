import React from 'react';
import './ResultViewer.css';

function ResultViewer({ result }) {
  return (
    <div className="result-viewer">
      <h3>Result</h3>
      <div className="result-details">
        <p><strong>Status:</strong> {result.status}</p>
        <p><strong>ID:</strong> {result.operation_id}</p>
        <p><strong>Prompt:</strong> {result.prompt}</p>
        
        {result.image_id && (
          <div className="image-details">
            <p><strong>Resolution:</strong> {result.resolution}</p>
            <p><strong>HDR:</strong> {result.hdr_enabled ? 'Yes' : 'No'}</p>
            <p><strong>PBR:</strong> {result.pbr_enabled ? 'Yes' : 'No'}</p>
            {result.mock_data && (
              <div className="image-preview">
                <img src={result.mock_data} alt="Generated" />
              </div>
            )}
          </div>
        )}
        
        {result.video_id && (
          <div className="video-details">
            <p><strong>Duration:</strong> {result.duration}s</p>
            <p><strong>FPS:</strong> {result.fps}</p>
            <p><strong>Total Frames:</strong> {result.total_frames}</p>
            <p><strong>Resolution:</strong> {result.resolution}</p>
          </div>
        )}
      </div>
      
      <button 
        className="export-button"
        onClick={() => alert('Export functionality would go here')}
      >
        Export
      </button>
    </div>
  );
}

export default ResultViewer;
