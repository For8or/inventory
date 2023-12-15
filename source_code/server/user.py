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
        logging.warning("User self data: %s", self)
        return self.role == 'admin'

    def first_login_completed(self):
        self.is_first_login = False
        db.update_user_first_login(self.id, self.is_first_login)

    @staticmethod
    def authenticate(username, password):
        user_data = db.read_user(username)
        logging.warning("User data: %s", user_data)
        if user_data and isinstance(user_data, tuple):
            user_details = user_data[0]  # Extract the inner tuple
            user = User(*user_details)
            if user and user.check_password(password):
                return user
        return None

    @staticmethod
    def add_new_user(username, password, role='user'):
        if role not in ['admin', 'user']:
            raise ValueError("Invalid role specified")

        password_hash = generate_password_hash(password)
        
        # Build the data dictionary
        user_data = {
            'username': username,
            'password_hash': password_hash,
            'role': role,
            'is_first_login': True
        }

        # Pass the data dictionary to the insert_user method
        db.insert_user(user_data)
        return user_data

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
            return redirect(url_for('equip.equipment'))
        else:
            flash('Invalid username or password')

    return render_template('user/login.html')

@usr.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    user_id = session['user_id']
    user_data = db.read_user_id(user_id)

    if user_data and isinstance(user_data, tuple):
        user_details = user_data[0]  # Extract the inner tuple
        user = User(*user_details)

        if request.method == 'POST':
            new_password = request.form['new_password']
            user.set_password(new_password)
            db.update_user_password(user_id, user.password_hash)
            user.first_login_completed()
            flash('Password successfully changed.')
            return redirect(url_for('equip.equipment'))

    return render_template('user/changepassword.html')

@usr.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    user_data = db.read_user_id(user_id)
    user_list = db.read_user(None)

    if user_data and isinstance(user_data, tuple):
        user_details = user_data[0]
        user = User(*user_details)

        if request.method == 'POST':
            new_password = request.form['new_password']
            user.set_password(new_password)
            db.update_user_password(user_id, user.password_hash)
            flash('Password successfully updated.')

    return render_template('user/profile.html', user=user_details, data=user_list)

@usr.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    user_id = session['user_id']
    user_data = db.read_user_id(user_id)

    if user_data and isinstance(user_data, tuple):
        user_details = user_data[0]
        user = User(*user_details)

        if request.method == 'POST':
            if user.is_admin():
                username = request.form['username']
                temporary_password = request.form['password']
                role = request.form['role']
                User.add_new_user(username, temporary_password, role)
                flash('New user added successfully.')
                return redirect(url_for('usr.profile'))
            else:
                flash('Only admins can add new users.')

    return render_template('user/adduser.html')

@usr.route('/deleteuser/<int:id>/')
@login_required
def deleteuser(id):
    data = db.read_user_id(id)

    if len(data) == 0:
        return redirect(url_for('usr.profile'))
    else:
        session['deleteuser'] = id
        return render_template('user/deleteuser.html', data = data)

@usr.route('/deleteuser', methods = ['POST'])
@login_required
def deleteuserpost():
    if request.method == 'POST' and request.form['deleteuser']:

        if db.delete_user(session['deleteuser']):
            flash('A user has been deleted')

        else:
            flash('A user can not be deleted')

        session.pop('deleteuser', None)

        return redirect(url_for('usr.profile'))
    else:
        return redirect(url_for('usr.profile'))
