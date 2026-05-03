# SmartStay Backend - User Authentication System

A Flask-based backend system for user registration and login with MySQL database.

## Features

- User registration with validation
- Secure login with JWT authentication
- Password hashing with bcrypt
- MySQL database integration
- RESTful API endpoints
- Input validation and error handling

## Requirements

- Python 3.8+
- MySQL Server
- Dependencies listed in `requirements.txt`

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL database:**
   - Create a MySQL database named `smartstay_db`
   - Update database credentials in `config.py` if needed
   - Run the schema:
   ```sql
   SOURCE database/schema.sql;
   ```

3. **Configure environment (optional):**
   - Set `SECRET_KEY` environment variable for JWT

## Database Schema

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### POST /api/register
Register a new user.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123"
}
```

**Response (201):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2024-01-01T00:00:00"
    }
}
```

### POST /api/login
Authenticate a user and return JWT token.

**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "SecurePass123"
}
```

**Response (200):**
```json
{
    "message": "Login successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

## Security Features

- **Password Hashing:** Uses bcrypt for secure password storage
- **JWT Authentication:** Stateless token-based authentication
- **SQL Injection Protection:** Parameterized queries
- **Input Validation:** Email format, password strength, username constraints

## Validation Rules

- **Username:** 3-50 characters, alphanumeric + underscore only
- **Email:** Valid email format, unique
- **Password:** Minimum 8 characters, must contain uppercase, lowercase, and number

## Running the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Testing

Run the test script:
```bash
python test_api.py
```

## Error Responses

All endpoints return JSON error responses with appropriate HTTP status codes:

- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid credentials)
- `409` - Conflict (duplicate email)
- `500` - Internal Server Error

## Dependencies

- Flask - Web framework
- Flask-JWT-Extended - JWT authentication
- PyMySQL - MySQL connector
- bcrypt - Password hashing