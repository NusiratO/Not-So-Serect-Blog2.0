from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    school_year = db.Column(db.String(128))
    school_name = db.Column(db.String(128))
    post = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

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
    comments = db.relationship("Comment", backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(128))
    day = db.Column(db.String(28))
    date = db.Column(db.DateTime, index=True)
    time = db.Column(db.String(28))

    def __repr__(self):
        return '<{} on {} at []>'.format(self.description, self.day, self.time)


class SnackingAndSlacking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, index=True)
    snacking_and_slacking_post = db.Column(db.String(128))
    food = db.Column(db.String(64))
    dinning_hall = db.relationship('DinningHall', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Post {}, {}>'.format(self.snacking_and_slacking_post, self.food)


class DinningHall(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    snacking_and_slacking_id = db.Column(db.Integer, db.ForeignKey('snacking_and_slacking.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.name)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __repr__(self):
        return '<Comment: {}>'.format(self.message)
