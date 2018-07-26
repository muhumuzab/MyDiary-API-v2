import os
from werkzeug.contrib.fixers import ProxyFix  # fix no spec in heroku

from application import create_app