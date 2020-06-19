from app.magic import router
from app.Errors.TestError import TestError


@router.get("/test_errors")
def test_errors():
    raise TestError(message="This test worked!")
