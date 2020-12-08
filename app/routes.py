from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post, Event, DinningHall, SnackingAndSlacking


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

@app.route('/populate')
def populate():
    user = User(userName='ebarry', password='valley13', email='ebarry@ithaca.edu', schoolYear='sophmore', schoolName='ComputerScience')
    user2 = User(userName='Nusi', password='valley1372', email='ebarry334@ithaca.edu', schoolYear='sophmore', schoolName='ComputerScience')
    db.session.add_all([user, user2])
    db.session.commit()
    post1 = Post(body='It is a beautiful day on campus today!', userID=user2.id)
    post2 = Post(body='I cannot wait for my computer science classes next semester', userID=user2.id)
    post3 = Post(body='Dont forget to join the Computer Science club!', userID=user.id)
    post4 = Post(body='Join club hockey especially if you are a goalie we graduated two last year', userID=user.id)
    post5 = Post(body='The food at Campus center was gas make sure to stop by', userID=user2.id)
    post6 = Post(body='Really excited to be on campus next semester', userID=user.id)
    db.session.add_all([post1,post2,post3,post4,post5,post6])
    db.session.commit()
    event = Event(body='There is a varsity basketball game tonight at 9pm. Be there or be Square.', day='Friday', date=date(2020, 8, 15),  )
@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()
   populate()
   body='Reset the database please log in or register'
   return render_template('base.html', title='reset', body=body)


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



