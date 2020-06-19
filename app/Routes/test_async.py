import time

from app.magic.Decorators.parse_objects import parse_objects
from app.magic.Decorators.background_tasks import run_in_background

from app.Models.TestUser import TestUser


from app.magic import router


@run_in_background
@parse_objects
def sleep_for_five(secs: float, test_user: TestUser):
    print("starting to sleep for test user", test_user)
    time.sleep(secs)
    test_user.slept = True
    test_user.save(merge=True)
    print("ended sleep for test user", test_user)


@router.post("/test_async")
def test_async(*, secs: float = 5, test_user: TestUser):
    task_id = sleep_for_five(secs, test_user)
    return {"task_id": task_id}
