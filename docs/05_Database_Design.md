# 1. Database Overview

## Purpose

This document records all database-related architectural decisions for the Car Dealership Inventory Management System.

It serves as the single source of truth for:
- Database architecture
- Entity design
- Relationships
- Constraints
- Business rules
- Performance decisions
- Migration strategy
- Future database expansion

Developers should follow this document before modifying the database schema.

---

# 2. Database Goals

## Primary Goals

- Build a reliable inventory management database.
- Maintain accurate dealership inventory.
- Store permanent sales history.
- Support secure authentication.
- Prevent invalid business operations.
- Keep the schema simple and maintainable.
- Follow industry-standard relational database practices.

---

## Design Philosophy

The database is designed around actual dealership workflows instead of academic database concepts.

Every table, column, relationship, and constraint must solve a real business problem.

Version 1 prioritizes:

- Simplicity
- Maintainability
- Data Integrity
- Security
- Performance
- Future scalability

Features without immediate business value are intentionally deferred instead of partially implemented.

---

## Database Scope (Version 1)

Included

- User Management
- Vehicle Inventory
- Purchase Records
- Role-Based Access Control
- Dashboard Statistics
- Inventory Search
- Vehicle Sales

Excluded

- Customer Management
- Manufacturer Management
- Payments
- Invoices
- Vehicle Images
- Reservations
- Analytics
- Notifications
- Multi-Branch Support
- Service History

These features are planned for future versions.

---

# 3. Technology Decisions

## Final Stack

| Component | Technology |
|------------|------------|
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Migration | Alembic |
| Driver | psycopg |
| Configuration | python-dotenv |

---

## Final Decisions

- PostgreSQL selected as the primary database.
- SQLAlchemy will be used for all database operations.
- Raw SQL should not be used inside business logic.
- Alembic manages all schema changes.
- Database credentials stored using environment variables.
- Every schema modification must go through migrations.

---

## Reasons

### PostgreSQL

Selected because it provides:

- ACID transactions
- Strong constraint support
- Excellent indexing
- High scalability
- Production-ready architecture
- Strong FastAPI integration

---

### SQLAlchemy

Selected because:

- ORM abstraction
- Cleaner code
- Repository Pattern support
- Easier testing
- Maintainable architecture

---

### Alembic

Selected because:

- Schema version control
- Safe upgrades
- Rollback support
- Team collaboration
- Repeatable deployments

---

## Rejected Alternatives

### SQLite

Rejected because:

- Limited concurrency
- Better suited for prototypes
- Future migration would be required

---

### MySQL

Rejected because:

- PostgreSQL provides stronger constraint support.
- Better aligned with project architecture.
- Better ecosystem for Python development.

---

## Notes for Developers

Do not replace PostgreSQL, SQLAlchemy, or Alembic unless the entire architecture is being redesigned.

# 4. Entity Design

## Overview

Version 1 of the system contains **three core entities**.

| Entity | Purpose |
|---------|---------|
| User | Represents authenticated dealership staff members. |
| Vehicle | Represents each physical vehicle in dealership inventory. |
| Purchase | Represents completed vehicle sales. |

Only entities required for Version 1 are included. Features such as Customer Management, Manufacturer Management, Payments, and Reservations are intentionally deferred.

---

# 4.1 User Entity

## Purpose

Represents authenticated dealership staff who access the system.

Users are responsible for:

- Managing inventory (Admin)
- Registering employees (Admin)
- Processing vehicle purchases (Employee)
- Accessing dashboards
- Logging into the application

---

## Final Attributes

| Column | Type | Notes |
|---------|------|------|
| id | Integer | Primary Key |
| full_name | String | Employee full name |
| email | String | Unique login identifier |
| password_hash | String | Encrypted password |
| phone | String | Contact number |
| role | Enum | ADMIN / EMPLOYEE |
| is_active | Boolean | Soft account status |
| created_at | Timestamp | Record creation time |
| updated_at | Timestamp | Last modification time |

---

## Final Decisions

- Email is used for login.
- Passwords are never stored in plain text.
- Role stored as ENUM.
- Users are deactivated instead of deleted.
- Only authenticated users can access APIs.
- Public registration is disabled.
- Admin creates employee accounts.

---

## Business Rules

