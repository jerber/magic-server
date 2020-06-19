import os
import uvicorn

from app.magic import app, handler

public_host = '0.0.0.0'
local_host = '127.0.0.1'
if __name__ == "__main__":
    uvicorn.run("main:app", host=public_host, port=8000, reload=True, log_level="info")
