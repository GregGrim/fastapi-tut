import sqlalchemy.orm as orm

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import database
import schemas

from utils import auth_utils, cache
from constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=schemas.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: orm.Session = Depends(database.get_db)):
    user = await auth_utils.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    cache.add_token(access_token, user.id)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/logout", dependencies=[Depends(auth_utils.get_current_user), Depends(auth_utils.logout_user)])
async def logout_user():
    return {"details": "User successfully logged out"}
