# Sprint 09 – Vehicle Frontend UI

## Objective

Implement the complete Vehicle Frontend UI for the Car Dealership Inventory Management System while preserving the approved Version 1 architecture.

This sprint exposes the previously implemented Vehicle CRUD APIs through a clean, professional React user interface by integrating the existing frontend architecture, Material UI components, API client, and JWT authentication.

This sprint intentionally does NOT introduce any backend changes, new database entities, purchase management, dashboard functionality, analytics, search, filtering, pagination, sorting, or additional architectural layers. Those responsibilities belong to subsequent sprints.

---

# Development Mode

You are acting as a Senior Software Engineer working on a production-quality React application.

Respect the existing architecture, project documentation, coding standards, and sprint boundaries.

Implement ONLY Sprint 09.

Do not perform any work from Sprint 10 or later.

If any requirement in this prompt conflicts with the approved project documentation or existing implementation, stop and report the conflict instead of making assumptions.

Do not redesign the frontend architecture, backend APIs, database design, or project structure.

Follow the existing coding style, folder structure, naming conventions, and implementation patterns already established in previous sprints.

---

# Implementation Priority

When implementing Sprint 09, always follow this priority order:

1. Existing project implementation
2. Approved project documentation
3. This sprint prompt

If any conflict exists, stop and report it instead of making assumptions.

---

# Approval Policy

Before writing any code:

1. Analyze the existing repository.
2. Analyze the approved project documentation.
3. Review the existing frontend structure.
4. Review the existing Vehicle CRUD APIs.
5. Explain the implementation plan.
6. List every file that will be created.
7. List every file that will be modified.
8. Explain why each modification is required.
9. Identify whether any project documentation requires updating.
10. Wait for approval.

Do not begin implementation until approval is given.

# Repository Rules

Current completed work:

- Project initialization
- Database infrastructure
- Application architecture
- User model
- Password hashing
- JWT authentication
- Login endpoint
- User CRUD APIs
- Vehicle model
- Vehicle repository
- Vehicle schemas
- Vehicle CRUD APIs
- Vehicle API tests

Do not modify completed backend functionality.

Maintain complete backward compatibility with the existing backend APIs, authentication system, database schema, and project architecture.

Do not refactor previously implemented backend modules unless it is absolutely required for Sprint 09.

If any backend modification appears necessary, explain the reason during the approval phase before making changes.

---

# Sprint Objective

Implement ONLY:

- Vehicle List page
- Add Vehicle page
- Edit Vehicle page
- Delete Vehicle functionality
- Reusable Vehicle Form component
- Vehicle API integration
- Loading states
- Error handling
- Success notifications
- Frontend tests (if already part of the project)

Nothing else.

Use the existing Vehicle CRUD APIs implemented during Sprint 08.

Do NOT redesign the backend APIs or database schema.

Do NOT implement:

- Purchase module
- Dashboard
- Analytics
- Charts
- Search
- Filtering
- Pagination
- Sorting
- File uploads
- Image uploads
- Vehicle images
- Sprint 10 functionality

---

# Approved Version 1 Frontend Architecture

The frontend officially follows:

React UI

↓

API Client

↓

FastAPI Backend

↓

Repository

↓

Database

The frontend should remain responsible only for:

- Rendering the UI
- Managing local component state
- Calling existing backend APIs
- Displaying validation errors
- Displaying loading states
- Displaying success/error notifications
- Navigation between pages

Business rules remain on the backend.

Do NOT introduce:

- Redux
- MobX
- Zustand
- Context-based global state management (unless already used)
- New API abstraction layers
- New frontend architectures
- Backend logic inside React components

Maintain the same project structure and coding style established in the existing frontend.

Keep components reusable, simple, and easy to maintain.

# Documentation Consistency

Before implementation, verify whether Sprint 09 requires any documentation updates.

Only update documentation if the implemented Vehicle Frontend UI changes an approved document.

If documentation updates are required, keep them minimal and limited to maintaining consistency.

Do NOT rewrite or restructure existing documentation.

Unless absolutely necessary, do NOT modify:

- Project Overview
- Requirement Analysis
- Development Standards
- System Architecture
- Database Design
- API Design
- Implementation Plan
- Testing & Deployment Plan

If no documentation changes are required, explicitly state that the documentation already reflects the Sprint 09 implementation.

---

# Allowed Files

Create only the files required for implementing the Vehicle Frontend UI.

This may include:

- Vehicle List page
- Vehicle Form component
- Add Vehicle page
- Edit Vehicle page
- Vehicle API client (only if not already present)
- Supporting frontend components that are directly required to implement the approved Vehicle UI.
- Do not create speculative reusable components.

Modify only when required:

- Existing routing configuration
- Existing navigation/menu
- Existing frontend entry points
- Existing API configuration

No additional files without approval.

Do not modify:

- Backend APIs
- Backend models
- Backend repository
- Backend database
- Authentication implementation
- User module
- Purchase module

---

# Vehicle UI Requirements

Implement a clean, responsive, and professional Vehicle Management interface using the approved frontend architecture.

Reuse existing frontend components wherever possible.

The UI should include:

## Vehicle List

Display all Vehicles returned by the existing backend API.

Each row should display the approved Vehicle fields.

Provide actions for:

- Edit
- Delete

Do NOT implement:

- Search
- Filtering
- Pagination
- Sorting
- Bulk actions

---

## Add Vehicle

Provide a form for creating a new Vehicle.

Use the existing backend validation.

Display validation errors returned by the API.

After successful creation:

- Show a success notification.
- Return to the Vehicle List.

---

## Edit Vehicle

Reuse the same Vehicle Form.

Populate the form using the existing Vehicle data.

Display backend validation errors.

After successful update:

- Show a success notification.
- Return to the Vehicle List.

---

## Delete Vehicle

Allow deletion only through the existing backend API.

Display a confirmation dialog before deletion.
Confirmation dialog should clearly display:

- Vehicle name
- Manufacturer
- Warning that deletion is permanent

Require explicit confirmation before deletion.

Display backend error messages if deletion is rejected (for example, SOLD vehicles).

Do not implement custom business rules in the frontend.

---

## Loading & Error States

Provide appropriate UI feedback for:

- Initial page loading
- API requests
- If no Vehicles exist:
Display a friendly empty-state message.
Provide a prominent "Add Vehicle" action.
Do not display an empty table without explanation.
- Validation failures
- Network failures
- Backend errors

Do not expose technical error details to the user.

Display clear, user-friendly messages consistent with the rest of the application.

---

## Reusable Components

Create reusable components only where justified.

The Vehicle Form should be shared between:

- Add Vehicle
- Edit Vehicle

Avoid unnecessary component abstraction.

Favor readability and maintainability over premature optimization.

# UI/UX Principles

The Vehicle Management UI should prioritize clarity, simplicity, and ease of use.

Design for dealership employees who interact with the system throughout the day.

The interface should feel professional rather than experimental.

Follow these principles:

- Clean spacing and alignment
- Consistent typography
- Consistent button placement
- Clear visual hierarchy
- Minimal visual clutter
- Responsive layout
- Accessible form labels
- Readable tables
- Logical navigation
- Fast task completion

Use Material UI components consistently.

Avoid excessive colors, animations, gradients, or decorative effects.

The interface should inspire confidence and professionalism.

# Visual Design Guidelines

The application represents a professional dealership management system.

Use a clean and modern business interface.

Prefer:

- White or light background
- Dark gray typography
- One primary accent color
- Limited secondary colors
- Consistent spacing
- Rounded but subtle component corners
- Professional icons
- Material UI defaults where appropriate

Use colors primarily to communicate meaning:

- Blue → Primary actions
- Green → Successful operations
- Orange → Warnings
- Red → Delete or destructive actions

Avoid excessive gradients, flashy effects, oversized shadows, or decorative styling.

Focus on usability over visual complexity.

# User Experience Expectations

Users should be able to complete common Vehicle Management tasks with minimal effort.

Design the UI so that users can:

- Understand the page immediately
- Locate primary actions easily
- Complete CRUD operations quickly
- Recover gracefully from errors
- Receive immediate feedback after actions

Every interaction should communicate clearly what happened and what the user should do next.



# API Integration Requirements

Integrate the Vehicle Frontend UI with the existing Vehicle CRUD APIs implemented during Sprint 08.

Reuse the existing API client and authentication mechanism wherever possible.

Do not modify backend endpoints.

Do not create duplicate API implementations.

The frontend should only consume the approved endpoints:

- POST /api/v1/vehicles
- GET /api/v1/vehicles
- GET /api/v1/vehicles/{vehicle_id}
- PUT /api/v1/vehicles/{vehicle_id}
- DELETE /api/v1/vehicles/{vehicle_id}

