from app.magic.Utils.importing import get_all_subfiles_and_dirs

from fastapi import APIRouter


from app.magic import app
from app.magic.Utils.middleware import CallRoute

sub_router = APIRouter(route_class=CallRoute)

# imports all of the subroutes...
__all__ = get_all_subfiles_and_dirs(__file__)
from . import *

app.include_router(sub_router, prefix="/sub_routes", tags=["sub_routes_boilerplate"])
