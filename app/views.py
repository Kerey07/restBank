# здесь будут представления
from app import app, db
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
    user = Users.query.filter_by(username=payload['login']).first()
    if user is None or not user.check_password(str(payload['password'])):
        return 'Invalid username or password'
    else:
        return 'welcome'



# Создание нового пользователя
@app.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    if Users.query.filter_by(username=payload['login']).first() is None:
        user = Users(username=payload['login'])
        user.set_password(payload['password'])
        db.session.add(user)
        db.session.commit()
        return 'Well done! U in!'
    else:
        return 'Not today bro((('




# # запрос операций по счетам пользователя
# @app.route('/my-history/<username>')
# def my_history(username):
