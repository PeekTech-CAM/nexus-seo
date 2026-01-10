# 🔒 NEXUS SEO INTELLIGENCE - Security Implementation Guide

## Executive Summary

This document outlines the comprehensive security architecture, threat model, and implementation details for Nexus SEO Intelligence. **Security is not an afterthought**—it's built into every layer of the application.

---

## 🎯 Security Principles

### Defense in Depth
Multiple layers of security controls ensure that if one layer is compromised, others remain effective.

### Least Privilege
Users and services have only the minimum permissions necessary to perform their functions.

### Zero Trust
Never trust, always verify. All requests are authenticated and authorized regardless of source.

### Fail Securely
When errors occur, the system defaults to denying access rather than granting it.

---

## 🛡️ Threat Model

### Attack Vectors & Mitigations

| Threat | Impact | Mitigation |
|--------|---------|-----------|
| **SQL Injection** | Critical | Parameterized queries, RLS, input validation |
| **XSS (Cross-Site Scripting)** | High | HTML sanitization, CSP headers |
| **CSRF** | High | JWT tokens, SameSite cookies |
| **Credential Stuffing** | High | Rate limiting, 2FA (roadmap) |
| **API Abuse** | Medium | Rate limiting, credit system |
| **Data Leakage** | Critical | RLS policies, encryption at rest |
| **Payment Fraud** | Critical | Stripe's fraud detection, webhook verification |
| **DDoS** | High | Cloudflare protection, rate limiting |
| **Privilege Escalation** | Critical | Role-based access, audit logging |

---

## 🔐 Authentication & Authorization

### Supabase Authentication

```python
# User login with secure session management
def login_user(email: str, password: str) -> Optional[Dict]:
    """
    Authenticate user with Supabase.
    
    Security features:
    - Passwords never stored in plaintext
    - bcrypt hashing (Supabase default)
    - JWT tokens with short expiration
    - Automatic token refresh
    """
    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if result:
            # Store minimal session data
            st.session_state.user = result.user
            st.session_state.token = result.session.access_token
            
            # Log authentication event
            log_auth_event(result.user.id, 'login', success=True)
            
            return result
    except AuthApiError as e:
        log_auth_event(email, 'login', success=False, error=str(e))
        return None
```

### JWT Token Handling

**Token Lifecycle:**
1. User authenticates → JWT issued (1 hour expiration)
2. Token included in Authorization header for API requests
3. Token validated on every request
4. Automatic refresh before expiration
5. Token revoked on logout

```python
def validate_jwt_token(token: str) -> Optional[Dict]:
    """
    Validate JWT token and extract user info.
    
    Security checks:
    - Signature verification
    - Expiration validation
    - Issuer validation
    - Not-before validation
    """
    try:
        # Supabase handles validation internally
        user = supabase.auth.get_user(token)
        
        if not user:
            logger.warning(f"Invalid token used")
            return None
        
        return user
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        return None
```

### Role-Based Access Control (RBAC)

```python
def require_role(allowed_roles: List[str]):
    """
    Decorator to enforce role-based access control.
    
    Usage:
        @require_role(['admin'])
        def admin_only_function():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = st.session_state.get('user')
            
            if not user:
                st.error("Authentication required")
                st.stop()
            
            user_role = get_user_role(user.id)
            
            if user_role not in allowed_roles:
                st.error("Insufficient permissions")
                log_unauthorized_access(user.id, f.__name__)
                st.stop()
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage
@require_role(['admin'])
def view_admin_dashboard():
    st.title("Admin Dashboard")
    # Admin-only content
```

---

## 🗄️ Database Security

### Row Level Security (RLS)

**Why RLS is Critical:**
- Enforced at the database layer
- Cannot be bypassed by application bugs
- Protects against SQL injection
- Prevents horizontal privilege escalation

