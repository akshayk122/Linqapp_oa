# Contact Notes API - Setup Guide

## 1. Project Structure Setup
```bash
mkdir contact_notes_api
cd contact_notes_api

# Create the following directory structure
mkdir app
mkdir app/models
mkdir app/schemas
mkdir app/routers
mkdir app/core
mkdir tests
mkdir alembic
```

## 2. Environment Setup

### 2.1 Create and Activate Virtual Environment
```bash
python -m venv venv

# For macOS/Linux
source venv/bin/activate

# For Windows
# venv\Scripts\activate
```

### 2.2 Create requirements.txt
Create a file named `requirements.txt` with the following dependencies:
```txt
fastapi==0.68.0
uvicorn==0.15.0
pyjwt==2.1.0
sqlalchemy==1.4.23
python-dotenv==0.19.0
pydantic==1.8.2
bcrypt==3.2.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.5
requests==2.26.0
pytest==6.2.5
httpx==0.19.0
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Configuration Files

### 3.1 Create .env file
Create a file named `.env` in the root directory:
```env
SECRET_KEY=your_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./contact_notes.db
```

### 3.2 Create database configuration
Create `app/core/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## 4. Core Components Setup

### 4.1 Models
Create the following files:
- `app/models/contact.py` - Contact model
- `app/models/note.py` - Note model
- `app/models/user.py` - User model for authentication

### 4.2 Schemas
Create Pydantic schemas:
- `app/schemas/contact.py`
- `app/schemas/note.py`
- `app/schemas/token.py`
- `app/schemas/user.py`

### 4.3 Routers
Create API route files:
- `app/routers/auth.py` - Authentication endpoints
- `app/routers/contacts.py` - Contact CRUD operations
- `app/routers/notes.py` - Notes CRUD operations

### 4.4 Core Utilities
Create utility files:
- `app/core/security.py` - JWT handling
- `app/core/config.py` - Configuration settings
- `app/core/dependencies.py` - Dependency injection

## 5. Database Setup

### 5.1 Initialize Database
Create `setup_db.py` in the root directory:
```python
from app.core.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
```

Run database initialization:
```bash
python setup_db.py
```

## 6. Running the Application

### 6.1 Create main application file
Create `main.py` in the root directory:
```python
from fastapi import FastAPI
from app.routers import auth, contacts, notes
from app.core.database import engine
from app.models import Base

app = FastAPI(title="Contact Notes API")

# Include routers
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(notes.router)

# Create database tables
Base.metadata.create_all(bind=engine)
```

### 6.2 Start the Application
```bash
uvicorn main:app --reload
```

## 7. Testing

### 7.1 Create test files
Create the following test files in the `tests` directory:
- `tests/test_auth.py`
- `tests/test_contacts.py`
- `tests/test_notes.py`
- `tests/conftest.py`

### 7.2 Run Tests
```bash
pytest
```

## 8. API Documentation Access
After starting the application:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 9. Next Steps
1. Implement the models, schemas, and routers according to the API specification
2. Add authentication logic in the security module
3. Implement rate limiting and retry mechanisms
4. Add proper error handling and validation
5. Write comprehensive tests
6. Add logging and monitoring

## 10. Production Considerations
1. Replace SQLite with PostgreSQL
2. Set up proper logging
3. Configure CORS
4. Implement rate limiting
5. Set up CI/CD pipeline
6. Configure proper security headers
7. Set up monitoring and alerting