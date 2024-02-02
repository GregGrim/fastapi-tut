from typing import TYPE_CHECKING, List

import database
import models
import schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_user(user: schemas.CreateUser, db: "Session") -> schemas.User:
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.User.model_validate(user)


async def get_user(user_id: int, db: "Session") -> schemas.User:
    user = db.query(models.User).filter(models.User.id == user_id).one()
    return user


async def delete_user(user: models.User, db: "Session"):
    db.delete(user)
    db.commit()


if __name__ == '__main__':
    pass
