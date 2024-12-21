import os
from flask import request

from app_instance import app
from common.routes import *


def configure_current_application():
    configure_app_routes()
    # configure_database()
