from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    body: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    contact_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }