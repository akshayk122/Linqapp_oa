
# Contact Notes API

A FastAPI-based RESTful service for managing contacts and their associated notes, featuring JWT authentication, field normalization, and robust error handling.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup & Installation](#setup--installation)
- [Running the Service Locally](#running-the-service-locally)
- [API Endpoints](#api-endpoints)
- [Key Decisions, Tradeoffs & Assumptions](#key-decisions-tradeoffs--assumptions)
- [Future Improvements](#future-improvements)
- [Bonus: Additional Features](#bonus-additional-features)

## Overview

This backend service provides a RESTful API for managing contacts and their attached notes. The system includes:
- **JWT-based Authentication:** Secure token issuance and verification.
- **CRUD Operations:** Full create, read, update, and delete capabilities for contacts and notes.
- **Field Normalization:** Automatically normalizes different inbound field names (e.g., `note_body`, `note_text`) to a standard field (`body`).
- **Error Handling:** Implements token expiration handling with retries, rate limiting with backoff strategies, and graceful error responses for timeouts and other errors.

## Features

- **Authentication:** Secure JWT-based flow to protect endpoints.
- **Contacts Management:** REST endpoints to create, update, retrieve, and delete contacts.
- **Notes Management:** REST endpoints to manage notes for each contact, including automatic field normalization.
- **Resilience:** Implements retries for outbound requests (to simulate token expiration handling), rate limiting with backoff, and proper timeout management.
- **Extensibility:** Designed to be decoupled, allowing for easy integration with queues or event buses for asynchronous note processing.

## Technology Stack

- **Language:** Python 3.8+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (ideal for building APIs with automatic Swagger documentation)
- **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI server for local and production use)
- **Authentication:** [PyJWT](https://pyjwt.readthedocs.io/)
- **Database:** SQLite (for local development; can be replaced with PostgreSQL or another RDBMS in production)
- **HTTP Requests:** [Requests](https://docs.python-requests.org/) or [httpx](https://www.python-httpx.org/) for outbound call simulation
- **Optional Tools:** Celery/Redis or RabbitMQ for event-based processing

## Setup & Installation

### Prerequisites
- **Python 3.8+**
- **Virtual Environment:** Use `venv` or `virtualenv`
- **(Optional) Docker:** For containerized deployment

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/contact-notes-api.git
   cd contact-notes-api
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Ensure you have a `requirements.txt` that includes:
   ```txt
   fastapi
   uvicorn
   pyjwt
   sqlalchemy
   requests
   python-dotenv
   # Optional extras: httpx, celery, redis, pytest
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your_jwt_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=sqlite:///./test.db
   ```
   These variables control your JWT settings and database connection.

5. **Database Setup**
   If using SQLAlchemy:
   - Create a setup script (e.g., `setup_db.py`) to initialize your database schema.
   ```bash
   python setup_db.py
   ```

## Running the Service Locally

1. **Set Up Python Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory with:
   ```
   SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=sqlite:///./contact_notes.db
   ```

3. **Initialize Database**
   ```bash
   python setup_db.py
   ```

4. **Seed Sample Data (Optional)**
   ```bash
   python seed_db.py
   ```

5. **Start the Server**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at:
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

## API Endpoints

### Authentication
- **POST `/token`**
  - **Description:** Authenticate and retrieve a JWT.
  - **Request Body:** Username and password credentials.
  - **Response:** A JWT access token.

### Contacts
- **GET `/contacts`**
  - **Description:** Retrieve a list of contacts.
- **POST `/contacts`**
  - **Description:** Create a new contact.
- **GET `/contacts/{contact_id}`**
  - **Description:** Retrieve a specific contact.
- **PUT `/contacts/{contact_id}`**
  - **Description:** Update an existing contact.
- **DELETE `/contacts/{contact_id}`**
  - **Description:** Delete a contact.

### Notes
- **GET `/contacts/{contact_id}/notes`**
  - **Description:** Retrieve all notes for a contact.
- **POST `/contacts/{contact_id}/notes`**
  - **Description:** Create a new note for a contact.
  - **Note:** Supports field normalization; `note_body` or `note_text` in the request will be normalized to the `body` field.
- **GET `/contacts/{contact_id}/notes/{note_id}`**
  - **Description:** Retrieve a specific note.
- **PUT `/contacts/{contact_id}/notes/{note_id}`**
  - **Description:** Update an existing note.
- **DELETE `/contacts/{contact_id}/notes/{note_id}`**
  - **Description:** Delete a note.

## Key Decisions, Tradeoffs & Assumptions

### Architecture
- **FastAPI Framework**: Chosen for its high performance, automatic OpenAPI documentation, and built-in type checking with Pydantic
- **SQLAlchemy ORM**: Provides database abstraction and future flexibility to switch from SQLite to production databases
- **JWT Authentication**: Stateless authentication allowing scalable deployment without shared session storage

### Database Design
- **SQLite for Development**: Simple setup, perfect for local development and testing
- **Relationship Structure**: 
  - Users -> Contacts (one-to-many)
  - Contacts -> Notes (one-to-many)
  - Cascading deletes for dependent records

### Security
- **Password Hashing**: Using bcrypt for secure password storage
- **Token-based Auth**: JWT tokens with configurable expiration
- **CORS Middleware**: Configured for development, needs production refinement

### Error Handling
- Comprehensive HTTP status codes
- Structured error responses
- Database transaction management
- Input validation using Pydantic schemas

- **Framework Choice:**  
  FastAPI is chosen due to its performance benefits, intuitive design, automatic data validation with Pydantic, and built-in API documentation support.

- **Authentication:**  
  JWT-based authentication provides a stateless approach to securing API endpoints, which is ideal for microservice architectures. This simplifies horizontal scaling as there is no session state management on the server.

- **Database:**  
  SQLite is used for local development simplicity. For production, it would be advisable to use a robust RDBMS like PostgreSQL.

- **Resilience Features:**  
  - **Token Expiration and Retries:** Outbound HTTP calls simulate token expiration by integrating retry mechanisms, potentially using libraries like `tenacity`.
  - **Rate Limiting with Backoff:** Custom middleware (or third-party libraries) are employed to simulate rate limiting. When limits are exceeded, an exponential backoff strategy helps to mitigate request flooding.
  - **Field Normalization:** The service normalizes incoming note data so that variations in field names (e.g., `note_body`, `note_text`) are internally mapped to a consistent field (`body`).

- **Assumptions:**  
  - The environment is controlled enough for simulated rate limiting and token expiration scenarios.
  - The service is part of a larger system, and therefore, integrations (like outbound token handling and event processing) are simplified for demonstration purposes.

## Future Improvements

1. **Production Readiness**
   - Switch to PostgreSQL for production
   - Implement proper logging system
   - Add request rate limiting
   - Set up monitoring and metrics

2. **Security Enhancements**
   - Add refresh token mechanism
   - Implement password reset flow
   - Add API key support for service-to-service communication
   - Enhanced input validation and sanitization

3. **Feature Additions**
   - Batch operations for contacts and notes
   - Search functionality with filters
   - Contact grouping/categorization
   - File attachments for notes
   - Contact import/export functionality

4. **Performance Optimizations**
   - Response caching
   - Database query optimization
   - Implement pagination for large datasets
   - Background task processing for heavy operations

5. **Testing and Quality**
   - Expand test coverage
   - Add integration tests
   - Implement CI/CD pipeline
   - Add API versioning

## Bonus: Additional Features

- **API Documentation:**  
  The service leverages FastAPI’s auto-generated documentation, available at `/docs` (Swagger UI) and `/redoc` (Redoc).
  
- **Integration Tests:**  
  Sample tests are available in the `tests/` directory. These tests can be run with:
  ```bash
  pytest
  ```

- **Event Bus / Queue:**  
  A decoupled processing approach using an event bus (e.g., with Celery and Redis) can be integrated to manage downstream processing, which makes the application more resilient and scalable under load.

## Project Structure
```
contact_notes_api/
├── app/
│   ├── core/          # Core functionality
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API routes
│   └── schemas/       # Pydantic schemas
├── tests/             # Test suite
├── alembic/           # Database migrations
├── main.py           # Application entry
└── requirements.txt  # Dependencies
```

