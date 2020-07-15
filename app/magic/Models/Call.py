from magicdb.Models import DateModel
from datetime import datetime
from typing import Any
from pydantic import AnyUrl
from fastapi import Request, Response
import json


class Call(DateModel):
    request_body: Any
    request_headers: dict
    time_took: datetime
    request_id: str
    request_url: AnyUrl
    request_base_url: AnyUrl
    response_body: Any
    response_status_code: int
    time_done: datetime
    time_received: datetime

    class Meta:
        collection_name = "_calls"


def make_call_from_request_and_response(request: Request, response: Response):
    print("request", request, "response", response)
    print(
        "body",
        json.loads(response.body),
        "headers",
        dict(response.headers),
        "status_code",
        response.status_code,
    )