- Email must be unique.
- Password must always be hashed.
- Every user must have exactly one role.
- Only active users can log in.
- Only Admin can create employees.
- Users with purchase history cannot be deleted.

---

## Constraints

- Primary Key → id
- Unique → email
- NOT NULL → full_name
- NOT NULL → email
- NOT NULL → password_hash
- NOT NULL → role
- Default → is_active = true

---

## Rejected Alternatives

### Username Login

Rejected.

Reason:
- Email is already unique.
- Reduces unnecessary fields.

---

### Role Table

Rejected.

Reason:
- Only two fixed roles exist.
- Separate table adds unnecessary complexity.

---

### Hard Delete

Rejected.

Reason:
- Purchase history must remain valid.
- Deactivation preserves historical references.

---

## Future Scope

- Profile Photo
- Password Reset
- Last Login
- Login History
- Multi-Factor Authentication
- Account Locking

---

## Notes for Developers

- Never expose password_hash in API responses.
- Role permissions must always be validated on the backend.
- Do not implement public signup.
- User deletion should remain disabled.

---

# 4.2 Vehicle Entity

## Purpose

Represents one physical vehicle owned by the dealership.

Each vehicle corresponds to exactly one inventory record.

Inventory is tracked per physical vehicle, not by quantity.

---

## Vehicle Lifecycle

AVAILABLE

↓

Purchased

↓

SOLD

Vehicle records are never removed after being sold.

---

## Final Attributes

| Column | Type | Notes |
|---------|------|------|
| id | Integer | Primary Key |
| vin | String | Unique Vehicle Identification Number |
| manufacturer | String | Brand name |
| model | String | Vehicle model |
| year | Integer | Manufacturing year |
| color | String | Vehicle color |
| fuel_type | Enum | Petrol/Diesel/CNG/Hybrid/Electric |
| transmission | Enum | Manual/Automatic |
| condition | Enum | New/Used |
| mileage | Integer | Kilometer reading |
| purchase_price | Decimal | Dealer purchase cost |
| selling_price | Decimal | Selling price |
| description | Text | Optional notes |
| status | Enum | AVAILABLE / SOLD |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Update timestamp |

---

## Final Decisions

- One physical vehicle = one database row.
- VIN uniquely identifies every vehicle.
- Manufacturer stored as plain text.
- Status managed using ENUM.
- Condition managed using ENUM.
- Inventory quantity is not maintained.
- Restocking inserts new vehicle records.

---

## Business Rules

- VIN must be unique.
- Only AVAILABLE vehicles can be sold.
- SOLD vehicles cannot be edited.
- SOLD vehicles cannot be deleted.
- Year cannot exceed current year.
- Mileage cannot be negative.
- Selling price must be greater than or equal to purchase price.

---

## Constraints

- Primary Key → id
- Unique → vin
- CHECK → mileage >= 0
- CHECK → purchase_price > 0
- CHECK → selling_price > 0

---

## Rejected Alternatives

### Manufacturer Table

Rejected.

Reason:
- No business benefit.
- Additional joins.
- Simple text storage is sufficient.

---

### Stock Table

Rejected.

Reason:
- Inventory managed per physical vehicle.

---

### Vehicle Images

Deferred.

Reason:
- Outside Version 1 scope.

---

### Reserved Status

Deferred.

Reason:
- Reservation module not included.

---

## Future Scope

- Vehicle Images
- Reservation Status
- Service History
- Multiple Pricing
- Insurance Information
- Warranty Details

---

## Notes for Developers

- Never update VIN after creation.
- Status changes only through purchase workflow.
- Inventory count should always be calculated from AVAILABLE vehicles.

# 4.3 Purchase Entity

## Purpose

Represents a completed vehicle sale.

A Purchase record permanently stores the details of a vehicle transaction and acts as the dealership's historical sales record.

Every purchase is linked to:
- One Vehicle
- One Employee (Seller)

---

## Final Attributes

| Column | Type | Notes |
|---------|------|------|
| id | Integer | Primary Key |
| vehicle_id | Integer | References Vehicle |
| customer_name | String | Customer full name |
| customer_phone | String | Customer contact number |
| sold_by | Integer | References User |
| selling_price | Decimal | Final selling price snapshot |
| purchase_date | Timestamp | Date & time of purchase |
| notes | Text | Optional remarks |
| created_at | Timestamp | Record creation timestamp |

