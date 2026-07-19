# Sprint 07 – Vehicle Module Foundation

## Objective

Implement the complete Vehicle Module Foundation for the Car Dealership Inventory Management System while preserving the approved Version 1 architecture.

This sprint establishes the backend data layer required for vehicle inventory management by implementing the Vehicle database model, validation schemas, repository layer, database migration, and comprehensive tests.

This sprint intentionally does NOT expose any Vehicle API endpoints or frontend functionality. Those responsibilities belong to subsequent sprints.

---

# Development Mode

You are acting as a Senior Software Engineer working on a production-quality FastAPI application.

Respect the existing architecture, project documentation, coding standards, and sprint boundaries.

Implement ONLY Sprint 07.

Do not perform any work from Sprint 08 or later.

If any requirement in this prompt conflicts with the approved project documentation or existing implementation, stop and report the conflict instead of making assumptions.

Do not redesign the project architecture or database design.

Follow the existing coding style, folder structure, naming conventions, and implementation patterns already established in previous sprints.

# Implementation Priority

When implementing Sprint 07, always follow this priority order:

1. Existing project implementation
2. Approved project documentation
3. This sprint prompt

If any conflict exists, stop and report it instead of making assumptions.

# Approval Policy

Before writing any code:

1. Analyze the existing repository.
2. Analyze the approved project documentation.
3. Review the existing User module implementation to maintain consistency.
4. Explain the implementation plan.
5. List every file that will be created.
6. List every file that will be modified.
7. Explain why each modification is required.
8. Identify whether any project documentation requires updating.
9. Wait for approval.

Do not begin implementation until approval is given.

---

# Repository Rules

Current completed work:

- Project initialization
- Database infrastructure
- Application architecture
- User model
- Password hashing
- User repository
- JWT authentication
- Login endpoint
- User CRUD APIs
- User CRUD tests

Do not modify completed functionality.

Maintain complete backward compatibility with the existing User module and authentication system.

Do not refactor previously implemented modules unless it is absolutely required for Sprint 07. If any refactoring is necessary, explain the reason before implementation.

---

# Sprint Objective

Implement ONLY:

- Vehicle SQLAlchemy model
- Vehicle Pydantic schemas
- Vehicle repository
- Alembic migration for Vehicle table
- Vehicle model tests
- Vehicle repository tests
- Vehicle schema validation tests

Nothing else.

Vehicle CRUD API endpoints will be implemented in Sprint 08.

Do not implement any frontend functionality, business logic, reporting, analytics, purchase management, or dashboard features in this sprint.

# Approved Version 1 Architecture

The project officially follows:

API

↓

Repository

↓

Database

The originally planned Service layer is intentionally deferred for Version 1.

Repositories remain responsible only for persistence operations.

Business logic should remain lightweight and only where appropriate.

Do NOT introduce:

- Service Layer
- Domain Layer
- Generic Repository Pattern
- Repository Base Classes
- Additional Architectural Abstractions

Maintain the same architecture and coding style established in previous sprints.

---

# Documentation Consistency

Before implementation, verify whether Sprint 07 requires any documentation updates.

Only update documentation if the implemented Vehicle foundation changes an approved document.

If documentation updates are required, keep them minimal and limited to maintaining consistency.

Do NOT rewrite or restructure existing documentation.

Unless absolutely necessary, do NOT modify:

- Project Overview
- Requirement Analysis
- Development Standards
- System Architecture
- Database Design
- API Design
- UI/UX Design
- Implementation Plan
- Testing & Deployment Plan

If no documentation changes are required, explicitly state that the documentation already reflects the Sprint 07 implementation.

---

# Allowed Files

Create only:

backend/app/models/vehicle.py

backend/app/schemas/vehicle.py

backend/app/repositories/vehicle_repository.py

backend/app/tests/test_vehicle_model.py

backend/app/tests/test_vehicle_repository.py

backend/app/tests/test_vehicle_schema.py

backend/alembic/versions/<vehicle_migration>.py

Modify only when required:

backend/app/database/base.py

backend/requirements.txt (only if a new dependency is absolutely required)

