from app.magic import router
from app.magic.Errors import BackendException


@router.get("/test_errors")
def test_errors():
    raise BackendException(message="This test worked!")
