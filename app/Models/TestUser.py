from magicdb.Models import MagicModel
from pydantic import BaseModel


class TestUser(MagicModel):
    name: str
    age: int
    slept: bool = False

    class Meta:
        collection_name = "_test_user"
