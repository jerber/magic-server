from functools import wraps
import inspect

from app.magic.config import settings
from app.magic.Errors import BackendException

from app.magic.Services.Doorman import CurrentUser

from app.magic.Services import Segment

from app.magic.Decorators.helpers import async_safe


def segment(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if not settings.segment_write_key:
            raise BackendException(
                message="You cannot use the segment decorator without the SEGMENT_WRITE_KEY env variable."
            )
        for key, val in kwargs.items():
            if issubclass(val.__class__, CurrentUser):
                uid = val.uid
                action = f.__name__
                Segment.track(uid, action)
        return await async_safe(f, *args, **kwargs)

    return wrapper