**Example Policy:**
```sql
-- Users can only view their own scans
CREATE POLICY "Users view own scans"
ON public.scans FOR SELECT
USING (auth.uid() = user_id);

-- Users can only update their own scans
CREATE POLICY "Users update own scans"
ON public.scans FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Admins can view all scans
CREATE POLICY "Admins view all scans"
ON public.scans FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND is_admin = true
    )
);
```

### Encryption

**Data at Rest:**
- Supabase encrypts all data with AES-256
- Database backups encrypted
- Disk-level encryption on storage volumes

**Data in Transit:**
- TLS 1.3 for all connections
- HSTS headers enforced
- Certificate pinning (mobile apps, roadmap)

```python
# Verify SSL certificate
session = requests.Session()
session.verify = True  # Enforce certificate validation

# Use only secure protocols
session.mount('https://', HTTPAdapter(max_retries=3))
```

### SQL Injection Prevention

**ALWAYS use parameterized queries:**

```python
# ✅ SECURE - Parameterized
result = supabase.table('scans').select('*').eq('user_id', user_id).execute()

# ✅ SECURE - Using prepared statements
query = supabase.table('scans').select('*')
query = query.filter('domain', 'eq', domain)
query = query.filter('user_id', 'eq', user_id)
result = query.execute()

# ❌ INSECURE - String concatenation (NEVER DO THIS)
query = f"SELECT * FROM scans WHERE user_id = '{user_id}'"
```

### Audit Logging

```python
def log_sensitive_operation(
    user_id: str,
    operation: str,
    resource_type: str,
    resource_id: str,
    success: bool,
    details: Optional[Dict] = None
):
    """
    Log all sensitive operations for compliance and forensics.
    
    Logged operations:
    - Data access (especially admin access)
    - Permission changes
    - Credit adjustments
    - Payment events
    - Failed authentication attempts
    """
    try:
        supabase.table('audit_logs').insert({
            'user_id': user_id,
            'action': operation,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'success': success,
            'metadata': details or {},
            'ip_address': get_client_ip(),
            'user_agent': get_user_agent(),
            'timestamp': datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        # Log to external service if database insert fails
        logger.critical(f"Failed to log audit event: {e}")
        sentry_sdk.capture_exception(e)
```

---

## 🌐 API Security

### Rate Limiting

**Multiple Layers:**

1. **Application Level (Flask-Limiter):**
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_user_id,  # Rate limit per user, not IP
    storage_uri="redis://localhost:6379",
    default_limits=["1000 per day", "100 per hour"]
)

@app.route('/api/scan')
@limiter.limit("10 per minute")
@require_auth
def create_scan():
    pass
```

2. **Database Level (Trigger):**
```sql
CREATE OR REPLACE FUNCTION check_api_rate_limit()
RETURNS TRIGGER AS $$
DECLARE
    request_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO request_count
    FROM api_requests
    WHERE user_id = NEW.user_id
    AND created_at > NOW() - INTERVAL '1 minute';
    
    IF request_count >= 20 THEN
        RAISE EXCEPTION 'Rate limit exceeded';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

3. **Infrastructure Level (Cloudflare):**
- DDoS protection
- Bot detection
- Geo-blocking (if needed)
- Challenge pages for suspicious traffic

### Input Validation

