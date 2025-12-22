# Vobio AI Studio - API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require the `X-User-ID` header:

```bash
curl http://localhost:8000/api/chat \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Endpoints

### Health & Status

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "vobio-api",
  "features": {
    "enable_code_execution": false,
    "enable_image_generation": true,
    "enable_video_generation": true,
    "enable_lifesync": true,
    "enable_human_approval": true,
    "enable_cost_tracking": true,
    "enable_safety_checks": true
  }
}
```

#### GET /api/features

Get feature flag status.

**Response:**
```json
{
  "status": "success",
  "features": {
    "enable_code_execution": false,
    "enable_image_generation": true,
    ...
  }
}
```

---

### Authentication

#### POST /api/auth/login

Mock passkey login (no real authentication in demo mode).

**Request:**
```json
{
  "username": "john_doe",
  "credential_data": {}
}
```

**Response:**
```json
{
  "status": "success",
  "user": {
    "user_id": "user-abc123",
    "username": "john_doe",
    "created_at": "2024-01-15T10:30:00Z",
    "passkey_credential_id": "mock-cred-xyz",
    "public_key": "mock-public-key"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

#### POST /api/auth/logout

Logout current user.

**Headers:**
- `X-User-ID: user123`

**Response:**
```json
{
  "status": "success",
  "message": "Logged out"
}
```

---

### AI Operations

#### POST /api/chat

Chat with AI assistant.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "message": "What's the weather like?"
}
```

**Response:**
```json
{
  "status": "success",
  "type": "chat",
  "message": "I received your message: 'What's the weather like?'. This is a mock AI response.",
  "model": "mock-gpt-4",
  "cost": 0.005
}
```

**Error Response (429 - Rate Limited):**
```json
{
  "detail": "Hourly limit exceeded: $2.00 / $2.00"
}
```

#### POST /api/generate/image

Generate an image from a text prompt.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "prompt": "A beautiful sunset over mountains",
  "style": "realistic"
}
```

**Response:**
```json
{
  "status": "success",
  "type": "image",
  "url": "https://via.placeholder.com/512x512?text=Mock+Image",
  "prompt": "A beautiful sunset over mountains",
  "style": "realistic",
  "model": "mock-stable-diffusion",
  "cost": 0.02
}
```

**Error Response (403 - Feature Disabled):**
```json
{
  "detail": "Image generation is disabled"
}
```

#### POST /api/generate/video

Generate a video from a text prompt.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "prompt": "A cat playing with a ball",
  "duration": 5
}
```

**Response:**
```json
{
  "status": "success",
  "type": "video",
  "url": "https://via.placeholder.com/720x480?text=Mock+Video",
  "prompt": "A cat playing with a ball",
  "duration": 5,
  "model": "mock-runway-gen2",
  "cost": 0.10
}
```

#### POST /api/lifesync/decision

LifeSync decision assistant - get recommendations for life decisions.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "scenario": "Should I change jobs or stay at current company?",
  "options": [
    "Stay at current job",
    "Take new offer at startup",
    "Freelance independently"
  ],
  "user_context": {
    "priority": "financial"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "type": "lifesync_decision",
  "scenario": "Should I change jobs or stay at current company?",
  "recommendation": "Stay at current job",
  "confidence": 0.75,
  "reasoning": "I recommend 'Stay at current job' based on comprehensive analysis. This option scores highest overall (7.45/10) with particular strength in Financial Impact. It clearly outperforms other options by a significant margin.",
  "all_options": [
    {
      "name": "Stay at current job",
      "total_score": 7.45,
      "factors": [
        {
          "name": "Financial Impact",
          "weight": 0.5,
          "value": 0.82,
          "score": 0.41,
          "description": "Economic consequences of this choice"
        },
        ...
      ]
    },
    ...
  ],
  "analysis_timestamp": "2024-01-15T10:30:00Z"
}
```

**User Context Options:**
- `priority`: "financial" | "growth" | "low_risk" | "balanced" (default)

---

### Safety & Validation

#### POST /api/safety/validate-code

Validate code for safety before execution.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "code": "import subprocess\nsubprocess.run(['ls'])"
}
```

**Response (Dangerous Code):**
```json
{
  "safe": false,
  "issues": [
    "Dangerous operation detected: subprocess"
  ],
  "risk_level": "critical",
  "requires_approval": true,
  "approval_request_id": "req-abc123"
}
```

**Response (Safe Code):**
```json
{
  "safe": true,
  "issues": [],
  "risk_level": "safe",
  "requires_approval": false
}
```

---

### Human Approval System

#### GET /api/approvals/pending

Get pending approval requests for the current user.

