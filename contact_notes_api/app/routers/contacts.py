from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..models.contact import Contact
from ..schemas.contact import ContactCreate, Contact as ContactSchema

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[ContactSchema])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contacts = db.query(Contact).filter(
        Contact.owner_id == int(current_user["sub"])
    ).offset(skip).limit(limit).all()
    return contacts

@router.post("/", response_model=ContactSchema)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_contact = Contact(**contact.dict(), owner_id=int(current_user["sub"]))
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/{contact_id}", response_model=ContactSchema)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactSchema)
def update_contact(
    contact_id: int,
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == int(current_user["sub"])
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return None