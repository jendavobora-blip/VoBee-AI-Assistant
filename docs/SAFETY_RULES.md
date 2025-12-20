# Safety Rules & Guidelines

## 🔒 Core Safety Principles

VoBee AI Assistant is designed with safety as a top priority. All operations follow strict safety rules to protect users, data, and systems.

## ⚠️ CRITICAL SAFETY RULES

### 1. Finance Operations - READ-ONLY MODE

**Rule**: All financial operations MUST be READ-ONLY by default.

```python
class FinanceAI:
    def __init__(self):
        self.READ_ONLY = True  # ✅ Always True
        self.AUTO_TRANSACTIONS = False  # ✅ Always False
```

**What This Means**:
- ✅ CAN analyze transactions
- ✅ CAN generate reports
- ✅ CAN provide recommendations
- ❌ CANNOT execute transactions
- ❌ CANNOT transfer money
- ❌ CANNOT modify account balances
- ❌ CANNOT make payments

**Affected Services**:
- `finance-ai`: READ-ONLY analysis
- `invoice-ai`: Can generate, NOT send payments
- `budget-ai`: Can plan, NOT execute transfers
- `tax-ai`: Can calculate, NOT file automatically
- `cashflow-ai`: Can project, NOT move funds

**Override Requirements**:
If automatic transactions are needed:
1. Explicit user approval required
2. Transaction preview mandatory
3. Confirmation step required
4. Audit log entry created
5. Rollback mechanism available

### 2. Self-Improvement - SUGGESTIONS ONLY

**Rule**: Self-improvement system NEVER auto-applies changes.

```python
class SelfImprovementSystem:
    def __init__(self):
        self.AUTO_APPLY = False  # ✅ Always False
```

**What This Means**:
- ✅ CAN analyze performance
- ✅ CAN identify bottlenecks
- ✅ CAN suggest optimizations
- ✅ CAN track improvement impact
- ❌ CANNOT auto-apply changes
- ❌ CANNOT modify configurations
- ❌ CANNOT restart services
- ❌ CANNOT change resource allocation

**All Suggestions Require**:
1. Human review
2. Manual approval
3. Controlled implementation
4. Monitoring after changes

### 3. Data Protection

**Rule**: Protect sensitive data at all times.

**Data Classification**:
```
🔴 CRITICAL: Passwords, API keys, financial data
🟡 SENSITIVE: PII, customer data, business secrets
🟢 PUBLIC: Documentation, public APIs
```

**Protection Measures**:
- ✅ Encrypt sensitive data at rest
- ✅ Encrypt data in transit (TLS/SSL)
- ✅ Never log sensitive data
- ✅ Sanitize all inputs
- ✅ Validate all outputs
- ❌ Never store passwords in plain text
- ❌ Never expose API keys in logs
- ❌ Never share data between tenants

### 4. Access Control

**Rule**: Strict role-based access control (RBAC).

**Access Levels**:
```python
ROLES = {
    'admin': ['read', 'write', 'delete', 'configure', 'manage_users'],
    'operator': ['read', 'write', 'configure'],
    'user': ['read', 'write'],
    'viewer': ['read']
}
```

**Protected Operations**:
- Module enable/disable: `admin` only
- Configuration changes: `admin` or `operator`
- Financial operations: Requires additional approval
- Security settings: `admin` only
- User management: `admin` only

### 5. Rate Limiting

**Rule**: Prevent abuse through rate limiting.

**Default Limits**:
```python
RATE_LIMITS = {
    'per_second': 10,    # 10 requests per second
    'per_minute': 100,   # 100 requests per minute
    'per_hour': 1000,    # 1000 requests per hour
    'per_day': 10000     # 10000 requests per day
}
```

**Burst Protection**:
- Token bucket algorithm
- Automatic throttling
- Graceful degradation
- Client notification

### 6. Input Validation

**Rule**: Validate ALL inputs before processing.

**Validation Checklist**:
```python
def validate_input(data):
    # ✅ Check data type
    if not isinstance(data, dict):
        raise ValueError("Invalid data type")
    
    # ✅ Check required fields
    required = ['action', 'data']
    if not all(field in data for field in required):
        raise ValueError("Missing required fields")
    
    # ✅ Sanitize strings
    data['action'] = sanitize_string(data['action'])
    
    # ✅ Validate ranges
    if 'amount' in data:
        if not (0 <= data['amount'] <= MAX_AMOUNT):
            raise ValueError("Amount out of range")
    
    # ✅ Check injection attempts
    if contains_sql_injection(data):
        raise SecurityError("Invalid input detected")
    
    return data
```

### 7. Output Sanitization

**Rule**: Sanitize ALL outputs to prevent XSS/injection.

**Sanitization Steps**:
```python
def sanitize_output(data):
    # ✅ Escape HTML
    if isinstance(data, str):
        data = html.escape(data)
    
    # ✅ Remove sensitive fields
    sensitive_fields = ['password', 'api_key', 'secret']
    for field in sensitive_fields:
        if field in data:
            data[field] = '[REDACTED]'
    
    # ✅ Validate JSON
    try:
        json.dumps(data)
    except:
        raise ValueError("Invalid output format")
    
    return data
```

### 8. Error Handling

**Rule**: Never expose internal details in errors.

**Safe Error Responses**:
```python
# ❌ BAD: Exposes internal details
return {"error": "Database connection failed at 192.168.1.5:5432"}

# ✅ GOOD: Generic user-friendly message
return {"error": "Service temporarily unavailable"}

# ✅ GOOD: With error ID for support
return {
    "error": "Service temporarily unavailable",
    "error_id": "ERR-12345",
    "support": "Contact support@vobee.ai"
}
```

**Error Logging**:
```python
# ✅ Log internally with full details
logger.error(f"Database connection failed: {detailed_error}", 
             exc_info=True, extra={'user_id': user_id})

# ✅ Return safe message to user
return {"error": "Service temporarily unavailable"}
```

## 🔐 Security Best Practices

### 1. Authentication & Authorization

```python
# ✅ Verify authentication
if not is_authenticated(request):
    return jsonify({"error": "Unauthorized"}), 401

# ✅ Check authorization
if not has_permission(user, 'write'):
    return jsonify({"error": "Forbidden"}), 403

# ✅ Validate tokens
if not verify_token(token):
    return jsonify({"error": "Invalid token"}), 401
```

### 2. Secure Communication

```python
# ✅ Use HTTPS/TLS
app.config['PREFERRED_URL_SCHEME'] = 'https'

# ✅ Validate certificates
requests.get(url, verify=True)

# ✅ Use secure headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### 3. Secrets Management

```python
# ❌ BAD: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"

# ✅ GOOD: Environment variables
API_KEY = os.getenv('API_KEY')

# ✅ BETTER: Secrets management service
from secrets_manager import get_secret
API_KEY = get_secret('api_key')
```

### 4. SQL Injection Prevention

```python
# ❌ BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ GOOD: Parameterized queries
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### 5. XSS Prevention

```python
# ❌ BAD: Direct insertion
return f"<div>{user_input}</div>"

# ✅ GOOD: Escape HTML
from html import escape
return f"<div>{escape(user_input)}</div>"

# ✅ BETTER: Use templating engine with auto-escaping
return render_template('page.html', data=user_input)
```

## 📋 Operations Requiring Approval

### Level 1: User Approval Required

- Financial transactions
- Data deletion
- System configuration changes
- User account modifications
- Security setting changes

### Level 2: Admin Approval Required

- Module deployment
- Database schema changes
- Network configuration
- Service restarts
- Backup restoration

### Level 3: Multi-Factor Approval Required

- Production deployments
- Data exports
- Security policy changes
- Emergency access
- System-wide changes

## 🚨 Incident Response

### Security Incident Procedure

1. **Detect**: Automated monitoring alerts
2. **Contain**: Isolate affected systems
3. **Investigate**: Determine scope and impact
4. **Remediate**: Fix vulnerabilities
5. **Recover**: Restore normal operations
6. **Learn**: Update security measures

