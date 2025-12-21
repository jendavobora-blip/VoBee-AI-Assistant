# Vobio AI Studio

> Extremely capable AI system that behaves like one calm, intelligent business partner.

## Features

- **Image Generation**: HDR, PBR rendering, multiple styles
- **Video Generation**: 4K/8K, NeRF support, 30-60 FPS
- **Mock AI Engine**: Runs without GPU, deterministic outputs
- **Electron Desktop App**: Cross-platform (Windows, macOS, Linux)
- **Real-time Progress**: Live updates during generation
- **Cancellation Support**: Stop operations mid-process

## Quick Start

### Backend

```bash
cd vobio-ai-studio/backend
pip install -r requirements.txt
python api_server.py
```

### Frontend

```bash
cd vobio-ai-studio/frontend
npm install
cd electron
npm install
npm start
```

## Architecture

- **Backend**: Python + FastAPI + PyTorch (mock mode)
- **Frontend**: Electron + React
- **IPC**: Secure context-isolated communication
- **AI Engine**: Abstracted, vendor-agnostic

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- 4GB RAM minimum
- Works on CPU (GPU optional)

## API Endpoints

### Backend Server (http://127.0.0.1:8000)

- `GET /health` - Health check
- `GET /gpu-info` - GPU information
- `POST /generate/image` - Generate an image
- `POST /generate/video` - Generate a video
- `GET /progress/{operation_id}` - Get operation progress
- `POST /cancel/{operation_id}` - Cancel an operation

## Configuration

The backend can be configured via environment variables:

- `SERVER_HOST` - Server host (default: 127.0.0.1)
- `SERVER_PORT` - Server port (default: 8000)
- `AI_MAX_RESOLUTION` - Maximum resolution (default: 4K)
- `AI_ENABLE_GPU` - Enable GPU if available (default: true)
- `AI_MOCK_MODE` - Use mock mode (default: true)
- `AI_LOG_LEVEL` - Logging level (default: INFO)

## Monetization (Prepared)

- Feature flags for Free/Pro/Ultra tiers
- 8K, batch, local GPU marked as Ultra-only
- Payment integration ready (not enforced yet)

## Development

### Running Backend Standalone

```bash
cd backend
python api_server.py
```

### Running Frontend Standalone (Development Mode)

```bash
cd frontend
npm start
```

### Building for Production

```bash
cd frontend
npm run build
cd electron
npm run build
```

## Project Structure

```
vobio-ai-studio/
├── backend/
│   ├── ai_engine.py          # Core AI engine with mocks
│   ├── api_server.py          # FastAPI server
│   ├── config.py              # Configuration management
│   ├── utils.py               # Helper functions
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── electron/
│   │   ├── main.js            # Electron main process
│   │   ├── preload.js         # IPC bridge
│   │   └── package.json       # Electron config
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── index.jsx          # React entry point
│   ├── public/
│   │   └── index.html
│   └── package.json           # Frontend dependencies
├── LICENSE                    # Proprietary license
└── README.md                  # This file
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 8000 is available
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't connect to backend
- Ensure backend is running on http://127.0.0.1:8000
- Check CORS settings in api_server.py
- Verify firewall settings

### GPU not detected
- This is normal - the app works fine on CPU
- To enable GPU: ensure PyTorch with CUDA is installed
- Set `AI_ENABLE_GPU=true` in environment

## Author

**Jan Vobora**  
Project: Vobio AI Studio

## License

Proprietary - All Rights Reserved

See [LICENSE](LICENSE) file for details.

## Notes

This application uses mock implementations for AI operations, making it:
- Fully functional without expensive GPU hardware
- Deterministic and predictable for demos
- Ready for production AI engine integration

The architecture is designed to easily swap mock implementations with real AI models when ready.