No additional files without approval.

Do not modify existing authentication, user management, routing, or API modules.

# Vehicle Model Requirements

Implement the Vehicle entity exactly as defined in the approved project documentation.

Do not redesign the data model.

Do not introduce additional fields unless required by the existing project documentation.

Implement the Vehicle SQLAlchemy model with the following fields:

- id
- manufacturer
- model
- vin
- year
- purchase_price
- selling_price
- color
- mileage
- fuel_type
- transmission
- condition
- description
- status
- created_at
- updated_at

---

# Database Constraints

Implement the following constraints:

### id

- Primary Key
- Auto Increment

### manufacturer

- Required
- Maximum 100 characters

### model

- Required
- Maximum 100 characters

### vin

- Required
- Unique
- Database Unique Constraint

### year

- Required
- Integer

### purchase_price

Use SQLAlchemy Numeric/Decimal.

Do NOT use Float.

Price must be greater than zero.

### selling_price

Use SQLAlchemy Numeric/Decimal.

Do NOT use Float.

Price must be greater than zero.

### color

Required.

### mileage

Required Integer.

Mileage cannot be negative.

### fuel_type

Implement using Enum.

Supported values:

- PETROL
- DIESEL
- ELECTRIC
- HYBRID

### transmission

Implement using Enum.

Supported values:

- MANUAL
- AUTOMATIC

### condition

Implement using Enum.

Supported values:

- NEW
- USED

### description

Optional.

### status

Implement using Enum.

Supported values:

- AVAILABLE
- SOLD

Default value:

AVAILABLE

### created_at

Automatically generated timestamp.

### updated_at

Automatically maintained timestamp.

---

# Relationships

Do NOT create any database relationships.

Vehicle must remain an independent entity during Sprint 07.

Purchase relationships will be implemented in later sprints.

---

# Model Implementation Requirements

Follow the same implementation style used by the existing User model.

Maintain consistency for:

- SQLAlchemy typing
- Column definitions
- Timestamp handling
- Default values
- Enum implementation
- Model organization

Do not introduce a BaseModel abstraction or any additional inheritance hierarchy.

# Repository Requirements

Create:

backend/app/repositories/vehicle_repository.py

Follow the same repository pattern used by the existing UserRepository.

Repositories remain responsible ONLY for:

- Database CRUD operations
- SQLAlchemy queries
- Persistence

Repositories must NOT contain:

- Business logic
- Authentication
- Authorization
- JWT handling
- HTTP responses
- Validation logic
- API-specific logic

Implement ONLY the following repository methods:

- create()
- get_by_id()
- get_all()
- update()
- delete()

Do NOT implement:

- Search
- Filtering
- Pagination
- Sorting
- Dashboard queries
- Analytics queries
- Purchase-related queries

These features belong to later sprints.

---

# Schema Requirements

Create:

backend/app/schemas/vehicle.py

Follow the same structure and coding style used in the existing User schemas.

Implement only:

- VehicleBase
- VehicleCreate
- VehicleUpdate
- VehicleRead

Use appropriate Pydantic validation for:

- Required fields
- Numeric values
- Enum values
- Optional fields

VehicleUpdate should support updating only editable Vehicle fields.

Do not expose internal database implementation details.

Maintain response consistency with the existing User schemas.

Do not create additional schema classes unless required by the approved project documentation.

---

# Migration Requirements

Create one Alembic migration for the Vehicle table.

The migration must include:

- Primary Key
- Unique VIN constraint
- Enum fields
- Numeric price fields
- Timestamp fields
- All approved Vehicle columns

Do NOT modify previous migrations.

Do NOT edit existing database tables.

Register the Vehicle model correctly so Alembic detects the new table.

The migration should be reversible using Alembic downgrade().

# Testing

Create comprehensive tests covering:

## Model Tests

- Vehicle model creation
- Default values
- Enum values
- Decimal price fields
- Timestamp generation
- Database constraints

## Repository Tests

Verify:

- Create Vehicle
- Retrieve Vehicle by ID
- Retrieve all Vehicles
- Update Vehicle
- Delete Vehicle

