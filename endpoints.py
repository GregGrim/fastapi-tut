from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import cache
import db_session
import schemas
import services
import auth_utils

import sqlalchemy.orm as orm

from constants import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()


@app.put("/users/", response_model=schemas.User)
async def create_user(user: schemas.CreateUser, db: orm.Session = Depends(db_session.get_db)):
    return await services.create_user(user=user, db=db)


@app.get("/users/{username}", response_model=schemas.User)
async def get_user(username: str, db: orm.Session = Depends(db_session.get_db)):
    user = await services.get_user(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user


@app.delete("/users/{username}")
async def delete_user(username: str, db: orm.Session = Depends(db_session.get_db)):
    user = await services.get_user(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")

    await services.delete_user(user, db=db)

    return "user successfully deleted"


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: orm.Session = Depends(db_session.get_db)):
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


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth_utils.get_current_user)):
    return current_user


if __name__ == '__main__':
    uvicorn.run(app)
