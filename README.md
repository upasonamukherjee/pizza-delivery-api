# Pizza Delivery API

A RESTful backend API for a Pizza Delivery system built using FastAPI, PostgreSQL, and SQLAlchemy, with JWT authentication and role-based access control.

## Project Overview

This project simulates a pizza ordering system where users can register, log in, and place, track, update and delete pizza orders. Staff members have extra permissions to manage all orders.

The application demonstrates:

- API Development with FastAPI
- Database Modeling with SQLAlchemy
- PostgreSQL Integration
- ORM Relationships
- Password Hashing
- JWT Authentication (access and refresh tokens)
- Role-Based Access Control
- CRUD Operations
- Interactive API Documentation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- PyJWT
- python-dotenv
- Uvicorn
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
├── create_tables.py
├── main.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## Database Design

### Users Table

- id
- username
- email
- password (stored as a salted hash)
- is_staff
- is_active

### Orders Table

- id
- quantity
- order_status (`PENDING`, `IN-TRANSIT`, `DELIVERED`)
- pizza_size (`SMALL`, `MEDIUM`, `LARGE`, `EXTRA-LARGE`)
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
- User Login with JWT access and refresh tokens
- Token Refresh Endpoint
- Protected Routes with Bearer Authentication
- Place an Order
- View My Orders and a Specific Order
- Update an Order
- Delete an Order
- Staff-Only Routes: list all orders, view any order, update order status
- Ownership Checks so users can only access their own orders
- Input Validation for pizza sizes and order statuses
- Swagger UI and ReDoc Documentation
- Environment Variables for secrets
- GitHub Version Control

## API Endpoints

### Auth

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/auth/` | Public | Health check |
| POST | `/auth/signup` | Public | Create an account |
| POST | `/auth/login` | Public | Get access and refresh tokens |
| GET | `/auth/me` | Access token | Return the logged-in username |
| GET | `/auth/refresh` | Refresh token | Get a new access token |

### Orders

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/orders/` | Public | Health check |
| POST | `/orders/order` | Logged in | Place an order |
| GET | `/orders/user/orders` | Logged in | List my orders |
| GET | `/orders/user/order/{id}` | Logged in | Get one of my orders |
| PUT | `/orders/order/update/{id}` | Owner | Update quantity and pizza size |
| DELETE | `/orders/order/delete/{id}` | Owner or staff | Delete an order |
| GET | `/orders/orders` | Staff | List all orders |
| GET | `/orders/orders/{id}` | Staff | Get any order by id |
| PATCH | `/orders/order/status/{id}` | Staff | Update order status |

## Authentication Flow

1. `POST /auth/signup` creates an account. The password is stored as a salted hash.
2. `POST /auth/login` returns an `access_token` (valid 30 minutes) and a `refresh_token` (valid 7 days).
3. In Swagger UI, click **Authorize** and paste the access token (without the `Bearer` prefix).
4. When the access token expires, authorize with the refresh token and call `GET /auth/refresh` to get a new access token.

Each token carries a `type` claim, so a refresh token cannot be used as an access token.

## Key Concepts Learned

- FastAPI Routing
- APIRouter
- Dependency Injection with `Depends`
- PostgreSQL Database Management
- SQLAlchemy ORM
- Foreign Keys
- Relationships
- back_populates
- ChoiceType
- Database Sessions
- Pydantic Schemas and Validation
- JWT Authentication and Token Refresh
- Authentication vs Authorization (401 vs 403)
- Environment Variables
- OpenAPI Documentation
- Git and GitHub

## How to Run

### Prerequisites

- Python 3.10 or newer
- PostgreSQL

### Setup

1. Clone the repository:

```bash
git clone https://github.com/upasonamukherjee/pizza-delivery-api.git
cd pizza-delivery-api
```

2. Create and activate a virtual environment:

```bash
python -m venv env
.\env\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create an empty PostgreSQL database named `pizza_delivery`.

5. Copy `.env.example` to `.env` and fill in your values:

```text
SECRET_KEY=your-long-random-string
DATABASE_URL=postgresql+psycopg2://postgres:your-password@localhost:5432/pizza_delivery
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

6. Create the database tables:

```bash
python create_tables.py
```

### Run FastAPI Application

```bash
uvicorn main:app --reload
```

### Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

ReDoc is also available at `http://127.0.0.1:8000/redoc`.

## Current Status

Complete. Authentication (signup, login, token refresh), order management (place, view, update, delete), staff-only order controls and API documentation are all implemented and working.

## Learning Objectives

This project was built to gain hands-on experience with:

- Backend Development
- REST APIs
- Database Design
- Authentication and Authorization
- SQLAlchemy ORM
- PostgreSQL
- Git and GitHub

## Author

Upasona Mukherjee

GitHub Repository:

https://github.com/upasonamukherjee/pizza-delivery-api