Pizza Delivery API
A RESTful backend API for a Pizza Delivery system built using FastAPI, PostgreSQL, and SQLAlchemy.

Project Overview
This project simulates a pizza ordering system where users can register, authenticate, and place pizza orders.

The application demonstrates:

API Development with FastAPI
Database Modeling with SQLAlchemy
PostgreSQL Integration
ORM Relationships
Password Hashing
CRUD Operations
Tech Stack
Python
FastAPI
PostgreSQL
SQLAlchemy
Pydantic
pgAdmin 4
Git
GitHub
Project Structure
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
└── README.md
Database Design
Users Table
id
username
email
password
is_staff
is_active
Orders Table
id
quantity
order_status
pizza_size
user_id
Relationships
One-to-Many Relationship
One User can place multiple Orders.

Each Order belongs to a single User.

Implemented using:

ForeignKey
relationship()
back_populates
Features Implemented
User Model Creation
Order Model Creation
PostgreSQL Integration
SQLAlchemy ORM
Database Relationships
Password Hashing
User Registration Endpoint (In Progress)
Key Concepts Learned
FastAPI Routing
APIRouter
PostgreSQL
SQLAlchemy ORM
Foreign Keys
Relationships
back_populates
ChoiceType
Database Sessions
Pydantic Schemas
Git and GitHub
How to Run
Activate virtual environment:

.\env\Scripts\activate
Run the FastAPI server:

uvicorn main:app --reload
Open Swagger Documentation:

http://127.0.0.1:8000/docs
Current Status
Project currently under development.

Planned Features
User Login
JWT Authentication
Create Order API
Update Order API
Delete Order API
Order Tracking
Author
Upasona Mukherjee

GitHub: https://github.com/upasonamukherjee/pizza-delivery-api