All API requests must:

- Reuse the existing JWT authentication mechanism.
- Reuse the existing API configuration.
- Handle loading states.
- Handle validation errors.
- Handle network failures.
- Handle backend error responses consistently.

Do not implement frontend business logic that duplicates backend validation.

---

# Testing

Create appropriate frontend tests only if the existing frontend project already contains a testing framework.

If frontend testing has not yet been established, do not introduce a testing framework during Sprint 09.

Instead, perform manual verification of:

- Vehicle List rendering
- Add Vehicle workflow
- Edit Vehicle workflow
- Delete Vehicle workflow
- Loading states
- Error handling
- Authentication behavior
- Navigation flow

Existing backend tests must continue passing.

Do not modify backend tests.

---

# Runtime Verification

Before declaring Sprint 09 complete verify:

- Frontend builds successfully.
- Frontend starts successfully.
- Existing login functionality continues to work.
- JWT authentication continues to work.
- Vehicle List loads correctly.
- Vehicle creation works correctly.
- Vehicle editing works correctly.
- Vehicle deletion works correctly.
- SOLD vehicle deletion displays the backend error correctly.
- Validation errors display correctly.
- Loading states function correctly.
- Navigation functions correctly.
- No routing conflicts.
- No console errors.
- No TypeScript/JavaScript build errors.

---

# Code Quality Expectations

Follow the coding standards established in previous sprints.

Maintain consistency with the existing frontend for:

- Folder structure
- Component organization
- Routing
- API integration
- Form handling
- Error handling
- Loading states
- Notifications
- Naming conventions

Keep components focused and reusable.

Avoid unnecessary abstraction.

Favor consistency and readability over optimization.

The implementation should appear as a natural continuation of the existing codebase.

---

# Strict Constraints

Do NOT implement:

- Purchase module
- Dashboard
- Analytics
- Reports
- Charts
- Search
- Filtering
- Pagination
- Sorting
- Image uploads
- Vehicle images
- Backend API changes
- Backend schema changes
- Authentication redesign
- Authorization redesign
- Redux
- MobX
- Zustand
- New frontend architecture
- New backend endpoints
- Performance optimizations
- Utility libraries unrelated to Sprint 09
- Documentation refactoring
- Sprint 10 functionality

Implement ONLY the Vehicle Frontend UI required for Sprint 09.

Stop immediately after Sprint 09 is complete.

Do not continue to Sprint 10 without approval.

---

# Important Notes

Preserve all existing functionality.

Do not modify completed backend modules unless absolutely required.

Do not introduce breaking changes.

If a better frontend architecture is discovered during implementation, do NOT implement it automatically.

Instead:

- Explain the proposed improvement.
- Explain why it is better.
- Wait for approval before changing the approved architecture.

The approved project architecture always takes priority over personal implementation preferences.

When multiple implementation approaches are possible, choose the one that is most consistent with the existing codebase.

---

# Completion Report

After implementation is complete, provide a final report containing the following sections.

## Implementation Summary

Provide a brief summary of the work completed during Sprint 09.

---

## Files Created

List every new file created.

---

## Files Modified

List every existing file modified.

Explain why each file required modification.

---

## UI Components Added

List every new React component created.

Briefly describe the responsibility of each component.

---

## Pages Added

List every page implemented.

Include:

- Route
- Purpose

---

## API Integration

Explain how the frontend integrates with the existing Vehicle CRUD APIs.

Confirm that no backend changes were required.

---

## Documentation Updated

State whether any documentation was updated.

If updated, explain exactly what changed and why.

If no documentation changes were required, explicitly state that the existing documentation already reflected the Sprint 09 implementation.

---

## Verification Results

Confirm:

- Frontend builds successfully.
- Frontend runs successfully.
- Vehicle CRUD UI functions correctly.
- Existing authentication remains unaffected.
- Backend remains unaffected.
- Navigation functions correctly.

---

## Manual Testing Performed

Summarize the manual verification completed for:

- Vehicle List
- Add Vehicle
- Edit Vehicle
- Delete Vehicle
- Authentication
- Error handling
- Loading states

---

## Risks Found

List any implementation risks, technical debt, or recommended improvements discovered during Sprint 09.

Do not implement those improvements automatically.

---

## Ready For Sprint 10?

State whether the project is ready to begin Sprint 10 (Vehicle Frontend Integration).

Do not continue to Sprint 10 without approval.