from sqlalchemy.orm import Session

from models import UserModel
from entities import User, CreateUser, BaseUser
from utils.crypto_utils import get_hash
from .repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, engine):
        self.engine = engine

    async def create_one(self, user: CreateUser) -> BaseUser:
        with Session(self.engine) as session:
            hashed_password = get_hash(sequence=user.hashed_password)
            user_data = user.model_dump()
            user_data['hashed_password'] = hashed_password
            user = UserModel(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return User.model_validate(user)

    async def get_one(self, username: str) -> User:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter(UserModel.username == username).first()
        return user

    async def delete_one(self, user: BaseUser) -> None:
        with Session(self.engine) as session:
            user = UserModel(**user.model_dump())
            session.delete(user)
            session.commit()
