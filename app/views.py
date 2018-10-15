# здесь будут представления
from app import app, db
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Users, AccountsSchema, Accounts, LogSchema, Log
from flask import request, jsonify, abort



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
        return abort(409, 'User already exists')  # Возвращаем ошибку


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


# проведение операций
@app.route('/operations', methods=['POST', 'GET'])
@login_required
def operations():
    if request.method == 'GET':
        operations_list = {'operation_name': ['PURCHASE', 'TRANSFER', 'WITHDRAWAL','CREATE']}
        return jsonify(operations_list)
    else:
        # разбираем прилетевший джейсон
        payload = request.get_json()
        operation_type = payload['operation_type']
        operation_value = payload['value']
        user_account_id = payload['user_account']
        user_account = Accounts.query.filter_by(accountID=user_account_id).first()
        if operation_type == 'PURCHASE':
            # пополнение
            new_user_acc_value = int(user_account.value) + int(operation_value)
            user_account.value = new_user_acc_value
            log = Log(account_owner=current_user.userID, account=user_account_id,type= operation_type,value= operation_value)
            db.session.add(log)
            db.session.commit()
            return str(user_account.value)
        elif operation_type == 'WITHDRAWAL':
            # списание
            new_user_acc_value = int(user_account.value) - int(operation_value)
            user_account.value = new_user_acc_value
            db.session.commit()
            log = Log(account_owner=current_user.userID, account=user_account_id, type=operation_type, value=operation_value)
            db.session.add(log)
            return str(user_account.value)
        elif operation_type == 'TRANSFER':
            # перевод между счетами
            new_user_acc_value = int(user_account.value) - int(operation_value)
            user_account.value = new_user_acc_value
            recipient_account_id = payload['recipient_account']
            recipient_account = Accounts.query.filter_by(accountID=recipient_account_id).first()
            new_recip_acc_value = int(recipient_account.value) + int(operation_value)
            recipient_account.value = new_recip_acc_value
            log = Log(account_owner=current_user.userID, account=user_account_id, type=operation_type, value=operation_value, recipient= recipient_account_id)
            db.session.add(log)
            db.session.commit()
            answer = {'donor_account':(user_account.value), 'recipient_account':(recipient_account.value)}
            return jsonify(answer)
        else:
            # создание нового счета
            new_account = Accounts(ownerID=current_user.userID, value=operation_value)
            db.session.add(new_account)
            log = Log(account_owner=current_user.userID, account=user_account_id, type=operation_type, value=operation_value)
            db.session.add(log)
            db.session.commit()
            return 'Account created'


@app.route('/history', methods=['POST'])
@login_required
def hisrory():
    log_schema = LogSchema(many=True)
    user = current_user.history
    account_history = log_schema.dump(user)
    return jsonify(account_history)
