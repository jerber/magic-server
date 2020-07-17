import time
from app.magic.config import settings

from app.magic.Decorators.helpers import async_safe


def timeit(method):
    async def timed(*args, **kwargs):
        s = time.time()
        result = await async_safe(method, *args, **kwargs)
        e = time.time()
        if settings.print_level > 0:
            print(f"{method.__name__} took {(e - s)*1_000} ms")
        return result

    return timed
