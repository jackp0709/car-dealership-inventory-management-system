# Sprint 05 – JWT Authentication

## Objective

Implement the authentication foundation for the Car Dealership Inventory Management System using JWT while maintaining the existing Clean Architecture.

This sprint establishes secure login, token generation, token validation, and authenticated user retrieval.

Registration, user management, authorization, refresh tokens, and other security features are intentionally excluded and belong to later sprints.

---

# Development Mode

You are acting as a Senior Software Engineer working on a production-quality FastAPI application.

Respect the existing architecture and sprint boundaries.

Implement ONLY Sprint 05.

Do not perform any work from Sprint 06 or later.

---

# Approval Policy

Before writing any code:

1. Analyze the repository.
2. Explain the authentication architecture.
3. List every file that will be created.
4. List every file that will be modified.
5. Explain why each modification is required.
6. Wait for approval.

Do not begin implementation until approval is given.

---

# Repository Rules

Current completed work:

- Project initialization
- Database infrastructure
- Application architecture
- User model
- User repository
- Password hashing
- Alembic migration

Do not modify completed architecture.

---

# Sprint Objective

Implement ONLY:

- JWT authentication utilities
- Login endpoint
- Authentication dependency
- Authentication schemas
- Authentication tests

Nothing else.

---

# Allowed Files

Create:

app/core/auth.py

app/api/v1/auth.py

app/schemas/auth.py

app/tests/test_auth.py

Modify:

app/api/v1/router.py

app/core/config.py (ONLY if JWT configuration is missing)

app/core/dependencies.py (ONLY if required)

requirements.txt (ONLY if JWT dependency is missing)

No additional files without approval.

---

# Authentication Requirements

Implement:

- authenticate_user()
- create_access_token()
- verify_token()
- get_current_user()

Responsibilities:

authenticate_user()

- Retrieve user by email
- Verify hashed password

create_access_token()

- Generate JWT
- Include subject
- Include expiration

verify_token()

- Validate JWT signature
- Validate expiration
- Return decoded payload

get_current_user()

- Extract Bearer token
- Verify JWT
- Retrieve authenticated user
- Return generic authentication error if invalid

Do NOT perform authorization or role checking.

---

# JWT Requirements

Use an industry-standard JWT library.

JWT payload must contain:

- sub
- exp

Configuration values must be used for:

- Secret key
- Algorithm
- Expiration time

Do NOT hardcode security values.

---

# API Requirements

Create ONLY:

POST /api/v1/auth/login

Request:

- email
- password

Successful Response:

- access_token
- token_type

No additional endpoints.

---

# Authentication Schemas

Create only:

- LoginRequest
- Token
- TokenData

Do NOT modify existing User schemas.

---

# Error Handling

Return generic authentication errors.

Invalid email:

401 Unauthorized

Invalid password:

401 Unauthorized

Expired token:

401 Unauthorized

Invalid token:

401 Unauthorized

Never expose whether the email or password was incorrect.

---

# Testing

Create tests for:

- Successful login
- Invalid email
- Invalid password
- JWT generation
- JWT validation
- Expired JWT
- Current user dependency

Existing tests must continue passing.

---

# Runtime Verification

Before declaring Sprint 05 complete verify:

- FastAPI starts successfully
- Login endpoint works
- JWT generated successfully
- JWT validated successfully
- Current user dependency works
- Existing health endpoints work
- Existing tests pass
- Authentication tests pass
- No circular imports

---

# Strict Constraints

Do NOT implement:

- Registration
- User CRUD
- Vehicle APIs
- Purchase APIs
- Refresh Tokens
- Logout
- OAuth
- Google Login
- Cookie Authentication
- Email Verification
- Password Reset
- Role-Based Authorization
- Permissions
- Middleware
- Sprint 06 functionality

Stop immediately after Sprint 05.

---

# Completion Report

Provide:

- Files Created
- Files Modified
- Dependencies Added
- Authentication Flow
- Verification Results
- Tests Executed
- Test Results
- API Endpoints Added
- Manual Changes Required
- Risks Found
- Ready for Sprint 06?

Wait for approval before continuing.