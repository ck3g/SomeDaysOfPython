import os
from .common import *  # pylint: disable=relative-beyond-top-level

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")


ALLOWED_HOSTS = []
