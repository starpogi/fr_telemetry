from . import BaseConfig


class Production(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    DEBUG = False
