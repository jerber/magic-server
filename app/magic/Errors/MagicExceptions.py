from fastapi import Request
from app.magic import app
from fastapi.responses import JSONResponse


class MagicException(Exception):
    def __init__(self, message: str):
        self.status_code = 452
        self.message = message


class BackendException(MagicException):
    pass


class FrontendException(MagicException):
    pass


@app.exception_handler(BackendException)
def backend_exception_handler(request: Request, exc: BackendException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": f"{exc.message}"},
    )


@app.exception_handler(FrontendException)
def frontend_exception_handler(request: Request, exc: FrontendException):
    return JSONResponse(
        status_code=418, content={"success": False, "message": f"{exc.message}"}
    )
