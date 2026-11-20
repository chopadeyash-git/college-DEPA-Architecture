# Consent Manager College Registration Prerequisites

**Project:** DEPA Academic Credential Trust & Consent Network  
**Prepared:** 7 November 2026  
**Audience:** Colleges applying to join the Consent Manager (CM) federation

## 1. Purpose

This report defines the institutional, operational, and technical prerequisites a new college should satisfy before it is registered and activated in the CM. It is tailored to this project’s current architecture: the CM is a trust and consent service, while each college remains responsible for its own student records and data exchange service.

The checklist below is a recommended onboarding standard, not a statement of statutory accreditation requirements. The college and CM operator should confirm applicable local education, privacy, and cybersecurity obligations before production use.

## 2. Executive summary

A college should be admitted only after the CM operator has:

1. Verified the institution and its authorized representatives.
2. Agreed the college’s role, permitted exchange purposes, and privacy responsibilities.
3. Received and checked unique organization details, production endpoints, and cryptographic key material.
4. Provisioned a named college administrator and a backend integration credential through a secure process.
5. Completed connectivity, identity, consent, authorization, security, and audit tests.
6. Recorded approval and activated the organization only after the readiness checks pass.

In the current software, an administrator creates an organization in **PENDING** status; only an administrator or super administrator can activate or suspend it. Backend federation endpoints reject organizations that are not **ACTIVE**. However, the application does not itself enforce the full institutional due-diligence checklist in this report.

## 3. Institutional and governance prerequisites

Before technical setup, the college should provide and confirm:

- **Legal identity:** official institution name, registration/accreditation identifier where applicable, country/jurisdiction, official address, and evidence that the institution is authorized to issue or verify academic credentials.
- **Authorized signatory:** name, official title, institutional email, and evidence of authority to accept the federation’s terms.
- **Institutional contact:** an actively monitored organization email address, plus named technical, privacy/data-protection, and incident-response contacts.
- **Federation agreement:** signed participation terms describing permitted purposes, responsibilities, acceptable use, suspension/termination, audit cooperation, and change notification.
- **Privacy and consent:** a documented explanation of how students are identified, informed, asked for consent, shown requested data fields, and given a way to withdraw consent where applicable.
- **Data governance:** a data inventory and field catalogue identifying the records the college may provide, the lawful purpose for each exchange, retention/deletion rules, and who can authorize access.
- **Responsibility boundaries:** confirmation that the college is the custodian of its academic records and that student records are not to be uploaded to or stored by the CM.
- **Risk and incident process:** named 24/7 or business-hours escalation contacts, breach/security incident notification procedure, and a process to suspend the integration or rotate credentials promptly.

## 4. Technical prerequisites

### 4.1 Organization profile and endpoints

The college should supply:

- A unique organization code and institution name.
- An official, monitored contact email.
- Stable production URLs for its login, onboarding, and data-exchange services, as applicable to the integration.
- A documented API specification, supported version, health-check URL, expected request/response formats, timeout limits, and maintenance window.
- A test environment that does not contain real student data, or uses appropriately protected test data.
- Network and DNS details needed for secure connectivity, including outbound/inbound firewall rules and escalation contacts.

All production services should use HTTPS with valid certificates. The current organization registration code validates supplied endpoint URLs as HTTP or HTTPS and rejects embedded user credentials; it does not require that every endpoint be populated or enforce HTTPS-only. HTTPS-only production use is therefore an onboarding requirement recommended by this report, not a current form validation rule.

### 4.2 Identity, credentials, and key management

- Designate at least one named college administrator; use an individual institutional account rather than a shared personal account.
- Provide a separate backend service credential for machine-to-machine access. It should be generated uniquely, shared only through an approved secret-delivery channel, stored in a secrets manager, restricted to the required systems, and rotated/revoked on a documented schedule.
- Generate and register the college’s required public key in the agreed format. Keep the matching private key exclusively within the college’s controlled environment; never send it to the CM.
- Document key ownership, key identifier, expiry/rotation schedule, emergency revocation procedure, and the overlap procedure for in-flight requests.
- Use separate credentials and keys for test and production environments.
- Apply least privilege, strong administrator authentication, secure password storage, and access review for college staff.

The project has a public-key registration/rotation route for authenticated organizations and keeps an old key temporarily for rotation overlap. The organization record also has fields for a public key and service credential. Do not treat putting a value into those fields as proof that key custody, credential delivery, or operational key rotation has been safely completed.

### 4.3 Federation and consent integration

