export const generateImage = async (params) => {
  const response = await fetch('http://127.0.0.1:8000/generate/image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  });
  
  if (!response.ok) {
    throw new Error('Image generation failed');
  }
  
  return await response.json();
};

export const generateVideo = async (params) => {
  const response = await fetch('http://127.0.0.1:8000/generate/video', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  });
  
  if (!response.ok) {
    throw new Error('Video generation failed');
  }
  
  return await response.json();
};

export const getProgress = async (operationId) => {
  const response = await fetch(`http://127.0.0.1:8000/progress/${operationId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch progress');
  }
  
  return await response.json();
};

export const cancelOperation = async (operationId) => {
  const response = await fetch(`http://127.0.0.1:8000/cancel/${operationId}`, {
    method: 'POST'
  });
  
  if (!response.ok) {
    throw new Error('Failed to cancel operation');
  }
  
  return await response.json();
};

export const getHealthStatus = async () => {
  const response = await fetch('http://127.0.0.1:8000/health');
  return await response.json();
};

export const getGPUInfo = async () => {
  const response = await fetch('http://127.0.0.1:8000/gpu-info');
  return await response.json();
};
