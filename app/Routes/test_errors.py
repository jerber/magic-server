from app.magic import router
from app.Errors.TestError import TestError


@router.get("/test_errors", tags=['boilerplate'])
def test_errors():
    raise TestError(message="This test worked!")
