# Security and offline behaviour

JWT bearer tokens have a configurable expiry. Passwords are hashed with Argon2. Production configuration rejects the development signing key, short signing keys and SQLite; set a unique SECRET_KEY of at least 32 characters, DATABASE_URL for managed PostgreSQL, APP_ENV=production and explicit CORS_ORIGINS. Public registration creates clinician accounts only; role changes are admin-only. Bootstrap the first administrator through backend/scripts/create_admin.py.

Audit events cover registration, login, prediction completion, administrative role changes and sync receipt metadata. Do not log patient feature values, passwords or tokens. Define audit retention, access and tamper-resistance policies before deployment. Add rate limiting, MFA, secret rotation, database migrations and monitoring before production.

The PWA stores only opaque queue IDs, timestamps and sync status in IndexedDB. It performs no offline clinical inference and sends receipt metadata only. Clinical-grade synchronization additionally requires encrypted device storage, idempotent server-side receipt handling, conflict semantics, device management and a privacy/security review.

This repository is a research prototype. Do not submit identifiable patient data or use its predictions to direct care. Production use requires ethics approval, local clinical validation, governance, penetration testing and independent evaluation.