import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'mohd-arham'
    JWT_SECRET_KEY = '%gAsDin-=08'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    SWAGGER = {
        'title': 'Task Manager API',
        'uiversion': 3
    }
