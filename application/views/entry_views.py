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
    

    @jwt_required
    def put(self,entry_id):

        query = "select * from entries where entry_id='{}'".format(entry_id)
        result = db.execute(query)
        entry = result.fetchone()
        if entry is None:
            return {'message': 'diary entry with given id does not exist'}, 404
        current_user_email = get_jwt_identity()
        query =  "select user_id from users where email='{}'"\
                    . format(current_user_email)
        result = db.execute(query)
        user_id = result.fetchone()
        if not entry[1] == user_id[0]:
            return {'message': 'You cannot change \
                        details of diary entry that you do not own'}, 401
        
        data = request.get_json()
       

        query = "update entries set title='{}',body='{}' where entry_id='{}'".format(data['title'], data['body'], int(entry_id))
        db.execute(query)
        
        query = "select * from entries where entry_id='{}'".format(entry_id)
        result = db.execute(query)
        entry = result.fetchone()
        return jsonify({'id': entry[0],'title': entry[2], 'body': entry[3]})

class Entries(Resource):

    @jwt_required
    def post(self):
        """ Creates a new diary entry """
        data = request.get_json()
        current_user_email = get_jwt_identity()
        # Check whether there is data
        if any(data):

            # save entry to data structure
            

                
            entry = DiaryEntry(data)
            # save data here
            entry.save(current_user_email)
            return {'message':
                    'diary entry added successfully.'}, 201
        else:
            return {'message': 'no data provided.'}, 409
