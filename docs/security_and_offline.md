# Security and offline behaviour

JWT bearer authentication has configurable expiry; change SECRET_KEY before deployment. Public registration creates clinician accounts only. Roles are admin, clinician, researcher and viewer. Admins alone manage roles. Prediction is limited to admin, clinician and researcher. Bootstrap the first admin through backend/scripts/create_admin.py.

Audit events cover registration, login, prediction completion, admin role changes and offline sync receipt metadata. Do not log patient feature values, passwords or tokens. Define retention and access policies.

The PWA caches the app shell and stores a local queue in IndexedDB. It does not perform offline clinical inference. Reconnection sends record identifiers and timestamps only; no patient features or prediction output are transmitted to the sync endpoint. Clinical-grade sync needs encryption at rest, idempotency, conflict semantics, device management and security review.

Production requires managed PostgreSQL and migrations, HTTPS, rate limits, monitoring, MFA, threat modelling, privacy impact assessment, ethics approval and local clinical validation.
