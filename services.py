from typing import TYPE_CHECKING, Any, List, cast

import database as _database
import models as _models
import schemas as _schemas

if TYPE_CHECKING: 
    from sqlalchemy.orm import Session


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db =_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()    


async def create_contact(
        contact: _schemas.CreateContact, db: "Session"
) -> _schemas.Contact:
    contact = _models.Contact(**contact.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _schemas.Contact.model_validate(contact)

async def get_all_contacts(db:"Session") -> List[_schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.from_orm, contacts))

async def get_contact(id: int, db:"Session"):
    contact = db.query(_models.Contact).filter(_models.Contact.id == id).first()
    return contact

async def delete_contact(contact: _models.Contact, db: "Session"):
    db.delete(contact)
    db.commit()


async def update_contact(
    contact_data: _schemas.CreateContact, contact: _models.Contact, db: "Session"
) -> _schemas.Contact:
    contact_obj = cast(Any, contact)
    for field_name in ("first_name", "last_name", "email", "phone_number"):
        setattr(contact_obj, field_name, getattr(contact_data, field_name))

    db.commit()
    db.refresh(contact)

    return _schemas.Contact.from_orm(contact)