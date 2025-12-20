# Invite-Only System - Setup Guide

## Quick Start

This guide will help you get the invite-only system up and running.

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database
- Python 3.11+

## Architecture Overview

The invite-only system consists of four microservices:

1. **Waitlist Service** (Port 5010) - Manages waiting list with priority scoring
2. **Invite Code Service** (Port 5011) - Generates and validates invite codes
3. **Referral Service** (Port 5012) - Tracks referrals and quality metrics
4. **Quality Gates Service** (Port 5013) - Monitors system health and controls invite flow

## Installation

### 1. Environment Setup

Create a `.env` file in the root directory:

```bash
# Database configuration
POSTGRES_PASSWORD=your_secure_password

# Optional service URLs (defaults to docker network)
WAITLIST_URL=http://waitlist:5000
INVITES_URL=http://invites:5000
REFERRALS_URL=http://referrals:5000
QUALITY_GATES_URL=http://quality-gates:5000
```

### 2. Database Schema

Initialize the database with the shared schema:

```bash
# Connect to PostgreSQL
psql -U orchestrator -d orchestrator_db

# Run the schema
\i services/shared/schema.sql
```

Or let the services auto-create tables on first run.

### 3. Start Services

```bash
# Start all services
docker-compose up -d waitlist invites referrals quality-gates

# Or start individually
docker-compose up -d waitlist
docker-compose up -d invites
docker-compose up -d referrals
docker-compose up -d quality-gates

# Check service status
docker-compose ps
```

### 4. Verify Services

```bash
# Check health endpoints
curl http://localhost:5010/health  # Waitlist
curl http://localhost:5011/health  # Invites
curl http://localhost:5012/health  # Referrals
curl http://localhost:5013/health  # Quality Gates
```

## API Gateway Integration

The API gateway automatically routes requests to the invite services:

- `/api/waitlist/*` → Waitlist Service
- `/api/invites/*` → Invite Code Service
- `/api/referrals/*` → Referral Service
- `/api/quality/*` → Quality Gates Service

Start the API gateway to access all services through a single endpoint:

```bash
docker-compose up -d api-gateway
```

## Frontend Setup

The landing page is located at `public/join.html`. Serve it with your web server:

### Using Python HTTP Server

```bash
cd public
python3 -m http.server 8080
```

Then visit: http://localhost:8080/join.html

### Using Nginx

Configure nginx to serve the `public` directory and proxy API requests to the API gateway.

## Usage Examples

### Join Waitlist

```bash
curl -X POST http://localhost:8000/api/waitlist/join \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "use_case": "I want to use VoBee for marketing automation",
    "persona": "solo_founder"
  }'
```

Response:
```json
{
  "status": "success",
  "position": 247,
  "total_waiting": 1853,
  "estimated_wait": "2-3 weeks"
}
```

### Generate Invite Codes

```bash
curl -X POST http://localhost:8000/api/invites/generate \
  -H "Content-Type: application/json" \
  -d '{
    "batch_size": 50,
    "batch_id": "BATCH-20251220"
  }'
```

### Redeem Invite Code

```bash
curl -X POST http://localhost:8000/api/invites/redeem \
  -H "Content-Type: application/json" \
  -d '{
    "code": "VOBEE-A7F3E9D2B1C4",
    "email": "user@example.com"
  }'
```

### Track Referral

```bash
curl -X POST http://localhost:8000/api/referrals/share \
  -H "Content-Type: application/json" \
  -d '{
    "inviter_email": "user@example.com",
    "recipient_email": "friend@example.com"
  }'
```

### Check Quality Gates

```bash
curl http://localhost:8000/api/quality/trust-score
```

## Running Tests

Run the test suite to verify everything works:

```bash
# Run all tests
./run_tests.sh

# Or run individual test files
python -m unittest tests.test_waitlist_scoring
python -m unittest tests.test_invite_codes
python -m unittest tests.test_referral_quality
python -m unittest tests.test_quality_gates
```

All 46 tests should pass:
- Waitlist Scoring: 6 tests
- Invite Codes: 11 tests
- Referral Quality: 11 tests
- Quality Gates: 18 tests

## Monitoring

### Service Health

```bash
# Check all service status
curl http://localhost:8000/status
```

### Quality Metrics

```bash
# Get trust score and metrics
curl http://localhost:8000/api/quality/trust-score

# Get active alerts
curl http://localhost:8000/api/quality/alerts
```

### Logs

```bash
# View service logs
docker-compose logs -f waitlist
docker-compose logs -f invites
docker-compose logs -f referrals
docker-compose logs -f quality-gates
```

## Configuration

### Priority Scoring

Adjust priority scores in `services/waitlist/scoring.py`:

```python
persona_scores = {
    'solo_founder': 10,
    'small_team': 15,
    'agency': 20,
    'content_creator': 8,
    'other': 5
}
```

### Code Expiration

Adjust invite code expiration in `services/invites/models.py`:

```python
self.expires_at = expires_at or (self.created_at + timedelta(days=7))
```

### Quality Thresholds

Adjust quality gate thresholds in `services/quality-gates/monitor.py`:

```python
thresholds = {
    'trust_score': 0.7,
    'churn_rate': 0.2
}
```

## Troubleshooting

### Services Won't Start

1. Check Docker is running: `docker ps`
2. Check database connection: `docker-compose logs postgres`
3. Verify environment variables are set
4. Check port conflicts: `netstat -tulpn | grep -E "5010|5011|5012|5013"`

### Database Connection Errors

1. Verify PostgreSQL is running
2. Check DATABASE_URL environment variable
3. Ensure database exists: `createdb orchestrator_db`
4. Run schema initialization: `psql -f services/shared/schema.sql`

### API Errors

1. Check service health: `curl http://localhost:PORT/health`
2. View service logs: `docker-compose logs SERVICE_NAME`
3. Verify API gateway routing: `curl http://localhost:8000/status`

## Documentation

- [Complete System Documentation](docs/INVITE_SYSTEM.md)
- [Referral Mechanics Guide](docs/REFERRAL_MECHANICS.md)
- [Quality Gates Guide](docs/QUALITY_GATES.md)

## Security Notes

1. **Never commit** `.env` files with real credentials
2. Use strong passwords for PostgreSQL
3. Enable HTTPS in production
4. Implement rate limiting on public endpoints
5. Add authentication for admin endpoints
6. Use environment-specific configurations

## Production Deployment

For production deployment:

1. Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
2. Enable SSL/TLS for all connections
3. Set up monitoring and alerting
4. Configure log aggregation
5. Implement backup and disaster recovery
6. Use Kubernetes for orchestration (see `kubernetes/` directory)
7. Set up CI/CD pipelines
8. Enable security scanning

## Support

For issues or questions:
- Check the documentation in `docs/`
- Review test examples in `tests/`
- File an issue on GitHub

## License

See LICENSE file in the repository root.