The college’s implementation should demonstrate that it can:

- Authenticate its backend to the CM using the provisioned organization credential.
- Submit and retrieve only requests belonging to the authenticated organization.
- Identify students reliably within the college’s own domain and avoid accepting client-supplied organization or student identifiers as trusted identity claims.
- Present a clear consent request, including requesting institution, purpose, requested fields, and relevant duration or expiry.
- Enforce student approval, rejection, and revocation without bypasses.
- Return only approved fields from the college’s data service; reject or redact all unapproved fields.
- Validate CM-issued authorization artefacts and reject expired, revoked, malformed, or wrong-organization grants.
- Transfer approved academic data directly between colleges over an authenticated encrypted channel. The CM must not receive the academic record payload.
- Handle retries, timeouts, duplicate requests, errors, and key rotation safely and without creating unintended duplicate disclosures.
- Emit useful, privacy-conscious audit events for access and administrative actions.

### 4.4 Operational readiness

- Maintain supported runtime, operating-system, database, and dependency versions, with security updates applied.
- Use a separate college database and service deployment; do not share database credentials or connection pools with the CM or another college.
- Enable encrypted transport, encrypted backups where appropriate, least-privilege database/service accounts, monitoring, and tested recovery procedures.
- Keep secrets out of source control, logs, screenshots, and support tickets.
- Retain audit and application logs under an approved schedule; do not put student record contents, passwords, private keys, or full service credentials in logs.
- Agree service availability, maintenance notification, support ownership, backup/recovery expectations, and a process to notify the CM when endpoints or institutional contacts change.

## 5. Suggested onboarding evidence pack

The college should submit the following to the CM operator through an approved secure channel:

1. Institutional identity/accreditation evidence and official address.
2. Signed participation and data-governance documents.
3. Authorized signatory details and the named administrator/contact list.
4. Privacy notice, consent journey, data inventory, and field-level exchange catalogue.
5. Endpoint and API integration specification, environment details, and network requirements.
6. Public key, key identifier, and key-rotation/revocation plan; **never the private key**.
7. Security contact, incident-response procedure, and recovery/continuity summary.
8. Results of the integration test plan in Section 7, with any exceptions and remediation dates.

The CM application currently records organization profile values; it does not provide a complete document-management or accreditation-verification workflow. The CM operator should retain and review evidence using an approved process outside the organization form until that capability is implemented.

## 6. Recommended onboarding lifecycle

| Stage | Action | Exit condition |
|---|---|---|
| 1. Application | College submits the evidence pack and identifies its provider, consumer, or dual role. | Required evidence received; application owner assigned. |
| 2. Institutional review | CM operator verifies identity, authority, agreements, contacts, purpose, and data responsibilities. | Review approved and recorded; unresolved issues have owners. |
| 3. CM registration | Authorized CM administrator creates the unique organization profile. | Organization exists as **PENDING** with correct details. |
| 4. Provisioning | Deliver administrator access and backend credential securely; register key material and endpoints. | College can authenticate in the test environment; secrets are not exposed. |
| 5. Integration testing | Run the security and functional tests below using test data. | All mandatory tests pass; exceptions formally accepted. |
| 6. Production approval | Review test evidence, contacts, monitoring, incident plan, and production endpoint readiness. | Named approver records the go-live decision. |
| 7. Activation | Authorized CM administrator changes the organization to **ACTIVE**. | Production federation calls work and the audit record is verified. |
| 8. Ongoing review | Periodically review contacts, keys, endpoints, access, incidents, and agreement status. | Changes are recorded; inactive or unsafe organizations are suspended. |

## 7. Go-live acceptance checklist

The CM operator and college should jointly verify each item:

- [ ] Institution and signatory identity verified; participation agreement accepted.
- [ ] Unique organization code, display name, and monitored contact email are correct.
- [ ] Required production endpoints resolve, use HTTPS, and pass certificate validation.
- [ ] Backend credential works only for the registered organization and is not exposed in logs or source control.
- [ ] Public key and key identifier are registered; private-key custody and rotation process are confirmed.
- [ ] An authorized college administrator can access only the appropriate organization functions.
- [ ] A test request identifies the correct student, purpose, fields, and requesting/serving organizations.
- [ ] Unapproved fields are not returned; rejected or revoked consent cannot authorize retrieval.
- [ ] Expired, altered, revoked, or wrong-organization authorization artefacts are rejected.
- [ ] Academic payload flows directly between college systems and is not sent through or persisted by the CM.
- [ ] Audit events are present for registration, activation, consent, grant, revocation, and administrative actions.
- [ ] Rate limits, error handling, monitoring, incident escalation, and credential/key revocation have been tested.
- [ ] Backups and recovery have been tested; service owners and support contacts are recorded.
- [ ] CM approval is recorded and the organization remains **PENDING** until the authorized approver activates it.

