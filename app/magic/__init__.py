from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from . import config


router = APIRouter()

app = FastAPI(
    title="GOAT SERVER",
    version="0.0.1",
    root_path="" if os.getenv("LOCAL") else f'/{os.getenv("STAGE")}',
)

from app.magic.Globals.G import g

from app import Routes


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    g.request = request
    g.app = app
    print("url path", request.url.path, "***url", request.url)
    response = await call_next(request)
    # also process the Tasks now
    start_tasks = time.time()
    if g.tasks:
        g.save_tasks()
        tasks_took = time.time() - start_tasks
        response.headers["X-Tasks-Time"] = str(tasks_took)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
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


def handler(event, context):
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        print("Lambda is warm!")
        return {}

    asgi_handler = Mangum(app, api_gateway_base_path=os.getenv("STAGE"))
    response = asgi_handler(event, context)
    return response
