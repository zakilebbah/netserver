from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User
from app import db

authmain = Blueprint('authmain', __name__)

# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

@authmain.route('/')
def index():
    return render_template('index.html')

@authmain.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.emailnet)


@authmain.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        #
        if db.session.query(User).filter_by(emailnet=email).first() is not None:
            return render_template('signup.html')
            # return redirect(url_for('authmain.signup'))
        user = User()
        user.usernamenet = username
        user.emailnet = email
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    else:
        return render_template('signup.html')

@authmain.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = db.session.query(User).filter_by(emailnet=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not user.verify_password(password):
            flash('Please check your login details and try again.')
            return render_template('profile.html') # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return render_template('profile.html')
    else:
        return render_template('login.html')


# @app.route('/signup', methods=['POST'])
# def signup_post():
#     # code to validate and add user to database goes here
#     return redirect(url_for('login'))


@authmain.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')



