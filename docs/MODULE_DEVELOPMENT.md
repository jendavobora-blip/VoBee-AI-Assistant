# Module Development Guide

## 🎯 Adding New AI Modules to VoBee

This guide explains how to add new AI modules to the VoBee AI Assistant system.

## 📋 Prerequisites

- Understanding of Docker and containerization
- Python 3.11+ knowledge
- Familiarity with Flask/FastAPI
- Understanding of VoBee architecture

## 🏗️ Module Structure

Every module follows this standard structure:

```
/services/your-module-ai/
├── main.py           # Main service code
├── Dockerfile        # Container configuration
├── requirements.txt  # Python dependencies
└── README.md        # Module documentation
```

## 📝 Step-by-Step Guide

### Step 1: Create Module Directory

```bash
mkdir -p services/your-module-ai
cd services/your-module-ai
```

### Step 2: Create main.py

Use this template:

```python
"""
Your Module AI Service
Features: List your main features here
"""

from flask import Flask, jsonify, request
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class YourModuleAI:
    """Your AI service description"""
    
    def __init__(self):
        self.data = {}
        logger.info("Your Module AI service initialized")
    
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process AI request
        
        Args:
            data: Request data
            
        Returns:
            Processing result
        """
        # Your processing logic here
        return {
            'status': 'processed',
            'result': 'your result',
            'timestamp': datetime.utcnow().isoformat()
        }

# Initialize service
service = YourModuleAI()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint - REQUIRED"""
    return jsonify({
        "status": "healthy",
        "service": "your-module-ai",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/process', methods=['POST'])
def process():
    """Process endpoint - REQUIRED"""
    try:
        data = request.json
        result = service.process_request(data)
        return jsonify({"result": "success", "data": result}), 200
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint - REQUIRED"""
    return jsonify({
        "active": True,
        "version": "1.0.0",
        "capabilities": ["capability1", "capability2"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Step 3: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "main.py"]
```

### Step 4: Create requirements.txt

```
Flask==3.0.0
requests==2.31.0
# Add your specific dependencies here
```

### Step 5: Create README.md

```markdown
# Your Module AI Service

Brief description of what your module does.

## Features

- Feature 1
- Feature 2
- Feature 3

## API Endpoints

### Health Check
\`\`\`bash
GET /health
\`\`\`

### Process Request
\`\`\`bash
POST /process
Content-Type: application/json

{
  "action": "your_action",
  "data": { /* your data */ }
}
\`\`\`

### Service Status
\`\`\`bash
GET /status
\`\`\`

## Usage Example

\`\`\`python
import requests

response = requests.post('http://localhost:5000/process', json={
    'action': 'process',
    'data': {'input': 'your input'}
})

print(response.json())
\`\`\`

## Docker

\`\`\`bash
docker build -t your-module-ai .
docker run -p 5000:5000 your-module-ai
\`\`\`

## Configuration

Environment variables:
- `PORT`: Service port (default: 5000)
- `LOG_LEVEL`: Logging level (default: INFO)
```

### Step 6: Add to docker-compose.yml

```yaml
  your-module-ai:
    build:
      context: ./services/your-module-ai
      dockerfile: Dockerfile
    ports:
      - "5200:5000"  # Use unique external port
    environment:
      - LOG_LEVEL=info
    networks:
      - ai-network
    restart: unless-stopped
```

### Step 7: Add to Kubernetes (optional)

Create deployment in `kubernetes/01-deployments.yaml`:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-module-ai
  namespace: ai-orchestration
spec:
  replicas: 2
  selector:
    matchLabels:
      app: your-module-ai
  template:
    metadata:
      labels:
        app: your-module-ai
    spec:
      containers:
      - name: your-module-ai
        image: ai-orchestration/your-module-ai:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: your-module-ai-service
  namespace: ai-orchestration
spec:
  selector:
    app: your-module-ai
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000
```

### Step 8: Register with Module Manager

The module will be automatically discovered by the module manager. To manually register:

```python
from services.orchestrator.module_manager import module_manager

module_manager.register_module(
    name='your-module-ai',
    category='your_category',  # business, finance, research, communication, creative, technical
    port=5200,
    dependencies=[]
)
```

### Step 9: Test Your Module

```bash
# Test health endpoint
curl http://localhost:5200/health

# Test process endpoint
curl -X POST http://localhost:5200/process \
  -H "Content-Type: application/json" \
  -d '{"action": "test", "data": {}}'

# Test status endpoint
curl http://localhost:5200/status
```

## ✅ Checklist

Before submitting your module:

- [ ] All required endpoints implemented (`/health`, `/process`, `/status`)
- [ ] Dockerfile builds successfully
- [ ] Health check works
- [ ] Process endpoint handles requests
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] README.md documentation complete
- [ ] Module tested locally
- [ ] Added to docker-compose.yml
- [ ] No breaking changes to existing services

## 🎨 Best Practices

### 1. Error Handling
```python
@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Process
        result = service.process_request(data)
        return jsonify({"result": "success", "data": result}), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return jsonify({"error": "Internal server error"}), 500
```

### 2. Logging
```python
# Use structured logging
logger.info(f"Processing request: {data.get('action')}")
logger.error(f"Error occurred: {error}", exc_info=True)
logger.debug(f"Detailed debug info: {details}")
```

### 3. Configuration
```python
import os

class Config:
    PORT = int(os.getenv('PORT', 5000))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
```

### 4. Graceful Shutdown
```python
import signal
import sys

def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    # Clean up resources
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

## 🔒 Security Considerations

1. **Input Validation**: Always validate input data
2. **Rate Limiting**: Implement rate limiting for public endpoints
3. **Authentication**: Add authentication if needed
4. **Secrets**: Never hardcode secrets, use environment variables
5. **CORS**: Configure CORS appropriately

## 📊 Monitoring Integration

Add metrics endpoint (optional but recommended):

```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()
```

## 🧪 Testing

Create tests for your module:

```python
import unittest
import json

class TestYourModule(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_process(self):
        response = self.app.post('/process',
            data=json.dumps({'action': 'test'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [VoBee Architecture](./MASTER_VISION.md)

---

*Last Updated: 2024-01-20*
