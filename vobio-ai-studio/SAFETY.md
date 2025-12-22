# Vobio AI Studio - Safety System Documentation

## Overview

The Vobio AI Studio Safety System provides comprehensive protection against malicious or accidental harmful operations. It implements defense-in-depth with multiple layers of validation, sandboxing, and human oversight.

## Core Principles

1. **Fail Secure**: When in doubt, deny the operation
2. **Defense in Depth**: Multiple independent safety checks
3. **Least Privilege**: Minimize permissions by default
4. **Human Oversight**: Critical operations require approval
5. **Audit Trail**: All operations logged for review

## Safety Components

### 1. Code Execution Safety

#### RestrictedPython Validation

All code is validated before execution using RestrictedPython:

```python
# Example: Dangerous code detection
code = """
import subprocess
subprocess.run(['rm', '-rf', '/'])
"""

validation = safety_system.validate_code(code)
# Result: {
#   "safe": False,
#   "risk_level": "critical",
#   "issues": ["Dangerous operation detected: subprocess"],
#   "requires_approval": True
# }
```

#### Risk Levels

- **safe**: No issues detected, can execute immediately
- **medium**: Minor concerns, may require approval
- **high**: Significant risks, requires approval
- **critical**: Extreme danger, block and alert

#### Dangerous Operations Blocked

- `subprocess` module
- `os.system()` calls
- `eval()` and `exec()`
- Dynamic imports with `__import__`
- File system destructive operations
- Network socket operations (unless approved)

### 2. File System Protection

#### Protected Files

The following files cannot be modified or deleted:

```json
{
  "protected_files": [
    "api_server_integrated.py",
    "safety_system.py",
    "feature_gates.py",
    "ai_orchestrator.py",
    "cost_tracker.py",
    "memory_service.py",
    "identity.py",
    ".env",
    "docker-compose.yml"
  ]
}
```

#### Allowed Write Directories

Write operations only permitted in:

- `skills/` - User-created skills and extensions
- `knowledge/` - User knowledge base
- `temp/` - Temporary files
- `logs/` - Application logs

#### File Operation Validation

```python
# Example: Protected file access
result = safety_system.validate_file_operation(
    file_path="/app/safety_system.py",
    operation="write"
)
# Result: {"allowed": False, "reason": "File is protected"}

# Example: Allowed operation
result = safety_system.validate_file_operation(
    file_path="/app/skills/my_skill.py",
    operation="write"
)
# Result: {"allowed": True, "reason": "Operation allowed"}
```

### 3. API Request Safety

#### Input Validation

All API requests validated for:

- **Payload Size**: Maximum 1MB
- **Injection Patterns**: SQL, XSS, command injection
- **Malicious Content**: Scripts, executable code

```python
# Example: XSS prevention
payload = {
    "prompt": "<script>alert('xss')</script>"
}

validation = safety_system.validate_api_call(
    endpoint="/api/generate/image",
    method="POST",
    payload=payload
)
# Result: {
#   "allowed": False,
#   "issues": ["Suspicious pattern detected: <script"]
# }
```

#### Output Sanitization

All outputs sanitized to prevent XSS:

```python
output = "<script>alert('xss')</script>"
safe_output = safety_system.sanitize_output(output)
# Result: "&lt;script&gt;alert('xss')&lt;/script&gt;"
```

### 4. Cost Limits

#### Configurable Thresholds

Environment variables:

```bash
DAILY_COST_LIMIT=10.0      # $10/day per user
HOURLY_COST_LIMIT=2.0      # $2/hour per user
MAX_API_CALLS_PER_MINUTE=10  # Rate limiting
```

#### Limit Enforcement

```python
# Before each operation
limit_check = cost_tracker.check_limits(user_id)

if not limit_check["allowed"]:
    raise HTTPException(
        status_code=429,
        detail=limit_check["reason"]
    )
```

#### Cost Tracking

All operations tracked with Langfuse:

- Operation type
- User ID
- Timestamp
- Cost
- Cumulative hourly/daily totals

### 5. Human Approval System

#### When Approval Required

Operations require human approval when:

1. **Code Execution**: Risk level medium or higher
2. **File Operations**: Writing to non-allowed directories
3. **High Costs**: Single operation > $1
4. **Unusual Patterns**: Detected by safety system

#### Approval Workflow

```
┌─────────────────┐
│ User Request    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Safety Check    │
└────────┬────────┘
         │
   ┌─────┴─────┐
   │           │
   ▼           ▼
[Safe]   [Requires Approval]
   │           │
   │           ▼
   │     ┌──────────────┐
   │     │ Create       │
   │     │ Approval     │
   │     │ Request      │
   │     └──────┬───────┘
   │           │
   │     ┌─────┴─────────┐
   │     │ Wait for      │
   │     │ Human Review  │
   │     │ (24h timeout) │
   │     └─────┬─────────┘
   │           │
   │     ┌─────┴─────┐
   │     │           │
   │     ▼           ▼
   │ [Approved] [Rejected/Expired]
   │     │           │
   │     │           ▼
   │     │      [Block & Log]
   │     │
   ▼     ▼
┌─────────────────┐
│ Execute         │
│ Operation       │
└─────────────────┘
```