## 8. Current CM implementation: what is and is not enforced

The following describes the repository’s current implementation, not a claim that every recommended prerequisite above is already automated:

| Area | Current behavior | Onboarding implication |
|---|---|---|
| Organization creation | `POST /api/admin/organizations`; restricted to administrator/super-administrator roles. Organization code, name, and email are required; duplicate code/email are rejected. | Registration is administrator-mediated, not open public self-registration. |
| Profile fields | Login endpoint, onboarding endpoint, data base URL, public key, and credentials are available as optional organization fields. | Collect the remaining evidence and required integration details through the onboarding process. |
| URL checks | Supplied URLs must have a valid host and use HTTP or HTTPS; embedded user information is rejected. Blank values are accepted. | Perform HTTPS-only and endpoint reachability checks before production. |
| Initial status | A newly created organization is saved as `PENDING`. | Do not assume creation grants production access. |
| Activation/suspension | `PATCH /api/admin/organizations/{id}/activate` and `/suspend`; admin/super-admin authorization is required. | Preserve explicit human approval and record who approved go-live. |
| College administrator | Can be created during organization setup when both admin email and password are supplied, or separately through the admin endpoint. | Provision a named account securely; avoid embedding an initial password in uncontrolled requests or logs. |
| Backend integration | Bridge endpoints authenticate organizations using the stored service credential; inactive organizations are refused. | Provision the credential securely and verify organization scoping in tests. |
| Public-key management | Authenticated organization can register or rotate a public key; the service supports a temporary previous-key overlap. | Include key ID, rotation, custody, and revocation checks in acceptance testing. |
| Student record handling | CM architecture is designed for consent artefacts and trust functions; academic data is exchanged directly between colleges. | Never upload student records as part of organization registration or to the CM. |
| Formal due diligence | There is no complete in-product accreditation evidence, agreement-signing, or go-live checklist workflow. | CM operator must conduct and record those checks separately. |

## 9. Industry-level security and codebase update plan

The current implementation is a useful functional prototype, but the inspected configuration should not be treated as production-ready. The following items are prioritized engineering work for the CM team. They are recommendations based on the current code/configuration, not features already delivered.

### 9.1 Priority 0 — before production onboarding

| Finding in current project | Required code/configuration update | Verification / release gate |
|---|---|---|
| Database password and JWT secret have fallback values in application configuration; the deployment environment file is tracked and contains credentials. | Remove all secret defaults from source-controlled configuration. Load secrets from a production secrets manager or protected deployment environment. Replace tracked environment files with non-secret templates. Treat any committed credential or key as exposed: rotate it, invalidate old values, review repository history and access, and do not merely delete the current copy. | A clean deployment fails fast if required secrets are absent. Secret scanning passes; no production credential remains in Git history or artifacts. |
| Hibernate schema management defaults to `update`. | Add versioned database migrations (for example Flyway or Liquibase); use `validate` or an equivalent non-mutating schema check in production. Review each migration and test both fresh installation and upgrade from the previous release. | Production startup cannot silently create or alter tables. Migration tests pass against the supported PostgreSQL version. |
| CORS accepts any origin pattern while allowing credentials. | Configure an explicit allowlist of the deployed CM frontend origins per environment. Do not combine wildcard origins with credentialed requests. Keep local-development origins in a development-only profile. | Requests from unapproved origins fail browser CORS checks; approved production origins work. |
| Service credentials are stored on the organization record and looked up as raw credential values. | Replace long-lived shared API keys with OAuth 2.0 client credentials or mutually authenticated TLS where feasible. If compatibility requires API keys, issue high-entropy, scoped, rotatable credentials; store a one-way verifier (not the raw secret), show the secret only at issuance, and support revocation and overlap during rotation. Never log the credential. | Tests prove a revoked, expired, wrong-organization, and wrong-scope credential is rejected; credential storage contains no recoverable secret. |
| College public keys are accepted from a generic JSON map and placed in the organization record. | Use a validated request DTO; validate key encoding, algorithm, minimum key size, key ID format, and allowed overlap bounds before persistence. Bind key ownership to the authenticated college. Protect key-update actions with audit events and rate limits. | Invalid, weak, oversized, and out-of-policy keys/overlap values are rejected; valid rotation supports only the documented transition window. |
| Generic exception handling returns `ex.getMessage()` to callers. | Return stable, non-sensitive error codes/messages and a correlation ID. Log full exception details only on the server with secrets and sensitive payloads redacted. Keep validation errors actionable without exposing stack traces, SQL, file paths, tokens, or internal topology. | Error contract tests confirm responses do not disclose exception internals; logs remain useful and redact secrets. |

