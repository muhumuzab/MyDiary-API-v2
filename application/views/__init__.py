""" create set for storing blaclisted tokens """
blacklist = set()
from application import jwt
from flask_jwt_extended.default_callbacks import default_expired_token_callback
