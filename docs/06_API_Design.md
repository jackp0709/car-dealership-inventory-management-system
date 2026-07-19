# 1. API Overview

## Purpose

This document defines the API architecture and communication standards for the Car Dealership Inventory Management System.

It serves as the single source of truth for:

- API architecture
- Endpoint design
- Request & response formats
- Authentication & authorization
- Validation rules
- Error handling
- Security standards
- Future API evolution

All backend APIs should follow the standards defined in this document.

---

# API Goals

## Primary Goals

- Build a clean and predictable RESTful API.
- Maintain consistent request and response formats.
- Secure endpoints using JWT authentication.
- Enforce Role-Based Access Control (RBAC).
- Provide clear validation and error messages.
- Keep APIs simple, maintainable, and scalable.
- Follow industry-standard REST practices.

---

## Design Philosophy

The API is designed around business resources rather than actions.

Each endpoint should represent a resource and use standard HTTP methods to perform operations.

Version 1 prioritizes:

- Simplicity
- Consistency
- Security
- Maintainability
- Performance
- Scalability

Features without immediate business value are intentionally deferred instead of partially implemented.

---

## API Scope (Version 1)

Included

- Authentication
- User Management
- Vehicle Management
- Purchase Management
- Sales Management
- Dashboard Statistics
- Vehicle Search
- Health Check

Excluded

- Customer Management
- Payments
- Invoice Management
- Notifications
- Vehicle Images
- Reservation System
- Multi-Branch Support
- Advanced Analytics

These features are planned for future versions.

---

# API Architecture

## Architecture Style

- RESTful API
- Resource-Oriented Design
- Stateless Communication
- JSON Request & Response Format

---

## Base URL

```
/api/v1
```

Example Endpoints

```
POST   /api/v1/auth/login

GET    /api/v1/vehicles

POST   /api/v1/purchases
```

---

## Final Decisions

- REST architecture selected.
- JSON used for all requests and responses.
- JWT used for authentication.
- API versioning starts with `/api/v1`.
- All protected endpoints require authentication.
- All responses follow a common response structure.

---

## Rejected Alternatives

### Action-Based APIs

Examples

```
/createVehicle
/updateVehicle
/deleteVehicle
```

Rejected.

Reason

- Not RESTful.
- Harder to maintain.
- Poor scalability.
- Less consistent with industry standards.

---

### Session-Based Authentication

Rejected.

Reason

- Less suitable for stateless APIs.
- JWT integrates better with React frontend.

---

## Notes for Developers

- Keep endpoints resource-oriented.
- Use appropriate HTTP methods.
- Do not expose internal implementation details through APIs.
- Every new endpoint should follow the standards defined in this document.

# 2. API Design Principles

## Purpose

This section defines the fundamental principles that every API endpoint must follow.

These principles ensure consistency, predictability, maintainability, and adherence to RESTful best practices across the application.

---

# 2.1 RESTful Resource Design

## Final Decisions

- APIs are resource-oriented.
- Endpoints represent nouns, not actions.
- Standard HTTP methods perform operations on resources.
- Resource URLs should remain clean and predictable.

Examples

✅ Good

```
GET    /vehicles
GET    /vehicles/{id}
POST   /vehicles
PUT    /vehicles/{id}
DELETE /vehicles/{id}
```

❌ Avoid

```
/createVehicle
/updateVehicle
/deleteVehicle
/getAllVehicles
```

---

# 2.2 Resource Naming

## Rules

- Use plural resource names.
- Use lowercase letters.
- Use kebab-case only if multiple words are required.
- Do not include verbs in endpoint names.

Examples

```
/vehicles
/users
/purchases
/dashboard
/auth
```

---

# 2.3 HTTP Method Usage

| Method | Purpose |
|---------|---------|
| GET | Retrieve data |
| POST | Create a new resource |
| PUT | Update an existing resource |
| DELETE | Remove an existing resource |

---

## Final Decisions

