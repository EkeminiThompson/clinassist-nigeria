# Security and offline behaviour

JWT bearer tokens have a configurable expiry. Passwords are hashed with Argon2. Login is limited to five attempts per minute per client IP and public registration to three attempts per hour. Local development uses in-memory rate-limit storage; production configuration requires shared Redis-backed storage so limits work across application workers. Production also rejects the development signing key, short signing keys, SQLite and wildcard CORS; set a unique SECRET_KEY of at least 32 characters, DATABASE_URL for managed PostgreSQL, ENVIRONMENT=production, explicit CORS_ORIGINS and RATE_LIMIT_STORAGE_URI=redis[s]://....

Run Alembic migrations before starting the API, then bootstrap the first administrator through backend/scripts/create_admin.py. Public registration creates clinician accounts only; role changes are admin-only.

Audit events cover registration, login, prediction completion, administrative role changes and sync receipt metadata. Do not log patient feature values, passwords or tokens. Define audit retention, access and tamper-resistance policies before deployment. MFA, secret rotation, monitoring and penetration testing remain production requirements.

The PWA stores only opaque queue IDs, timestamps and sync status in IndexedDB. It performs no offline clinical inference. The sync API accepts only opaque receipt metadata; it rejects clinical payload fields and stores an idempotent per-user receipt protected by a unique constraint. This is not a patient-record synchronization system.

This repository is a research prototype. Do not submit identifiable patient data or use its predictions to direct care. Production use requires ethics approval, local clinical validation, governance and independent evaluation.