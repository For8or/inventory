from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
db = Database()
con = Blueprint('con',__name__)
@con.route('/condition/')
def condition():
    data = db.read_condition(None)
    return render_template('condition/condition.html', data = data)

@con.route('/addcondition/')
def addcondition():
    return render_template('condition/addcondition.html')
 
@con.route('/addcondition/', methods = ['POST', 'GET'])
def addconditionpost():
    if request.method == 'POST' and request.form['save']:
        if db.insert_condition(request.form):
            flash("A new condition has been added")
        else:
            flash("A new condition can not be added")

        return redirect(url_for('con.condition'))
    else:
        return redirect(url_for('con.condition'))

@con.route('/updatecondition/<int:id>/')
def updatecondition(id):
    data = db.read_condition(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updatecondition'] = id
        return render_template('condition/updatecondition.html', data = data)

@con.route('/updatecondition', methods = ['POST'])
def updateconditionpost():
    if request.method == 'POST' and request.form['updatecondition']:

        if db.update_condition(session['updatecondition'], request.form):
            flash('A condition has been updated')

        else:
            flash('A condition can not be updated')

        session.pop('updatecondition', None)

        return redirect(url_for('con.condition'))
    else:
        return redirect(url_for('con.condition'))

@con.route('/deletecondition/<int:id>/')
def deletecondition(id):
    data = db.read_condition(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deletecondition'] = id
        return render_template('condition/deletecondition.html', data = data)

@con.route('/deletecondition', methods = ['POST'])
def deleteconditionpost():
    if request.method == 'POST' and request.form['deletecondition']:

        if db.delete_condition(session['deletecondition']):
            flash('A condition has been deleted')

        else:
            flash('A condition can not be deleted')

        session.pop('deletecondition', None)

        return redirect(url_for('con.condition'))
    else:
        return redirect(url_for('con.condition'))