from typing import TYPE_CHECKING

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