```python
from validators import url as validate_url
import bleach
import re

class InputValidator:
    """
    Comprehensive input validation for all user inputs.
    """
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL input with security checks.
        
        Checks:
        - Valid URL format
        - No malicious protocols (javascript:, data:, file:)
        - No localhost/internal IPs
        - HTTPS preferred
        """
        # Basic validation
        if not validate_url(url):
            return False, "Invalid URL format"
        
        # Security checks
        parsed = urlparse(url)
        
        # Check for malicious protocols
        if parsed.scheme not in ['http', 'https']:
            return False, "Only HTTP/HTTPS protocols allowed"
        
        # Check for internal/localhost
        if parsed.netloc in ['localhost', '127.0.0.1', '0.0.0.0']:
            return False, "Cannot scan localhost"
        
        # Check for private IP ranges
        if re.match(r'^(10|172\.(1[6-9]|2[0-9]|3[01])|192\.168)\.', parsed.netloc):
            return False, "Cannot scan private IP addresses"
        
        return True, None
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """
        Sanitize HTML content to prevent XSS.
        """
        ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3']
        ALLOWED_ATTRIBUTES = {}
        
        return bleach.clean(
            content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def sanitize_string(s: str, max_length: int = 255) -> str:
        """
        Sanitize general string input.
        """
        # Remove null bytes
        s = s.replace('\x00', '')
        
        # Truncate to max length
        s = s[:max_length]
        
        # Strip whitespace
        s = s.strip()
        
        return s
```

### CORS Configuration

```python
from flask_cors import CORS

# Strict CORS policy
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://app.nexusseo.com",
            "https://nexusseo.com"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 3600
    }
})
```

---

## 💳 Payment Security

### Stripe Integration Best Practices

```python
class SecureStripeService:
    """
    Secure Stripe integration with comprehensive checks.
    """
    
    def verify_webhook_signature(self, payload: bytes, sig_header: str) -> Optional[Dict]:
        """
        Verify Stripe webhook signature using constant-time comparison.
        
        Security: Prevents timing attacks
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                STRIPE_WEBHOOK_SECRET
            )
            return event
        except stripe.error.SignatureVerificationError as e:
            logger.warning(f"Invalid webhook signature: {e}")
            # Log for security monitoring
            self._log_security_event('invalid_webhook_signature', {
                'error': str(e),
                'headers': dict(request.headers)
            })
            return None
    
    def process_webhook_idempotently(self, event: Dict) -> bool:
        """
        Process webhook with idempotency to prevent duplicate processing.
        
        Critical for financial operations.
        """
        event_id = event['id']
        
        # Check if already processed (idempotency)
        existing = self.supabase.table('stripe_events').select('*').eq('id', event_id).execute()
        
        if existing.data and existing.data[0].get('processed'):
            logger.info(f"Event {event_id} already processed, skipping")
            return True
        
        # Store event first (prevents race conditions)
        self.supabase.table('stripe_events').upsert({
            'id': event_id,
            'type': event['type'],
            'data': event,
            'processed': False
        }, on_conflict='id').execute()
        
        # Process event...
        # (processing logic here)
        
        # Mark as processed
        self.supabase.table('stripe_events').update({
            'processed': True,
            'processed_at': datetime.utcnow().isoformat()
        }).eq('id', event_id).execute()
        
        return True
```

### PCI Compliance

**We DON'T handle credit cards directly** - Stripe handles all card data:

✅ **DO:**
- Use Stripe Checkout (hosted payment page)
- Use Stripe Elements for embedded forms
- Store only Stripe customer IDs
- Use Stripe webhooks for payment events

❌ **DON'T:**
- Store credit card numbers
- Store CVV codes
- Handle raw card data
- Log payment details

---

## 🚨 Incident Response

### Security Incident Response Plan

#### Phase 1: Detection (0-1 hour)
1. Automated alerts trigger (failed logins, unusual activity)
2. Security team notified
3. Initial assessment of severity

#### Phase 2: Containment (1-4 hours)
1. Isolate affected systems
2. Revoke compromised credentials
3. Block malicious IPs/users
4. Preserve evidence

#### Phase 3: Eradication (4-24 hours)
1. Identify root cause
2. Patch vulnerabilities
3. Clean compromised systems
4. Verify fix

#### Phase 4: Recovery (24-48 hours)
1. Restore services
2. Monitor for recurrence
3. Validate security controls

#### Phase 5: Post-Incident (48+ hours)
1. Conduct post-mortem
2. Update security policies
3. Notify affected users (if required)
4. Improve defenses

### Security Event Monitoring