---

## Final Decisions

- One purchase represents one completed vehicle sale.
- Customer information is stored directly in the Purchase table.
- Selling price is copied from Vehicle during purchase.
- Purchase records are permanent.
- Purchase records cannot be deleted.
- Purchase records cannot be reassigned to another vehicle.

---

## Business Rules

- A vehicle can only have one purchase.
- Purchase must reference an existing vehicle.
- Purchase must reference an existing employee.
- Customer Name is mandatory.
- Customer Phone is mandatory.
- Selling Price is stored as a historical snapshot.
- Purchase creation and vehicle status update must occur within a single transaction.

---

## Editable Fields

Allowed

- customer_name
- customer_phone
- notes

Not Allowed

- vehicle_id
- sold_by
- selling_price
- purchase_date

---

## Constraints

- Primary Key → id
- Foreign Key → vehicle_id
- Foreign Key → sold_by
- Unique → vehicle_id
- NOT NULL → customer_name
- NOT NULL → customer_phone
- NOT NULL → selling_price
- NOT NULL → purchase_date

---

## Rejected Alternatives

### Customer Table

Rejected.

Reason:
- Customer management is outside Version 1 scope.
- Customer information is only required during purchase.
- Separate table would increase complexity without business value.

---

### Payment Table

Deferred.

Reason:
- Payment processing is not included in Version 1.

---

### Multiple Purchases per Vehicle

Rejected.

Reason:
- One physical vehicle can only be sold once.

---

## Future Scope

- Customer Entity
- Payment Records
- Invoice Generation
- Financing Information
- Delivery Status
- Purchase Cancellation Workflow

---

## Notes for Developers

- Purchase records represent historical business data.
- Never overwrite historical selling prices.
- Vehicle status must change to SOLD immediately after successful purchase.
- Purchase creation must always use a database transaction.

---

# 4.4 Entity Relationships

## Relationship Summary

| Parent Entity | Child Entity | Relationship |
|--------------|-------------|--------------|
| User | Purchase | One-to-Many |
| Vehicle | Purchase | One-to-One |

---

## User → Purchase

One employee can process multiple vehicle sales.

Relationship

```
User (1)
    │
    │
    └──────< Purchase (Many)
```

Foreign Key

```
purchase.sold_by → user.id
```

Delete Rule

- Users are never deleted.
- Users are deactivated using `is_active`.

---

## Vehicle → Purchase

One vehicle can only be sold once.

Relationship

```
Vehicle (1)
      │
      │
      └──────── Purchase (1)
```

Foreign Key

```
purchase.vehicle_id → vehicle.id
```

Delete Rule

- Vehicle cannot be deleted after sale.
- Purchase history must remain valid.

---

## Final Decisions

- Purchase acts as the bridge between Vehicle and User.
- Customer is not an independent entity.
- Relationships are intentionally minimal.
- Avoid unnecessary joins.

---

# 4.5 Deferred Entities

The following entities were intentionally excluded from Version 1.

---

## Customer

Status

Deferred

Reason

Customer management is outside the current project scope.

Customer details required during purchase are stored directly inside the Purchase table.

---

## Manufacturer

Status

Deferred

Reason

Manufacturer names are stored as plain text.

Creating a Manufacturer table provides no additional business value.

---

## Vehicle Images

Status

Deferred

Reason

Image upload and storage are not required for inventory management.

---

## Reservation

Status

Deferred

Reason

Vehicle reservation workflow is not included in Version 1.

Vehicle status only supports:

- AVAILABLE
- SOLD

---

## Payments

Status

Deferred

Reason

Payment processing is outside the assignment scope.

---

## Invoice

Status

Deferred

Reason

Invoices can be generated later from Purchase records.

---

## Reports & Analytics

Status

Deferred

Reason

Basic dashboard statistics are sufficient for Version 1.

Advanced reporting can be added later.

---

## Notifications

Status

Deferred

Reason

No notification system is required.

---

## Multi-Branch Support

Status

Deferred

Reason

Version 1 targets a single dealership.

---

## Audit Logs

Status

Deferred

Reason

