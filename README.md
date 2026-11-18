# Pizza Delivery API

A RESTful backend API for a Pizza Delivery system built using FastAPI, PostgreSQL, and SQLAlchemy.

## Project Overview

This project simulates a pizza ordering system where users can register, authenticate, and place pizza orders.

The application demonstrates:

- API Development with FastAPI
- Database Modeling with SQLAlchemy
- PostgreSQL Integration
- ORM Relationships
- Password Hashing
- CRUD Operations

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- pgAdmin 4
- Git
- GitHub

## Project Structure

```text
pizza-delivery-api/
│
├── auth_routes.py
├── order_routes.py
├── database.py
├── models.py
├── schemas.py
├── init_db.py
├── create_tables.py
├── main.py
├── README.md
└── .gitignore
```

## Database Design

### Users Table

- id
- username
- email
- password
- is_staff
- is_active

### Orders Table

- id
- quantity
- order_status
- pizza_size
- user_id

## Relationships

### One-to-Many Relationship

- One User can place multiple Orders.
- Each Order belongs to a single User.

Implemented using:

```python
ForeignKey
relationship()
back_populates
```

## Features Implemented

- User Model Creation
- Order Model Creation
- PostgreSQL Integration
- SQLAlchemy ORM
- Database Relationships
- Password Hashing
- User Registration Endpoint
- GitHub Version Control

## Key Concepts Learned

- FastAPI Routing
- APIRouter
- PostgreSQL Database Management
- SQLAlchemy ORM
- Foreign Keys
- Relationships
- back_populates
- ChoiceType
- Database Sessions
- Pydantic Schemas
- Git and GitHub

## How to Run

### Activate Virtual Environment

```bash
.\env\Scripts\activate
```

### Run FastAPI Application

```bash
uvicorn main:app --reload
```

### Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

## Current Status

Project is currently under development.

### Upcoming Features

- User Login
- JWT Authentication
- Create Order API
- Update Order API
- Delete Order API
- Order Tracking

## Learning Objectives

This project was built to gain hands-on experience with:

- Backend Development
- REST APIs
- Database Design
- Authentication
- SQLAlchemy ORM
- PostgreSQL
- Git and GitHub

## Author

Upasona Mukherjee

GitHub Repository:

https://github.com/upasonamukherjee/pizza-delivery-api