**Important:** values already committed to source control must be regarded as compromised even if a later commit removes them. Rotate the database password, JWT signing secret, and any service credentials in the applicable environments; invalidate old tokens/keys as appropriate and review access to the repository and deployment artifacts.

### 9.2 Priority 1 — strengthen the production security baseline

1. **Authentication and sessions**
   - Require multi-factor authentication for CM administrators and college administrators; consider federated SSO for institutional staff.
   - Reduce the current 24-hour user JWT lifetime for privileged access; adopt short-lived access tokens and a controlled refresh/re-authentication policy. Support revocation or account-disable enforcement for sensitive operations.
   - Validate issuer, audience, signature algorithm, expiry, and key ID explicitly. Keep authentication-signing keys separate from college assertion keys and data-encryption keys; rotate using a documented overlap and emergency revocation procedure.
   - Do not put credentials in URLs. Use authorization headers over TLS and redact authorization/API-key headers from access and application logs.

2. **Transport and network**
   - Enforce HTTPS at the internet-facing ingress with modern TLS configuration, automatic certificate renewal, and HTTP-to-HTTPS redirection. Configure the application/proxy trust boundary explicitly; trust forwarded headers only from known reverse proxies.
   - Require TLS for PostgreSQL connections across network boundaries and restrict ingress/egress with firewalls or security groups. Expose only necessary service ports; keep the database private.
   - Consider mTLS for service-to-service traffic, or a managed OAuth2 client-credentials flow with narrow scopes, audience restrictions, and credential rotation.

3. **Authorization and organization lifecycle**
   - Make organization activation a gated state transition: evidence review, endpoint/key validation, named approver, successful test evidence, and audit event must all be present before activation.
   - Separate organization registration, approval, activation, suspension, credential issuance, and key rotation permissions. Require a second approver for production activation and high-impact key/credential changes.
   - Enforce organization scoping at every query and mutation, including list, grant, key, and audit endpoints. Add negative authorization tests for cross-organization access.
   - Model provider, consumer, and dual-role capabilities explicitly; issue only the roles/scopes needed for the institution’s approved purpose.

4. **Rate limiting and abuse controls**
   - The existing limiter is an in-memory per-process sliding window and applies one broad threshold to several auth/registration paths. It is not shared across replicas and its state resets on restart.
   - Replace or supplement it with a distributed gateway/Redis limiter. Apply separate thresholds to login, OTP verification/resend, invitation validation, key rotation, and machine-to-machine APIs; key limits by relevant account/organization and network source, with safe lockout and alerting policies.
   - Trust forwarded client IPs only when the request came from configured proxy infrastructure. Add request-size limits, timeouts, concurrency limits, and abuse monitoring.

5. **Application and browser controls**
   - Replace permissive CORS with environment-specific origin allowlists. Add suitable response security headers (for example CSP, HSTS at the HTTPS edge, frame restrictions, content-type protections, and a restrictive referrer policy) and review frontend storage of access tokens.
   - Preserve CSRF protections if browser authentication uses cookies; if authentication is bearer-token-only, document the threat model and ensure tokens are not ambiently sent by browsers.
   - Add request validation for endpoint URLs and key payloads; use a DTO rather than an unbounded generic map. Enforce HTTPS-only public endpoint URLs at production onboarding and verify endpoint ownership/reachability without creating an SSRF-capable arbitrary URL fetcher.

### 9.3 Priority 2 — operational controls and assurance

