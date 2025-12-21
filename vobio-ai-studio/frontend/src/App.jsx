import React, { useState } from 'react';
import PromptInput from './components/PromptInput';
import ProgressDisplay from './components/ProgressDisplay';
import ResultViewer from './components/ResultViewer';
import './App.css';

function App() {
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [result, setResult] = useState(null);
  const [operationId, setOperationId] = useState(null);

  const handleGenerate = async (type, params) => {
    setGenerating(true);
    setProgress(0);
    setStage('Starting...');
    setResult(null);

    try {
      let response;
      if (type === 'image') {
        response = await window.api.generateImage(params);
      } else {
        response = await window.api.generateVideo(params);
      }

      setOperationId(response.operation_id);

      const interval = setInterval(async () => {
        const progressData = await window.api.getProgress(response.operation_id);
        setProgress(progressData.progress);
        setStage(progressData.stage);

        if (progressData.progress >= 100) {
          clearInterval(interval);
          setResult(response);
          setGenerating(false);
        }
      }, 500);

    } catch (error) {
      console.error('Generation failed:', error);
      setGenerating(false);
    }
  };

  const handleCancel = async () => {
    if (operationId) {
      await window.api.cancelOperation(operationId);
      setGenerating(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Vobio AI Studio</h1>
        <p className="tagline">Extremely capable AI system that behaves like one calm, intelligent business partner.</p>
      </header>
      
      <main className="app-main">
        <PromptInput onGenerate={handleGenerate} disabled={generating} />
        
        {generating && (
          <ProgressDisplay 
            progress={progress} 
            stage={stage} 
            onCancel={handleCancel}
          />
        )}
        
        {result && <ResultViewer result={result} />}
      </main>
    </div>
  );
}

export default App;
