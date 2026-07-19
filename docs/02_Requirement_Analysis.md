# Phase 1 - Requirement Analysis

## Purpose

The purpose of this document is to define the functional and non-functional requirements, business rules, assumptions, constraints, project scope, and planned enhancements for the Car Dealership Inventory Management System before development begins.

This document acts as the foundation for system architecture, database design, API design, UI planning, testing, and implementation.

---

# 1. Functional Requirements

## FR-1 Authentication & Authorization

The system shall provide secure authentication and authorization using JWT.

Features include:

- Admin-controlled employee registration
- User login
- JWT-based authentication
- Role-based authorization
- Logout functionality

Roles:

- Admin
- Employee

---

## FR-2 Vehicle Inventory Management

The system shall allow administrators to manage dealership inventory.

Features include:

- Add Vehicle
- Update Vehicle
- Delete Available Vehicle
- View Vehicle Details
- View Vehicle List

---

## FR-3 Vehicle Search

The system shall allow users to quickly locate vehicles.

Features include:

- Search by Manufacturer
- Search by Model
- Filter by Availability
- Filter by Price (if implemented)

---

## FR-4 Vehicle Sales

Employees can sell available vehicles through the Sales module, subject to seller-identity enforcement.

Features include:

- Create a Sale record
- Prevent duplicate sales
- Automatically update vehicle status to Sold
- Capture customer details during sale

---

## FR-5 Inventory Monitoring

The system shall provide inventory visibility.

Features include:

- Available Inventory
- Sold Inventory
- Low Stock Monitoring
- Restocking Inventory

---

## FR-6 Dashboard

The system shall provide dashboards for different user roles.

Admin Dashboard:

- Inventory Summary
- Low Stock Information
- Recent Vehicles
- Quick Actions

Employee Dashboard:

- Available Inventory
- Search
- Sales Workflow

---

# 2. Non-Functional Requirements

The application shall satisfy the following quality attributes.

## Security

- JWT Authentication
- Password Hashing
- Protected APIs
- Role-Based Access Control

---

## Performance

- Fast search
- Responsive UI
- Efficient database queries

---

## Reliability

- Prevent duplicate sales
- Prevent invalid inventory operations
- Maintain data consistency

---

## Usability

- Clean interface
- Easy navigation
- Minimal learning curve

---

## Maintainability

- Clean Architecture
- SOLID Principles
- Modular Codebase

---

## Scalability

The architecture should allow future expansion without major redesign.

Examples:

- Multi-branch dealerships
- Analytics
- Customer Management

---

## Availability

The system should remain stable during normal dealership operations.

---

## Compatibility

The application should run in modern web browsers.

---

# 3. Business Rules

## BR-1 Vehicle Identity

Each physical vehicle represents one inventory record.

Every vehicle must have a unique VIN/Chassis Number.

VIN duplication is not allowed.

---

## BR-2 Vehicle Status

Supported statuses:

- Available
- Sold

Future versions may introduce:

- Reserved
- Inactive

---

## BR-3 Sale Rule

Only Available vehicles can be sold.

After sale:

Available → Sold

A Sold vehicle cannot be sold again.

---

## BR-4 Delete Rule

Available vehicles may be deleted.

Sold vehicles cannot be deleted because they represent completed business transactions.

---

## BR-5 Edit Rule

Available vehicles can be edited.

Sold vehicles cannot be modified.

---

## BR-6 Restock Rule

Restocking creates new vehicle records.

Inventory quantity is never increased by editing an existing record.

---

## BR-7 Search Rule

Employees primarily work with Available vehicles.

Administrators can view both Available and Sold inventory.

---

## BR-8 Role Permissions

### Admin

Can:

- Manage Inventory
- Restock
- Delete Available Vehicles
- Register Employees
- View Dashboard

### Employee

Can:

- Search Inventory
- View Vehicles
- Record Vehicle Sales

Cannot:

- Add Vehicles
- Delete Vehicles
- Restock
- Register Users

---

## BR-9 Validation Rules

The system shall validate:

- VIN must be unique
- Manufacturer is required
- Model is required
- Price must be greater than zero
- Manufacturing year cannot be in the future

---

## BR-10 Audit Rule

Every record shall maintain:

- Created At
- Updated At

---

# 4. Constraints

## Assignment Constraints

All mandatory assignment requirements must be implemented.

---

## Technology Constraints

Backend:

- FastAPI

Frontend:

- React

Database:

- PostgreSQL

Authentication:

- JWT

---

## Time Constraints

Priority is given to:

- High Business Value
- Low Implementation Complexity

---

## Code Quality Constraints

The project shall follow:

- SOLID Principles
- Clean Architecture
- Test-Driven Development
- Documentation
- Professional Git History

---

## Scope Constraints

Version 1 intentionally excludes:

- Finance
- Insurance
- Service Records
- Multi-Branch Support
- Payment Gateway
- Advanced Analytics

---

## User Constraints

Primary users are dealership staff.

The interface should prioritize simplicity and efficiency.

---

## Scalability Constraints

Although Version 1 supports one dealership, the architecture should allow future expansion.

---

## Security Constraints

Sensitive operations require authenticated users with appropriate roles.

---

## Recruiter Constraint

Every major engineering decision must have a clear technical or business justification.

---

# 5. Assumptions

- The system is designed for a single dealership.
- Employee accounts are created only by administrators.
- Every vehicle has a valid and unique VIN.
- Internet connectivity is available.
- One purchase transaction sells one vehicle.
- Inventory updates occur immediately.
- Employees enter accurate information.
- The application is seeded with one default administrator account during initial deployment.
- The administrator should change the default password after the first login.

---

# 6. Scope

## Core Scope

### Authentication

- Login
- Admin Registration of Employees
- JWT Authentication
- Role-Based Access

### Inventory

- Add Vehicle
- Update Vehicle
- Delete Available Vehicle
- View Inventory

### Search

- Manufacturer
- Model
- Availability
- Price Filter (Optional)

### Sales

- Create Sale record
- Prevent duplicate sales
- Store Customer Name
- Store Customer Phone Number

### Inventory Monitoring

- Available Inventory
- Sold Inventory
- Low Stock
- Restocking

### Dashboard

- Inventory Summary
- Dashboard Cards
- Quick Actions

---

## Value-Added Scope

### User Experience

- Confirmation Dialogs
- Loading Indicators
- Toast Notifications
- Empty State Screens
- Smart Form Validation

### Security

- Protected Routes
- Password Change Recommendation
- JWT Expiration Handling
- Role-Based UI

### Data Integrity

- VIN Validation
- Year Validation
- Price Validation
- Prevent Editing Sold Vehicles
- Prevent Deleting Sold Vehicles

### Business Improvements

- Dashboard Summary Cards
- Low Stock Alerts
- Status Badges
- Recently Added Vehicles

### Engineering Improvements

- Clean Architecture
- SOLID Principles
- Repository Pattern
- Service Layer
- DTO Validation
- Global Exception Handling
- Automated Testing
- Docker Support
- Environment Configuration
- Swagger Documentation
- Professional README
- PROMPTS.md

---

## Future Scope

### Inventory

- Vehicle Reservation
- Vehicle Images
- CSV Import/Export

### Sales

- Customer Management Module
- Customer Purchase History
- Invoice Generation
- Payment Tracking

### Management

- Multi-Branch Support
- Reports
- Analytics Dashboard
- Revenue Statistics

### Integrations

- Email Notifications
- SMS Notifications
- QR/Barcode Support
- Manufacturer API Integration

### Advanced Features

- Audit Logs
- Soft Delete
- Activity History
- Role Management
- Two-Factor Authentication
- Password Reset
- AI Demand Forecasting
- Price Recommendation Engine

---

# 7. Engineering Trade-offs

The following features were intentionally deferred to keep Version 1 focused and maintain high implementation quality.

| Feature                    | Decision | Reason                                           |
|----------------------------|----------|--------------------------------------------------|
| Vehicle Reservation        | Deferred | Valuable but increases workflow complexity       |
| Multi-Branch Support       | Deferred | Single dealership assumption                     |
| Customer Management Module | Deferred | Future Sale information is sufficient for Version 1 |
| Service History            | Deferred | Separate business domain                         |
| Payment Gateway            | Deferred | Outside assignment scope                         |
| AI Forecasting             | Deferred | Better suited for Version 2 or Version 3         |
|------------------------------------------------------------------------------------------|
---

# Phase 1 Summary

Version 1 focuses on delivering a realistic dealership inventory management system with clean architecture, strong engineering practices, thoughtful business rules, and selected product enhancements that improve usability without unnecessary complexity.

The project emphasizes solving real dealership problems rather than simply implementing CRUD operations. Future enhancements have been intentionally documented to demonstrate product thinking and long-term system evolution.
