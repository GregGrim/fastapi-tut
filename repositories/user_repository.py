from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from exceptions import UserCreationException, UserDoesNotExistException
from models import UserModel
from entities import User, CreateUser
from utils.crypto_utils import get_hash
from .repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, engine):
        self.engine = engine

    def create_one(self, user: CreateUser) -> User:
        with Session(self.engine) as session:
            hashed_password = get_hash(sequence=user.hashed_password)
            user_data = user.model_dump()
            user_data["hashed_password"] = hashed_password
            user = UserModel(**user_data)
            try:
                session.add(user)
                session.commit()
            except SQLAlchemyError as e:
                error_message = (
                    str(e.__dict__["orig"]) if "orig" in e.__dict__ else str(e)
                )
                raise UserCreationException(
                    detail=f"Failed to create the record: {error_message}"
                )
            session.refresh(user)
            return User.model_validate(user)

    def get_one(self, user_id: str) -> User:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise UserDoesNotExistException()
        return User.model_validate(user)

    def get_one_by_username(self, username: str) -> User:
        with Session(self.engine) as session:
            user = (
                session.query(UserModel).filter(UserModel.username == username).first()
            )
            if not user:
                raise UserDoesNotExistException()
        return User.model_validate(user)

    def delete_one(self, user_id: str) -> None:
        with Session(self.engine) as session:
            user = self.get_one(user_id)
            session.delete(user)
            session.commit()
