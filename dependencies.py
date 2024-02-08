import sqlalchemy as sa

from settings import app_settings
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from use_cases.auth_use_case import AuthUseCase
from use_cases.user_use_cases import UserUseCase


async def get_user_use_case():
    return UserUseCase(UserRepository(
        engine=sa.create_engine(
            f"postgresql://{app_settings.DB_USER}:"
            f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}")),
        TokenRepository(app_settings.REDIS_HOST, app_settings.REDIS_PORT))


async def get_auth_use_case():
    return AuthUseCase(user_repo=UserRepository(
        engine=sa.create_engine(
            f"postgresql://{app_settings.DB_USER}:"
            f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"),),
        token_repo=TokenRepository(app_settings.REDIS_HOST, app_settings.REDIS_PORT))
