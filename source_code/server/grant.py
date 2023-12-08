from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
import logging
db = Database()
gran = Blueprint('gran',__name__)
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('usr.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
@gran.route('/grant/')
@login_required
def grant():
    data = db.read_grant(None)
    return render_template('grant/grant.html', data = data)

@gran.route('/addgrant/')
@login_required
def addgrant():
    return render_template('grant/addgrant.html')
 
@gran.route('/addgrant/', methods = ['POST', 'GET'])
@login_required
def addgrantpost():
    if request.method == 'POST' and request.form['save']:
        logging.warning(request.form)
        if db.insert_grant(request.form):
            flash("A new grant has been added")
        else:
            flash("A new grant can not be added")

        return redirect(url_for('gran.grant'))
    else:
        return redirect(url_for('gran.grant'))

@gran.route('/updategrant/<int:id>/')
@login_required
def updategrant(id):
    data = db.read_grant(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updategrant'] = id
        return render_template('grant/updategrant.html', data = data)

@gran.route('/updategrant', methods = ['POST'])
@login_required
def updategrantpost():
    if request.method == 'POST' and request.form['updategrant']:

        if db.update_grant(session['updategrant'], request.form):
            flash('A grant has been updated')

        else:
            flash('A grant can not be updated')

        session.pop('updategrant', None)

        return redirect(url_for('gran.grant'))
    else:
        return redirect(url_for('gran.grant'))

@gran.route('/deletegrant/<int:id>/')
@login_required
def deletegrant(id):
    data = db.read_grant(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deletegrant'] = id
        return render_template('grant/deletegrant.html', data = data)

@gran.route('/deletegrant', methods = ['POST'])
@login_required
def deletegrantpost():
    if request.method == 'POST' and request.form['deletegrant']:

        if db.delete_grant(session['deletegrant']):
            flash('A grant has been deleted')

        else:
            flash('A grant can not be deleted')

        session.pop('deletegrant', None)

        return redirect(url_for('gran.grant'))
    else:
        return redirect(url_for('gran.grant'))