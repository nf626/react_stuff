import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://hbnb_evo_2:default_pwd@localhost:5000/hbnb_evo_2_db'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://nigel:123@localhost:5000/hbnb_evo_2_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
