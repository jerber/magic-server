from fastapi import Request

# from app.magic import app
# from app.magic.app_factory import create_app
from app.magic.app_factory import app

from fastapi.responses import JSONResponse


class MagicException(Exception):
    def __init__(self, message: str):
        self.status_code: int = 452
        self.message: str = message


class BackendException(MagicException):
    pass


class FrontendException(MagicException):
    pass


class FirestoreException(MagicException):
    pass


class TwilioException(MagicException):
    pass


# app = create_app()


@app.exception_handler(MagicException)
def backend_exception_handler(request: Request, exc: MagicException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": f"{exc.message}", "error": True},
    )
