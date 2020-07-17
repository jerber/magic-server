import time

from magicdb.Models import DateModel, MagicModel
from datetime import datetime
from typing import Any, Optional
from pydantic import AnyUrl, BaseModel
from fastapi import Request as FastAPIRequest
from fastapi import Response as FastApiResponse
import json
from typing import Optional

from app.magic.Utils.random_utils import random_str

from app.magic.Decorators.background_tasks import run_in_background
from app.magic.Decorators.parse_objects import parse_objects
from app.magic.Decorators.time import async_timeit, sync_timeit

from app.magic.config import settings


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
    method: str
    scheme: str
    port: Optional[int]


class Times(BaseModel):
    time_received: datetime
    time_done: datetime
    secs_took: float


class Call(DateModel):
    request: Request
    response: Response = None
    error: Error = None
    times: Times

    class Meta:
        collection_name = "_calls"


@run_in_background
@parse_objects
def save_call(call: Call):
    call.save()


async def get_request_body(request: FastAPIRequest):
    # first try json, then body, then form...
    errors = []
    try:
        result = await request.json() or None
        return result
    except Exception as json_error:
        errors.append(f"json_error {json_error}")

    try:
        result = await request.form() or None
        return dict(result)
    except Exception as form_error:
        errors.append(f"form_error {form_error}")

    try:
        result = await request.body() or None
        return result
    except Exception as body_error:
        errors.append(f"body_error {body_error}")

    if settings.print_level > 1:
        print("get_request_body_errors", errors)

    return None


def make_body_jsonable(body):
    try:
        json.dumps(body)
        return body
    except TypeError as _:
        pass

    # now try making string
    try:
        body_str = str(body)
        return body_str
    except TypeError as _:
        pass

    return None


def safe_loads(body):
    if body is None:
        return body
    try:
        return json.loads(body)
    except TypeError as _:
        pass

    try:
        return str(body)
    except TypeError as _:
        pass

    return None


async def make_call_from_request_and_response(
    request: FastAPIRequest,
    response: Optional[FastApiResponse],
    error: Optional[Exception],
    times_dict: dict,
):
    if not settings.save_calls:
        return

    body = await get_request_body(request)
    jsonable_body = make_body_jsonable(body)

    request_obj = Request(
        request_id=random_str(30),
        body=jsonable_body,
        headers=dict(request.headers),
        cookies=dict(request.cookies),
        url=str(request.url),
        url_path=request.url.path,
        root_url=str(request.url).replace(request.url.path, ""),
        query_params=dict(request.query_params),
        ip_address=request.client.host,
        method=request.method,
        scheme=request.url.scheme,
        port=request.url.port,
    )

    response_obj = (
        None
        if not response
        else Response(
            body=safe_loads(response.body),
            headers=dict(response.headers),
            status_code=response.status_code,
        )
    )

    error_obj = (
        None
        if not error
        else Error(
            error_class=str(error.__class__),
            error_dict=make_body_jsonable(error.__dict__),
        )
    )

    # maybe wrap this whole thing w a try catch just in case so it does not fuck up everything else
    # will do this once I test this out for a while... prob

    call = Call(
        request=request_obj,
        response=response_obj,
        error=error_obj,
        times=Times(**times_dict),
    )

    save_call(call)
