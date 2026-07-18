# 1. UI Overview

## Purpose

The Car Dealership Inventory Management System provides a simple, intuitive, and responsive web interface for managing vehicle inventory, purchases, and users. The UI is designed to help employees perform daily tasks efficiently while allowing administrators to manage the system with ease.

---

## Objectives

- Provide a clean and easy-to-use interface.
- Minimize the number of clicks required for common tasks.
- Ensure consistency across all pages.
- Deliver a responsive experience for desktop and laptop users.
- Display clear feedback for user actions and validation errors.

---

## Technology

- React.js
- Material UI (MUI)
- React Router
- Axios

Material UI's default design system will be used to provide a modern, responsive, and consistent user experience without extensive custom styling.

---

## Target Users

- **Administrator** – Manages users, vehicles, purchases, and system operations.
- **Employee** – Searches vehicles, records purchases, and views assigned dashboard information.

---

## UI Scope

The application includes the following screens:

- Login
- Dashboard
- Vehicle Management
- Purchase Management
- User Management (Admin)
- User Profile

Each screen is designed with simplicity, usability, and maintainability as the primary goals.

---

## Notes for Developers

- Keep the interface simple and uncluttered.
- Reuse common UI components wherever possible.
- Prioritize functionality and usability over visual complexity.
- Follow Material UI design patterns for consistency.

# 2. Design Principles

The user interface is designed to prioritize usability, consistency, and efficiency. Every screen should help users complete their tasks with minimal effort while maintaining a clean and professional appearance.

---

## Core Principles

### Simplicity

- Keep the interface clean and uncluttered.
- Display only information relevant to the current task.
- Avoid unnecessary animations or decorative elements.

---

### Consistency

- Use the same layout across all pages.
- Maintain consistent colors, buttons, forms, and navigation.
- Follow Material UI design patterns throughout the application.

---

### Ease of Navigation

- Allow users to access major features within one or two clicks.
- Keep navigation predictable using a fixed sidebar and top navigation bar.
- Clearly highlight the currently active page.

---

### Responsive Design

- Support common desktop and laptop screen sizes.
- Ensure tables, forms, and navigation remain usable on smaller screens.

---

### User Feedback

Provide immediate feedback for user actions through:

- Success notifications
- Error messages
- Validation messages
- Confirmation dialogs for critical actions

---

### Accessibility

- Use descriptive labels for all form fields.
- Ensure buttons and icons are easy to identify.
- Maintain sufficient spacing between interactive elements.

---

## Notes for Developers

- Prioritize functionality over visual complexity.
- Reuse common UI components to maintain consistency.
- Keep user interactions simple, predictable, and intuitive.

# 3. Application Layout

The application follows a dashboard-based layout to provide a consistent user experience across all pages.

---

## Overall Layout

```
+--------------------------------------------------------------+
| Logo | Page Title                  User Menu | Logout        |
+----------------------+---------------------------------------+
|                      |                                       |
|      Sidebar         |           Main Content                |
|                      |                                       |
|                      |                                       |
|                      |                                       |
+----------------------+---------------------------------------+
```

---

## Layout Components

| Component | Description |
|-----------|-------------|
| Header | Displays logo, page title, logged-in user, and logout button. |
| Sidebar | Provides navigation to all major modules. |
| Main Content | Displays the currently selected page, including tables, forms, and dashboard widgets. |

---

## Header

### Components

- Application Logo
- Current Page Title
- Logged-in User Name
- User Profile Menu
- Logout Button

---

## Sidebar Navigation

### Administrator

- Dashboard
- Vehicles
- Purchases
- Users
- Profile

### Employee

- Dashboard
- Vehicles
- Purchases
- Profile

> **Note:** Navigation items are displayed based on the user's role.

---

## Main Content

The main content area displays the selected module and may include:

- Dashboard Cards
- Data Tables
- Search & Filters
- Forms
- Dialog Boxes
- Success/Error Notifications
- Pagination

---

## Common Layout Rules

- Header and Sidebar remain visible on all authenticated pages.
- The page title updates automatically based on the selected module.
- Tables should support scrolling for large datasets.
- Forms should be centered and easy to read.
- Important actions (Add, Save, Delete) should remain clearly visible.

