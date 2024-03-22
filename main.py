from fastapi import FastAPI, APIRouter
from api.handlers import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = get_application()

router = APIRouter()
