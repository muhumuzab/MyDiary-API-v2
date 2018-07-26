from datetime import datetime
from application import db


class DiaryEntry():
    """Model of a diary entry

    title: title of diary entry,
    body: body of diary entry,
    
    """
    def __init__(self, data):
        self.title = data['title']
        self.body = data['body']
        

    def save(self, current_user_email):
        # insert new record
        query = "INSERT INTO entries (owner_id, title, body) \
                VALUES ((SELECT user_id from users where email ='{}'), '{}', '{}')" \
                                                    . format(current_user_email,
                                                        self.title,
                                                        self.body)
        db.execute(query)        
