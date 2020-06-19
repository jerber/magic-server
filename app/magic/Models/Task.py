from magicdb.Models import DateModel, MagicModel


class TaskParams(MagicModel):
    args: list
    kwargs: dict


# for now cannot accept an object that does not have the dict ability...
class Task(DateModel):
    url: str
    status: str
    sent: bool
    secret_token: str
    params: str = None

    class Meta:
        collection_name = "_tasks"
