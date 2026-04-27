# ADR-020: Security and Privacy Design

## Status
Accepted

## Context

Security requirements:
- Private data protection
- No external data leaks
- Credential management
- Access control

## Decision

**Security Principles**:

1. **Data Isolation**
   - All project data local only
   - No cloud uploads
   - Encrypted local storage option

2. **Credential Management**
   - Environment variables for secrets
   - No hardcoded credentials
   - Regular rotation support

3. **Access Control**
   ```python
   class AccessLevel(Enum):
       PUBLIC = 0      # Safe to share
       INTERNAL = 1    # Project members
       RESTRICTED = 2  # Specific roles
       CONFIDENTIAL = 3  # Sensitive
   ```

4. **Audit Logging**
   ```python
   def log_access(action, resource, user):
       audit_log.append({
           "timestamp": now(),
           "action": action,
           "resource": resource,
           "user": user
       })
   ```

**Protected Data Categories**:
- `data/memory_v2/` - Personal memory
- `data/q_values/` - Learning data
- `data/feedback_production/` - User feedback
- `data/reasoning/` - Thought traces

**No-Go Zones**:
- Desktop, Downloads, Documents
- System directories
- External network transmission

## Consequences

### Positive
- Strong privacy protection
- Compliance-ready design
- No accidental data leaks
- Audit trail available

### Negative
- Shared environment complexity
- Backup complexity for protected data
- Recovery procedures more involved

## Implementation
`.workbuddy_security_policy.md`