# Security Policy (SECURITY.md)

Home-ERP treats household data privacy and integrity with top priority. Because domestic systems manage personal finances, household member identities, and domestic schedules, stringent security controls are enforced.

## Reporting Vulnerabilities

If you discover a security vulnerability in Home-ERP, please do not disclose it publicly through GitHub issues or social media.

Contact the maintainer directly:
- **Email**: `diego.rivera.estefano@gmail.com`

Provide a detailed description of the vulnerability, reproduction steps, and potential impact. You will receive an acknowledgment within 48 hours.

## Core Security Standards

1. **Household Isolation**:
   - Every database query touching domestic resources must filter strictly by `household_id`.
   - Direct Object Reference (IDOR) attacks are mitigated by validating that the requesting user is an active member of the target household before executing queries or mutations.
2. **Authentication and Sessions**:
   - Secure session cookies (`SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SECURE = True` in production).
   - Password hashing utilizing standard PBKDF2 with SHA256 or Argon2.
3. **Data Protection at Rest**:
   - Sensitive financial account numbers and external tokens must be encrypted at rest using field-level encryption if persisted.
4. **Input Validation and CSRF**:
   - CSRF protection is enforced on all mutation requests (`POST`, `PUT`, `DELETE`).
   - Unpoly requests automatically transmit CSRF tokens via meta tag integration (`<meta name="csrf-token" content="...">` and `up.protocol.config.csrfToken = ...`).
