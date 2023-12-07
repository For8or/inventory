from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
db = Database()
own = Blueprint('own',__name__)
@own.route('/owner/')
def owner():
    data = db.read_owner(None)
    return render_template('owner/owner.html', data = data)

@own.route('/addowner/')
def addowner():
    return render_template('owner/addowner.html')
 
@own.route('/addowner/', methods = ['POST', 'GET'])
def addownerpost():
    if request.method == 'POST' and request.form['save']:
        if db.insert_owner(request.form):
            flash("A new owner has been added")
        else:
            flash("A new owner can not be added")

        return redirect(url_for('own.owner'))
    else:
        return redirect(url_for('own.owner'))

@own.route('/updateowner/<int:id>/')
def updateowner(id):
    data = db.read_owner(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updateowner'] = id
        return render_template('owner/updateowner.html', data = data)

@own.route('/updateowner', methods = ['POST'])
def updateownerpost():
    if request.method == 'POST' and request.form['updateowner']:

        if db.update_owner(session['updateowner'], request.form):
            flash('A owner has been updated')

        else:
            flash('A owner can not be updated')

        session.pop('updateowner', None)

        return redirect(url_for('own.owner'))
    else:
        return redirect(url_for('own.owner'))

@own.route('/deleteowner/<int:id>/')
def deleteowner(id):
    data = db.read_owner(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deleteowner'] = id
        return render_template('owner/deleteowner.html', data = data)

@own.route('/deleteowner', methods = ['POST'])
def deleteownerpost():
    if request.method == 'POST' and request.form['deleteowner']:

        if db.delete_owner(session['deleteowner']):
            flash('A owner has been deleted')

        else:
            flash('A owner can not be deleted')

        session.pop('deleteowner', None)

        return redirect(url_for('own.owner'))
    else:
        return redirect(url_for('own.owner'))