from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime

from application.models.entry_models import DiaryEntry
from application import db

api = Namespace('diary entry', Description='Operations on entries')
