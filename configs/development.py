class Dev:
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/fr"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Test:
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/fr"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
