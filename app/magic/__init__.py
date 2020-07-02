from pathlib import Path
import time
import os
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from . import config


router = APIRouter()


app = FastAPI() if os.environ.get("LOCAL") else FastAPI(root_path="/dev")

from app.magic.Globals.G import g

# add auth here... for now hardcode but in future look to env variable for which auth...
from .Auth import Doorman
from .Auth.Doorman import get_current_user, CurrentUser

GET_USER = Depends(get_current_user)

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
    print("url path", request.url.path)
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


@app.get("/")
def read_root():
    print("hello world!")
    return {"Hello": "World", "cwd": Path.cwd(), "dir": os.listdir()}


app.include_router(router)

handler = Mangum(app, enable_lifespan=False)
