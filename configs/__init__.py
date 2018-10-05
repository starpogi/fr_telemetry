class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/fr"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = True
    SQLALCHEMY_ECHO = False
    TESTING = False

    PARSE_WORKERS = 4
