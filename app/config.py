import os

SECRET_KEY=os.environ.get('SECRET_KEY', 'dev')


SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_DSN')
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=os.environ.get('FLASK_ENV') == 'development'
