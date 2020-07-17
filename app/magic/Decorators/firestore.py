import os
from functools import wraps
from app.magic.Errors import FirestoreException

from app.magic.Decorators.helpers import async_safe


def need_firestore(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise FirestoreException(
                message="You must supply a firestore service account to use this endpoint!"
            )
        return await async_safe(f, *args, **kwargs)

    return wrapper
