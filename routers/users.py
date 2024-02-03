from fastapi import APIRouter, Depends, HTTPException

import database
import models
import schemas
import sqlalchemy.orm as orm

from utils import auth_utils, db_utils, cache

router = APIRouter(prefix="/users")


@router.put("/", response_model=schemas.UserSchema)
async def create_user(user: schemas.CreateUser, db: orm.Session = Depends(database.get_db)):
    return await db_utils.create_user(user=user, db=db)


@router.get("/get/{username}", response_model=schemas.UserSchema)
async def get_user(username: str, db: orm.Session = Depends(database.get_db)):
    user = await db_utils.get_user(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user


@router.delete("/remove")
async def delete_user(current_user: models.User = Depends(auth_utils.get_current_user),
                      db: orm.Session = Depends(database.get_db)):
    cache.remove_all_user_tokens(user_id=current_user.id)
    await db_utils.delete_user(user=current_user, db=db)
    return "user successfully deleted"


@router.get("/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return current_user
