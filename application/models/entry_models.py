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
