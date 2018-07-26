from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime
import re

from application.models.user_model import User
from application import db
from . import blacklist


try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs