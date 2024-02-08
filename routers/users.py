from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies import get_user_use_case, get_auth_use_case
from entities import User, CreateUser
from settings import oauth2_scheme
from use_cases.auth_use_case import AuthUseCase
from use_cases.user_use_cases import UserUseCase


router = APIRouter(prefix="/users")


@router.put("/signup", response_model=User, status_code=status.HTTP_200_OK)
async def create_user(user: CreateUser, user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)]):
    return await user_use_case.add_user(user)


@router.get("/get/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(username: str, user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)]):
    return await user_use_case.get_user(username)


@router.delete("/remove", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
                      auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
                      token: Annotated[str, Depends(oauth2_scheme)]):
    current_user = await auth_use_case.get_current_user(token=token)
    await user_use_case.delete_user(current_user.id)


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
                        token: Annotated[str, Depends(oauth2_scheme)]):
    current_user = await auth_use_case.get_current_user(token=token)
    return current_user