**Headers:**
- `X-User-ID: user123`

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "requests": [
    {
      "request_id": "req-abc123",
      "user_id": "user123",
      "operation_type": "code_execution",
      "operation_data": {
        "code": "import subprocess..."
      },
      "risk_level": "critical",
      "reason": "Code validation issues: Dangerous operation detected: subprocess",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00Z",
      "expires_at": "2024-01-16T10:30:00Z",
      "reviewed_at": null,
      "reviewed_by": null,
      "review_comment": null
    }
  ]
}
```

#### POST /api/approvals/{request_id}

Approve or reject an approval request.

**Headers:**
- `X-User-ID: reviewer123`

**Request (Approve):**
```json
{
  "action": "approve",
  "comment": "Reviewed and looks safe"
}
```

**Request (Reject):**
```json
{
  "action": "reject",
  "comment": "Too risky"
}
```

**Response:**
```json
{
  "status": "success",
  "action": "approve"
}
```

**Error Response (404):**
```json
{
  "detail": "Request not found or already processed"
}
```

---

### Cost Tracking

#### GET /api/costs/usage

Get current user's cost usage.

**Headers:**
- `X-User-ID: user123`

**Response:**
```json
{
  "user_id": "user123",
  "hourly_usage": 0.15,
  "hourly_limit": 2.0,
  "hourly_remaining": 1.85,
  "hourly_reset_at": "2024-01-15T11:00:00Z",
  "daily_usage": 2.45,
  "daily_limit": 10.0,
  "daily_remaining": 7.55,
  "daily_reset_at": "2024-01-16T00:00:00Z",
  "total_usage": 125.30
}
```

#### GET /api/costs/limits

Check if user can make requests (cost limit check).

**Headers:**
- `X-User-ID: user123`

**Response (Within Limits):**
```json
{
  "allowed": true,
  "reason": null,
  "hourly_usage": 0.15,
  "hourly_limit": 2.0,
  "daily_usage": 2.45,
  "daily_limit": 10.0,
  "total_usage": 125.30
}
```

**Response (Exceeded Limits):**
```json
{
  "allowed": false,
  "reason": "Hourly limit exceeded: $2.00 / $2.00",
  "hourly_usage": 2.0,
  "hourly_limit": 2.0,
  "daily_usage": 2.45,
  "daily_limit": 10.0,
  "total_usage": 125.30
}
```

---

### Memory & Context

#### GET /api/memory/context

Get user's context from memory service.

**Headers:**
- `X-User-ID: user123`

**Response:**
```json
{
  "status": "success",
  "context": "User Context:\n- User prefers detailed explanations\n- Previous conversation about Python programming\n- Asked about machine learning models"
}
```

#### POST /api/memory/store

Store a memory for the user.

**Headers:**
- `X-User-ID: user123`

**Request:**
```json
{
  "content": "User prefers concise responses",
  "metadata": {
    "category": "preference",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Response:**
```json
{
  "status": "success"
}
```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid X-User-ID header |
| 403 | Forbidden | Feature disabled or permission denied |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit or cost limit exceeded |
| 500 | Internal Server Error | Server error |

## Rate Limiting

### Cost-Based Limits

- **Hourly**: $2.00 per user (configurable via `HOURLY_COST_LIMIT`)
- **Daily**: $10.00 per user (configurable via `DAILY_COST_LIMIT`)

### Operation Costs (Mock Mode)

| Operation | Cost |
|-----------|------|
| Chat | $0.005 |
| LifeSync Decision | $0.01 |
| Image Generation | $0.02 |
| Video Generation | $0.10 |

## Mock Mode

By default, the API runs in mock mode:

- No real AI providers called
- Deterministic responses
- No API keys required
- Safe for development/testing

To disable mock mode (requires real AI providers):

```bash
MOCK_MODE=false
```

## Examples

### Complete Chat Flow

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice"}'

# Response includes user_id: "user-abc123"

# 2. Check cost limits
curl http://localhost:8000/api/costs/limits \
  -H "X-User-ID: user-abc123"

# 3. Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "X-User-ID: user-abc123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'

# 4. Check usage
curl http://localhost:8000/api/costs/usage \
  -H "X-User-ID: user-abc123"
```

### LifeSync Decision Flow

```bash
# Get recommendation
curl -X POST http://localhost:8000/api/lifesync/decision \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Buy a house or continue renting?",
    "options": ["Buy house", "Continue renting", "Buy condo"],
    "user_context": {"priority": "financial"}
  }'
```

### Code Safety Check

```bash
# Validate safe code
curl -X POST http://localhost:8000/api/safety/validate-code \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")"}'

# Validate dangerous code
curl -X POST http://localhost:8000/api/safety/validate-code \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{"code": "import subprocess; subprocess.run([\"rm\", \"-rf\", \"/\"])"}'
```

## SDK/Client Libraries

Currently, use HTTP clients:

- **Python**: `requests` or `httpx`
- **JavaScript**: `fetch` or `axios`
- **cURL**: Command line

Example Python client:

```python
import requests

class VobioClient:
    def __init__(self, base_url, user_id):
        self.base_url = base_url
        self.user_id = user_id
    
    def chat(self, message):
        response = requests.post(
            f"{self.base_url}/api/chat",
            headers={"X-User-ID": self.user_id},
            json={"message": message}
        )
        return response.json()

client = VobioClient("http://localhost:8000", "user123")
result = client.chat("Hello!")
print(result)
```

## Observability

### Langfuse Dashboard

View traces and costs at: http://localhost:3000

### Logs

```bash
# View API logs
docker-compose -f vobio-ai-studio/docker-compose.yml logs -f vobio-api

# Filter specific endpoint
docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api | grep "/api/chat"
```

## Support

- **Documentation**: `/vobio-ai-studio/ARCHITECTURE.md`
- **Safety**: `/vobio-ai-studio/SAFETY.md`
- **Issues**: Check Docker logs
- **Health**: GET `/health`
