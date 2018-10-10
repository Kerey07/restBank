from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Users(UserMixin, db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# @login.user_loader
# def load_user(userID):
#     return User.query.get(int(userID))


class Accounts(db.Model):
    accountID = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey(Users.userID))
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<Accounts %r>'.format(self.owner)


class Log(db.Model):
    operationID = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.Integer, db.ForeignKey(Accounts.accountID))
    recipient = db.Column(db.Integer, db.ForeignKey(Accounts.accountID))
    type = db.Column(db.String)
    value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'Log %r'.format(self.donor)
