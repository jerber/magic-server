import os
from functools import wraps
from fastapi import Request, Body
from app.magic import router


from app.magic.Globals.G import g
from app.magic.Models.Task import Task, TaskParams

import inspect
from fastapi import HTTPException
import json
from datetime import datetime

from app.magic.Utils.random_utils import random_str
from app.magic.Errors import BackendException


def run_in_background(f):
    router_path = f"/run_in_background/{f.__name__}"

    @router.post(router_path, tags=["background_tasks"])
    def endpoint(
        request: Request,
        task_id: str = Body(...),
        secret_token: str = Body(...),
        params: str = Body(...),
    ):
        print("endpoint just received!", "params", params)
        task = Task.collection.get(task_id)
        if not task or secret_token != task.secret_token:
            raise HTTPException(status_code=404, detail="Invalid task request.")

        if task.status == "done":
            raise HTTPException(
                status_code=404, detail="This task was already completed."
            )

        j_params = json.loads(params)
        args = j_params.get("args", [])
        kwargs = j_params.get("kwargs", {})
        print("inspect", inspect.signature(f), "a", args, "k", kwargs)

        f(*args, **kwargs)
        return {"success": True, "message": ""}

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not os.getenv("HasDB"):
            raise BackendException(
                message="You cannot add tasks if you do not add a DB!"
            )
        print("given to function", "args", args, "kwargs", kwargs)
        task_params = TaskParams(args=list(args), kwargs=kwargs)
        task = Task(
            task_id=random_str(30),
            url=g.base_url + router_path,
            status="queued",
            sent=False,
            secret_token=random_str(50),
            created_at=datetime.utcnow(),
            params=task_params.json(),
        )
        g.tasks.append(task)

        return task.id

    return wrapper
