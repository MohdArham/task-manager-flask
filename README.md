# Task Manager API

A **Flask-based Task Manager REST API** featuring **JWT authentication**, **SQLite database**, and **Swagger documentation** for easy testing and integration.

---

## Features

- User Authentication (Register, Login using JWT)
- CRUD operations for tasks
- JWT-protected creation, update, and deletion of tasks
- Public endpoint for listing tasks
- SQLite database (self-contained)
- ORM powered by SQLAlchemy
- JWT authentication via `flask-jwt-extended`
- Interactive API docs using Swagger UI
- Auto database migrations with Flask-Migrate

---

## Project Structure

```
task-manager-flask/
│
├── app.py                   # Main application entry point
├── config.py                # Static configuration (no env vars)
├── extensions.py            # DB, JWT, Migrate initialization
├── models.py                # Database models
├── auth.py                  # Authentication blueprint
├── routes.py                # Task management blueprint
├── data.db                  # SQLite database (auto-created)
├── schemas.py               # Schemas
├── tests/                   # Pytest test files
│ └── test_app.py            # API tests for tasks and auth
└── requirements.txt         # Python dependencies
```

---

## Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/MohdArham/task-manager-flask.git
cd task-manager-flask
```

### 2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the application
```
python app.py
```

You’ll see output similar to:
```
=========================Flask Task Manager API Started=============================
```

---

## API Documentation

Swagger UI is automatically available at:

 **http://127.0.0.1:5000/apidocs**

You can test all endpoints directly from your browser.

---

## Example Endpoints

| Method   | Endpoint         | Description                    |
|----------|------------------|--------------------------------|
| `POST`   | `/auth/register` | Create a new user              |
| `POST`   | `/auth/login`    | Get JWT token                  |
| `GET`    | `/tasks`         | List all tasks (public)        |
| `POST`   | `/tasks`         | Create new task (JWT required) |
| `PUT`    | `/tasks/<id>`    | Update a task (JWT required)   |
| `DELETE` | `/tasks/<id>`    | Delete a task (JWT required )  |

---

## Tech Stack

- **Flask** – Web framework  
- **Flask-JWT-Extended** – JWT authentication  
- **Flask-SQLAlchemy** – ORM for database  
- **Flask-Migrate** – Database migrations  
- **Flasgger** – Swagger UI  
- **SQLite** – Local database  

---

## Running Tests

Tests are included in `tests/test_app.py` using **pytest**. They cover:

- User registration and login
- JWT-protected task creation, update, and deletion
- Public task listing
- Unauthorized access to protected routes

Run tests with:

```
pytest -v
```
---

## Notes

- All configuration values are **static** inside `config.py` for demo/interview use.
- This code is **not production-ready** — do not use static secrets in a real deployment.
- In production, move secrets and database URIs to environment variables.

---

## Author

**Mohd Arham**  
Software Developer at Binary Semantics  
mohdarham94@gmail.com   
**https://www.linkedin.com/in/mohammad-arham-4ab292248/****
