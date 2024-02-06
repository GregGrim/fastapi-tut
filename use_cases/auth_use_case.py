from fastapi import HTTPException, status

from entities import BaseUser, Token
from exceptions import credentials_exception
from repositories.cache_repository import CacheRepository
from repositories.user_repository import UserRepository
from services import read_access_token, create_access_token
from utils.crypto_utils import verify_sequence


class AuthUseCase:

    def __init__(self, user_repo: UserRepository, cache_repo: CacheRepository):
        self.user_repo = user_repo
        self.cache_repo = cache_repo

    async def authenticate_user(self, username: str, password: str) -> BaseUser:
        user = await self.user_repo.get_one(username)
        if user and verify_sequence(source_sequence=password, target_sequence_hash=user.hashed_password):
            return user

    async def get_current_user(self, token: str) -> BaseUser:
        username = await read_access_token(token)
        user = await self.user_repo.get_one(username)
        if user is None:
            raise credentials_exception
        if not self.cache_repo.token_exists(token, user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
        return user

    async def login_user(self, username: str, password: str) -> Token:
        user = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await create_access_token(data={"sub": user.username})
        self.cache_repo.add_token(access_token, user.id)
        return Token(access_token=access_token, token_type="bearer")

    async def logout_user(self, token: str):
        self.cache_repo.remove_token(token)
        return {"details": "User successfully logged out"}
