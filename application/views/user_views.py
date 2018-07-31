from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime
import re

from . import blacklist

from application.models.user_model import User
from application import db



api = Namespace('Users', Description='User operations')

def validate_email(email):
    match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
    if match is not None:
        return True
    return False 

class UserSignUp(Resource):
    """ Enable user to sign up """
    def post(self):
        
        userData = request.get_json()
        firstname = userData['firstname']
        secondname = userData['secondname']
        confirmPassword = userData['confirm_password']
        phone = userData['phone']
        email = userData['email']
        password = userData["password"]
        
        """ check for empty fields """
        if email == "" or phone.strip() == ""\
                or confirmPassword.strip() == "" or password.strip() == ""\
                or firstname.strip() == "" or secondname.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        """ check if password id less than 6 characters """
        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        """ match email against regular expression """
        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        """ if passwords dont match """
        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        try:
            query = "select email from users where email='%s'\
             or phone='%s'" % (email, phone)
            result = db.execute(query)
            user = result.fetchone()
            """ if no user, save user data """
            if user is None:
                userObject = User(userData)
                userObject.save()
                return {'message': 'Account created.'}, 201
            return {'message': 'User exists.'}, 409
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500



class UserLogin(Resource):
    """ Enable user to login / generate jwt token """
    def post(self):
    
        userData = request.get_json()
        email = userData['email']
        password = userData['password']

        """ check for empty fields """
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
                return {'message': 'You have succesfully logged in.', 'token': token}, 201
            else:
                return {'message': 'Invalid password.'}, 401
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500

class Logout(Resource):
    """ log out user """
    @jwt_required
    def post(self):
        """ blacklist user's token """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return ({'message': 'You have successfully logged out'}), 200






api.add_resource(UserSignUp, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Logout, '/auth/logout')