import time
import os
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.magic.Globals.G import g

from . import config

router = APIRouter()


app = FastAPI() if os.environ.get("LOCAL") else FastAPI(root_path="/dev")

# add auth here... for now hardcode but in future look to env variable for which auth...
from .Auth import Doorman
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
