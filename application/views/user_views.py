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

api = Namespace('Users', Description='User operations')

def validate_email(email):
    match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
    if match is not None:
        return True
    return False