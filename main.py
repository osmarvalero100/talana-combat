from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.web import router as router_web
from src.routers.api import router as router_api
from src.database import engine, Base


def get_application() -> FastAPI:
    ''' Configure, start and return the application '''
    
    application = FastAPI()

    Base.metadata.create_all(bind=engine)

    application.mount("/static", StaticFiles(directory="static"), name="static")

    application.include_router(router_web)
    application.include_router(router_api, prefix="/api")

    return application


app = get_application()