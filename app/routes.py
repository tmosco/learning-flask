from app import app, db
from flask import render_template, flash, redirect, url_for, request
# this is where the function created in form.py is imported
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Feyisayo'}
    posts = [
        {
            'author': {'username': 'Tomi'},
            'body': 'What a lucky guy he is to get her!'
        },
        {
            'author': {'username': 'Feyisayo'},
            'body': 'I thank God for bringing you into my life'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

#i need to create a new page for the user to see



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, str(form.remember_me.data)))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user',username=user.username)
        return redirect(next_page)
        # return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        # print(form.username.data, form.password.data, form.email.data)
        user.set_password(form.password.data)
        print('Congratulations,you are now  a registered user!')
        db.session.add(user)
        db.session.commit()
        flash('Congratulations,you are now  a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/user/<username>')
@login_required  # use this to prevebnt others from entering the site thr the urel
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # check_user = User.query.filter_by(username=form.username.data).first()
        # if check_user:
        #     flash('name already taken')
        #     return redirect(url_for('edit_profile'))
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
