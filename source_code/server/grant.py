from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
import logging
db = Database()
gran = Blueprint('gran',__name__)
@gran.route('/grant/')
def grant():
    data = db.read_grant(None)
    return render_template('grant/grant.html', data = data)

@gran.route('/addgrant/')
def addgrant():
    return render_template('grant/addgrant.html')
 
@gran.route('/addgrant/', methods = ['POST', 'GET'])
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
def updategrant(id):
    data = db.read_grant(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updategrant'] = id
        return render_template('grant/updategrant.html', data = data)

@gran.route('/updategrant', methods = ['POST'])
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
def deletegrant(id):
    data = db.read_grant(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deletegrant'] = id
        return render_template('grant/deletegrant.html', data = data)

@gran.route('/deletegrant', methods = ['POST'])
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