- **Secrets and keys:** use a managed secrets/KMS or HSM service for production signing keys where available; limit key access to the service identity. Keep private keys out of images, source control, backups accessible to general operators, and logs. A local filesystem key provider is acceptable for development only; production multi-instance deployments need secure shared key lifecycle/rotation that does not depend on mutable local disk.
- **Database:** create a dedicated least-privilege CM database account; prohibit default superuser credentials; encrypt backups, test restore, monitor privileged queries, and define retention/deletion for consent and audit data.
- **Auditability:** record actor, organization, action, timestamp, outcome, and correlation ID for registration, review, activation/suspension, access, consent, key, and credential events. Protect audit records against unauthorized alteration and define retention and access review. Avoid recording student academic payloads or secrets.
- **Monitoring and incident response:** centralize structured logs and metrics; alert on repeated login/OTP failures, unusual key changes, elevated denial rates, unexpected org activity, and service errors. Define incident severity, response owner, credential/key revocation, partner notification, and evidence-preservation procedures.
- **Supply chain:** pin and routinely update dependencies; run software composition analysis and secret scanning in CI; produce an SBOM for releases; scan container images and infrastructure configuration; build signed, reproducible release artifacts where feasible.
- **Resilience:** define service-level objectives, health/readiness probes, backups, disaster recovery targets, capacity limits, and a tested rollback plan. Run more than one CM instance only after shared state, signing keys, rate limiting, and session/token behavior are designed for clustering.
- **Independent assurance:** before production, conduct threat modeling, code review, dependency/container scanning, API authorization testing, and an independent penetration test with written scope and remediation tracking.

### 9.4 Illustrative production configuration

This is a target configuration shape, not a drop-in configuration for every environment. Secret values must come from the deployment secret manager; never paste real secrets into this report, a `.env` committed to Git, or a command transcript.

```properties
# Production profile: deploy only behind the approved HTTPS ingress.
spring.profiles.active=prod
spring.datasource.url=${SPRING_DATASOURCE_URL}
spring.datasource.username=${SPRING_DATASOURCE_USERNAME}
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD}
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.open-in-view=false

# Fail startup when a secret is not provisioned. Do not define a source-code fallback.
app.jwt.secret=${APP_JWT_SECRET}
app.jwt.expiration-ms=${APP_JWT_EXPIRATION_MS}
app.rate-limit.enabled=true
app.rate-limit.trust-proxy-headers=false

# Replace with the exact deployed origins; implement as a typed property used by CORS config.
app.cors.allowed-origins=${APP_CORS_ALLOWED_ORIGINS}
```

The current `SecurityConfig` has CORS configured in Java, so adding a property alone will not change behavior: the configuration must be wired to the CORS bean and tested. Keep local-development settings separate from production and ensure the production process cannot silently fall back to development secrets, schema mutation, or wildcard origins.

### 9.5 Recommended codebase work packages

| Work package | Representative code/config areas | Definition of done |
|---|---|---|
| Secrets and production profiles | `application.properties`, `JwtUtil`, deployment templates, CI secret scanning | No secret fallbacks; required settings validated at startup; compromised values rotated; production and development settings isolated. |
| Database migration control | backend migration resources, `pom.xml`, deployment pipeline | Versioned migrations; production schema validation; clean-install and upgrade tests. |
| CORS, TLS, and headers | `SecurityConfig`, ingress/reverse-proxy configuration | Exact origin allowlist, TLS enforced at edge, proxy trust documented, security headers checked. |
| Machine identity | `Organization`, `BridgeConsentController`, authentication service/repository | Scoped, revocable, rotatable non-recoverable credentials or OAuth2/mTLS; no plaintext credential storage; cross-org denial tests. |
| Onboarding workflow | `OrganizationService`, `AdminController`, organization DTO/entity, CM UI | Required evidence/status tracked; activation guard and dual approval; immutable audit trail; clear pending/rejected/suspended states. |
| Key lifecycle | public-key registration route, `StudentAssertionValidator`, key storage | Strict key validation, authenticated ownership, bounded overlap, safe rotation/revocation, multi-instance-safe production storage. |
| Abuse and error handling | `RateLimitingFilter`, exception advice, API gateway | Distributed route-specific limits; generic client errors with correlation IDs; safe structured logs and alerts. |
| Verification and assurance | backend tests, CI pipeline, deployment checks | AuthN/AuthZ negative tests, security regression suite, SCA/secret scanning, SBOM, documented go-live evidence. |

### 9.6 Endpoint design and sample API contracts

The routes below show how a production onboarding and exchange interface can fit this project. The **Existing project route** column is what was found in the repository. The **Recommended contract** column is a target design; new `/api/v1` routes and controls are not implemented merely by documenting them here.

