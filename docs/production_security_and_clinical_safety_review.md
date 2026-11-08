# Production security and clinical safety review

**Review type:** Repository-level design/code review performed during implementation.  
**Status:** Preliminary internal review; not an independent penetration test, clinical safety assessment, legal opinion or regulatory determination.  
**Release decision:** **Not approved for production clinical use.** The application deliberately blocks prediction in production.

## Findings addressed on the feature branch

| Finding | Severity before fix | Remediation | Status |
|---|---|---|---|
| Public self-registration assigned the clinician role | Critical | New accounts are viewer-only; clinician/researcher access requires administrator provisioning | Addressed in code |
| Existing self-registered clinician accounts retained broad access | High | Alembic migration demotes prior clinician-role accounts to viewer; administrators must re-authorise legitimate users | Migration added; requires deployment execution and account review |
| API documentation/OpenAPI exposed in production | Medium | Docs, ReDoc and OpenAPI routes disabled when ENVIRONMENT=production | Addressed in code |
| Unvalidated benchmark could be exposed as clinical prediction in production | Critical | Production prediction endpoint returns HTTP 503 until Nigerian external validation and governance gates are completed | Addressed in code |
| Benchmark score bands could be mistaken for clinical risk categories | High | Service now emits a not-clinically-calibrated label; interface renamed to experimental benchmark scoring with explicit warning | Addressed in code |
| Offline queue could be misunderstood as offline clinical inference or patient-record sync | High | Queue stores opaque receipt metadata only; sync API rejects clinical payload fields; interface explicitly says no offline inference | Addressed in code and tests |
| Production rate limiting could be process-local | High | Production settings require Redis/Rediss shared storage | Configuration guard present; deployment verification required |

## Remaining production security blockers

1. **Identity and access:** MFA, email/institutional identity verification, clinician credential verification, account lifecycle/deactivation, token revocation, and an audited break-glass procedure.
2. **Session security:** Review JWT issuer/audience/algorithm policy, key rotation, revocation strategy, token storage (frontend currently uses browser localStorage), and XSS exposure. Consider a backend-for-frontend with Secure, HttpOnly, SameSite cookies if compatible with deployment architecture.
3. **Transport and browser protections:** Enforce HTTPS, HSTS, CSP, frame-ancestors, X-Content-Type-Options, Referrer-Policy and a restrictive Permissions-Policy at the reverse proxy/platform layer.
4. **Infrastructure:** Managed secrets, encrypted managed database and backups, private network access, least-privilege database/service accounts, Redis authentication/TLS, trusted-proxy configuration for accurate rate limits, and tested restore procedures.
5. **Application security:** Independent penetration test, dependency and container scanning, SAST/DAST, threat modelling, abuse-case tests, API schema review, input bounds, and verification of every authorization path.
6. **Audit and incident response:** Centralized access-controlled logs, tamper resistance, retention schedule, alerting, breach-response playbook, and incident-response exercises. Do not log patient-level features or identifiers.
7. **Operational resilience:** Availability monitoring, health checks, backups, disaster recovery, rollback, model artifact integrity/signing, and change-management controls.

## Clinical safety and governance blockers

- No authentic Nigerian hospital cohort or independent external validation is currently available.
- No Nigerian HREC approval, institutional permission, data-use agreement, DPIA or DPO sign-off has been obtained.
- The public Pima benchmark is a historical cohort of adult women of Pima heritage; it cannot validate performance or fairness in Nigerian patients.
- Synthetic shifts are stress tests, not substitutes for real site shift.
- No clinician-led hazard analysis, clinical workflow evaluation, prospective study, human-factors assessment, or post-deployment monitoring plan has been approved.
- Model score and entropy-based abstention are not clinically calibrated; neither is a safe triage threshold.
- Regulatory classification and applicable medical-device obligations must be assessed against the final intended use and claims by qualified local counsel/regulators.

## Mandatory release gates

Prediction must remain disabled in production until all of the following are independently documented and approved:
- HREC and institutional permissions, lawful basis, DPIA/DPO review and signed data-use agreements.
- Verified site provenance and independent temporal/site-held-out validation.
- Prespecified calibration and subgroup acceptance criteria with adequate sample/event counts.
- Clinician-approved intended use, safety case, escalation/override procedure and workflow evaluation.
- Independent security assessment and closure of all high/critical findings.
- Monitoring, incident response, rollback, model versioning and change-control procedures.
- Formal sign-off by the clinical PI, hospital governance, institutional data protection officer and project security owner.

## Scope limitations

This review inspected repository code and configuration. It did not test a deployed environment, inspect cloud IAM/network rules, verify database encryption, execute a penetration test, interview clinicians, or provide legal advice. “Addressed in code” means the branch contains a mitigation; it does not certify the deployed system.
