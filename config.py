import os

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'User')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME',"capstone")
DB_URL = os.getenv('DATABASE_URL',"postgresql+psycopg2://{}:{}@{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))

SQLALCHEMY_DATABASE_URI = DB_URL
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False