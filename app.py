from fastapi import FastAPI

from routers.users import router as users_router
from routers.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI()
    _add_routers(app)

    return app


def _add_routers(app: FastAPI):
    app.include_router(users_router)
    app.include_router(auth_router)
