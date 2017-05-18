import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'fv\x01\x82\x8f\xc5\x0f\xaaHQ\xe6\x1a[\x14\x92\xa5S7L\xbfs\xd6\x99\x95'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
