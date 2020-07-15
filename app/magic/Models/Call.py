from magicdb.Models import DateModel, MagicModel
from datetime import datetime
from typing import Any
from pydantic import AnyUrl, BaseModel
from fastapi import Request as FastAPIRequest
from fastapi import Response as FastApiResponse
import json
from typing import Optional
from app.magic.Utils.random_utils import random_str


class Error(BaseModel):
    error_class: str
    error_dict: dict = {}


class Response(BaseModel):
    body: Any
    headers: dict
    status_code: int


class Request(BaseModel):
    request_id: str
    body: Any
    headers: dict
    cookies: dict
    url: str
    url_path: str
    root_url: str
    query_params: dict
    ip_address: str


class Call(DateModel):
    request: Request
    response: Response = None
    error: Error = None
    time_received: datetime
    time_done: datetime
    time_took: datetime

    class Meta:
        collection_name = "_calls"


async def make_call_from_request_and_response(
    request: FastAPIRequest,
    response: Optional[FastApiResponse],
    error: Optional[Exception],
):
    body_json = await request.body() or None
    r = Request(
        request_id=random_str(30),
        body=None if not body_json else json.loads(body_json),
        headers=dict(request.headers),
        cookies=dict(request.cookies),
        url=str(request.url),
        url_path=request.url.path,
        root_url=str(request.url).replace(request.url.path, ""),
        query_params=dict(request.query_params),
        ip_address=request.client.host,
    )
    print("RUUUUU", r)
    r.save()

    print(request.__dict__)
    print("URRRLL", request.url)
    print("url path", request.url.path)
    print("reeeee", request.url.__dict__)
    print("ipp address", request.client.host)
    body_json = await request.body() or None
    if body_json:
        body = json.loads(body_json)
        print("request_body", body)

    print("request_query_params", dict(request.query_params))
    print("request_headers", dict(request.headers))
    print("request_cookies", request.cookies)

    print("request", request, "response", response)
    if response:
        print(
            "body",
            json.loads(response.body),
            "headers",
            dict(response.headers),
            "status_code",
            response.status_code,
        )
    if error:
        print("error dict", error.__dict__)
        print("error class", str(error.__class__))
