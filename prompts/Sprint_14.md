# Current Project Status

The following modules are complete and should be treated as stable:

- Authentication
- Vehicle Management
- Purchase Management

The Sales module should integrate with these completed modules.

Do not refactor completed functionality unless a verified blocking defect is discovered.

# Sprint Discipline

Remain strictly within the scope of this sprint.

If you discover functionality that belongs to a future sprint:

- Document it.
- Do not implement it.
- Continue completing the current sprint.

Avoid scope creep.

# Sprint 14 – Sales Backend Foundation

# Objective

Implement the backend foundation for the Sales Management module of the Car Dealership Inventory Management System.

The Purchase Management module was completed during Sprint 13 and must be treated as production-ready.

Sprint 14 focuses exclusively on establishing the backend architecture required for Sales Management.

This sprint lays the foundation for the Sales CRUD APIs that will be implemented during Sprint 15.

At the end of this sprint, the backend should contain all core Sales infrastructure while maintaining compatibility with the existing project architecture.

This sprint should NOT implement:

- Sales CRUD API endpoints
- Sales frontend pages
- Dashboard integration
- Reports or analytics

Those features belong to later sprints.

---

# Development Mode

Develop production-quality software.

Prioritize:

- Maintainability
- Readability
- Consistency
- Reliability
- Simplicity

Every implementation should follow the architecture already established within the project.

Avoid temporary implementations.

Do not leave:

- TODO comments
- Placeholder methods
- Stub implementations
- Commented-out code
- Dead code
- Debugging statements

Every completed component should be production-ready.

---

# Initial Repository Review

Before implementing any code:

1. Review the current repository.
2. Understand the completed Vehicle Management module.
3. Understand the completed Purchase module.
4. Review the existing repository architecture.
5. Reuse existing backend patterns wherever appropriate.

Do not begin implementation until the current architecture has been fully understood.

---

# Approval Policy

Before making architectural changes, stop and explain:

- Why the change is necessary.
- Which files will be modified.
- Why the existing architecture is insufficient.

Wait for approval before changing:

- Database architecture
- Authentication flow
- Existing API contracts
- Repository architecture
- Shared utilities
- Existing project structure

Normal backend implementation for the Sales module does not require approval.

---

# Repository Rules

Preserve the existing project architecture.

Do NOT:

- Rename existing files.
- Move existing files.
- Refactor completed modules.
- Modify Vehicle functionality.
- Modify Purchase functionality.
- Modify Authentication.
- Modify existing API contracts.
- Modify completed migrations.
- Introduce unnecessary third-party libraries.

Only create or modify files required for implementing the Sales backend foundation.

Reuse existing project patterns whenever possible.

Avoid unnecessary abstraction.

Do not create duplicate repositories, helpers, utilities, or shared components when equivalent implementations already exist.

# Scope

Sprint 14 focuses exclusively on implementing the backend foundation for the Sales Management module.

The objective is to establish all backend infrastructure required to support Sales CRUD APIs in Sprint 15.

Do not implement REST API endpoints during this sprint.

Do not implement frontend functionality.

The Sales backend should integrate cleanly with the existing Vehicle and Purchase modules.

---

# Functional Requirements

Implement the complete backend foundation for Sales Management.

This includes:

- Sales database model
- SQLAlchemy relationships
- Pydantic request and response schemas
- Repository implementation
- Dependency injection
- Database migration
- Validation rules
- Inventory update foundation
- Proper transaction handling
- Unit tests

Implement unit tests only for the backend foundation introduced in this sprint.

Examples include:

- Model validation
- Repository initialization
- Relationship configuration
- Transaction behavior
- Migration integrity

Do not implement endpoint tests during this sprint because Sales APIs have not yet been introduced.

The implementation should remain consistent with the existing backend architecture.

---

# Sales Entity

Create a Sales entity representing the sale of a vehicle.

The entity should contain all fields required by the business domain.

Include appropriate:

- Primary key
- Foreign key relationships
- Monetary fields
- Customer information
- Sale date
- Audit timestamps

Use the same naming conventions and coding style already established throughout the project.

---

# Database Relationships

Implement appropriate SQLAlchemy relationships between:

- Sales
- Vehicle

