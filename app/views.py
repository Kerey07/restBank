# здесь будут представления
from app import app, db
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Users, Accounts
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
    login_user(user)
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


# Окончание сеанса
@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return 'goodbye'


# запрос операций по счетам пользователя
@app.route('/accounts/<username>')
@login_required
def accounts(username):
    accounts = Accounts.query.filter_by(username=username)
    return accounts

