from datetime import timedelta, timezone, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Annotated
from sqlalchemy.orm import Session

import models

from constants import SECRET_KEY, JWT_ALGORITHM
from database import get_db
from exceptions import credentials_exception
from schemas import TokenData

from utils.crypto_utils import verify_sequence
from utils.cache import remove_token, token_exists
from utils.db_utils import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str, db: "Session") -> models.User | None:
    user = await get_user(username, db)
    if user and verify_sequence(source_sequence=password, target_sequence_hash=user.hashed_password):
        return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db=Depends(get_db)) -> models.User:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    if not token_exists(token, user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    return user


async def logout_user(token: Annotated[str, Depends(oauth2_scheme)]):
    remove_token(token)
    return "User logged out"
