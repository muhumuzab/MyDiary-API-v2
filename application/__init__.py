from flask import Flask, Blueprint
from flask_restplus import Api
from flask_jwt_extended import JWTManager

from application.config import configuration
from application.manage import Database


db = None
jwt = None

def create_app(config, database=None):

    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(configuration[config])
    app.url_map.strict_slashes = False


    # initialize api
    api = Api(app=app,
              title='My Diary',
              doc='/api/v1/documentation',
              description='My Diary is a online journal where users can write down \
                          their thoughts and feelings')



    global jwt
    jwt = JWTManager(app)
    jwt._set_error_handler_callbacks(api)        

    from application.views import blacklist 
    """
    This decorator sets the callback function that will 
    be called when a protected endpoint 
    is accessed and will check if the JWT has been been revoked.

    Returns True if the token has been blacklisted or False otherwise.
    """
   
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist


    global db
    db = Database(app.config)

    from application.views.entry_views import api as entries
    from application.views.user_views import api as user
    api.add_namespace(entries, path='/api/v1')
    api.add_namespace(user, path='/api/v1')

    #from application.docs.views import docs
    #app.register_blueprint(docs)

    """ Create database tables """
    db.create_all()
    return app








