---

## Notes for Developers

- Maintain a consistent layout across all pages.
- Reuse common components wherever possible.
- Avoid unnecessary page reloads by using React Router navigation.
- Keep the interface clean, responsive, and user-friendly.

# 4. Page Designs

---

# 4.1 Login Page

**Purpose**

Authenticate users before accessing the system.

| Component | Description |
|-----------|-------------|
| Email Field | Enter registered email |
| Password Field | Enter password |
| Login Button | Authenticate user |

**Validation**

- Email is required.
- Password is required.
- Display error for invalid credentials.

---

# 4.2 Dashboard

**Purpose**

Provide a quick overview of dealership operations.

| Widget | Description |
|--------|-------------|
| Total Vehicles | Total inventory count |
| Available Vehicles | Vehicles available for sale |
| Sold Vehicles | Total sold vehicles |
| Recent Purchases | Latest purchase records |

**Actions**

- View Inventory
- Add Vehicle (Admin)
- Purchase Vehicle

---

# 4.3 Vehicle List

**Purpose**

View and manage vehicle inventory.

| Component | Description |
|-----------|-------------|
| Search Bar | Search vehicles |
| Filter | Filter by availability |
| Vehicle Table | Display vehicle details |
| Pagination | Navigate records |

**Actions**

- View
- Edit (Admin)
- Delete (Admin)

---

# 4.4 Add Vehicle

**Purpose**

Register a new vehicle in the inventory.

**Fields**

- Manufacturer
- Model
- Year
- Color
- VIN
- Price
- Status

**Actions**

- Save
- Reset
- Cancel

---

# 4.5 Edit Vehicle

**Purpose**

Update an existing vehicle.

**Fields**

Same as Add Vehicle.

**Actions**

- Update
- Cancel

---

# 4.6 Purchase Vehicle

**Purpose**

Record a vehicle sale.

**Fields**

- Customer Name
- Customer Phone
- Selected Vehicle
- Selling Price

**Actions**

- Complete Purchase
- Cancel

---

# 4.7 Purchase History

**Purpose**

View completed purchases.

| Component | Description |
|-----------|-------------|
| Search | Search purchases |
| Purchase Table | Purchase records |
| Pagination | Navigate records |

**Actions**

- View Details

---

# 4.8 User Management (Admin)

**Purpose**

Manage system users.

| Component | Description |
|-----------|-------------|
| User Table | List all users |
| Search | Find users |
| Role Badge | Display user role |

**Actions**

- Add User
- Edit User
- Deactivate User

---

# 4.9 Profile

**Purpose**

Allow users to view their account information.

**Information**

- Full Name
- Email
- Role

**Actions**

- Change Password
- Update Profile

# 5. Common Components

The following reusable components should be used throughout the application to maintain consistency and reduce duplicate code.

| Component | Purpose |
|-----------|---------|
| Navbar | Display application title, logged-in user, and logout option. |
| Sidebar | Navigate between application modules. |
| Dashboard Card | Display key statistics on the dashboard. |
| Data Table | Display vehicles, purchases, and users. |
| Search Bar | Quickly search records. |
| Filter Dropdown | Filter records by status or category. |
| Form Fields | Collect user input with validation. |
| Buttons | Perform actions such as Add, Save, Update, Delete, and Cancel. |
| Confirmation Dialog | Confirm critical actions like deletion. |
| Snackbar / Toast | Display success and error notifications. |
| Loading Spinner | Indicate ongoing API requests. |
| Pagination | Navigate through large datasets. |
| Empty State | Display a message when no records are available. |

---

## Notes for Developers

- Build reusable React components whenever possible.
- Follow Material UI component standards.
- Keep component styling consistent across the application.
- Avoid duplicating UI logic.

# 6. Future UI Enhancements

The current UI is designed to satisfy the project requirements. Future versions may include:

- Dark Mode
- Advanced Search & Filters
- Data Export (Excel/PDF)
- Charts and Analytics Dashboard
- Mobile-optimized Layout
- User Profile Photo
- Keyboard Shortcuts
- Multi-language Support

---

## Notes for Developers

- Prioritize usability over visual complexity.
- Introduce new features without affecting the existing user experience.
- Continue following Material UI design guidelines.