- GET is read-only.
- POST creates new resources.
- PUT replaces or updates an existing resource.
- DELETE removes allowed resources.
- PATCH is not used in Version 1.

---

## Rejected Alternative

### PATCH Requests

Rejected for Version 1.

Reason

- Adds unnecessary complexity.
- Full updates using PUT are sufficient.
- Easier validation and implementation.

---

# 2.4 Stateless Communication

## Final Decisions

- Every request is independent.
- Server stores no client session.
- Authentication is performed using JWT.
- Client sends JWT with every protected request.

---

# 2.5 Idempotency

## Rules

| Method | Idempotent |
|---------|------------|
| GET | ✅ Yes |
| PUT | ✅ Yes |
| DELETE | ✅ Yes |
| POST | ❌ No |

---

## Notes

Repeated GET, PUT, or DELETE requests should produce the same final result.

POST requests create new resources and therefore are not idempotent.

---

# 2.6 URI Structure

## Rules

- Keep URLs simple.
- Use resource identifiers.
- Avoid deeply nested routes.
- Do not expose internal implementation details.

Examples

```
GET /vehicles
GET /vehicles/{id}
POST /purchases
GET /users
```

---

# 2.7 API Versioning

## Final Decisions

Current Version

```
/api/v1
```

Rules

- Every endpoint belongs to a version.
- Future versions should avoid breaking existing clients.
- New features should be added without affecting Version 1 whenever possible.

---

## Notes for Developers

- Follow REST principles consistently.
- Keep endpoints predictable.
- Prefer simplicity over unnecessary abstraction.
- Every new endpoint must comply with these design principles.

# 3. API Standards

## Purpose

This section defines the common standards that every API endpoint must follow.

These standards ensure consistency between the frontend and backend while simplifying development, testing, and maintenance.

---

# 3.1 Base URL

## Current Version

```
/api/v1
```

Examples

```
POST   /api/v1/auth/login

GET    /api/v1/vehicles

POST   /api/v1/purchases
```

---

## Rules

- Every endpoint must begin with `/api/v1`.
- Future API versions should use a new version prefix.
- Existing API versions should remain backward compatible whenever possible.

---

# 3.2 Content Type

## Request

```
Content-Type: application/json
```

## Response

```
Content-Type: application/json
```

## Accept Header

```
Accept: application/json
```

---

## Final Decisions

- JSON is the only supported data format.
- XML responses are not supported.
- All request and response bodies use UTF-8 encoded JSON.

---

# 3.3 Standard Response Format

## Success Response

Current Version 1 endpoints return the response model directly. For example, vehicle endpoints return the vehicle representation and the login endpoint returns the token representation.

```json
{
    "id": 1,
    "manufacturer": "Example Manufacturer"
}
```

---

## Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": []
}
```

---

## Final Decisions

- Success responses follow their declared response model.
- Error responses use the project's standard `success`, `message`, and `errors` structure.
- Response models remain consistent within each endpoint type.

---

# 3.4 HTTP Status Codes

| Status Code | Purpose |
|-------------|---------|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Resource deleted successfully |
| 400 | Bad request |
| 401 | Authentication required |
| 403 | Access denied |
| 404 | Resource not found |
| 409 | Conflict (Duplicate resource) |
| 422 | Validation failed |
| 500 | Internal server error |

---

## Rules

- Always return the appropriate HTTP status code.
- Do not return `200 OK` for failed operations.
- Use `422` for validation errors.
- Use `409` for duplicate resources (e.g., duplicate VIN or email).

---

# 3.5 Authentication Header

Protected endpoints require the following header:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Rules

- JWT must be included in every protected request.
- Missing or invalid tokens return `401 Unauthorized`.
- Authorization is validated before business logic executes.

---

# 3.6 Pagination Standard

Vehicle listing returns all records in Version 1. Pagination for `GET /vehicles` is intentionally deferred to a future version.

---

# 3.7 Date & Time Format

Standard

```
ISO 8601 (UTC)
```

Example

```json
{
    "created_at": "2026-07-18T14:35:21Z"
}
```

---

## Final Decisions

- All timestamps use ISO 8601.
- Store and transmit timestamps in UTC.
- Frontend is responsible for converting to the user's local timezone if required.

---

# Notes for Developers

- Keep request and response formats consistent.
- Use standard HTTP status codes.
- Never introduce custom response structures.
- Every new endpoint must comply with these API standards.

# 4. Authentication & Authorization

## Purpose

This section defines how users authenticate, how JWT tokens are managed, and how Role-Based Access Control (RBAC) secures the API.

All protected endpoints must follow these authentication and authorization standards.

---

# 4.1 Authentication Strategy

## Selected Method

- JWT (JSON Web Token)

---

## Final Decisions

- JWT is used for authentication.
- API is stateless.
- Server does not maintain user sessions.
- Every protected request must include a valid JWT.
- Public endpoints do not require authentication.

---

## Authentication Flow

```
Login
   ↓
