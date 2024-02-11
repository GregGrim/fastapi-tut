from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from routers.users import router as users_router
from routers.auth import router as auth_router
from exceptions import (
    app_exception_handler,
    TutAppException,
    validation_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI()
    _add_routers(app)
    _add_exc_handlers(app)

    return app


def _add_routers(app: FastAPI):
    app.include_router(users_router)
    app.include_router(auth_router)


def _add_exc_handlers(app: FastAPI):
    app.add_exception_handler(TutAppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
