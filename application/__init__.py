from flask import Flask, Blueprint
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from application.config import configuration
from application.manage import Database