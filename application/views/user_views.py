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

class UserSignUp(Resource):

    @api.doc('user accounts',
             responses={201: 'CREATED',
                        400: 'BAD FORMAT', 409: 'CONFLICT'})
    @api.expect(usermodel)
    def post(self):
        """User sign up"""
        userData = request.get_json()
        firstname = userData['firstname']
        secondname = userData['secondname']
        confirmPassword = userData['confirm_password']
        phone = userData['phone']
        email = userData['email']
        password = userData["password"]
        
        if email == "" or phone.strip() == ""\
                or confirmPassword.strip() == "" or password.strip() == ""\
                or firstname.strip() == "" or secondname.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        try:
            query = "select email from users where email='%s'\
             or phone='%s'" % (email, phone)
            result = db.execute(query)
            user = result.fetchone()
            if user is None:
                userObject = User(userData)
                userObject.save()
                return {'message': 'Account created.'}, 201
            return {'message': 'User exists.'}, 409
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500



class UserLogin(Resource):

    
    def post(self):
        """User login
        :returns JWT after successful login
        """

        userData = request.get_json()
        email = userData['email']
        password = userData['password']

        if email.strip() == "" or password.strip() == "":
            return {"message": "Password or email cannot be empty."}, 401

        try:
            query = "select password from users where email='{}'"\
                    . format(email)
            result = db.execute(query)
            user = result.fetchone()

            if user is None:
                return {'message': 'User not found.'}, 404

            if check_password_hash(user[0], password):
                token = create_access_token(identity=email)
                return {'message': 'logged in.', 'token': token}, 201
            else:
                return {'message': 'Invalid password.'}, 401
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500

api.add_resource(UserSignUp, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')