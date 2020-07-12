from app.magic import router
import time
import boto3
import os
from app.magic.Models.Task import Task
from fastapi.encoders import jsonable_encoder

TASKS_TABLE = os.environ.get("TASKS_TABLE_NAME")
dynamodb = boto3.resource("dynamodb")


@router.post("/test_dynamo", tags=["boilerplate"])
def test_dynamo(task: Task):
    start = time.time()
    table = dynamodb.Table(TASKS_TABLE)
    resp = table.put_item(Item=jsonable_encoder(task))
    time_took = time.time() - start
    print("dynamo resp", resp)

    return {"task_id": task.task_id, "time_took": time_took}
