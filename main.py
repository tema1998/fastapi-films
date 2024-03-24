from fastapi import FastAPI, APIRouter
from api.core_handlers import core_router
from api.auth_handler import auth_router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(core_router, prefix="/core", tags=["core"])
    application.include_router(auth_router, prefix="/auth", tags=["auth"])
    return application


app = get_application()

