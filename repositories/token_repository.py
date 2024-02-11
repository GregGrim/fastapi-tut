from typing import Annotated

import redis
from datetime import timedelta, timezone, datetime

from fastapi import Depends
from jose import jwt, JWTError

from settings import app_settings
from settings import oauth2_scheme
from exceptions import CredentialsException


class TokenRepository:
    def __init__(self, redis_host: str, redis_port: str) -> None:
        self.r_db = redis.Redis(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )

    def add_token(self, token: str, user_id: str):
        key = self.get_auth_redis_key(user_id, token)
        self.r_db.set(key, 1)
        self.r_db.expire(
            key, timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    def token_exists(self, token: str, user_id: str) -> bool:
        return bool(self.r_db.exists(self.get_auth_redis_key(user_id, token)))

    def remove_token(self, token: str):
        keys_to_delete = self.r_db.keys(f"auth:*:{token}")
        for key in keys_to_delete:
            self.r_db.delete(key)

    def remove_all_user_tokens(self, user_id: str):
        keys_to_delete = self.r_db.keys(f"auth:{user_id}:*")
        for key in keys_to_delete:
            self.r_db.delete(key)

    def get_auth_redis_key(self, user_id: str, token: str) -> str:
        return f"auth:{user_id}:{token}"

    async def create_access_token(self, data: dict) -> str:
        expires_delta = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, app_settings.SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM
        )
        return encoded_jwt

    async def read_access_token(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> str:
        try:
            payload = jwt.decode(
                token, app_settings.SECRET_KEY, algorithms=[app_settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise CredentialsException()
        except JWTError:
            raise CredentialsException()
        return user_id
