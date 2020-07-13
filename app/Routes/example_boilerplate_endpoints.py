"""There are all boilerplate examples of using routes..."""

from app.magic import router


"""Example of background tasks."""
import time

from app.magic.Decorators.parse_objects import parse_objects
from app.magic.Decorators.background_tasks import run_in_background

from app.Models.TestUser import TestUser


@run_in_background
@parse_objects
def sleep_for_five(secs: float, test_user: TestUser = None):
    print("starting to sleep for test user", test_user)
    if not test_user:
        TestUser(name="Jon", age=3)
    time.sleep(secs)
    test_user.slept = True
    test_user.save(merge=True)
    print("ended sleep for test user", test_user)


@router.post("/test_async_with_firestore", tags=["boilerplate"])
def test_async(*, secs: float = 5, test_user: TestUser):
    task_id = sleep_for_five(secs, test_user)
    return {"task_id": task_id}


@router.post("/test_async_without_firestore", tags=["boilerplate"])
def test_async(*, secs: float = 5):
    task_id = sleep_for_five(secs)
    return {"task_id": task_id}


"""Example of auth."""

from app.magic.Services.Doorman import CurrentUser, GET_USER


@router.get("/get_current_user", response_model=CurrentUser, tags=["boilerplate"])
def get_current_user(current_user: CurrentUser = GET_USER):
    print(current_user)
    return current_user


"""Adding to DynamoDB Table."""

from app.magic.Models.Task import Task
from fastapi.encoders import jsonable_encoder
from typing import List


@router.post("/test_dynamo", tags=["boilerplate"])
def test_dynamo(tasks: List[Task]):
    start = time.time()
    with Task.get_table().batch_writer() as batch:
        for task in tasks:
            batch.put_item(Item=jsonable_encoder(task))
    time_took = time.time() - start

    return {"task_ids": [task.task_id for task in tasks], "time_took": time_took}


"""Errors example."""

from app.Errors.TestError import TestError


@router.get("/test_errors", tags=["boilerplate"])
def test_errors():
    raise TestError(message="This test worked!")


"""Sending to segment example and test."""


from app.magic.Services.Segment import analytics


@router.post("/test_segment", tags=["boilerplate"])
def test_segment(id: str, action, body: dict):
    analytics.track(id, action, body)
    return "done!"


"""Twilio Example"""

from app.magic.Services.Twilio import send_text
from app.magic.FieldTypes import PhoneNumber
from fastapi import APIRouter

# example for using new router too
r = APIRouter()


@r.get("/send_text")
def send_text_router(phone_number: PhoneNumber, body: str):
    sid = send_text(to=phone_number, body=body)
    return sid


from app.magic import app

app.include_router(r, prefix="/text", tags=["boilerplate"])
