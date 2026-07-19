# Sprint 03 - Application Architecture Skeleton

## Objective

Establish the backend application architecture that all future features will build upon.

This sprint focuses on organizing the FastAPI application into a scalable and maintainable structure following the project's Hybrid Clean Architecture.

The objective is **not** to implement any business functionality. Instead, create the architectural skeleton that will support future development.

---

# prompt

# Development Mode

Work incrementally.

Complete **one major task at a time**.

After completing each task:

- Explain what was implemented.
- Explain why it was necessary.
- Show the affected files.
- Wait for my approval before continuing.

Never continue automatically.

Quality is more important than speed.

---

# Approval Policy

Never enable automatic approval mode.

Before executing any command that modifies the project:

- Explain the purpose.
- Wait for explicit approval.

Do not assume approval.

Always stop before:

- Installing packages
- Creating multiple files
- Refactoring existing files
- Running migrations
- Executing database commands
- Running destructive commands
- Performing large architectural changes

---

# Safety Rules

Before modifying any existing file:

- Explain why the modification is necessary.
- Preserve existing functionality.
- Make the smallest possible change.
- Never rewrite working code without justification.

If there are multiple architectural approaches:

- Explain the available options.
- Recommend the most suitable one.
- Wait for approval before implementation.

---

# Context

Sprint 01 and Sprint 02 have already been completed successfully.

Before writing any code:

1. Read every document inside the `docs/` directory.
2. Inspect the current repository.
3. Understand the existing architecture.
4. Continue from the current implementation.
5. Treat the documentation as the single source of truth.

Do not recreate previously completed work.

---

# Repository Rules

Treat this as an actively developed production project.

Do not:

- Reinitialize the project
- Modify completed Sprint 01 work
- Modify completed Sprint 02 work unnecessarily
- Rename folders
- Rename files
- Move files without justification
- Reorganize the project structure unless required by the architecture

Only create files that belong to Sprint 03.

---

# Sprint Objective

Build the backend architecture skeleton.

This sprint may include:

- API versioning (`/api/v1`)
- Router organization
- Central router registration
- API package structure
- Shared dependency wiring
- Exception handler registration
- Middleware registration (if required by the architecture)
- Placeholder routers where appropriate
- Health endpoint integration into versioned routing
- Clean package organization

The architecture should be scalable and ready for future modules.

---

# Strict Constraints

Do **NOT** implement:

## Database

- User model
- Vehicle model
- Purchase model
- Database tables
- Database relationships

## Authentication

- JWT
- Login
- Register
- Password hashing
- Authorization

## Business Logic

- CRUD operations
- Services
- Repositories
- Business rules
- Validation logic
- Dashboard logic

## Frontend

- React pages
- UI components
- Forms
- Routing
- Material UI implementation

## Database Operations

- Alembic migrations
- Seed data

Sprint 03 is architecture only.

---

# Architecture Expectations

The resulting backend should provide a clean foundation for future development.

The architecture should make it easy to add:

- Authentication
- User module
- Vehicle module
- Purchase module
- Dashboard module

without requiring future restructuring.

Every new feature should be able to plug into the architecture with minimal modification.

---

# Coding Standards

Follow the project's Development Standards.

Additionally:

- Follow Hybrid Clean Architecture
- Use Dependency Injection
- Keep modules small
- Use meaningful names
- Follow SOLID principles
- Keep responsibilities separated
- Avoid duplication
- Prefer readability over cleverness

Do not add unnecessary comments.

---

# Runtime Verification Policy

If verification requires:

- PostgreSQL
- Environment variables
- Docker
- API keys
- External services

Stop.

Explain the required setup.

Wait for confirmation.

Do not invent credentials.

---

# Expected Deliverables

By the end of Sprint 03, the backend should contain:

- Versioned API structure
- Central router registration
- Organized package hierarchy
- Exception handling framework
- Middleware registration (if applicable)
- Shared routing architecture
- Clean import structure
- Successful application startup
- Successful route verification

The project should be fully prepared for Sprint 04.

---

# Completion Report

When Sprint 03 is complete, provide:

## Summary

- What was implemented
- Why it was implemented

## Files Created

List every new file.

## Files Modified

List every modified file.

## Verification

Describe how the architecture was verified.

## Architecture Decisions

Explain important design decisions made during implementation.

## Manual Changes

Describe any steps I must perform manually.

## Lessons Learned

Summarize important architectural lessons from Sprint 03.

## Ready For

Clearly state why the project is now ready for Sprint 04 (User Module).