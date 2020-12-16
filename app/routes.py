from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EventForm, SnackingSlackingForm, CommentForm
from app.models import User, Post, Event, DinningHall, SnackingAndSlacking, Comment
import requests


@app.route('/')
@app.route('/home')
def homepage():
    title = 'Home'
    events = Event.query.all()
    posts = Post.query.all()
    reviews = SnackingAndSlacking.query.all()
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?zip=14850,us&appid=475b2c8051316db693d4f475ff9614f9")
    text = r.json()
    temp = float(text['main']['temp'])
    temp_f = (temp - 273.15) * (9 / 5) + 32
    return render_template('home.html', title=title, temp_f=int(temp_f), events=events, posts=posts, reviews=reviews)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
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
    user = User(username='ebarry', email='ebarry@ithaca.edu', school_year='sophmore',
                school_name='ComputerScience')
    user2 = User(username='Nusi', email='ebarry334@ithaca.edu', school_year='sophmore',
                 school_name='ComputerScience')
    user.set_password('valley13')
    user2.set_password('valley1372')
    post1 = Post(body='It is a beautiful day on campus today!', user_id=user2.id)
    post2 = Post(body='I cannot wait for my computer science classes next semester', user_id=user2.id)
    post3 = Post(body='Dont forget to join the Computer Science club!', user_id=user.id)
    post4 = Post(body='Join club hockey especially if you are a goalie we graduated two last year', user_id=user.id)
    post5 = Post(body='The food at Campus center was gas make sure to stop by', user_id=user2.id)
    post6 = Post(body='Really excited to be on campus next semester', user_id=user.id)

    d = datetime(2021, 2, 20)
    d2 = datetime(2021, 2, 25)
    d3 = datetime(2021, 3, 15)
    d4 = datetime(2021, 3, 12)
    d5 = datetime(2021, 2, 20)
    d6 = datetime(2021, 4, 13, 10)
    d7 = datetime(2021, 4, 14, 12)
    d8 = datetime(2021, 4, 15, 7)
    d9 = datetime(2021, 4, 16, 10)
    d10 = datetime(2021, 4, 17, 2)

    event = Event(description='There is a varsity basketball game tonight at 9pm. Be there or be Square.', day='Friday',
                  date=d, time='9pm')
    event2 = Event(
        description='Club sports sign up starts on February 30th make sure to check out all of the club on the club '
                    'sports website',
        day='Friday', date=d2, time='7am')
    event3 = Event(description='Mens Lacrosse game today at 11am', day='Wednesday',
                   date=d3, time='11am')
    event4 = Event(description='PARTY AT 112 Kendal Street Saturday Night 9pm!!! GET YO DANCE ONNN!!!!', day='Saturday',
                   date=d4, time='9pm')
    event5 = Event(description='There is a varsity basketball game tonight at 9pm. Be there or be Square.',
                   day='Saturday', date=d5, time='9pm')
    cc = DinningHall(name="Campus Center")
    ter = DinningHall(name='Terraces')

    food = SnackingAndSlacking(date=d6, snacking_and_slacking_post='Today the breakfast at CC was really good',
                               food='pancakes, bacon, eggs')
    food1 = SnackingAndSlacking(date=d7, snacking_and_slacking_post='I had an amazing lunch after class today. Got '
                                                                    'myself a grilled cheese with fries',
                                food='Grilled Cheese, Fries')
    food2 = SnackingAndSlacking(date=d8, snacking_and_slacking_post='Freaking steak dinner at CC tongiht everyone '
                                                                    'better be there its so goodddddd!!!',
                                food='Steak, Mashed Potatoes, Bread')
    food3 = SnackingAndSlacking(date=d9, snacking_and_slacking_post='Always gotta get froot loops for breakfast '
                                                                    '#everymorning',
                                food='Froot Loop Cereal ')
    food4 = SnackingAndSlacking(date=d10,
                                snacking_and_slacking_post='The subs at terraces are slapping today make sure to get '
                                                           'one',
                                food='Fresh subs')
    db.session.add_all([user, user2, post1, post2, post3, post4, post5, post6, food, food1, food2, food3, food4, event,
                        event2, event3, event4, event5, cc, ter])
    db.session.commit()
    comment1 = Comment(message='This was a really good post.', user_id=user.id, post_id=post6.id)
    comment2 = Comment(message='I dislike this post', user_id=user.id, post_id=post4.id)
    comment3 = Comment(message='This was a really good post. Love to see it', user_id=user2.id, post_id=post2.id)
    comment4 = Comment(message='Hey how are you!!', user_id=user2.id, post_id=post1.id)
    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()
    return render_template('base.html', title='Populated the DataBase with base data')


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
    body = 'Reset the database please log in or register'
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
        user = User(email=form.email.data, username=form.username.data, school_name=form.school_name.data,
                    school_year=form.student_year.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('createAnAccount.html', title='Register', form=form)


@app.route('/events', methods=['GET', 'POST'])
def events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(description=form.description.data,
                      date=form.date.data,
                      day=form.day.data,
                      time=form.time.data)
        db.session.add(event)
        db.session.commit()
        flash('You post an event!')
        return redirect(url_for('events'))
    posts = Event.query.all()
    return render_template('events.html', title='Home', form=form, posts=posts)


@app.route('/Blog', methods=['GET', 'POST'])
def Blog():
    form = PostForm()
    comment = Comment()
    if form.validate_on_submit():
        post = Post(body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('You post your blog on the board!')
        return redirect(url_for('Blog'))
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('Blog.html', title="Share Your Piece", form=form, posts=posts, commentForm=comment,
                           comments=comments)


@app.route('/newSnacking', methods=['GET', 'POST'])
def Snacking():
    form = SnackingSlackingForm()
    form.selectDinning.choices = [(v.id, v.name) for v in DinningHall.query.all()]
    if form.validate_on_submit():
        snacking = SnackingAndSlacking(snacking_and_slacking_post=form.snacking_and_slacking_post.data,
                                       food=form.food.data,
                                       date=form.date.data)
        db.session.add(snacking)
        db.session.commit()
        # Connect Snacking to Dinninghall
        dining = DinningHall.query.filter_by(id=form.selectDinning.data).first()
        db.session.add(dining)
        db.session.commit()
        flash('You posted your review for Snacking and Slacking!')
        return redirect(url_for('Snacking'))
    posts = SnackingAndSlacking.query.all()
    return render_template('SnackingAndSlacking.html', title="Snacking and Slacking", form=form, posts=posts)
