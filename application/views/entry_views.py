from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime

from application.models.entry_models import DiaryEntry
from application import db

api = Namespace('diary entry', Description='Operations on entries')


class Entry(Resource):
    @jwt_required
    def get(self, entry_id=None):
        
        query = ''
        
        query = "SELECT * from entries where entry_id = {}"\
                . format(entry_id)

                  
        result = db.execute(query)
        row = result.fetchone()
        return jsonify([{'id': row[0], 'title': row[2],'body': row[3]}])
    