```python
class SecurityMonitor:
    """
    Real-time security event monitoring and alerting.
    """
    
    ALERT_THRESHOLDS = {
        'failed_logins': 5,          # 5 failed attempts in 15 minutes
        'api_errors': 50,            # 50 errors in 5 minutes
        'webhook_failures': 10,      # 10 consecutive failures
        'credit_anomaly': 10000,     # 10k credits used in 1 hour
    }
    
    def check_failed_login_threshold(self, user_id: str):
        """
        Alert on suspicious login activity.
        """
        failed_attempts = self.supabase.table('audit_logs').select('*').match({
            'user_id': user_id,
            'action': 'login',
            'success': False
        }).gte('created_at', datetime.utcnow() - timedelta(minutes=15)).execute()
        
        if len(failed_attempts.data) >= self.ALERT_THRESHOLDS['failed_logins']:
            self.trigger_alert('SECURITY_THREAT', {
                'type': 'brute_force_attempt',
                'user_id': user_id,
                'attempts': len(failed_attempts.data)
            })
            
            # Temporarily lock account
            self.lock_account(user_id, duration_minutes=30)
    
    def trigger_alert(self, level: str, details: Dict):
        """
        Send security alert to team.
        """
        logger.critical(f"SECURITY ALERT [{level}]: {details}")
        
        # Send to PagerDuty / Slack / Email
        # notify_security_team(level, details)
        
        # Log to Sentry
        sentry_sdk.capture_message(
            f"Security Alert: {level}",
            level='error',
            extras=details
        )
```

---

## 🔍 Security Checklist

### Pre-Launch Security Audit

- [ ] All environment variables secured (not in code)
- [ ] RLS policies enabled on all tables
- [ ] JWT tokens have short expiration (1 hour)
- [ ] Rate limiting configured on all endpoints
- [ ] Input validation on all user inputs
- [ ] SQL injection protections verified
- [ ] XSS protections tested
- [ ] CORS configured correctly
- [ ] HTTPS enforced (HSTS headers)
- [ ] Webhook signatures verified
- [ ] Idempotency keys implemented for payments
- [ ] Audit logging enabled
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies scanned for vulnerabilities
- [ ] Secrets rotation procedure documented
- [ ] Incident response plan documented
- [ ] Security monitoring configured
- [ ] Backup procedures tested
- [ ] Data retention policies implemented

### Ongoing Security Maintenance

**Weekly:**
- [ ] Review failed login attempts
- [ ] Check error logs for anomalies
- [ ] Monitor API abuse patterns

**Monthly:**
- [ ] Update dependencies
- [ ] Review audit logs
- [ ] Test backup restoration
- [ ] Review access permissions

**Quarterly:**
- [ ] Rotate API keys
- [ ] Security penetration testing
- [ ] Review and update security policies
- [ ] Conduct security training

---

## 📚 Security Resources

### Tools
- **Snyk** - Dependency vulnerability scanning
- **OWASP ZAP** - Web application security testing
- **Burp Suite** - Penetration testing
- **Security Headers** - HTTP security header analysis
- **SSL Labs** - SSL/TLS configuration testing

### Standards & Compliance
- **OWASP Top 10** - Web application security risks
- **PCI DSS** - Payment card industry standards (Stripe handles this)
- **GDPR** - EU data protection regulation
- **CCPA** - California consumer privacy act

### Further Reading
- [OWASP Security Guidelines](https://owasp.org)
- [Stripe Security Best Practices](https://stripe.com/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/platform/security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## 🚀 Next Steps

1. **Implement 2FA** - Add two-factor authentication
2. **Security Headers** - Implement CSP, X-Frame-Options, etc.
3. **WAF** - Deploy Web Application Firewall (Cloudflare)
4. **Penetration Testing** - Hire security firm for audit
5. **Bug Bounty** - Launch bug bounty program

---

**Security is everyone's responsibility. When in doubt, err on the side of caution.**

*Last Updated: 2025-01-03*