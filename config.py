import os
from os import environ as env

from dotenv import load_dotenv
load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI=env['SQLALCHEMY_DATABASE_URI']