Verify Email & Password
   ↓
Generate JWT
   ↓
Return Token + User Information
   ↓
Frontend Stores Token
   ↓
JWT Sent in Authorization Header
```

---

# 4.2 Login

## Endpoint

```
POST /api/v1/auth/login
```

---

## Authentication Method

- Email
- Password

---

## Success Response

```json
{
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
}
```

---

## Final Decisions

- Login returns JWT.
- Password is never returned.

---

# 4.3 JWT Token

## Token Type

```
Bearer Token
```

---

## Authorization Header

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Token Payload

```
sub
exp
```

---

## Token Expiry

```
Configurable (30 minutes in `.env.example`)
```

---

## Final Decisions

- Only access tokens are implemented.
- Refresh tokens are not included in Version 1.
- Users authenticate again after token expiration.

---

# 4.4 Logout

## Final Decisions

- Logout is handled by the frontend.
- Frontend removes the stored JWT.
- Backend does not blacklist tokens.
- No server-side session exists.

---

# 4.5 Protected Routes

Authentication Required

- User APIs
- Vehicle APIs
- Purchase APIs
- Sales APIs
- Dashboard APIs

Authentication Not Required

- Login
- Health Check
- Initial `POST /users` bootstrap request, only when no users exist

---

# 4.6 Authorization (RBAC)

## Roles

```
ADMIN
EMPLOYEE
```

---

## Admin Permissions

- Manage Users
- Create Vehicles
- Update Vehicles
- Delete Available Vehicles
- View All Vehicles
- View Dashboard
- View Purchase History
- View Sales History

---

## Employee Permissions

- View Available Vehicles
- Search Vehicles
- Record Vehicle Sales (only for the authenticated employee's seller identity)
- View Assigned Dashboard

---

## Final Decisions

- Authorization is role-based.
- Backend always validates permissions.
- Frontend role checks improve UX but do not replace backend authorization.

---

# 4.7 Authentication Failures

| Situation | Status Code |
|------------|-------------|
| Missing Token | 401 |
| Invalid Token | 401 |
| Expired Token | 401 |
| Insufficient Permission | 403 |
| Inactive User | 403 |

---

# 4.8 Security Rules

- Passwords are stored using bcrypt hashing.
- JWT secret key is stored in environment variables.
- Tokens are never logged.
- Passwords are never included in API responses.
- Authorization is validated before executing business logic.

---

## Notes for Developers

- Never trust frontend authorization.
- Always validate JWT before accessing protected resources.
- Keep authentication stateless.
- Do not implement refresh tokens or server-side sessions in Version 1.

# 5. API Modules

This section provides a high-level overview of all API endpoints grouped by module.

---

# 5.1 Authentication APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| POST | /auth/login | Public | Authenticate user |

---

# 5.2 User APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /users | Admin | List all users |
| GET | /users/{id} | Admin | Get user details |
| GET | /users/me | Authenticated | Get current user profile |
| POST | /users | Public when no users exist; Authenticated otherwise | Create user |
| PUT | /users/{id} | Admin | Update user |
| DELETE | /users/{id} | Admin | Deactivate user |

---

## Initial User Bootstrap

When the database contains no users, `POST /api/v1/users` may be called without a JWT to create the initial account. Once a user exists, the endpoint requires a valid Bearer token. Duplicate email addresses return `409 Conflict`.

---

# 5.3 Vehicle APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /vehicles | Admin, Employee | List vehicles |
| GET | /vehicles/{id} | Admin, Employee | Get vehicle details |
| POST | /vehicles | Admin | Add vehicle |
| PUT | /vehicles/{id} | Admin | Update vehicle |
| DELETE | /vehicles/{id} | Admin | Delete available vehicle |

---

# 5.4 Purchase APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /purchases | Admin, Employee | View vehicle acquisition history |
| GET | /purchases/{id} | Admin, Employee | View acquisition details |
| POST | /purchases | Admin | Record a vehicle acquisition |
| PUT | /purchases/{id} | Admin | Update supported acquisition details |
| DELETE | /purchases/{id} | Admin | Delete a vehicle acquisition record |

Purchase APIs represent dealership vehicle acquisitions and do not change a vehicle's sold status.

---

# 5.5 Sales APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /sales | Admin, Employee | View sales history |
| GET | /sales/{id} | Admin, Employee | View sale details |
| POST | /sales | Admin, Employee | Record a sale; employees may only select themselves as seller |
| PUT | /sales/{id} | Admin | Update a sale |
| DELETE | /sales/{id} | Admin | Delete a sale |

Creating a sale validates that the vehicle is available and marks it `SOLD` as part of the operation.

---

# 5.6 Dashboard APIs

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /dashboard/summary | Admin, Employee | Combined dashboard response |
| GET | /dashboard/operational-metrics | Admin, Employee | Vehicle, purchase, and sale counts |
| GET | /dashboard/financial-metrics | Admin, Employee | Purchase cost, sales revenue, and estimated gross profit |
| GET | /dashboard/recent-activity | Admin, Employee | Recent purchases and sales |

---

# 5.7 Health Check API

| Method | Endpoint | Access | Purpose |
|---------|----------|--------|---------|
| GET | /health | Public | Check API availability |

---

## Notes for Developers

- Endpoints follow RESTful conventions.
- All protected endpoints require JWT authentication.
- Endpoint details, validation, and error handling are defined by the implementation.

# 6. Validation & Error Handling

This section defines the validation rules and error response standards used across the API.

---

# 6.1 Validation Rules

| Field | Validation |
|--------|------------|
| Required Fields | Must not be empty |
| Email | Valid email format |
| Password | Minimum 8 characters |
| Vehicle Price | Greater than 0 |
| Manufacturing Year | Valid year |
| VIN | Must be unique |
| Quantity | Positive integer |

---

# 6.2 Standard Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": [
        {
            "field": "email",
            "message": "Invalid email format."
        }
    ]
}
```

---

# 6.3 Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Validation Failed |
| 500 | Internal Server Error |

---

# 6.4 Best Practices

- Validate all input before processing.
- Return meaningful error messages.
- Do not expose sensitive information in responses.
- Log internal errors for debugging purposes.
- Use consistent response formats across all endpoints.

---

## Notes for Developers

- Keep validation rules centralized.
- Prefer clear error messages over generic failures.
- Ensure all APIs follow the same validation and error-handling standards.

# 7. Future Enhancements

The current API is designed to satisfy the project requirements while maintaining simplicity and maintainability. Future versions may include the following enhancements:

- Refresh Token authentication.
- Advanced filtering, sorting, and pagination.
- Customer management module.
- Audit logs for important operations.
- Soft delete and data recovery.
- Rate limiting and API throttling.
- Email notifications and password reset.
- API documentation using Swagger/OpenAPI.

---

## Notes for Developers

- Focus on delivering a stable Version 1 before adding new features.
- Future enhancements should remain backward compatible whenever possible.
- New endpoints must follow the established API standards.
