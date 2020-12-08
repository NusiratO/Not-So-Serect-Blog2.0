from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    schoolYear = db.Column(db.String(128))
    schoolName = db.Column(db.String(128))
    post = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.userName)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(128))
    Day = db.Column(db.String(28))
    Date = db.Column(db.DateTime, index=True)
    Time = db.Column(db.String(28))

    def __repr__(self):
        return '<{} on {} at []>'.format(self.Description, self.Day, self.Time)


class SnackingAndSlacking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date = db.Column(db.DateTime, index=True)
    SSPost = db.Column(db.String(128))
    Food = db.Column(db.String(64))

    def __repr__(self):
        return '<Post {}, {}>'.format(self.SSPost, self.Food)


class DinningHall(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(64))

    def __repr__(self):
        return '<Post {}>'.format(self.Name)
