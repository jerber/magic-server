import os
from fastapi import FastAPI, Request
import magicdb
import json
import requests
import threading


class G:
    def __init__(self, app: FastAPI = None, request: Request = None) -> None:
        self._app = app
        self._request = request
        self.tasks = []

    @property
    def app(self) -> FastAPI:
        return self._app

    @app.setter
    def app(self, app: FastAPI) -> None:
        self._app = app

    @property
    def request(self) -> Request:
        return self._request

    @request.setter
    def request(self, request: Request) -> None:
        self._request = request

    @property
    def base_url(self) -> str:
        url = str(self.request.url)
        path = self.request.url.path
        url = url[: url.rindex(path)]
        url = url if os.environ.get("LOCAL") else url + f"/{os.getenv('STAGE')}"
        return url

    @property
    def url(self) -> str:
        return str(self.request.url)

    """TASKS"""

    def run_tasks_locally(self, task):
        # make a dict but make sure dates are properly parsed
        d = json.loads(task.json())
        d["task_id"] = task.id
        resp = requests.post(task.url, json=d)
        print("og resp", resp.content)
        print("resp from local task", resp.content)

    def save_tasks(self):
        """This will have a limit of 500 background tasks at a time..."""
        if not self.tasks:
            return

        batch = magicdb.batch()
        count = 0
        saved_tasks = []
        while len(self.tasks) and count < 500:
            task = self.tasks.pop(0)
            task.save(batch=batch)
            saved_tasks.append(task)
            count += 1
        batch.commit()
        if os.environ.get("LOCAL"):
            for task in saved_tasks:
                threading.Thread(target=self.run_tasks_locally, args=(task,)).start()


g = G()
