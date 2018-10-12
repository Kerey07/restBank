# здесь будут представления
from app import app, db, ma
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Users, Accounts, AccountsSchema, UsersSchema
from flask import request, jsonify
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
@app.route('/accounts')
@login_required
def accounts():
    account_schema = AccountsSchema(many=True)
    user = current_user.accounts
    accounts_result = account_schema.dump(user)
    return jsonify(accounts_result)


