from distutils.debug import DEBUG


import os
DEBUG = True
# Connect to the database
SECRET_KEY='a secret'
SQLALCHEMY_DATABASE_URI = 'your psycopg2 URI connection'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_NAME = "info.db"
SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}'
print(DB_NAME)
