from flask import Flask, make_response,jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from application import db


class DiaryEntry():
    """Model of a diary entry

    title: title of diary entry,
    body: body of diary entry,
    date_created: date when diary entry was created,
    date_modified: date when diary entry was modified
    
    """
    def __init__(self, data):
        self.title = data['title']
        self.body = data['body']
        self.date_modified = None
        self.date_created = datetime.datetime.utcnow()
	    #
        

    def save(self, current_user_email):
        # insert new record
        query = "INSERT INTO entries (owner_id, title, body, date_created, date_modified) \
                VALUES ((SELECT user_id from users where email ='{}'), '{}', '{}', '{}','{}')" \
                                                    . format(current_user_email,
                                                        self.title,
                                                        self.body,
                                                        self.date_created,
                                                        self.date_modified
                                                        )
        db.execute(query)        

    """ get a single diary entry """
   
    def get_diary_entry(self, entry_id=None):
        
  
        query = "SELECT * from entries where entry_id = {}"\
                . format(entry_id)      
        result = db.execute(query)
        row = result.fetchone()
        #response = make_response(jsonify([{'id': row[0], 'title': row[2],'body': row[3], \
                                            #'date_created' : row[4],'date_modified' : row[5]}]), 200)
        return [{'id': row[0], 'title': row[2],'body': row[3], \
                                            'date_created' : row[4],'date_modified' : row[5]}], 200
        
    
    """ update a diary entry """
    def update_diary_entry(self,entry_id):

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
        
        return {'id': entry[0],'title': entry[2], 'body': entry[3],'date_created': entry[4],'date_modified': entry[5]}

    """ Create diary entry """
    
    def post(self):
        
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

    """ get all diary entries """
    
    def get(self):

        response = {}

        try:
            query = "SELECT * from entries"
            result = db.execute(query)
            rows = result.fetchall()
            if (len(rows) == 0):

                # if no diary entries
                return {'message': 'Found no diary entries'}, 404
            else:

                response = make_response(jsonify([
                    {'id': row[0], 'title': row[2], 'body': row[3]}
                    for row in rows]), 200)
                return response
            
        except Exception as e:
            return {'message': 'Request not successful'}, 500

    