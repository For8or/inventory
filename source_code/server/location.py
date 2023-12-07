from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
db = Database()
loc = Blueprint('loc',__name__)
@loc.route('/location/')
def location():
    data = db.read_location(None)
    return render_template('location/location.html', data = data)

@loc.route('/addlocation/')
def addlocation():
    return render_template('location/addlocation.html')
 
@loc.route('/addlocation/', methods = ['POST', 'GET'])
def addlocationpost():
    if request.method == 'POST' and request.form['save']:
        if db.insert_location(request.form):
            flash("A new location has been added")
        else:
            flash("A new location can not be added")

        return redirect(url_for('loc.location'))
    else:
        return redirect(url_for('loc.location'))

@loc.route('/updatelocation/<int:id>/')
def updatelocation(id):
    data = db.read_location(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updatelocation'] = id
        return render_template('location/updatelocation.html', data = data)

@loc.route('/updatelocation', methods = ['POST'])
def updatelocationpost():
    if request.method == 'POST' and request.form['updatelocation']:

        if db.update_location(session['updatelocation'], request.form):
            flash('A location has been updated')

        else:
            flash('A location can not be updated')

        session.pop('updatelocation', None)

        return redirect(url_for('loc.location'))
    else:
        return redirect(url_for('loc.location'))

@loc.route('/deletelocation/<int:id>/')
def deletelocation(id):
    data = db.read_location(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deletelocation'] = id
        return render_template('location/deletelocation.html', data = data)

@loc.route('/deletelocation', methods = ['POST'])
def deletelocationpost():
    if request.method == 'POST' and request.form['deletelocation']:

        if db.delete_location(session['deletelocation']):
            flash('A location has been deleted')

        else:
            flash('A location can not be deleted')

        session.pop('deletelocation', None)

        return redirect(url_for('loc.location'))
    else:
        return redirect(url_for('loc.location'))