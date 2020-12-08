from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post


@app.route('/')
@app.route('/home')
def homepage():
    title = {'title': 'Whats Happening In & Out of IC?'}
    body = {'body': 'Page is Under Construction. Apologizes in Advance!'}
    return render_template('index.html', title='Home', user=title, body=body)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userName=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, userName=form.username.data, schoolName=form.schoolName.data,
                    schoolYear=form.studentYear.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('createAnAccount.html', title='Register', form=form)


@app.route('/events')
def events():
    title = {'title': 'Whats Happening In & Out of IC?'}
    body = {'body': 'Page is Under Construction. Apologizes in Advance!'}
    return render_template('events.html', title='Home', user=title, body=body)


@app.route('/Blog', methods=['GET', 'POST'])
def Blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('You post your blog on the board!')
        return redirect(url_for('Blog'))
    posts = Post.query.all()
    return render_template('Blog.html', title="Share Your Piece", form=form, posts=posts)


