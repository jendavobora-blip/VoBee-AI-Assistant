# Email AI Service

AI-powered email campaign management and automation service.

## Features

- 📧 **Email Campaign Creation**: Create and manage email campaigns
- 🎯 **Subject Line Optimization**: AI-powered subject line suggestions
- 🧪 **A/B Testing**: Test different email variants
- 🤖 **Automation**: Automated email sequences and triggers

## API Endpoints

### Health Check
```bash
GET /health
```

### Create Campaign
```bash
POST /process
Content-Type: application/json

{
  "action": "create_campaign",
  "subject": "Your subject line",
  "content": "Email content",
  "target_audience": ["segment1", "segment2"],
  "ab_testing": true,
  "optimize_subject": true
}
```

### Run A/B Test
```bash
POST /process
Content-Type: application/json

{
  "action": "ab_test",
  "campaign_id": "campaign_123",
  "variants": [
    {"subject": "Variant A", "content": "Content A"},
    {"subject": "Variant B", "content": "Content B"}
  ]
}
```

### Service Status
```bash
GET /status
```

## Configuration

Set environment variables:
- `PORT`: Service port (default: 5000)

## Example Usage

```python
import requests

# Create campaign
response = requests.post('http://localhost:5000/process', json={
    'action': 'create_campaign',
    'subject': 'Special Offer',
    'content': 'Check out our latest deals!',
    'target_audience': ['customers'],
    'optimize_subject': True
})

print(response.json())
```

## Docker

```bash
docker build -t email-ai .
docker run -p 5000:5000 email-ai
```
