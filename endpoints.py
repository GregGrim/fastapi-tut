from typing import Annotated, TYPE_CHECKING, List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import schemas
import services

import sqlalchemy.orm as orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.put("/users/", response_model=schemas.User)
async def create_user(user: schemas.CreateUser, db: orm.Session = Depends(services.get_db)):
    return await services.create_user(user=user, db=db)


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: orm.Session = Depends(services.get_db)):
    user = await services.get_user(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: orm.Session = Depends(services.get_db)):
    user = await services.get_user(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")

    await services.delete_user(user, db=db)

    return "user successfully deleted"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
