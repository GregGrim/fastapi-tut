import database
import models
import schemas

from sqlalchemy.orm import Session

from utils.crypto_utils import get_hash


def add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


async def create_user(user: schemas.CreateUser, db: "Session") -> schemas.UserSchema:

    hashed_password = get_hash(sequence=user.hashed_password)

    user_data = user.model_dump()
    user_data['hashed_password'] = hashed_password
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.UserSchema.model_validate(user)


async def get_user(username: str, db: "Session") -> models.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


async def delete_user(user: models.User, db: "Session") -> None:
    db.delete(user)
    db.commit()


if __name__ == '__main__':
    add_tables()
