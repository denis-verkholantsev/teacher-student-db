
class Config(object):
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1313@localhost:7654/postgres"
    SECRET_KEY = "my_secret_key"
    TESTING = False