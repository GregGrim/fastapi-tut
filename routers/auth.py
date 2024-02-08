from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_auth_use_case
from entities import Token
from settings import oauth2_scheme
from use_cases.auth_use_case import AuthUseCase

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)]):
    return await auth_use_case.login_user(form_data.username, form_data.password)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
                      token: Annotated[str, Depends(oauth2_scheme)]):
    await auth_use_case.logout_user(token)
