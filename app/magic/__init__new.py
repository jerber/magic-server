from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings


@lru_cache()
def create_app():
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        root_path="" if settings.local else f"/{settings.stage}",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
