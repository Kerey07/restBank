from app import db


class Users(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.username


class Accounts(db.Model):
    accountID = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey(Users.userID))
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<Accounts %r>' % self.owner


class Log(db.Model):
    operationID = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.Integer, db.ForeignKey(Accounts.accountID))
    recipient = db.Column(db.Integer, db.ForeignKey(Accounts.accountID))
    type = db.Column(db.String)
    value = db.Column(db.Integer)

    def __repr__(self):
        return 'Log %r' % self.donor
