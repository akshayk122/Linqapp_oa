from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.contact import Contact
from app.models.note import Note

def seed_database():
    db = SessionLocal()
    try:
        # Create test users
        test_users = [
            {
                "email": "john@example.com",
                "username": "john_doe",
                "password": "password123"
            },
            {
                "email": "jane@example.com",
                "username": "jane_smith",
                "password": "password456"
            }
        ]

        db_users = []
        for user_data in test_users:
            hashed_password = get_password_hash(user_data["password"])
            db_user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=hashed_password,
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            db_users.append(db_user)

        # Create contacts for each user
        contacts_data = [
            {
                "name": "Alice Cooper",
                "email": "alice@example.com",
                "phone": "123-456-7890"
            },
            {
                "name": "Bob Wilson",
                "email": "bob@example.com",
                "phone": "098-765-4321"
            },
            {
                "name": "Carol Brown",
                "email": "carol@example.com",
                "phone": "555-555-5555"
            }
        ]

        for user in db_users:
            for contact_data in contacts_data:
                db_contact = Contact(
                    name=contact_data["name"],
                    email=contact_data["email"],
                    phone=contact_data["phone"],
                    owner_id=user.id
                )
                db.add(db_contact)
                db.commit()
                db.refresh(db_contact)

                # Add notes for each contact
                notes_data = [
                    {
                        "body": f"First meeting with {contact_data['name']} went well"
                    },
                    {
                        "body": f"Follow-up scheduled with {contact_data['name']}"
                    },
                    {
                        "body": f"Discussed project details with {contact_data['name']}"
                    }
                ]

                for note_data in notes_data:
                    db_note = Note(
                        body=note_data["body"],
                        contact_id=db_contact.id
                    )
                    db.add(db_note)

                db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed_database()