created_at and updated_at provide sufficient tracking for Version 1.

Detailed audit logging can be introduced later.

---

## Soft Delete

Status

Deferred

Reason

Only User accounts require deactivation.

Vehicle and Purchase records remain permanently stored.

---

## AI Features

Status

Deferred

Reason

Machine Learning and predictive analytics are outside the scope of this project.

---

# Notes for Developers

Before introducing any deferred entity:

- Verify that it solves a real business problem.
- Ensure it fits the project scope.
- Avoid adding tables solely for normalization.
- Prefer simplicity unless additional complexity provides measurable value.

# 5. Database Rules & Constraints

## Purpose

This section defines all database constraints, business rules, validation rules, and transaction rules that must always be enforced throughout the application.

These rules act as the authoritative reference for backend implementation and database schema design.

---

# 5.1 Primary Keys

## Final Decisions

| Table | Primary Key |
|---------|------------|
| User | id |
| Vehicle | id |
| Purchase | id |

### Notes

- All primary keys use auto-increment integers.
- Primary keys are immutable.
- Primary keys are never reused.

---

# 5.2 Foreign Keys

## Final Decisions

| Child Table | Column | References |
|--------------|--------|------------|
| Purchase | vehicle_id | Vehicle.id |
| Purchase | sold_by | User.id |

---

## Rules

- Foreign keys must always reference existing records.
- Invalid references must be rejected.
- Foreign key values cannot be NULL.

---

# 5.3 Unique Constraints

## User

- email must be unique.

Reason

Two employees cannot share the same login account.

---

## Vehicle

- vin must be unique.

Reason

Each physical vehicle has a unique VIN.

---

## Purchase

- vehicle_id must be unique.

Reason

One vehicle can only be sold once.

---

# 5.4 NOT NULL Constraints

## User

- full_name
- email
- password_hash
- role

---

## Vehicle

- vin
- manufacturer
- model
- year
- fuel_type
- transmission
- condition
- mileage
- purchase_price
- selling_price
- status

---

## Purchase

- vehicle_id
- customer_name
- customer_phone
- sold_by
- selling_price
- purchase_date

---

# 5.5 CHECK Constraints

## Vehicle

Mileage

```
mileage >= 0
```

Purchase Price

```
purchase_price > 0
```

Selling Price

```
selling_price > 0
```

---

## Service Layer Validation

The following rules are enforced in the service layer instead of database CHECK constraints.

- selling_price >= purchase_price
- year <= current year
- New vehicles should have minimal mileage
- Vehicle must be AVAILABLE before purchase

Reason

These rules depend on business logic rather than fixed database constraints.

---

# 5.6 ENUM Values

## User Role

```
ADMIN
EMPLOYEE
```

---

## Vehicle Status

```
AVAILABLE
SOLD
```

---

## Vehicle Condition

```
NEW
USED
```

---

## Fuel Type

```
PETROL
DIESEL
CNG
HYBRID
ELECTRIC
```

---

## Transmission

```
MANUAL
AUTOMATIC
```

---

# 5.7 Business Rules

## BR-1

VIN must be unique.

---

## BR-2

Vehicle status can only be:

- AVAILABLE
- SOLD

---

## BR-3

Only AVAILABLE vehicles can be sold.

---

## BR-4

AVAILABLE vehicles may be deleted.

---

## BR-5

SOLD vehicles cannot be deleted.

---

## BR-6

AVAILABLE vehicles may be edited.

---

## BR-7

SOLD vehicles cannot be edited.

---

## BR-8

Restocking creates new vehicle records.

Inventory quantity is never increased on an existing record.

---

## BR-9

Employees can search only AVAILABLE vehicles.

Admins can view both AVAILABLE and SOLD vehicles.

---

## BR-10

Vehicle validation

- VIN unique
- Manufacturer required
- Model required
- Positive prices
- Valid manufacturing year

---

## BR-11

Vehicle mileage cannot be negative.

---

## BR-12

Vehicle year cannot exceed the current year.

---

## BR-13

NEW vehicles should have minimal mileage.

---

## BR-14

Selling price must not be lower than purchase price.

---

## BR-15

Purchase must reference an existing vehicle.

---

## BR-16

Purchase must reference an existing employee.

---

## BR-17

