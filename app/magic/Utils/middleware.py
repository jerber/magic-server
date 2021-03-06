from datetime import datetime

from fastapi import Request, Response

from fastapi.routing import APIRoute
from typing import Callable

from app.magic.Models.Call import make_call_from_request_and_response


class CallRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = None
            error = None
            time_received = datetime.utcnow()
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                print("Error in call route", e.__dict__)
                error = e
            time_done = datetime.utcnow()
            delta = time_done - time_received
            secs_took = delta.seconds + delta.microseconds / 1_000_000
            times = {
                "time_received": time_received,
                "time_done": time_done,
                "secs_took": secs_took,
            }
            await make_call_from_request_and_response(request, response, error, times)
            if error:
                raise error
            return response

        return custom_route_handler
