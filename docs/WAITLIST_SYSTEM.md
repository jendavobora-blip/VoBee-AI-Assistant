# VoBee Waitlist & Invite-Only System

## Overview

The VoBee waitlist and invite-only system is designed to control user quality and pace of adoption through a controlled growth strategy.

## System Components

### 1. Waitlist Service (Port 5009)

Backend microservice handling all waitlist and invite operations.

**Technology Stack:**
- Python 3.11
- Flask framework
- PostgreSQL database
- SQLAlchemy ORM
- SMTP email integration

### 2. User-Facing Pages

- **`/public/join.html`** - Waitlist signup page
- **`/public/redeem.html`** - Invite code redemption page

### 3. Admin Dashboard

- **`/admin/growth-metrics.html`** - Complete admin control panel

## Getting Started

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# Database
DATABASE_URL=postgresql://waitlist:waitlist@postgres:5432/waitlist_db

# Admin Authentication
ADMIN_TOKEN=your-secure-admin-token-here

# SMTP Configuration
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@vobee.ai
SMTP_PASSWORD=your-smtp-password
FROM_EMAIL=noreply@vobee.ai
FROM_NAME=VoBee Team

# Debug Mode (set to false in production)
EMAIL_DEBUG_MODE=true
DEBUG=false
PORT=5009
```

### Database Setup

The service automatically creates all required database tables on startup:

- `waitlist_entries` - User waitlist entries
- `invite_codes` - Generated invite codes
- `referrals` - Referral tracking
- `user_accounts` - User account data
- `quality_metrics` - System health metrics
- `invite_batches` - Batch generation logs

### Docker Deployment

The service is containerized and can be deployed via Docker Compose:

```yaml
waitlist-service:
  build:
    context: ./services/waitlist-service
    dockerfile: Dockerfile
  ports:
    - "5009:5009"
  environment:
    - DATABASE_URL=postgresql://waitlist:waitlist@postgres:5432/waitlist_db
    - ADMIN_TOKEN=${ADMIN_TOKEN}
    - SMTP_HOST=${SMTP_HOST}
    - SMTP_PORT=${SMTP_PORT}
    - SMTP_USER=${SMTP_USER}
    - SMTP_PASSWORD=${SMTP_PASSWORD}
  depends_on:
    - postgres
  networks:
    - ai-network
  restart: unless-stopped
```

## API Endpoints

### Public Endpoints

#### POST `/api/waitlist/join`

Join the waitlist.

**Request:**
```json
{
  "email": "user@example.com",
  "use_case": "Detailed description of how you plan to use VoBee (min 20 chars)",
  "persona": "solo_founder"
}
```

**Valid personas:** `agency`, `small_team`, `solo_founder`, `content_creator`, `other`

**Response:**
```json
{
  "success": true,
  "position": 42,
  "total_waiting": 150,
  "estimated_wait": "1-2 týdny / 1-2 weeks",
  "priority_score": 15.5
}
```

**Rate Limit:** 10 requests per minute per IP

#### GET `/api/invites/validate/{code}`

Validate an invite code.

**Response:**
```json
{
  "valid": true,
  "issued_to": "user@example.com",
  "expires_at": "2025-12-27T12:00:00"
}
```

#### POST `/api/invites/redeem`

Redeem an invite code and create account.

**Request:**
```json
{
  "code": "VOBEE-ABC123XYZ789",
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "email": "user@example.com",
  "tier": "trial",
  "trial_days": 14
}
```

#### POST `/api/referrals/generate`

Generate personal referral code (requires eligibility).

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "code": "VOBEE-REF456DEF123",
  "expires_at": "2025-12-27T12:00:00",
  "codes_remaining": 2
}
```

#### GET `/api/referrals/stats/{email}`

Get referral statistics for a user.

**Response:**
```json
{
  "codes_earned": 3,
  "codes_available": 2,
  "referral_count": 5,
  "active_referrals": 4,
  "referral_quality_score": 0.8,
  "is_eligible": true
}
```

### Admin Endpoints (Require Authorization Header)

All admin endpoints require: `Authorization: Bearer {ADMIN_TOKEN}`

#### GET `/api/waitlist/stats`

Get comprehensive waitlist statistics.

**Response:**
```json
{
  "total": 150,
  "pending": 120,
  "invited": 25,
  "joined": 5,
  "avg_priority_score": 12.5,
  "by_persona": {
    "agency": {"count": 30, "avg_score": 20.0},
    "small_team": {"count": 45, "avg_score": 15.5},
    "solo_founder": {"count": 50, "avg_score": 10.2},
    "content_creator": {"count": 20, "avg_score": 8.5},
    "other": {"count": 5, "avg_score": 5.0}
  }
}
```

#### POST `/api/invites/generate-batch`

Generate batch of invite codes for top waitlist users.

**Request:**
```json
{
  "batch_size": 50,
  "created_by": "admin@vobee.ai",
  "notes": "Weekly batch release"
}
```

**Response:**
```json
{
  "success": true,
  "batch_id": "BATCH-20251220-120000",
  "generated": 50,
  "codes": [
    {
      "email": "user1@example.com",
      "code": "VOBEE-ABC123XYZ789",
      "expires_at": "2025-12-27 12:00 UTC"
    }
  ]
}
```

#### GET `/api/quality/health`

Get quality gate health metrics.

**Response:**
```json
{
  "trust_score": 0.82,
  "churn_rate": 0.12,
  "dau": 150,
  "mau": 500,
  "feature_adoption_rate": 0.65,
  "paid_conversion_rate": 0.08,
  "referral_quality_score": 0.75,
  "invite_pause_status": false,
  "pause_reasons": []
}
```

