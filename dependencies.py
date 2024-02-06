import sqlalchemy as sa

from entities import settings
from repositories.cache_repository import CacheRepository
from repositories.user_repository import UserRepository
from use_cases.auth_use_case import AuthUseCase
from use_cases.user_use_cases import UserUseCase


async def get_user_use_case():
    return UserUseCase(UserRepository(
        engine=sa.create_engine(
            f"postgresql://{settings.DB_USER}:"
            f"{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")),
        CacheRepository())


async def get_auth_use_case():
    return AuthUseCase(user_repo=UserRepository(
        engine=sa.create_engine(
            f"postgresql://{settings.DB_USER}:"
            f"{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"),),
        cache_repo=CacheRepository())
