import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'You and me knows very well it is secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PASSWORD = 'annet'
    HOST = 'localhost'
    USER = 'postgres'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_NAME = 'diary'

class TestingConfig(Config):
    TESTING = False
    DEBUG = True
    DATABASE_NAME = 'test_diary'