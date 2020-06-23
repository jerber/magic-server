import time

from app.magic.Decorators.parse_objects import parse_objects
from app.magic.Decorators.background_tasks import run_in_background

from app.Models.TestUser import TestUser

from app.magic import router

from fastapi import Body, Depends

from app.magic import get_current_user, CurrentUser, GET_USER


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


@router.post("/test_async_with_firestore")
def test_async(*, secs: float = 5, test_user: TestUser):
    task_id = sleep_for_five(secs, test_user)
    return {"task_id": task_id}


@router.post("/test_async_without_firestore")
def test_async(*, secs: float = 5):
    task_id = sleep_for_five(secs)
    return {"task_id": task_id}


@router.get("/hello")
def hello(current_user: CurrentUser = GET_USER):
    return current_user