| Purpose | Existing project route | Recommended contract and controls |
|---|---|---|
| Register institution | `POST /api/admin/organizations` | Keep administrator-mediated registration; validate required organization profile fields and create `PENDING`. Do not expose an unauthenticated public endpoint that can self-activate an institution. |
| Verify key ownership | No challenge/proof-of-possession flow found | Add `POST /api/v1/admin/organizations/{orgId}/key-challenges`, then `POST /api/v1/admin/organizations/{orgId}/keys` with the signed challenge and public JWK. Require admin MFA, second-person approval for production, short challenge expiry, one-time nonce, and an audit record. |
| Activate institution | `PATCH /api/admin/organizations/{id}/activate` | Keep the route admin-only, but enforce all readiness gates server-side and require a distinct second approver for production activation. |
| Create federation data request | `POST /api/bridge/data-requests` | Retain machine authentication; production target is mTLS plus organization scope (or OAuth2 client credentials with restricted audience/scope). Derive caller organization from authenticated identity, never from a trusted request-body field. |
| Retrieve consumer grant | `GET /api/bridge/consumer/data-requests/{id}/grant` | Return only the authenticated consumer’s grant. Return a short-lived access token and grant metadata, not academic data. |
| Publish CM verification key | `GET /api/access-grants/public-key?kid={kid}` | Publish public keys through a cacheable JWKS endpoint such as `GET /.well-known/jwks.json`; pin allowed algorithms and key IDs in verifiers. Do not publish private material. |
| Register/rotate college key | `POST /api/bridge/organizations/public-key` | Replace generic map input with a validated versioned DTO and challenge proof-of-possession. Scope the operation to the authenticated college; reject unknown algorithms, weak/invalid keys, reused IDs, and unbounded overlap periods. |
| Fetch provider data | `POST /api/data/access/{grantId}` (and currently `GET` is also allowed) | Production should allow POST only, require TLS/mTLS and a short-lived CM grant token, verify grant status and exact provider audience, then return only approved fields. Remove or disable the plaintext GET path in production. |
| Verify/revoke access | `GET /api/access-grants/{grantId}/validate`; consent revocation routes exist under CM/college controllers | Keep grant validation server-to-server and authenticated in production; public access should reveal no personal or grant details. Revocation must take effect promptly at the provider, not only in the CM database. |

#### Sample proposed key-enrollment exchange

The challenge routes below are a recommended addition, not existing routes. Both calls use an administrator access token over HTTPS; the final key enrollment must also prove possession of its matching private key.

```http
POST /api/v1/admin/organizations/ORG_123/key-challenges
Authorization: Bearer <admin-access-token>
Content-Type: application/json

{
  "keyPurpose": "student-assertion",
  "algorithm": "RS256"
}
```

```json
{
  "challengeId": "CHG_random-opaque-id",
  "nonce": "base64url-32-random-bytes",
  "expiresAt": "2026-11-07T07:05:00Z"
}
```

The college signs the exact challenge payload (including challenge ID, organization ID, purpose, and expiry) with its private signing key. It then submits only the public key and proof:

```http
POST /api/v1/admin/organizations/ORG_123/keys
Authorization: Bearer <admin-access-token>
Content-Type: application/json

{
  "challengeId": "CHG_random-opaque-id",
  "keyPurpose": "student-assertion",
  "kid": "college-a-assertion-2026-01",
  "publicJwk": {
    "kty": "RSA",
    "use": "sig",
    "alg": "RS256",
    "kid": "college-a-assertion-2026-01",
    "n": "<base64url-modulus>",
    "e": "AQAB"
  },
  "proof": "<detached-signature-over-canonical-challenge>"
}
```

The server must consume the challenge once, confirm it is unexpired and bound to that organization and purpose, verify the signature using the submitted public key, reject duplicate `kid` values, validate key type/size, and audit the result. It must not accept private keys or service secrets in this request. A production activation call should reference the approved onboarding record and be blocked if required key enrollment or other readiness checks are incomplete.

#### Sample data exchange contract

```http
POST /api/data/access/GRANT_123
Authorization: Bearer <short-lived-CM-access-token>
Content-Type: application/json
Accept: application/jose+json
```

The provider validates the token signature against a trusted CM JWKS, pins the expected algorithm, checks `iss`, `aud` (this provider), `exp`, `nbf`, `iat`, `kid`, grant ID, purpose, and approved field scope, and checks current grant/revocation state. It then queries its local student record and returns only the approved fields. The response is an encrypted JWE envelope, not plain academic JSON:

```json
{
  "protected": "<base64url-JWE-protected-header>",
  "encrypted_key": "",
  "iv": "<base64url-96-bit-nonce>",
  "ciphertext": "<base64url-ciphertext>",
  "tag": "<base64url-128-bit-authentication-tag>"
}
```