### Incident Severity Levels

```
🔴 CRITICAL: Active security breach, data loss
🟡 HIGH: Potential breach, service degradation
🟢 MEDIUM: Security warning, minor issues
🔵 LOW: Informational, no immediate threat
```

## 📊 Audit & Compliance

### Audit Logging Requirements

**What to Log**:
- ✅ All authentication attempts
- ✅ All authorization failures
- ✅ Configuration changes
- ✅ Data access (especially sensitive)
- ✅ Financial operations
- ✅ Module enable/disable
- ✅ Error conditions

**What NOT to Log**:
- ❌ Passwords
- ❌ API keys
- ❌ Session tokens
- ❌ Credit card numbers
- ❌ Personal health information

**Log Format**:
```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "event": "module_disabled",
  "user": "admin@vobee.ai",
  "module": "email-ai",
  "reason": "maintenance",
  "ip": "192.168.1.100",
  "session_id": "sess_abc123"
}
```

### Compliance Requirements

- **GDPR**: Right to deletion, data portability
- **SOC 2**: Security controls, audit trails
- **HIPAA**: (if healthcare data) Encryption, access controls
- **PCI DSS**: (if payment data) Secure handling, encryption

## ⚙️ Safe Configuration

### Configuration Best Practices

```python
# ✅ Safe defaults
CONFIG = {
    'finance_read_only': True,        # Always safe mode
    'auto_apply_changes': False,      # Never auto-apply
    'require_approval': True,         # Always require approval
    'log_sensitive_data': False,      # Never log secrets
    'enable_rate_limiting': True,     # Always protect
    'validate_inputs': True,          # Always validate
    'sanitize_outputs': True,         # Always sanitize
}
```

### Configuration Changes

```python
# ✅ Require confirmation
def change_config(key, value):
    if key in CRITICAL_CONFIGS:
        if not confirm_change(key, value):
            raise SecurityError("Change not confirmed")
    
    # Log change
    audit_log.log({
        'action': 'config_change',
        'key': key,
        'old_value': config[key],
        'new_value': value
    })
    
    # Apply change
    config[key] = value
```

## 🛡️ Defense in Depth

### Multiple Layers of Security

```
1. Network Layer: Firewall, VPN, network segmentation
2. Application Layer: Authentication, authorization, validation
3. Data Layer: Encryption, access controls, backups
4. Monitoring Layer: Logging, alerting, anomaly detection
5. Response Layer: Incident response, recovery procedures
```

## 📝 Safety Checklist

Before deploying any new feature:

- [ ] Input validation implemented
- [ ] Output sanitization implemented
- [ ] Error handling without info leakage
- [ ] Authentication & authorization checked
- [ ] Rate limiting configured
- [ ] Audit logging enabled
- [ ] Sensitive data encrypted
- [ ] Secrets properly managed
- [ ] Financial operations READ-ONLY
- [ ] Self-improvement suggestions only
- [ ] Security headers configured
- [ ] SQL injection prevented
- [ ] XSS prevention implemented
- [ ] CSRF tokens used (if web)
- [ ] TLS/HTTPS enforced

---

## 🎯 Summary

**Remember the Core Rules**:

1. 🔒 **Finance = READ-ONLY**: Never auto-execute financial transactions
2. 💡 **Self-Improvement = SUGGESTIONS**: Never auto-apply changes
3. 🔐 **Data = PROTECTED**: Encrypt, validate, sanitize always
4. ✅ **Approval = REQUIRED**: Critical operations need confirmation
5. 📝 **Audit = MANDATORY**: Log everything important
6. 🛡️ **Defense = LAYERED**: Multiple security measures
7. ⚠️ **Errors = SAFE**: Never expose internal details
8. 🔑 **Secrets = SECURE**: Never hardcode or log

**When in Doubt**:
- Choose the safer option
- Require approval rather than auto-execute
- Log the operation
- Test thoroughly
- Document the decision

---

*Last Updated: 2024-01-20*
*Version: 1.0*