If the existing project architecture requires additional relationships, implement them using the same conventions.

Relationships should be bidirectional where appropriate.

---

# Database Migration

Create an Alembic migration for the Sales table.

The migration should:

- Follow existing migration conventions.
- Be reversible.
- Preserve compatibility with existing migrations.
- Avoid modifying previously completed migrations.

Do not alter unrelated database tables.

---

# Repository Layer

Implement a Sales repository following the existing repository pattern.

Implement only the repository foundation required by the Sales module.

Do not implement complete CRUD workflows unless they are necessary to establish the backend architecture.

Sprint 15 will implement the full Sales CRUD operations.

Reuse existing repository conventions established by the Vehicle and Purchase modules.

Do not introduce a new repository architecture.

---

# Validation Rules

Implement backend validation for Sales data.

Validation should ensure:

- Required fields are present.
- Monetary values are valid.
- Invalid foreign keys are rejected.
- Invalid dates are rejected where applicable.
- Business rule violations produce meaningful validation errors.

Validation should be implemented using the same patterns already used throughout the backend.

---

# Inventory Foundation

Prepare the backend architecture required to support inventory updates in Sprint 15.

This sprint should establish the necessary models, relationships, validation, and transactional design.

Do NOT implement inventory updates that are triggered by API endpoints.

The actual sale workflow and inventory modification logic belong to Sprint 15.

---

# Error Handling

Implement consistent backend error handling.

Handle scenarios such as:

- Missing records
- Invalid references
- Validation failures
- Database integrity violations
- Transaction failures

Return meaningful exceptions using the existing backend error handling strategy.

Do not introduce a separate error handling framework.

---

# Code Quality

Follow clean architecture principles.

Ensure:

- Small, focused classes
- Clear method names
- Minimal duplication
- Consistent formatting
- Readable code
- Proper type hints where applicable

Do not leave:

- Unused imports
- Dead code
- Commented-out implementations
- Temporary workarounds
- Debug logging

The Sales backend foundation should be production-ready and fully aligned with the architecture established by the existing Vehicle and Purchase modules.

# Backend Architecture & Implementation Requirements

The Sales backend must follow the same architectural patterns already established within the project.

Before creating any new model, schema, repository, dependency, utility, or helper, verify whether an equivalent implementation already exists and reuse it whenever possible.

Avoid duplicate implementations.

---

# Project Structure

Organize the Sales module using the existing backend structure.

Follow the same directory organization, naming conventions, and module structure used by the Vehicle and Purchase modules.

Maintain consistency across:

- Models
- Schemas
- Repositories
- Dependencies
- Database migrations
- Configuration
- Validation
- Exception handling

Do not introduce a new architectural pattern.

---

# Database Models

Implement the Sales database model using the existing SQLAlchemy conventions.

Ensure:

- Consistent naming
- Appropriate column types
- Proper constraints
- Foreign key relationships
- Audit timestamps
- ORM relationships

Reuse existing base classes and mixins where appropriate.

---

# Repository Layer

Implement the Sales repository using the project's existing repository pattern.

The repository should encapsulate all database interaction required for future Sales CRUD APIs.

Do not:

- Write raw SQL unless the project already does so.
- Duplicate logic from existing repositories.
- Introduce another persistence abstraction.

Keep repository methods cohesive and reusable.

---

# Schemas

Implement request and response schemas using the project's existing Pydantic conventions.

Ensure:

- Clear separation between Create, Update, and Response schemas.
- Appropriate field validation.
- Consistent naming.
- Proper serialization.

Reuse validation patterns already established throughout the backend.

---

# Dependency Injection

Register Sales dependencies using the same dependency injection approach already used by the project.

Reuse existing dependency providers whenever possible.

Do not create duplicate dependency patterns.

---

# Database Transactions

Ensure every Sales operation is designed to execute safely within a database transaction.

Database consistency must always be preserved.

If an operation fails:

- Roll back all related changes.
- Prevent partial database updates.
- Return an appropriate exception.

Use the project's existing transaction management strategy.

---

# Inventory Consistency

Prepare the Sales module so that inventory updates occur atomically.

Future Sales CRUD endpoints should be able to:

- Record the sale.
- Update inventory.
- Commit both changes together.

