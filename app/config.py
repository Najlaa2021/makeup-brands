import os

class Config:
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/finaldb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