#### Approval API

```bash
# Get pending approvals
GET /api/approvals/pending
Headers: X-User-ID: user123

# Approve request
POST /api/approvals/{request_id}
Headers: X-User-ID: reviewer123
Body: {"action": "approve", "comment": "Looks safe"}

# Reject request
POST /api/approvals/{request_id}
Headers: X-User-ID: reviewer123
Body: {"action": "reject", "comment": "Too risky"}
```

### 6. Quarantine System

#### When Files Quarantined

- Failed safety validation
- Contains dangerous code patterns
- Triggered security alerts

#### Quarantine Process

```python
# Automatic quarantine
quarantine_path = safety_system.quarantine_file(
    file_path="/app/skills/suspicious.py",
    reason="Contains subprocess calls"
)
# File moved to: /app/quarantine/suspicious.py.quarantined
```

#### Quarantine Location

- **Directory**: `/app/quarantine/`
- **Naming**: `{original_name}.quarantined`
- **Persistence**: Docker volume `quarantine_volume`

## Emergency Procedures

### 1. Emergency Shutdown

```bash
# Stop all services immediately
./stop.sh

# Or Docker Compose directly
cd vobio-ai-studio
docker-compose down
```

### 2. Disable Feature Flags

```bash
# Edit .env file
ENABLE_CODE_EXECUTION=false
ENABLE_IMAGE_GENERATION=false
ENABLE_VIDEO_GENERATION=false

# Restart services
./start.sh
```

### 3. Clear Cost Limits

Cost limits reset automatically:
- **Hourly**: Every hour
- **Daily**: Every 24 hours

To manually reset, restart the API service:

```bash
docker-compose restart vobio-api
```

### 4. Review Quarantined Files

```bash
# List quarantined files
docker exec vobio-api ls -la /app/quarantine/

# View quarantined file content
docker exec vobio-api cat /app/quarantine/suspicious.py.quarantined

# Remove quarantined file
docker exec vobio-api rm /app/quarantine/suspicious.py.quarantined
```

### 5. Check Safety Logs

```bash
# View API logs
docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api

# Filter for safety events
docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api | grep -i "safety\|quarantine\|blocked"

# Follow logs in real-time
docker-compose -f vobio-ai-studio/docker-compose.yml logs -f vobio-api
```

## Configuration

### Environment Variables

```bash
# Safety System
ENABLE_CODE_EXECUTION=false      # Master switch for code execution
CODE_EXECUTION_TIMEOUT=30        # Max execution time (seconds)

# Cost Limits
DAILY_COST_LIMIT=10.0
HOURLY_COST_LIMIT=2.0
MAX_API_CALLS_PER_MINUTE=10

# Approval System
APPROVAL_TIMEOUT_HOURS=24        # Auto-expire after this time
```

### Protected Files Configuration

Edit `vobio-ai-studio/config/protected_files.json`:

```json
{
  "protected_files": [
    "add_file_here.py"
  ],
  "allowed_write_dirs": [
    "new_dir/"
  ]
}
```

Restart API service for changes to take effect.

## Best Practices

### For Users

1. **Request Minimal Permissions**: Only ask for what you need
2. **Review Code**: Before execution, review generated code
3. **Monitor Costs**: Check usage regularly
4. **Report Issues**: Notify admins of suspicious activity

### For Administrators

1. **Regular Audits**: Review quarantine and logs weekly
2. **Update Protections**: Add new files to protected list
3. **Cost Monitoring**: Adjust limits based on budget
4. **Approval Review**: Process approval requests promptly

### For Developers

1. **Validate Inputs**: Always use Pydantic models
2. **Sanitize Outputs**: Call `safety_system.sanitize_output()`
3. **Check Permissions**: Validate operations before execution
4. **Log Security Events**: Use logger for all safety decisions

## Audit Trail

All safety events logged with:

- **Timestamp**: ISO 8601 format
- **User ID**: Who triggered the event
- **Operation**: What was attempted
- **Decision**: Allowed/blocked/quarantined
- **Reason**: Why the decision was made

Example log entry:

```
2024-01-15T10:30:45 - safety_system - WARNING - File quarantined: /app/skills/hack.py -> /app/quarantine/hack.py.quarantined (Reason: Contains subprocess calls)
```

## Testing Safety

Run safety-specific tests:

```bash
# Test code validation
curl -X POST http://localhost:8000/api/safety/validate-code \
  -H "Content-Type: application/json" \
  -H "X-User-ID: test-user" \
  -d '{"code": "import subprocess"}'

# Expected: {"safe": false, "risk_level": "critical"}
```

## Compliance

The safety system helps meet:

- **GDPR**: User data protection
- **SOC 2**: Security controls
- **ISO 27001**: Information security
- **OWASP Top 10**: Web application security

## Support

For security concerns:

1. Check logs: `docker-compose logs vobio-api`
2. Review quarantine: `/app/quarantine/`
3. Consult documentation: This file
4. Emergency: Run `./stop.sh`
