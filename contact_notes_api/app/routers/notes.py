from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..models.note import Note
from ..models.contact import Contact
from ..schemas.note import NoteCreate, Note as NoteSchema

router = APIRouter(
    prefix="/contacts/{contact_id}/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[NoteSchema])
def get_notes(
    contact_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    notes = db.query(Note).filter(
        Note.contact_id == contact_id
    ).offset(skip).limit(limit).all()
    return notes

@router.post("/", response_model=NoteSchema)
def create_note(
    contact_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db_note = Note(**note.dict(), contact_id=contact_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{note_id}", response_model=NoteSchema)
def get_note(
    contact_id: int,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.contact_id == contact_id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteSchema)
def update_note(
    contact_id: int,
    note_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.contact_id == contact_id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    contact_id: int,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.contact_id == contact_id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return None