For `ECDH-ES` direct key agreement, `encrypted_key` is empty and the protected header contains the ephemeral public key (`epk`), `alg: "ECDH-ES"`, `enc: "A256GCM"`, `kid`, and the agreed content type. The consumer decrypts using its own registered private recipient key. The JWE authenticates ciphertext integrity, but does **not** by itself prove who sent the envelope: authenticate the connection with TLS/mTLS and, if the envelope must be verifiable after leaving the TLS channel, sign the exact JWE representation with a separate provider signing key (for example a nested JWS). Never reuse the JWT signing key as an ECDH key.

If the current consumer-ephemeral-key request is retained for compatibility, bind the ephemeral key to the authenticated request and grant, authenticate the provider response with mTLS or a provider signature, include all security-relevant metadata as authenticated data, and reject replayed request IDs. Prefer a reviewed JOSE implementation over custom envelope-crypto code.

### 9.7 Cryptographic algorithm and key profile

Use different keys for different purposes. All keys are per institution and per environment; test keys must never be accepted in production. Public keys may be distributed; private keys remain under the owning service’s control and must never be sent to the CM or another college.

| Purpose | Recommended algorithm/profile | Private-key handling | Rotation and validation |
|---|---|---|---|
| CM-signed data-access JWT | `RS256` with RSA 3072-bit or stronger for compatibility with the current verifier; include `kid`, issuer, exact provider audience, grant ID, purpose, approved field scope, `iat`, `nbf`, and short `exp` (target 5 minutes or less, bounded by grant expiry). | CM-only signing key in KMS/HSM in production; never in source control or a general shared volume. | Publish public keys via JWKS; overlap old public key only until the maximum issued-token lifetime plus clock skew, then remove/revoke. |
| College student assertion | `RS256` with RSA 3072-bit or stronger, distinct key pair per college and environment; include `kid`, issuer/org identity, CM audience, action/target, unique `jti`, `iat`, and `exp` (target 60 seconds). | College-only signing key in KMS/HSM or protected keystore; CM receives only the public key. | Proof-of-possession at enrollment; keep a bounded previous-key overlap; reject unregistered `kid`, expired assertions, wrong audience, and replayed `jti`. |
| Service-to-service authentication | TLS 1.3 with mTLS client certificates where operationally supported; otherwise OAuth 2.0 client credentials using short-lived signed access tokens and narrow audience/scopes. | Private client key in KMS/HSM or managed secret store, not a database field. | Certificate/token rotation and revocation must be automated and tested. Do not use the same secret for student assertions, JWT signing, or encryption. |
| Optional application-layer payload encryption | JWE `ECDH-ES` + `A256GCM`; P-256 (`secp256r1`) recipient key and fresh ephemeral sender key per envelope. Use a maintained JOSE library implementing the standard Concat KDF and protected headers. | Recipient ECDH private key stays at the consuming college; never use an RSA signing key for ECDH. | New ephemeral key per envelope; unique 96-bit GCM nonce per content-encryption key; rotate static recipient key by `kid` and a documented overlap window. |
| TLS channel encryption | TLS 1.3; allow TLS 1.2 only where required by verified partner compatibility and with secure cipher suites. | TLS private keys in managed certificate store; no self-signed production endpoint certificates unless covered by a managed private PKI and trust distribution. | Automated certificate renewal, expiry monitoring, and revocation procedure. |

Use PEM `BEGIN PRIVATE KEY` (PKCS#8) for an exported private key only when a protected keystore/KMS is not available, and PEM `BEGIN PUBLIC KEY` (X.509 SubjectPublicKeyInfo) for public-key exchange. In a JWKS, RSA public values are represented as `n` and `e`; never include `d`, `p`, `q`, or any private CRT values. Treat `kid` as an identifier, not as proof of trust: trust comes from an authenticated enrollment and controlled JWKS/key pinning.

#### Sample Java: provision an RSA signing key pair (development/test only)

Production private keys should be generated and retained by a KMS/HSM. This snippet is only for generating isolated non-production test keys; do not commit generated files.

```java
KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
generator.initialize(3072, SecureRandom.getInstanceStrong());
KeyPair pair = generator.generateKeyPair();

// Keep pair.getPrivate() secret. Export only the public key to the CM
// through the authenticated key-enrollment process.
byte[] privatePkcs8 = pair.getPrivate().getEncoded();
byte[] publicSpki = pair.getPublic().getEncoded();
```

#### Sample Java: sign a short-lived organization assertion with JJWT

The organization code, audience, action, target, key ID, and short expiry must be set by trusted server-side code, not copied from untrusted client claims. This is a signing example, not a complete authentication or replay-protection implementation.

```java
Instant now = Instant.now();
String token = Jwts.builder()
    .header().keyId(keyId).and()
    .issuer(registeredOrganizationCode)
    .subject(studentId)
    .audience().add("consent-manager").and()
    .claim("action", action)
    .claim("targetId", targetId)
    .id(UUID.randomUUID().toString())
    .issuedAt(Date.from(now))
    .notBefore(Date.from(now.minusSeconds(2)))
    .expiration(Date.from(now.plusSeconds(60)))
    .signWith(collegeRsaPrivateKey, Jwts.SIG.RS256)
    .compact();
```

The verifier must select the key by `kid` only from the registered organization’s trusted key set, pin `RS256` (no algorithm fallback), require the expected issuer and audience, validate all time claims, bind the action/target to the current request, and atomically reject a previously seen `jti` until the assertion expires.

JWTs are signed, not encrypted. Keep access-token claims minimal; do not put names, emails, grades, or other direct identifiers in them. Prefer an opaque, purpose-limited student reference and resolve it only inside the authorized provider.

### 9.8 Existing crypto implementation gaps to address

The following observations are specific to the current repository and should be resolved before claiming the sample exchange is production-safe:

- College A and College B currently derive a 16-byte AES key by copying the first bytes of raw ECDH output. Replace this with a standard JOSE implementation (`ECDH-ES`/`A256GCM`) or a reviewed HKDF-SHA-256 design. Never use raw shared-secret bytes directly as an AES key.
- The current ECDH utility requests generic `"EC"` with integer size `256`, rather than explicitly selecting and validating `secp256r1`. It does not show binding of the ephemeral key to authenticated peer identity, key ID, grant, and request. Use a standard envelope format and authenticated transport.
- The current encryption format concatenates a 12-byte GCM nonce with ciphertext/tag, but does not define a versioned interoperable envelope or explicit bounds/validation for decoded input. Prefer JOSE parsing with strict size and algorithm allowlists.
- The current utility uses the platform default charset when converting plaintext to bytes and back. Interoperable JSON encryption must use UTF-8 explicitly.
- `StudentAssertionValidator` contains a shared-secret HS256 fallback when an organization has no RSA public key. Remove this fallback for production assertions; require a registered public key and reject all algorithms other than the configured asymmetric profile.
- The current provider data controller accepts GET as well as POST and can return plain data when encryption input is omitted. Disable the plaintext path for production; test that missing or malformed encryption requirements fail closed.
- The current CM and college key providers persist RSA-2048 private keys on local disk. Upgrade production keys to the profile above and managed KMS/HSM-backed storage; verify permissions, backups, multi-instance behavior, key identifiers, rotation, and revocation.
- The current CM access JWT defaults to a 24-hour lifetime. Set the production lifetime to a short value, never exceed the access grant’s expiry, and ensure maximum token TTL and clock skew are included in key-rotation overlap.

### 9.9 Production go/no-go gates

Do not activate a new college for production until all applicable gates pass:

- No default/committed credentials remain active; rotations and revocations are recorded.
- Production configuration is fail-closed and uses migrations, TLS, least privilege, exact CORS origins, and managed secrets.
- Organization identity, scope, endpoint ownership, key custody, and named contacts have been verified.
- Authentication, authorization, consent, revocation, and cross-organization denial tests pass.
- Security findings from review/testing are triaged; critical/high issues are fixed or explicitly block go-live.
- Monitoring, audit retention, backup/restore, incident response, and partner escalation are operational.
- A named approver records the decision, date, evidence references, accepted residual risks, and rollback/suspension plan.

## 10. Recommendation

Adopt Sections 3–7 as the college onboarding policy and Sections 9.1–9.6 as the technical production-readiness plan. Keep organization creation and activation administrator-controlled, require evidence review and the go/no-go gates before activation, and track each codebase work package to completion. The current repository should be treated as a prototype until the Priority 0 controls are implemented and verified. Revalidate institutional contacts, endpoints, access, and cryptographic keys periodically and whenever the college reports a material change.

---

**Report basis:** review of the project README and Consent Manager organization registration, administration, security, and bridge-integration code. This report is an operational recommendation for the project and should be reviewed by the institution’s legal, privacy, and security owners before production adoption.