Customer Name is mandatory.

---

## BR-18

Customer Phone is mandatory.

---

## BR-19

One vehicle can have only one purchase.

---

## BR-20

Selling price is copied into Purchase during sale.

Future price changes must not affect historical purchases.

---

## BR-21

Purchase creation and vehicle status update must execute inside one database transaction.

---

## BR-22

Historical purchase records are permanent.

Purchases are never deleted.

---

# 5.8 Delete Policy

## User

Delete

❌ Not Allowed

Action

Deactivate account using:

```
is_active = false
```

Reason

Historical purchase records must remain valid.

---

## Vehicle

Delete

✅ Allowed

Condition

Vehicle status must be AVAILABLE.

---

Delete

❌ Not Allowed

Condition

Vehicle status is SOLD.

---

## Purchase

Delete

❌ Never Allowed

Reason

Purchases represent permanent business history.

---

# 5.9 Update Policy

## User

Allowed

- full_name
- phone
- password
- is_active

Not Allowed

- id

---

## Vehicle

Allowed (AVAILABLE only)

- manufacturer
- model
- color
- prices
- description

Not Allowed

- VIN
- status after SOLD

---

## Purchase

Allowed

- customer_name
- customer_phone
- notes

Not Allowed

- vehicle_id
- sold_by
- selling_price
- purchase_date

---

# 5.10 Transaction Rules

## Purchase Transaction

The following operations must execute within a single database transaction.

1. Validate vehicle availability.
2. Create Purchase record.
3. Update Vehicle status to SOLD.
4. Commit transaction.

If any step fails:

- Rollback transaction.
- No data should be modified.

---

## Notes for Developers

- Database constraints should protect data integrity.
- Business logic belongs in the service layer.
- Never rely only on frontend validation.
- Backend validation is mandatory.
- Database constraints and service validations must remain consistent.

# 6. Database Implementation Standards

## Purpose

This section defines implementation standards that must be followed while developing the database schema, SQLAlchemy models, repositories, and migrations.

These standards ensure consistency across the project and prevent different developers from implementing the database in different ways.

---

# 6.1 Naming Conventions

## Tables

Rules

- Use singular table names.
- Use lowercase.
- Use snake_case.

Examples

- user
- vehicle
- purchase

---

## Columns

Rules

- Use snake_case.
- Use descriptive names.
- Avoid abbreviations unless universally accepted.

Examples

- full_name
- purchase_price
- selling_price
- customer_phone
- created_at

---

## Primary Keys

Rule

Every table uses:

```
id
```

---

## Foreign Keys

Rules

Reference the parent entity.

Examples

```
vehicle_id
sold_by
```

---

## Constraint Names

Convention

```
pk_<table>

fk_<child>_<parent>

uq_<table>_<column>

idx_<table>_<column>

ck_<table>_<rule>
```

Examples

```
pk_vehicle

fk_purchase_vehicle

uq_vehicle_vin

idx_vehicle_status
```

---

# 6.2 Data Types

## Integer

Used For

- Primary Keys
- Foreign Keys
- Year
- Mileage

---

## String (VARCHAR)

Used For

- Names
- Email
- VIN
- Manufacturer
- Model
- Color
- Phone Numbers

---

## TEXT

Used For

- description
- notes

---

## ENUM

Used For

- role
- status
- condition
- fuel_type
- transmission

---

## DECIMAL (NUMERIC)

Used For

- purchase_price
- selling_price

Precision

```
NUMERIC(12,2)
```

---

## TIMESTAMP

Used For

- created_at
- updated_at
- purchase_date

---

# 6.3 Default Values

| Column | Default |
|---------|----------|
| is_active | true |
| status | AVAILABLE |
| mileage | 0 |
| created_at | Current Timestamp |
| updated_at | Current Timestamp |
| description | NULL |
| notes | NULL |

---

# 6.4 NULL Handling

Nullable

- description
- notes

Not Nullable

- All Primary Keys
- All Foreign Keys
- Required business fields

---

# 6.5 Character Limits

| Column | Limit |
|---------|-------|
| full_name | 100 |
| email | 255 |
| phone | 20 |
| manufacturer | 50 |
| model | 100 |
| color | 30 |
| vin | 17 |
| customer_name | 100 |
| customer_phone | 20 |

