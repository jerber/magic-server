from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.responses import RedirectResponse

from . import config


router = APIRouter()

# TODO /dev problem
# app = FastAPI() if os.environ.get("LOCAL") else FastAPI(root_path="/dev")
# app = FastAPI(openapi_url="/dev/openapi.json", version='0.0.1')
app = FastAPI(openapi_url="/dev/openapi.json")  # This worked w double dev for redirect
# app = FastAPI()
# app = FastAPI(root_path="/dev")
# app = FastAPI(
#     servers=[
#         {"url": "/", "description": "Current environment"},
#         {"url": "/dev", "description": "Dev env"},
#     ],
# )

from app.magic.Globals.G import g

from app import Routes


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO tell if it is coming from the amazon given url, and if it is, append the dev??


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    g.request = request
    g.app = app
    print("path params", request.path_params)
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


@app.get("/openapi.json")
def dev_docs():
    print("you are being redirected now...")
    message = "hi there!"
    print(message)
    response = RedirectResponse(url="/dev/dev/openapi.json")
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

    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response
