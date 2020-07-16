from fastapi import APIRouter

from .config import settings
from app.magic.app_factory import app, handler

from app.magic.Errors.MagicExceptions import MagicException

background_router = APIRouter()

from app.magic.Utils.middleware import CallRoute  # this requires a background router

router = APIRouter(route_class=CallRoute)

from app import Routes  # import all of the routes

app.include_router(router)
app.include_router(background_router)