---

# 6.6 Decimal Precision

Purchase Price

```
NUMERIC(12,2)
```

Selling Price

```
NUMERIC(12,2)
```

Reason

- Accurate financial calculations.
- Avoid floating-point precision issues.

---

# 6.7 Timestamp Standards

Tables using timestamps

- User
- Vehicle
- Purchase

Rules

- created_at records creation time.
- updated_at updates on every modification.
- purchase_date stores sale completion time.

---

# 6.8 Indexing Strategy

Primary Keys

Automatically indexed.

---

Unique Indexes

- email
- vin

---

Search Indexes

Vehicle

- manufacturer
- model
- status
- condition
- fuel_type
- transmission

Purchase

- purchase_date
- sold_by

---

Composite Index

```
(manufacturer, status)
```

Reason

Supports the most common inventory search.

---

# 6.9 Query Optimization

Rules

- Always paginate inventory listings.
- Filter at database level.
- Avoid unnecessary joins.
- Never use SELECT *.
- Load only required columns.
- Index frequently searched fields.
- Use transactions for critical operations.

---

# 6.10 Pagination Strategy

Pagination is mandatory for:

- Vehicle Listing
- Purchase History

Recommended Default

```
20 records/page
```

Support

- page
- page_size

---

# 6.11 Developer Guidelines

Follow these standards while implementing the database.

- Never modify applied migrations.
- Never bypass repository layer.
- Never store plain text passwords.
- Never hardcode database credentials.
- Never expose internal IDs unnecessarily through APIs.
- Keep business logic in the service layer.
- Keep SQLAlchemy models focused on persistence.
- Validate input before database operations.
- Keep database schema synchronized through Alembic migrations.

# 7. Migration Strategy

## Purpose

This section defines how database schema changes are managed throughout the project.

All schema modifications must be version-controlled using Alembic to ensure every developer works with the same database structure.

---

# 7.1 Migration Tool

Selected Tool

- Alembic

Reason

- Database schema versioning
- Safe incremental updates
- Rollback support
- Repeatable deployments
- Team collaboration

---

# 7.2 Migration Workflow

Standard workflow

```
Modify SQLAlchemy Models
        ↓
Generate Migration
        ↓
Review Migration
        ↓
Apply Migration
        ↓
Verify Database
```

Rules

- Never modify database tables manually.
- Every schema change requires a migration.
- Always review autogenerated migrations before applying them.

---

# 7.3 Migration Order

Initial database setup should follow this order.

1. User
2. Vehicle
3. Purchase

Reason

Purchase depends on both User and Vehicle through foreign keys.

---

# 7.4 Seed Data

Default Administrator

| Field | Value |
|--------|-------|
| Name | System Administrator |
| Email | admin@dealer.com |
| Password | admin123 |
| Role | ADMIN |
| Active | true |

Rules

- Seed data should only create the initial administrator.
- No sample vehicles or purchases should be inserted automatically.

Security Note

- Change the default administrator password after first login.

---

# 7.5 Environment Configuration

Database configuration must be stored in environment variables.

Example

```env
DATABASE_URL=postgresql://username:password@localhost:5432/car_dealership
```

Rules

- Never hardcode credentials.
- Never commit `.env` files.
- Provide a `.env.example` file for setup.

---

# 7.6 Rollback Strategy

If a migration fails:

1. Stop deployment.
2. Roll back to the previous migration.
3. Fix the issue.
4. Generate a new migration.
5. Retry deployment.

Rules

- Never delete migration history.
- Never edit an already applied migration.
- Create a new migration to fix mistakes.

---

# 7.7 Developer Workflow

Database setup for a new developer:

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies.
4. Configure `.env`.
5. Create the PostgreSQL database.
6. Run Alembic migrations.
7. Seed the default administrator.
8. Start the application.

---

# 7.8 Migration Best Practices

- Keep migrations small and focused.
- Use descriptive migration names.
- Test migrations on a clean database.
- Commit migration files to version control.
- Keep SQLAlchemy models and migrations synchronized.
- Use transactions whenever possible.

---

# Notes for Developers

- Alembic is the only supported migration tool.
- Do not manually alter production schemas.
- Migration history is part of the project's source code.
- Every pull request affecting the database must include the required migration files.

