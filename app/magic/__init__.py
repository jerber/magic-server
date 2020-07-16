from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request

from mangum import Mangum

from .config import settings
from app.magic.app_factory import app


from app.magic.Errors.MagicExceptions import MagicException

background_router = APIRouter()

from app.magic.Utils.middleware import CallRoute  # this requires a background router...


router = APIRouter(route_class=CallRoute)

from app.magic.Globals.G import g


from app import Routes


@app.middleware("http")
async def add_process_time_and_tasks(request: Request, call_next):
    start_time = time.time()
    g.request = request
    g.app = app
    print("url path", request.url.path, "***url", request.url)
    response = await call_next(request)
    response.headers["X-Tasks-Time"] = str(g.save_tasks())  # queue tasks
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


@app.get("/", tags=["boilerplate"])
def read_root():
    print("hello world!")
    return {
        "Hello": "Worlda!",
        "cwd": Path.cwd(),
        "dir": os.listdir(),
    }


app.include_router(router)
app.include_router(background_router)


def handler(event, context):
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        print("Lambda is warm!")
        return {}

    asgi_handler = Mangum(app, api_gateway_base_path=os.getenv("STAGE"))
    response = asgi_handler(event, context)
    return response
