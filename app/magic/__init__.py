import time
import os
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.magic.Globals.G import g

from app.magic import config

router = APIRouter()
from app import Routes

app = FastAPI() if os.environ.get("LOCAL") else FastAPI(openapi_prefix="/dev")

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
    response = await call_next(request)
    # also process the Tasks now
    start_tasks = time.time()
    g.save_tasks()
    tasks_took = time.time() - start_tasks
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Tasks-Time"] = str(tasks_took)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)

handler = Mangum(app, enable_lifespan=False)
