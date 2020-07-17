from functools import wraps

from app.magic.config import settings
from app.magic.Errors import BackendException

from app.magic.Services.Doorman import CurrentUser

from app.magic.Services import Segment

from app.magic.Decorators.helpers import async_safe


def segment(keywords=None):
    def inner_function(f):
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
                    segment_d = {}
                    if keywords:
                        segment_d = {k: kwargs.get(k) for k in keywords}
                    Segment.track(uid, action, segment_d)
            return await async_safe(f, *args, **kwargs)

        return wrapper

    return inner_function
