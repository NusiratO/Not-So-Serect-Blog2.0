from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, DateField, SelectField, \
    SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


def validate_username(username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError('Username is already taken!')


def validate_email(email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
        raise ValidationError('Email is already taken!')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    student_year = StringField('What is year?', validators=[DataRequired()])
    school_name = StringField('What is your school?', validators=[DataRequired()])
    submit = SubmitField('Register')


class PostForm(FlaskForm):
    post = TextAreaField('Share Your Piece!', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    description = TextAreaField('Want to add an event?', validators=[DataRequired(), Length(min=1, max=140)])
    day = StringField('What is the day?', validators=[DataRequired()])
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d')
    time = StringField('What time?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SnackingSlackingForm(FlaskForm):
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d')
    snacking_and_slacking_post = TextAreaField('What is slacking or snacking?', validators=[DataRequired(), Length(min=1, max=140)])
    food = StringField('Whats the meal', validators=[DataRequired()])
    selectDinning = SelectField('Select a dininghall', choices=[], coerce=int)
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    post = TextAreaField('What would you like to comment?', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Post")
