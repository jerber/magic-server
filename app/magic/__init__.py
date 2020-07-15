from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.routing import APIRoute

from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.magic.Models.Call import make_call_from_request_and_response
from typing import Callable

from . import config


class CallRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            make_call_from_request_and_response(request, response)
            """
            print("rrororooro", response)
            print("BODY", response.body)
            print(dir(response))
            print("ddddddd", response.__dict__)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            response.headers["X-SPAKL-Time"] = str(duration)

            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            """
            return response

        return custom_route_handler


router = APIRouter(route_class=CallRoute)
# router = APIRouter()

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
    # make_call_from_request_and_response(request, response)
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
