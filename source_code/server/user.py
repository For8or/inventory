from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
from functools import wraps
import logging
db = Database()
usr = Blueprint('usr', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('usr.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

class User:
    def __init__(self, id, username, password_hash, role, is_first_login):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.is_first_login = is_first_login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def first_login_completed(self):
        self.is_first_login = False
        db.update_user_first_login(self.id, self.is_first_login)

    @staticmethod
    def authenticate(username, password):
        user_data = db.read_user(username)
        logging.warning("User: %s",user_data)
        if user_data and isinstance(user_data, tuple):
            user = User(*user_data[0])
            if user and user.check_password(password):
                return user
        return None

    @staticmethod
    def add_new_user(username, password, role='user'):
        if role not in ['admin', 'user']:
            raise ValueError("Invalid role specified")

        password_hash = generate_password_hash(password)
        new_user = User(None, username, password_hash, role, True)
        db.insert_user(new_user)
        return new_user

@usr.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authenticated_user = User.authenticate(username, password)
        
        if authenticated_user:
            session['user_id'] = authenticated_user.id
            if authenticated_user.is_first_login:
                return redirect(url_for('usr.changepassword'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('user/login.html')

@usr.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    
    user_id = session['user_id']
    user_data = db.read_user_id(user_id)

    if user_data and isinstance(user_data, tuple):
        user = User(*user_data[0])

        if request.method == 'POST':
            new_password = request.form['new_password']
            user.set_password(new_password)
            db.update_user_password(user_id, user.password_hash)
            user.first_login_completed()
            flash('Password successfully changed.')
            return redirect(url_for('usr.profile'))

    return render_template('user/changepassword.html')

@usr.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    user = db.read_user_id(user_id)

    if request.method == 'POST' and user and isinstance(user, User):
        new_password = request.form['new_password']
        user.set_password(new_password)
        db.update_user_password(user_id, user.password_hash)
        flash('Password successfully updated.')

    return render_template('user/profile.html', user=user)

@usr.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if not db.read_user_id(session['user_id']).is_admin():
        flash('Only admins can add new users.')
        return redirect(url_for('usr.profile'))

    username = request.form['username']
    temporary_password = request.form['password']
    role = request.form['role']
    User.add_new_user(username, temporary_password, role)
    flash('New user added successfully.')
    return redirect(url_for('usr.profile'))
