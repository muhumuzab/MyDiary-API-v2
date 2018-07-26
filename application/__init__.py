from flask import Flask, Blueprint
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from application.config import configuration
from application.manage import Database


db = None
jwt = None

def create_app(config, database=None):

    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    CORS(app)
    app.config.from_object(configuration[config])
    app.url_map.strict_slashes = False

    # Enable swagger editor
    app.config['SWAGGE_UI_JSNEDITOR'] = True

    # initialize api
    api = Api(app=app,
              title='My Diary',
              doc='/api/v1/documentation',
              description='My Diary is a online journal where users can write down \
                          their thoughts and feelings')



    global jwt
    jwt = JWTManager(app)
    jwt._set_error_handler_callbacks(api)                      

    global db
    db = Database(app.config)

    from application.views import blacklist

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    from application.views.entry_views import api as rides
    from application.views.user_views import api as user
    api.add_namespace(rides, path='/api/v1')
    api.add_namespace(user, path='/api/v1')










































