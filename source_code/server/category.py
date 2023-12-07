from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
db = Database()
cat = Blueprint('cat',__name__)
@cat.route('/category/')
def category():
    data = db.read_category(None)
    return render_template('category/category.html', data = data)

@cat.route('/addcategory/')
def addcategory():
    return render_template('category/addcategory.html')
 
@cat.route('/addcategory/', methods = ['POST', 'GET'])
def addcategorypost():
    if request.method == 'POST' and request.form['save']:
        if db.insert_category(request.form):
            flash("A new category has been added")
        else:
            flash("A new category can not be added")

        return redirect(url_for('cat.category'))
    else:
        return redirect(url_for('cat.category'))

@cat.route('/updatecategory/<int:id>/')
def updatecategory(id):
    data = db.read_category(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['updatecategory'] = id
        return render_template('category/updatecategory.html', data = data)

@cat.route('/updatecategory', methods = ['POST'])
def updatecategorypost():
    if request.method == 'POST' and request.form['updatecategory']:

        if db.update_category(session['updatecategory'], request.form):
            flash('A category has been updated')

        else:
            flash('A category can not be updated')

        session.pop('updatecategory', None)

        return redirect(url_for('cat.category'))
    else:
        return redirect(url_for('cat.category'))

@cat.route('/deletecategory/<int:id>/')
def deletecategory(id):
    data = db.read_category(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deletecategory'] = id
        return render_template('category/deletecategory.html', data = data)

@cat.route('/deletecategory', methods = ['POST'])
def deletecategorypost():
    if request.method == 'POST' and request.form['deletecategory']:

        if db.delete_category(session['deletecategory']):
            flash('A category has been deleted')

        else:
            flash('A category can not be deleted')

        session.pop('deletecategory', None)

        return redirect(url_for('cat.category'))
    else:
        return redirect(url_for('cat.category'))