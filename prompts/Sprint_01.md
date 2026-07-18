# Sprint 01 – Project Initialization

## Sprint Objective

Initialize the project by creating a clean and professional full-stack foundation for the Car Dealership Inventory Management System.

This sprint focuses only on project setup and does **not** implement any business logic.

---

## AI Prompt

|
V

# Development Mode

Work incrementally.

Complete one task at a time.

After each major task:

- Explain what was completed.
- Wait for confirmation before continuing.

Do not implement future sprints.

Do not generate unnecessary code.

Focus on quality over speed.

---

# Sprint 01 - Project Initialization

## Context

You are an experienced Senior Full Stack Software Engineer working on an existing software project.

This project has already completed its planning and architecture phase. The repository contains comprehensive documentation inside the `docs/` folder, including:

- Project Overview
- Requirement Analysis
- Development Standards
- System Architecture
- Database Design
- API Design
- UI/UX Design
- Implementation Plan
- Testing & Deployment Guide

These documents define every architectural and implementation decision for the project.

**Before writing any code, carefully study every document inside the `docs/` folder and strictly follow them throughout development.**

Do not redesign the architecture or make assumptions that contradict the documentation.

---

# Project

Car Dealership Inventory Management System

A full-stack web application that enables dealership employees to manage vehicle inventory, process vehicle purchases, manage users, and monitor dealership statistics.

This project is being developed as an internship assignment and therefore emphasizes:

- Clean Architecture
- Professional folder structure
- Readable code
- Maintainability
- Scalability
- Industry best practices

Code quality is more important than speed.

---

# Technology Stack

## Backend

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Pydantic
- Python 3.12+

## Frontend

- React (Vite)
- Material UI
- Axios
- React Router

## Version Control

- Git

---

# Objective of Sprint 01

Sprint 01 focuses ONLY on project initialization.

This sprint should NOT implement business logic.

This sprint should create a clean and production-ready project foundation for future development.

---

# Tasks

## 1. Study Documentation

Read every document inside the `docs/` folder before starting implementation.

All future decisions must follow these documents.

If documentation conflicts with your assumptions, documentation always wins.

---

## 2. Backend Initialization

Create the backend project.

Requirements:

- FastAPI application
- Python virtual environment (mention required packages)
- Proper folder structure according to documentation
- requirements.txt
- .env.example
- .gitignore
- README section if required
- Verify application starts successfully

Do not implement authentication or database models yet.

---

## 3. Frontend Initialization

Create the frontend project using Vite.

Install and configure:

- React
- Material UI
- React Router
- Axios

Remove unnecessary boilerplate.

Create a clean project structure according to the documentation.

Do not implement UI pages yet.

---

## 4. Repository Structure

Ensure the repository contains:

```
Car-Dealership-Inventory-System/

backend/
frontend/
docs/
prompts/
README.md
.gitignore
```

The structure should be clean and professional.

---

## 5. Configuration

Create initial configuration files where appropriate.

Examples include:

### Backend

- requirements.txt
- .env.example

### Frontend

- package.json
- vite.config.js

Only create the initial configuration.

No business configuration is required yet.

---

## 6. Verify Setup

Ensure:

### Backend

- FastAPI starts successfully

### Frontend

- React application starts successfully

No runtime errors should exist.

---

# Coding Standards

Follow every rule defined inside Development Standards documentation.

Additionally:

- Keep functions small.
- Use meaningful naming.
- Keep code modular.
- Avoid duplication.
- Avoid unnecessary comments.
- Prefer readability over cleverness.
- Write code that is easy for another developer to maintain.

---

# Important Constraints

Do NOT implement:

- Authentication
- Database models
- CRUD APIs
- JWT
- Alembic
- SQLAlchemy models
- Business logic
- Validation
- Dashboard
- Vehicle module
- Purchase module

Those belong to later sprints.

Stay strictly within Sprint 01.

---

# Expected Deliverables

At the end of Sprint 01, the repository should contain:

✓ Backend initialized

✓ Frontend initialized

✓ Folder structure created

✓ Dependencies installed

✓ Configuration files created

✓ FastAPI running

✓ React running

✓ Repository ready for Sprint 02

---

# Output Format

For every task:

1. Explain what you are doing.

2. Explain why it is necessary.

3. Generate the required files.

4. Explain any commands that must be executed.

5. Verify completion before moving to the next task.

Do not skip verification.

---

# Final Verification

Before declaring Sprint 01 complete, verify:

- Backend starts successfully.
- Frontend starts successfully.
- Repository structure matches documentation.
- No unnecessary files remain.
- Project is ready for Sprint 02.

If any issue is found, fix it before completing the sprint.

---






## AI Output Summary

**Tasks Completed**

- Reviewed all project documentation.
- Initialized FastAPI backend.
- Initialized React (Vite) frontend.
- Installed required dependencies.
- Created repository structure.
- Added configuration files.
- Verified backend startup.
- Verified frontend startup.
- Completed Sprint 01 verification.

---

## Manual Review & Changes

Document any manual improvements made after reviewing the AI-generated code.

Example:

- Reviewed folder structure.
- Confirmed no business logic was added.
- Verified project matches documentation.
- Removed unnecessary generated files (if applicable).

---

## Sprint Outcome

**Status:** ✅ Completed

Sprint 01 successfully established the project foundation and prepared the repository for Sprint 02 (Database & Environment Setup).