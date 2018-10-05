from . import BaseConfig


class CircleCITest(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@127.0.0.1:3306/circle_test"
    TESTING = True
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


class LocalTest(BaseConfig):
    TESTING = True
    SQLALCHEMY_ECHO = False
