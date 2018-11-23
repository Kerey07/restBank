# модуль инициации
import logging

from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import Config

logging.basicConfig(filename='flask.log', level=logging.DEBUG, filemode='w')

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
ma = Marshmallow(app)

from app import views, models
