from distutils.debug import DEBUG


import os

class Config(object):
    POSTS_PER_PAGE = 10
    #SQLALCHEMY_ECHO = True
    #This above line will print all SQL queries executed as part of ORM

class ProdConfig(Config):
    SECRET_KEY = os.urandom(24)

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = os.urandom(24)