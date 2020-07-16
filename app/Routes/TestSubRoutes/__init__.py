from app.magic.Utils.importing import get_all_subfiles_and_dirs

from fastapi import APIRouter

# from app.magic import app
from app.magic.app_factory import app

sub_router = APIRouter()

# imports all of the subroutes...
__all__ = get_all_subfiles_and_dirs(__file__)
from . import *

app.include_router(sub_router, prefix="/sub_routes", tags=["sub_routes_boilerplate"])
