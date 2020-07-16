import os
import boto3

from magicdb.Models import DateModel, MagicModel
from app.magic.config import settings


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(settings.tasks_table_name)


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