# 8. Future Database Evolution

## Purpose

This section documents database enhancements intentionally deferred from Version 1.

These features should only be implemented when they solve a real business problem and fit the project requirements.

The current schema should remain as simple as possible while supporting future expansion.

---

# 8.1 Guiding Principles

Future database changes should follow these principles:

- Solve a real business requirement.
- Preserve existing data integrity.
- Avoid unnecessary normalization.
- Maintain backward compatibility whenever possible.
- Introduce new tables only when justified.
- Prefer extending existing entities before creating new ones.

---

# 8.2 Planned Enhancements

## Customer Management

Status

Deferred

Business Value

- Customer profiles
- Purchase history
- Repeat customer tracking
- Customer search

Expected Changes

New Table

```
customer
```

Purchase will reference:

```
customer_id
```

instead of storing customer details directly.

---

## Manufacturer Management

Status

Deferred

Business Value

- Standardized manufacturer data
- Manufacturer-specific reporting
- Logo and metadata support

Expected Changes

New Table

```
manufacturer
```

Vehicle will store:

```
manufacturer_id
```

instead of manufacturer text.

---

## Vehicle Images

Status

Deferred

Business Value

- Inventory photos
- Improved user experience
- Vehicle gallery

Expected Changes

New Table

```
vehicle_image
```

Relationship

```
Vehicle (1)

↓

VehicleImage (Many)
```

---

## Reservation System

Status

Deferred

Business Value

- Hold vehicles temporarily
- Prevent simultaneous sales
- Reservation expiry

Expected Changes

Vehicle Status

```
AVAILABLE
RESERVED
SOLD
```

New Table

```
reservation
```

---

## Payment Management

Status

Deferred

Business Value

- Payment tracking
- Multiple payment methods
- Outstanding balances

Expected Changes

New Table

```
payment
```

Relationship

```
Purchase (1)

↓

Payment (Many)
```

---

## Invoice Management

Status

Deferred

Business Value

- Printable invoices
- PDF generation
- Tax calculations

Expected Changes

New Table

```
invoice
```

Relationship

```
Purchase (1)

↓

Invoice (1)
```

---

## Service History

Status

Deferred

Business Value

- Maintenance tracking
- Repair history
- Warranty records

Expected Changes

New Table

```
service_record
```

Relationship

```
Vehicle (1)

↓

ServiceRecord (Many)
```

---

## Multi-Branch Support

Status

Deferred

Business Value

- Multiple dealership locations
- Branch-wise inventory
- Branch-level reporting

Expected Changes

New Table

```
branch
```

Vehicle

```
branch_id
```

User

```
branch_id
```

Purchase

```
branch_id
```

---

## Audit Logging

Status

Deferred

Business Value

- Track every database change
- Compliance
- User activity history

Expected Changes

New Table

```
audit_log
```

---

## Notifications

Status

Deferred

Business Value

- Low stock alerts
- Purchase notifications
- Employee notifications

Expected Changes

New Table

```
notification
```

---

## Advanced Analytics

Status

Deferred

Business Value

- Sales trends
- Inventory insights
- Business intelligence

Expected Changes

Analytical tables or materialized views may be introduced based on reporting requirements.

---

# 8.3 Evolution Rules

Future schema changes must follow these rules:

- Existing primary keys should never change.
- Existing foreign key relationships should remain stable.
- Existing APIs should remain compatible whenever possible.
- Use Alembic for every schema modification.
- Avoid breaking changes unless absolutely necessary.

---

# 8.4 Version Roadmap

## Version 1

- User Management
- Vehicle Inventory
- Purchase Management
- Authentication
- Dashboard
- Search

---

## Version 2

Recommended additions

- Customer Management
- Vehicle Images
- Reservation System
- Invoice Generation

---

## Version 3

Recommended additions

- Payment Management
- Service History
- Multi-Branch Support
- Notifications
- Advanced Reports

---

# Notes for Developers

Version 1 is intentionally minimal.

Before introducing any new table or relationship:

- Confirm the business requirement.
- Evaluate implementation complexity.
- Ensure it aligns with the existing architecture.
- Preserve backward compatibility wherever possible.
- Prefer incremental evolution over large-scale redesign.