Design the foundation to support this behavior without introducing unnecessary complexity.

---

# Exception Handling

Follow the existing backend exception handling strategy.

Handle:

- Missing resources
- Duplicate records
- Invalid references
- Validation failures
- Database integrity errors
- Transaction failures

Return consistent error responses.

Do not expose internal exception details.

---

# Logging

Reuse the existing logging strategy.

Do not introduce a new logging framework.

Log only meaningful events.

Avoid excessive logging.

Do not leave debugging statements.

---

# Performance

Write efficient database code.

Avoid:

- N+1 query patterns
- Redundant database lookups
- Unnecessary object creation
- Duplicate queries

Reuse relationships and query patterns already established within the project.

---

# Code Quality

Follow clean coding principles.

Ensure:

- Small focused methods
- Meaningful class names
- Meaningful variable names
- Minimal code duplication
- Readable type hints
- Consistent formatting

Remove:

- Unused imports
- Dead code
- Commented-out code
- Temporary implementations
- TODO comments
- Debugging code

The Sales backend foundation should be production-ready and maintain the same quality standards as the completed Vehicle and Purchase modules.

# Verification & Testing Requirements

Sprint 14 must not be considered complete until all verification steps have been executed successfully.

Do not assume correctness based solely on successful code generation.

Verify every implemented backend component.

---

# Repository Review

Before implementation:

- Review the completed Vehicle backend.
- Review the completed Purchase backend.
- Ensure the Sales backend follows the same architectural patterns.

Do not duplicate existing implementations.

---

# Database Verification

Verify that the Sales database model has been implemented correctly.

Ensure:

- The model is registered correctly.
- Relationships are configured correctly.
- Constraints are valid.
- Foreign keys are correct.
- Audit fields behave consistently.

Confirm that the schema matches the intended business model.

---

# Migration Verification

Run the Alembic migration.

Verify:

- Migration executes successfully.
- Rollback executes successfully.
- Reapplying the migration succeeds.
- Existing tables remain unaffected.
- No previously completed migration is modified.

The migration should be fully reversible.

---

# Repository Verification

Verify that the Sales repository functions correctly.

Ensure repository methods:

- Execute successfully.
- Return expected results.
- Handle invalid input gracefully.
- Follow the existing repository conventions.

Do not leave unused repository methods.

---

# Validation Verification

Verify all implemented validation rules.

Test scenarios including:

- Missing required fields
- Invalid foreign keys
- Invalid monetary values
- Invalid dates
- Invalid business rules

Validation errors should be meaningful and consistent with the existing backend.

---

# Transaction Verification

Verify transaction behavior.

Ensure that:

- Successful operations commit correctly.
- Failed operations roll back correctly.
- Partial database updates cannot occur.

Database consistency must always be preserved.

---

# Backend Test Suite

Run the complete backend test suite.

Verify:

- Existing tests continue to pass.
- No regressions are introduced.
- New Sales foundation tests pass.
- Test coverage remains consistent.

If any test fails:

1. Identify the root cause.
2. Fix the issue.
3. Re-run the full test suite.

Repeat until all backend tests pass.

---

# Application Verification

Verify that the backend application starts successfully.

Confirm:

- FastAPI starts without errors.
- Dependency injection works correctly.
- Database initialization succeeds.
- Sales components load correctly.
- Existing modules continue to function.

---

# Regression Testing

Verify that Sprint 14 does not impact completed functionality.

Ensure:

- Authentication continues to work.
- Vehicle backend remains unchanged.
- Purchase backend remains unchanged.
- Existing API endpoints continue functioning.
- Existing database models remain unaffected.

No completed functionality should regress.

---

# Code Quality Verification

Perform a final code review.

Verify:

- No duplicate implementations.
- No unused imports.
- No dead code.
- No commented-out code.
- No TODO comments.
- No debugging statements.
- Consistent formatting.
- Meaningful naming.

The implementation should be production-ready.

---

# Mandatory Verification Gate

Continue fixing issues until ALL of the following succeed:

✓ Database model implemented correctly.

✓ Relationships verified.

✓ Alembic migration succeeds.

✓ Migration rollback succeeds.

✓ Repository implementation verified.

✓ Validation rules verified.

✓ Transaction handling verified.

