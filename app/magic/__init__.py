"""Imports the Routes and the app and glues them all together"""
from fastapi import APIRouter

from .config import settings
from app.magic.app_factory import create_app, create_handler

app = create_app(config_settings=settings)
handler = create_handler(app)

background_router = APIRouter()
# this requires a background router
from app.magic.Utils.middleware import CallRoute

router = APIRouter(route_class=CallRoute)


def add_routes(this_app):

    # import all of the routes
    from app import Routes

    this_app.include_router(router)
    this_app.include_router(background_router)


add_routes(app)
