# здесь будут представления
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# авторизация пользователя
@app.route('/login/<username>/<password>')
def login(username, password):
    if username == "login":
        if password == "password":
            return "True"
        else:
            return "False"
    else:
        return "False login"


# # запрос операций по счетам пользователя
# @app.route('/my-history/<username>')
# def my_history(username):
