# Phase 3 - System Architecture

## Purpose

This document defines the overall software architecture of the Car Dealership Inventory Management System.

It establishes how different components interact, defines architectural principles, standard request flows, authentication strategy, module responsibilities, and future scalability considerations.

The objective is to build a maintainable, scalable, secure, and production-quality software architecture while keeping Version 1 focused on assignment requirements.

---

# 1. High-Level System Architecture

The application follows a **Layered Three-Tier Architecture**.

```text
┌────────────────────┐
│ Presentation Layer │
│       React        │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Business Layer    │
│      FastAPI       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│     Data Layer     │
│ PostgreSQL + ORM   │
└────────────────────┘
```

---

## Presentation Layer

Responsible for:

- User Interface
- Forms
- Dashboard
- Client-side Validation
- User Interaction

Not responsible for:

- Business Logic
- Database Access

---

## Business Layer

Responsible for:

- Authentication
- Authorization
- Business Rules
- Inventory Management
- Purchase Management
- Validation
- API Processing

Not responsible for:

- UI Rendering
- Direct Database Operations

---

## Data Layer

Responsible for:

- Data Storage
- Relationships
- Constraints
- Transactions
- Data Persistence

Not responsible for:

- Business Decisions
- Presentation Logic

---

# 2. Architectural Principles

The application follows these architectural principles:

- Layered Three-Tier Architecture
- Separation of Concerns
- Single Responsibility Principle
- Defense in Depth
- Security by Default
- Business Logic centralized in Services
- Repository-only database access
- Future-ready modular design
- Simplicity over unnecessary complexity

---

# 3. Layer Communication Rules

Application flow:

```text
React

↓

FastAPI Routes

↓

Service Layer

↓

Repository Layer

↓

Database
```

Rules:

- Every layer communicates only with the layer directly below it.
- Routes never communicate directly with the database.
- Business logic exists only in Services.
- Repositories only perform data access.
- Frontend never communicates directly with the database.

---

# 4. Backend Module Architecture

The backend follows a Hybrid Architecture.

Modules:

- Authentication
- User Management
- Vehicle Management
- Purchase Management
- Dashboard
- Health Check

Search functionality is implemented within the Vehicle Management module.

Future modules:

- Customer Management
- Reports
- Reservations
- Payments
- Notifications
- Multi-Branch Management

---

## Module Responsibilities

### Authentication

- Login
- JWT Generation
- Password Verification
- Token Validation

---

### User Management

- Employee Registration
- Employee Management
- Role Assignment

---

### Vehicle Management

- Vehicle CRUD
- Inventory Management
- Vehicle Status
- Search Operations

---

### Purchase Management

- Vehicle Purchase
- Customer Information
- Purchase Records
- Inventory Update

---

### Dashboard

- Statistics
- Recent Vehicles
- Low Stock Summary
- Inventory Overview

---

### Health Check

- API Status
- Deployment Monitoring

---

# 5. Frontend Module Architecture

Frontend follows a Hybrid Architecture.

Structure:

- Pages
- Components
- Layouts
- API Layer
- Zustand Store
- Hooks
- Services
- Utilities

---

## Layouts

### Auth Layout

Login-related pages.

---

### Admin Layout

Admin dashboard with complete navigation.

---

### Employee Layout

Restricted navigation based on role.

---

## State Management

Global state stores:

- JWT Token
- Logged-in User
- User Role
- Authentication Status

Local component state stores:

- Form Data
- Search Filters
- Pagination
- UI State

---

# 6. Authentication & Authorization Flow

Authentication process:

```text
User Login

↓

FastAPI Authentication

↓

Password Verification

↓

JWT Generation

↓

Return Token

↓

Frontend Stores Token

↓

Redirect to Dashboard
```

---

## JWT Strategy

JWT contains:

- User ID
- Email
- Role
- Expiration Time

JWT never contains:

- Password
- Sensitive Information

---

## Authentication Decisions

- JWT Authentication
- Local Storage for Version 1
- bcrypt Password Hashing
- 60-minute Token Expiration
- No Refresh Tokens in Version 1

---

## Authorization

Roles:

- ADMIN
- EMPLOYEE

Authorization is enforced on every protected endpoint.

Backend remains the final authority for permission checks.

---

# 7. Standard Request Lifecycle

Every request follows the same lifecycle.

```text
React

↓

Axios

↓

FastAPI Route

↓

Authentication

↓

Authorization

↓

Validation

↓

Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

Response

↓

Frontend
```

---

## Request Principles

- Thin Routes
- Business Logic in Services
- Repository Pattern
- Validation before Business Logic
- Standard API Responses
- Transactional Operations

---

# 8. Error & Validation Strategy

Validation occurs at three layers.

Layer 1

Frontend Validation

- Required Fields
- User Experience Validation

---

Layer 2

Backend Validation

- Pydantic Validation
- Business Validation

---

Layer 3

Database Validation

- Unique Constraints
- Foreign Keys
- NOT NULL Constraints

---

## Error Categories

| Type | HTTP Status |
|------|-------------|
| Validation Error | 422 |
| Authentication Error | 401 |
| Authorization Error | 403 |
| Resource Not Found | 404 |
| Business Rule Violation | 409 |
| Internal Server Error | 500 |

---

## Logging

Application logging uses:

- INFO
- WARNING
- ERROR

---

## Exception Strategy

Global Exception Handler

Custom Exception Hierarchy

Consistent JSON Error Responses

No internal implementation details exposed to users.

---

# 9. Scalability Strategy

Version 1 supports:

- Modular Architecture
- Stateless Authentication
- Pagination
- Database Indexing
- Future Feature Expansion

---

Future expansion:

- Multi-Branch Support
- Customer Management
- Reservation System
- Reports
- AI Features
- Notifications

Architecture is intentionally designed to support these additions without major restructuring.

---

# 10. Architecture Readiness

| Capability | Status |
|------------|--------|
| Multiple Users | ✅ |
| Large Inventory | ✅ |
| Modular Expansion | ✅ |
| Database Growth | ✅ |
| Docker Deployment | ✅ |
| Multi-Branch | Future Version |
| High Availability | Future Version |
| Horizontal Scaling | Future Version |

---

# Phase 3 Summary

The system follows a Layered Three-Tier Architecture combined with a Hybrid Backend and Frontend Architecture.

Business logic is isolated within Services, database access is centralized through Repositories, and authentication is implemented using JWT with Role-Based Access Control.

The architecture emphasizes maintainability, security, modularity, and future scalability while intentionally keeping Version 1 focused on delivering a clean, production-quality inventory management system.