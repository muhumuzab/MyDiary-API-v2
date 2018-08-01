import json
import unittest
from application import create_app, db

class BaseUserAccount(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        from application import db

        self.user_data = {
            "firstname":"muhumuza",
            "secondname":"brian",
            "email": "muhumuza@gmail.com",
            "password": "abc123",
            "phone": "0718881111",
            "confirm_password": "abc123"
        }
        self.details_with_invalid_password = {
            "email": "muhumuza@gmail.com",
            "password": "abc1234",
        }
        self.user_not_exist = {
            "email": "muhumuza@gmail3435xbf.com",
            "password": "abc123",
        }
        self.login_with_empty_password = {
            "email": "muhumuza@gmail.com",
            "password":""
        }
        self.data_with_unmatching_passwords = {
            "firstname":"muhumuza",
            "secondname":"brian",
            "email": "muhumuza@gmail.com",
            "password": "muhumuza1",
            "phone": "0719800509",
            "confirm_password": "muhumuza11"
        }
        self.data_with_invalid_email = {
            "firstname":"muhumuza",
            "secondname":"brian",
            "email": "muhumuza2@gmail.com",
            "password": "muhumuza1",
            "phone": "0719800509",
            "confirm_password": "muhumuza1"
        }
        self.data_with_empty_password = {
            "firstname":"muhumuza",
            "secondname":"brian",
            "email": "muhumuza@gmail.com",
            "password": "  ",
            "phone": "0719800509",
            "confirm_password": "  "
        }

        self.data_with_short_password = {
            "firstname":"muhumuza",
            "secondname":"brian",
            "email": "muhumuza@gmail.com",
            "password": "mfcf",
            "phone": "0719800509",
            "confirm_password": "mfcf"
        }
        
        self.db = db
        self.db.drop_all()
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        self.app = None
        