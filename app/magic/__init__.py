from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# from . import config
from .config import settings
from app.magic.app_factory import app

background_router = APIRouter()
from app.magic.Decorators.background_tasks import run_in_background

app.include_router(background_router)

from app.magic.Errors.MagicExceptions import MagicException

# from app.magic.Models.Call import make_call_from_request_and_response


from app.magic.Utils.middleware import CallRoute


# from app.magic.app_factory import create_app


# app = create_app()


# @app.exception_handler(MagicException)
# def backend_exception_handler(request: Request, exc: MagicException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"success": False, "message": f"{exc.message}"},
#     )

router = APIRouter(route_class=CallRoute)
# router = APIRouter()

from app.magic.Globals.G import g

from app import Routes


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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


@background_router.get("/baccckk")
def backk():
    return "back"


print("app in magic", app)
app.include_router(router)
app.include_router(background_router)
print("def apppp", app.__dict__)
print("routttaa", app.router.__dict__)
for route in app.router.routes:
    print(route.__dict__)
    print("\n\n")


def handler(event, context):
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        print("Lambda is warm!")
        return {}

    asgi_handler = Mangum(app, api_gateway_base_path=os.getenv("STAGE"))
    response = asgi_handler(event, context)
    return response
