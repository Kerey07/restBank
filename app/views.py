# здесь будут представления
from app import app
from flask_login import current_user, login_user
from app.models import Users
from flask import request
import json


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    print(payload)
    user = Users.query.filter_by(username=payload('username')).first()
    if user is None:
        return 'fuck'
    elif Users.check_password(payload('password')):
        return 'welcome'
    else:
        return 'badpass'



# # запрос операций по счетам пользователя
# @app.route('/my-history/<username>')
# def my_history(username):
