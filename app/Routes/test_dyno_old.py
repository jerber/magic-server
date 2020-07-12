from app.magic import router
import time
import boto3
import os
from app.magic.Models.Task import Task

TASKS_TABLE = os.environ.get('USERS_TABLE')
client = boto3.client('dynamodb')


@router.post("/test_dyno_old", tags=['boilerplate'])
def test_dyno_old(task: Task):
    start = time.time()
    resp = client.put_item(
        TableName=TASKS_TABLE,
        # Item={
        #     'task_id': {'S': task_id},
        #     'url': {'S': url},
        #     'status': {'S': status}
        # }
        Item=task.dict()
    )
    time_took = time.time() - start

    return {
        'task_id': task.task_id,
        'time_took': time_took
    }