Test both successful operations and failure scenarios where applicable.

## Schema Tests

Validate:

- Valid Vehicle payload
- Missing required fields
- Invalid year
- Invalid prices
- Negative mileage
- Invalid enum values
- Optional description field

Existing tests must continue passing.

---

# Runtime Verification

Before declaring Sprint 07 complete verify:

- FastAPI starts successfully
- Existing authentication still works
- Login endpoint still works
- Existing User CRUD still works
- Vehicle model imports correctly
- Alembic migration executes successfully
- Vehicle table is created correctly
- Alembic downgrade succeeds
- Repository CRUD functions correctly
- Existing health endpoints work
- Existing tests pass
- Vehicle tests pass
- No circular imports
- No migration conflicts
- No lint-level issues

---

# Code Quality Expectations

Follow the coding standards established in previous sprints.

Maintain consistency with the existing project for:

- Folder structure
- Naming conventions
- SQLAlchemy implementation
- Repository implementation
- Pydantic schemas
- Test structure
- Type hints
- Documentation style

Do not introduce unnecessary abstractions.

Favor consistency over optimization.

The implementation should appear as a natural continuation of the existing codebase rather than a separate coding style.

# Strict Constraints

Do NOT implement:

- Vehicle API endpoints
- Vehicle CRUD routes
- API router registration
- Purchase module
- Purchase CRUD
- Dashboard
- Reports
- Analytics
- Search
- Filtering
- Pagination
- Sorting
- File uploads
- Image uploads
- Vehicle images
- Authentication changes
- JWT changes
- Login changes
- Registration
- Password Reset
- Email Verification
- Role-Based Authorization
- Permissions
- Middleware
- Service Layer
- Generic Repository Pattern
- Base Repository
- Additional database tables
- Additional migrations
- Background tasks
- Caching
- Performance optimizations
- Documentation refactoring
- Sprint 08 functionality

Implement ONLY the Vehicle foundation required for Sprint 07.

Stop immediately after Sprint 07 is complete.

Do not continue to future sprint work without approval.

---

# Important Notes

Preserve all existing functionality.

Do not modify completed modules unless absolutely required.

Do not introduce breaking changes.

If a better architectural approach is discovered during implementation, do NOT implement it automatically.

Instead:

- Explain the proposed improvement.
- Explain why it is better.
- Wait for approval before changing the approved architecture.

The approved project architecture always takes priority over personal implementation preferences.

When multiple implementation approaches are possible, choose the one that is most consistent with the existing codebase rather than introducing a new pattern.

# Completion Report

After implementation is complete, provide a final report containing the following sections.

## Implementation Summary

Provide a brief summary of the work completed during Sprint 07.

---

## Files Created

List every new file created.

---

## Files Modified

List every existing file modified.

Explain why each file required modification.

---

## Database Changes

Summarize:

- New Vehicle table
- Constraints
- Enum fields
- Migration created

---

## Repository Methods Added

List every repository method implemented.

---

## Schemas Added

List every Pydantic schema implemented.

---

## Documentation Updated

State whether any documentation was updated.

If updated, explain exactly what changed and why.

If no documentation changes were required, explicitly state that the existing documentation already reflected the implemented design.

---

## Verification Results

Confirm:

- FastAPI starts successfully
- Vehicle model imports successfully
- Vehicle repository functions correctly
- Alembic migration succeeds
- Alembic downgrade succeeds
- Existing User module remains unaffected
- Existing authentication remains unaffected

---

## Tests Executed

List every test executed.

Separate:

- Existing tests
- New Vehicle tests

---

## Test Results

Report:

- Total tests executed
- Total tests passed
- Total tests failed

If any test fails, explain the cause.

---

## Manual Changes Required

List any manual actions required after implementation.

If none are required, explicitly state:

"None."

---

## Risks Found

List any implementation risks, technical debt, or recommended improvements discovered during Sprint 07.

Do not implement those improvements automatically.

---

## Ready For Sprint 08?

State whether the project is ready to begin Sprint 08 (Vehicle CRUD APIs).

Do not continue to Sprint 08 without approval.