import sqlalchemy as sa

from repositories.log_repository import LogRepository
from settings import app_settings
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from use_cases.auth_use_case import AuthUseCase
from use_cases.log_use_case import LogUseCase
from use_cases.user_use_case import UserUseCase


def get_user_use_case():
    return UserUseCase(
        UserRepository(
            engine=sa.create_engine(
                f"postgresql://{app_settings.DB_USER}:"
                f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"
            )
        ),
        TokenRepository(app_settings.REDIS_HOST, app_settings.REDIS_PORT),
    )


def get_auth_use_case():
    return AuthUseCase(
        user_repo=UserRepository(
            engine=sa.create_engine(
                f"postgresql://{app_settings.DB_USER}:"
                f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"
            ),
        ),
        token_repo=TokenRepository(app_settings.REDIS_HOST, app_settings.REDIS_PORT),
        log_repo=LogRepository(
            sa.create_engine(
                f"postgresql://{app_settings.DB_USER}:"
                f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"
            )
        ),
    )


def get_log_use_case():
    return LogUseCase(
        log_repo=LogRepository(
            sa.create_engine(
                f"postgresql://{app_settings.DB_USER}:"
                f"{app_settings.DB_PASS}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"
            )
        ),
    )
