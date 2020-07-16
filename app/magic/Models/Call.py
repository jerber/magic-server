from magicdb.Models import DateModel, MagicModel
from datetime import datetime
from typing import Any
from pydantic import AnyUrl, BaseModel
from fastapi import Request as FastAPIRequest
from fastapi import Response as FastApiResponse
import json
from typing import Optional

from app.magic.Utils.random_utils import random_str

from app.magic.Decorators.background_tasks import run_in_background


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
def save_call(call: Call):
    call.save()


async def make_call_from_request_and_response(
    request: FastAPIRequest,
    response: Optional[FastApiResponse],
    error: Optional[Exception],
    times_dict: dict,
):
    body_json = await request.body() or None
    request_obj = Request(
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

    response_obj = (
        None
        if not response
        else Response(
            body=json.loads(response.body),
            headers=dict(response.headers),
            status_code=response.status_code,
        )
    )

    error_obj = (
        None
        if not error
        else Error(error_class=str(error.__class__), error_dict=error.__dict__)
    )

    # TODO what if error.__Dict is not json encodable... must check that before...
    # or maybe wrap this whole thing w a try catch just in case so it does not fuck up everything else

    call = Call(
        request=request_obj,
        response=response_obj,
        error=error_obj,
        times=Times(**times_dict),
    )

    call.save()
