import os
from pathlib import Path

import time
from functools import lru_cache

from mangum import Mangum

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

from app.magic.Globals.G import g


def add_cors(new_app):
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_tasks_and_process_time_middleware(new_app):
    @new_app.middleware("http")
    async def add_process_time_and_tasks(request: Request, call_next):
        start_time = time.time()
        g.request = request
        g.app = new_app
        print("url path", request.url.path, "***url", request.url)
        response = await call_next(request)
        response.headers["X-Tasks-Time"] = str(g.save_tasks())  # queue tasks
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response


def add_hello_world_testing_route(new_app):
    @new_app.get("/", tags=["boilerplate"])
    def read_root():
        print("hello world!")
        return {
            "Hello": "Worlda!",
            "cwd": Path.cwd(),
            "dir": os.listdir(),
        }


def add_addons(new_app):
    add_cors(new_app)
    add_tasks_and_process_time_middleware(new_app)
    add_hello_world_testing_route(new_app)


@lru_cache()
def create_app(config_settings=settings):
    new_app = FastAPI(
        title=config_settings.app_name,
        version=config_settings.version,
        root_path="" if config_settings.local else f"/{config_settings.stage}",
    )

    add_addons(new_app)

    return new_app


app = create_app()


def handler(event, context):
    """Handler to give to lambda... which wraps FastAPI"""
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        print("Lambda is warm!")
        return {}

    asgi_handler = Mangum(app, api_gateway_base_path=os.getenv("STAGE"))
    response = asgi_handler(event, context)
    return response