#### POST `/api/quality/update`

Update quality metrics.

**Request:**
```json
{
  "dau": 150,
  "mau": 500,
  "feature_adoption_rate": 0.65,
  "paid_conversion_rate": 0.08,
  "referral_quality_score": 0.75
}
```

### Monitoring Endpoint

#### GET `/metrics`

Prometheus-compatible metrics endpoint.

## Priority Scoring Algorithm

Users are prioritized based on:

### Persona Weights
- **Agency:** 20 points
- **Small Team:** 15 points
- **Solo Founder:** 10 points
- **Content Creator:** 8 points
- **Other:** 5 points

### Use Case Quality
- **Detailed (30+ words):** +10 points
- **Moderate (15-29 words):** +5 points
- **High-intent keywords (3+):** +5 points
- **Some keywords (1-2):** +3 points

### Domain Validation
- Disposable/temporary email domains are rejected
- Common patterns checked: tempmail, throwaway, 10minutemail, etc.

## Quality Gates

The system automatically monitors health metrics and pauses invites when quality drops:

### Trust Score Formula

```
trust_score = (DAU/MAU × 0.3) + (feature_adoption × 0.2) + 
              (paid_conversion × 0.3) + (referral_quality × 0.2)
```

### Pause Conditions
- Trust score < 0.75
- 30-day churn rate > 20%

### Resume Conditions
- Trust score > 0.80
- 30-day churn rate < 15%

## Referral System

### Eligibility Requirements

Users become eligible for referral codes when:
1. **14+ days** since trial started
2. **10+ active usage days** recorded
3. Have **available codes** remaining

### Initial Allocation
- New users receive **3 referral codes** upon redemption
- Codes expire after **7 days** if unused

## Email Templates

### Waitlist Confirmation
Sent immediately when user joins waitlist.

**Subject:** `You're on the VoBee waitlist (#position)`

**Content:** Position number, total waiting, estimated wait time

### Invite Ready
Sent when user is selected for batch invite generation.

**Subject:** `Your VoBee invite code is ready`

**Content:** Invite code, redemption instructions, expiration date

## Security Features

### Input Sanitization
- All user-submitted text is sanitized
- XSS prevention on text inputs
- Maximum length limits enforced

### Rate Limiting
- 10 requests/minute per IP on waitlist join
- In-memory storage (consider Redis for production scaling)

### Email Hashing
- User emails are hashed (SHA-256) for analytics
- GDPR-friendly approach to privacy

### Authentication
- Admin endpoints protected by token authentication
- Tokens passed via Authorization header

## Brand Compliance

All UI follows VoBee brand guidelines:

- **Calm authority** tone in copy
- **No hype language** (avoid "revolutionary", "amazing", etc.)
- **Control and quality** emphasis over speed
- **Czech language** option for Czech users
- **Minimal design** matching PWA aesthetic
- **Color scheme:** Primary yellow (#ffc107), dark backgrounds

## Usage Examples

### Join Waitlist (Frontend)

```javascript
const response = await fetch('http://localhost:5009/api/waitlist/join', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    persona: 'agency',
    use_case: 'We need VoBee to automate client reporting and data analysis for our digital marketing agency.'
  })
});

const data = await response.json();
console.log(`Position: #${data.position}`);
```

### Generate Invite Batch (Admin)

```javascript
const response = await fetch('http://localhost:5009/api/invites/generate-batch', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer admin-secret-token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    batch_size: 50,
    created_by: 'admin@vobee.ai',
    notes: 'Weekly release'
  })
});
```

### Redeem Invite Code

```javascript
const response = await fetch('http://localhost:5009/api/invites/redeem', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'VOBEE-ABC123XYZ789',
    email: 'user@example.com',
    password: 'securepass123'
  })
});
```

## Monitoring & Logging

### Health Check
- Endpoint: `GET /health`
- Returns service status

### Prometheus Metrics
- Endpoint: `GET /metrics`
- Tracks waitlist size, invites, users

### Application Logs
All major events are logged:
- Waitlist joins
- Invite generation
- Code redemptions
- Quality gate triggers
- Metric updates

## Troubleshooting

### Service Won't Start
- Check DATABASE_URL is correct
- Verify PostgreSQL is running
- Check port 5009 is available

### Emails Not Sending
- Verify SMTP credentials
- Check EMAIL_DEBUG_MODE setting
- Review application logs
- Test SMTP connection separately

### Quality Gates Triggering
- Review metrics in admin dashboard
- Check DAU/MAU ratio
- Verify churn rate calculation
- Update metrics manually if needed

### Invite Codes Not Working
- Verify code hasn't expired (7 days)
- Check code hasn't been used already
- Ensure code format is correct

## Production Checklist

Before deploying to production:

- [ ] Set strong ADMIN_TOKEN
- [ ] Configure production SMTP credentials
- [ ] Set EMAIL_DEBUG_MODE=false
- [ ] Enable DEBUG=false
- [ ] Configure proper PostgreSQL credentials
- [ ] Set up database backups
- [ ] Configure Redis for rate limiting (optional)
- [ ] Set up SSL/TLS for HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and alerting
- [ ] Review and adjust quality gate thresholds
- [ ] Test email delivery
- [ ] Verify all endpoints with production data

## Support

For issues or questions:
- Check application logs
- Review this documentation
- Contact: Jan Vobora (VoBee Team)

---

**© 2025 VoBee AI Assistant**
