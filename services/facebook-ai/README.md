# Facebook AI Service

AI-powered social media management for Facebook.

## Features

- 📱 **Content Posting**: Create and schedule social media posts
- 📊 **Engagement Analysis**: Track likes, shares, comments
- 🎯 **Content Optimization**: AI-powered content suggestions
- ⏰ **Smart Scheduling**: Optimal posting times

## API Endpoints

### Health Check
```bash
GET /health
```

### Create Post
```bash
POST /process
Content-Type: application/json

{
  "action": "create_post",
  "content": "Your post content",
  "scheduled_time": "2024-01-01T12:00:00Z"
}
```

### Analyze Engagement
```bash
POST /process
Content-Type: application/json

{
  "action": "analyze_engagement",
  "post_id": "post_123"
}
```

### Service Status
```bash
GET /status
```

## Docker

```bash
docker build -t facebook-ai .
docker run -p 5000:5000 facebook-ai
```
