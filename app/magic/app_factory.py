from functools import lru_cache

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .config import settings


@lru_cache()
def create_app(config_settings=settings):
    print("creating app")
    app = FastAPI(
        title=config_settings.app_name,
        version=config_settings.version,
        root_path="" if config_settings.local else f"/{config_settings.stage}",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
