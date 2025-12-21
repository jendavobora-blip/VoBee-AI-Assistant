const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  generateImage: (params) => ipcRenderer.invoke('generate-image', params),
  generateVideo: (params) => ipcRenderer.invoke('generate-video', params),
  getProgress: (operationId) => ipcRenderer.invoke('get-progress', operationId),
  cancelOperation: (operationId) => ipcRenderer.invoke('cancel-operation', operationId)
});
