from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from models import db, User, Reservation

auth = Blueprint('auth', __name__)

def redirect_dest(fallback):
    dest = request.args.get('next')
    if dest:
        redirect(dest)
    else:
        redirect(fallback)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists', 'error')
        return redirect(url_for("auth.signup"))

    new_user = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256')) # type: ignore
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f"Sign Up successful! Welcome {new_user.name}. Please log in to continue.", "success")
        return redirect(url_for("main.index"))
    except Exception as e:
        print(e)
        return "Issue signing up"

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect('/login') # if the user doesn't exist or password is wrong, reload the page

    # user has the right credentials
    login_user(user, remember=remember)
    flash(f"Login Successful! Welcome back {user.name}","success")
    return redirect(url_for("main.index"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))