✓ Backend application starts successfully.

✓ Backend test suite passes.

✓ Existing functionality remains unaffected.

✓ No runtime exceptions occur.

✓ No failing backend tests remain.

Do NOT stop after resolving the first issue.

Continue fixing issues until all verification required for Sprint 14 succeeds.

Do not delay Sprint 15 by attempting to solve issues that belong to future functionality.

# Completion Report

After completing Sprint 14, provide a comprehensive implementation report.

The report must include:

## 1. Sprint Summary

Summarize everything implemented during Sprint 14.

Explain how the Sales backend foundation was established and how it integrates with the existing Vehicle and Purchase modules.

Clearly distinguish between completed foundation work and functionality planned for Sprint 15.

---

## 2. Files Created

List every newly created file.

---

## 3. Files Modified

List every modified file.

Briefly explain why each file was changed.

---

## 4. Database Changes

List:

- New database models
- Relationships
- Alembic migration
- Constraints
- Indexes (if any)

Confirm that no existing tables or completed migrations were modified.

---

## 5. Repository Implementation

List every repository implemented or modified.

Explain the responsibility of each repository.

Confirm that the existing repository architecture remains unchanged.

---

## 6. Validation Rules

Summarize every validation rule implemented.

Explain how invalid data is handled.

---

## 7. Transaction Handling

Explain how database consistency is maintained.

Describe how transaction rollback is handled when failures occur.

---

## 8. Verification Results

Provide the results of every verification step.

Include:

Database

- Migration executed successfully
- Rollback executed successfully
- Relationships verified

Backend

- Application startup result
- Backend tests executed
- Tests passed
- Tests failed

Foundation

Confirm successful verification of:

- Sales model
- Repository
- Schemas
- Validation
- Dependency injection
- Transaction handling
- Inventory foundation

---

## 9. Assumptions

Document every assumption made during implementation.

If no assumptions were required, explicitly state:

"No assumptions were made."

---

## 10. Known Issues

List any remaining issues.

If none exist, explicitly state:

"No known issues."

Do not hide unresolved problems.

---

## 11. Recommended Commit Message

Recommend a single Git commit message following the existing project commit style.

Example:

feat: implement sales backend foundation

---

## 12. Next Sprint Readiness

Confirm whether Sprint 15 can begin immediately.

If any prerequisite is missing, clearly explain what remains to be completed.

---

# Definition of Done

Sprint 14 is complete only if ALL of the following conditions are satisfied:

✓ Sales database model implemented.

✓ SQLAlchemy relationships implemented.

✓ Pydantic schemas implemented.

✓ Repository layer implemented.

✓ Dependency injection configured.

✓ Alembic migration implemented.

✓ Migration executes successfully.

✓ Migration rollback succeeds.

✓ Validation rules implemented.

✓ Transaction handling implemented.

✓ Inventory update foundation prepared.

✓ Backend application starts successfully.

✓ Existing backend tests continue to pass.

✓ New Sales foundation tests pass.

✓ No runtime exceptions remain.

✓ No unnecessary files or dependencies were introduced.

✓ No regressions were introduced into completed modules.

✓ Code follows the existing backend architecture and coding standards.

Sprint 14 should establish a complete backend foundation but should NOT implement Sales CRUD API endpoints or frontend functionality.

Only after every Definition of Done item has been satisfied should Sprint 14 be considered complete.

---

# Mandatory Final Review

Before finishing Sprint 14, perform one final backend review.

Verify:

- Project structure
- Database model
- Repository implementation
- Schemas
- Relationships
- Migration
- Dependency injection
- Transaction handling
- Validation
- Backend startup
- Backend tests

If any issue is discovered:

1. Identify the root cause.
2. Fix the issue.
3. Repeat verification.
4. Repeat the final review.

Continue this cycle until no remaining issues are found.

Only then declare Sprint 14 successfully completed.

---

# Sprint Boundary

Sprint 14 ends after the backend foundation has been fully implemented and verified.

Do NOT implement:

- Sales CRUD API endpoints
- Sales frontend pages
- Dashboard integration
- Analytics
- Reporting
- Additional inventory features beyond the required backend foundation

Those features belong to future sprints.

Remain strictly within the defined scope of Sprint 14.