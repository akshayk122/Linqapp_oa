from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, contacts, notes
from app.core.database import engine
from app.models import user, contact, note

# Create database tables
user.Base.metadata.create_all(bind=engine)
contact.Base.metadata.create_all(bind=engine)
note.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contact Notes API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Contact Notes API"}