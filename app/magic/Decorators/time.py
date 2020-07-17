import time
from app.magic.config import settings


def async_timeit(method):
    async def timed(*args, **kwargs):
        s = time.time()
        result = await method(*args, **kwargs)
        e = time.time()
        if settings.print_level > 0:
            print(f"{method.__name__} took {(e - s)*1_000} ms")
        return result

    return timed


def sync_timeit(method):
    def timed(*args, **kwargs):
        s = time.time()
        result = method(*args, **kwargs)
        e = time.time()
        if settings.print_level > 0:
            print(f"{method.__name__} took {(e - s)*1_000} ms")
        return result

    return timed
