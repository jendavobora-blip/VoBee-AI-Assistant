const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  mainWindow.loadFile(path.join(__dirname, '../public/index.html'));
  
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackend() {
  const backendPath = path.join(__dirname, '../../backend/api_server.py');
  backendProcess = spawn('python', [backendPath]);
  
  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });
  
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });
}

app.whenReady().then(() => {
  startBackend();
  setTimeout(createWindow, 2000);
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

ipcMain.handle('generate-image', async (event, params) => {
  return await fetch('http://127.0.0.1:8000/generate/image', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  }).then(r => r.json());
});

ipcMain.handle('generate-video', async (event, params) => {
  return await fetch('http://127.0.0.1:8000/generate/video', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  }).then(r => r.json());
});

ipcMain.handle('get-progress', async (event, operationId) => {
  return await fetch(`http://127.0.0.1:8000/progress/${operationId}`)
    .then(r => r.json())
    .catch(() => ({ progress: 0, stage: 'Unknown' }));
});

ipcMain.handle('cancel-operation', async (event, operationId) => {
  return await fetch(`http://127.0.0.1:8000/cancel/${operationId}`, {
    method: 'POST'
  }).then(r => r.json());
});
