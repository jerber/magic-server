import os
import boto3

from magicdb.Models import DateModel, MagicModel


TASKS_TABLE = os.environ.get("TASKS_TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TASKS_TABLE)


class TaskParams(MagicModel):
    args: list
    kwargs: dict


# for now cannot accept an object that does not have the dict ability...
class Task(DateModel):
    task_id: str
    url: str
    status: str
    sent: bool
    secret_token: str
    params: str = None

    class Meta:
        collection_name = "_tasks"

    @staticmethod
    def get_table():
        return table
