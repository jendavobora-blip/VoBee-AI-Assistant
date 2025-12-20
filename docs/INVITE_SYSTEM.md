# Invite-Only System Documentation

## Overview

The VoBee invite-only system controls user growth through a multi-stage process combining waitlists, secure invite codes, referral mechanics, and quality gates.

## Architecture

### Components

1. **Waitlist Service** (Port 5010)
   - Manages the waiting list for early access
   - Implements priority scoring algorithm
   - Tracks position and estimated wait times

2. **Invite Code Service** (Port 5011)
   - Generates secure invite codes
   - Validates and redeems codes
   - Tracks code usage and expiration

3. **Referral Service** (Port 5012)
   - Tracks referral chains
   - Calculates referral quality scores
   - Manages reward distribution

4. **Quality Gates Service** (Port 5013)
   - Monitors system health metrics
   - Calculates trust scores
   - Controls invite flow based on thresholds

## API Endpoints

### Waitlist Service

#### Join Waitlist
```
POST /api/waitlist/join
Content-Type: application/json

{
  "email": "user@example.com",
  "use_case": "Marketing automation for my startup",
  "persona": "solo_founder"
}

Response:
{
  "status": "success",
  "position": 247,
  "total_waiting": 1853,
  "estimated_wait": "2-3 weeks"
}
```

#### Get Statistics
```
GET /api/waitlist/stats

Response:
{
  "total": 1853,
  "processed_today": 50
}
```

### Invite Code Service

#### Generate Codes
```
POST /api/invites/generate
Content-Type: application/json

{
  "batch_size": 50,
  "batch_id": "BATCH-20251220"
}

Response:
{
  "status": "success",
  "batch_id": "BATCH-20251220",
  "generated": 50,
  "codes": ["VOBEE-A7F3E9D2B1C4", ...]
}
```

#### Redeem Code
```
POST /api/invites/redeem
Content-Type: application/json

{
  "code": "VOBEE-A7F3E9D2B1C4",
  "email": "user@example.com"
}

Response:
{
  "status": "success",
  "message": "Invite code redeemed successfully",
  "email": "user@example.com"
}
```

#### Check Code Status
```
GET /api/invites/{code}/status

Response:
{
  "valid": true,
  "expires_at": "2025-12-27T00:00:00Z",
  "used": false,
  "status": "active"
}
```

### Referral Service

#### Earn Codes
```
POST /api/referrals/earn
Content-Type: application/json

{
  "user_email": "user@example.com"
}

Response:
{
  "earned": true,
  "codes_available": 3,
  "message": "You earned 3 invite codes"
}
```

#### Share Referral
```
POST /api/referrals/share
Content-Type: application/json

{
  "inviter_email": "user@example.com",
  "recipient_email": "friend@example.com"
}

Response:
{
  "status": "success",
  "referral_id": "uuid",
  "message": "Referral tracked successfully"
}
```

#### Get Quality Metrics
```
GET /api/referrals/{email}/quality

Response:
{
  "referred_count": 5,
  "quality_score": 0.82,
  "rewards": [
    {
      "type": "invite_codes",
      "amount": 3,
      "reason": "First 3 referrals"
    }
  ]
}
```

### Quality Gates Service

#### Get Trust Score
```
GET /api/quality/trust-score

Response:
{
  "trust_score": 0.83,
  "churn_rate": 0.12,
  "fraud_rate": 0.02,
  "engagement_rate": 0.75,
  "invites_paused": false,
  "health_status": "healthy"
}
```

#### Evaluate Gate
```
POST /api/quality/evaluate-gate

Response:
{
  "invites_allowed": true,
  "trust_score": 0.83,
  "metrics": {...},
  "alerts": []
}
```

## Priority Scoring

The waitlist uses a priority scoring algorithm to determine position:

```python
def calculate_priority_score(email, use_case, persona):
    score = 0
    
    # Persona scores
    persona_scores = {
        'solo_founder': 10,
        'small_team': 15,
        'agency': 20,
        'content_creator': 8,
        'other': 5
    }
    score += persona_scores.get(persona, 5)
    
    # Detailed use case bonus
    if len(use_case.split()) > 20:
        score += 10
    
    # Keyword matching bonus
    keywords = ['marketing', 'content', 'automation', 'time']
    if any(word in use_case.lower() for word in keywords):
        score += 5
    
    return score
```

## Code Generation

Invite codes are generated securely:

```python
import secrets
import hashlib

def generate_invite_code():
    random_bytes = secrets.token_bytes(16)
    hash_digest = hashlib.sha256(random_bytes).hexdigest()
    return f"VOBEE-{hash_digest[:12].upper()}"
```

Format: `VOBEE-XXXXXXXXXXXX` (12 hex characters)

## Database Schema

### Waitlist Table
```sql
CREATE TABLE waitlist (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    use_case TEXT NOT NULL,
    persona VARCHAR(50) NOT NULL,
    priority_score INTEGER DEFAULT 0,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invited_at TIMESTAMP
);
```

### Invite Codes Table
```sql
CREATE TABLE invite_codes (
    code VARCHAR(20) PRIMARY KEY,
    issued_to VARCHAR(255),
    batch_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    used_by VARCHAR(255),
    used_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);
```

### Referrals Table
```sql
CREATE TABLE referrals (
    id UUID PRIMARY KEY,
    inviter_email VARCHAR(255) NOT NULL,
    invited_email VARCHAR(255) NOT NULL,
    invite_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

### Environment Variables

**Waitlist Service:**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Invite Codes Service:**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Referrals Service:**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Quality Gates Service:**
(No database required - uses in-memory metrics)

## Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d waitlist invites referrals quality-gates

# Check service health
docker-compose ps

# View logs
docker-compose logs -f waitlist
```

### Using Kubernetes

Services are configured in the main Kubernetes deployment manifests with appropriate resource limits and health checks.

## Monitoring

### Health Checks

All services expose `/health` endpoints:

```
GET http://service:5000/health

Response:
{
  "status": "healthy",
  "service": "service_name",
  "timestamp": "2025-12-20T00:00:00Z"
}
```

### Metrics

Monitor the following metrics:
- Waitlist growth rate
- Invite redemption rate
- Referral conversion rate
- Trust score trends
- Alert frequency

## Security

1. **Invite Codes**: Generated using cryptographically secure random bytes
2. **Validation**: All inputs validated before database insertion
3. **Expiration**: Codes expire after 7 days by default
4. **Rate Limiting**: Consider implementing rate limiting on API endpoints
5. **Database**: Use parameterized queries to prevent SQL injection

## Troubleshooting

### Common Issues

**Database Connection Errors:**
- Verify DATABASE_URL is correctly set
- Ensure PostgreSQL is running
- Check network connectivity

**Invalid Invite Codes:**
- Check code expiration
- Verify code hasn't been used
- Confirm code exists in database

**Waitlist Position Issues:**
- Positions are recalculated based on priority score
- New entries can change existing positions
- Check priority_score calculation

## Future Enhancements

1. Email notification system integration
2. Redis caching for frequently accessed data
3. Advanced analytics dashboard
4. A/B testing for priority scoring
5. Machine learning for fraud detection
6. Webhook support for external integrations
