import os
from functools import wraps
from app.magic.Errors import FirestoreException


def need_firestore(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise FirestoreException(
                message="You must supply a firestore service account to use this endpoint!"
            )
        return f(*args, **kwargs)

    return wrapper
