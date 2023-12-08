from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
import logging
db = Database()
equip = Blueprint('equip',__name__)
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('usr.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
@equip.route('/')
@login_required
def equipment():
    data,funding = db.read_equipment(None)
    logging.warning(data)
    return render_template('equipment/equipment.html', data = data)

@equip.route('/addequipment/')
@login_required
def addequipment():
    category = db.read_category(None)
    owner = db.read_owner(None)
    location = db.read_location(None)
    condition = db.read_condition(None)
    grant = db.read_grant(None)
    return render_template('equipment/addequipment.html', category = category, owner = owner, location = location, condition = condition, grant = grant)
 
@equip.route('/addequipment/', methods = ['POST', 'GET'])
@login_required
def addequipmentpost():
    wia = request.form.get("wia")
    category = request.form.get("category")
    cost = request.form.get("cost")
    aquired = request.form.get("aquired")
    description_field = request.form.get("description_field")
    serial_field = request.form.get("serial_field")
    owner_field = request.form.get("owner_field")
    use_field = request.form.get("use_field")
    location_field = request.form.get("location_field")
    condition_field = request.form.get("condition_field")
    inspection = request.form.get("inspection")
    disposition = request.form.get("disposition")
    grant_data = request.form.getlist("grant[]")
    notes = request.form.get("notes")
    save = request.form.get("save")
    if request.method == 'POST' and save:
        if db.insert_equipment(wia,category,cost,aquired,description_field,serial_field,owner_field,use_field,location_field,condition_field,inspection,disposition,grant_data,notes):
            flash("A new equipment has been added")
        else:
            flash("A new equipment can not be added")

        return redirect(url_for('equip.equipment'))
    else:
        return redirect(url_for('equip.equipment'))

@equip.route('/updateequipment/<int:id>/')
@login_required
def updateequipment(id):
    data,funding = db.read_equipment(id)

    if len(data) == 0:
        return redirect(url_for('equip.equipment'))
    else:
        session['updateequipment'] = id
        length_funding = len(funding)
        category = db.read_category(None)
        owner = db.read_owner(None)
        location = db.read_location(None)
        condition = db.read_condition(None)
        grant = db.read_grant(None)
        return render_template('equipment/updateequipment.html', data=data, funding=funding, length_funding=length_funding,category = category, owner = owner, location = location, condition = condition, grant = grant)

@equip.route('/updateequipment', methods = ['POST'])
@login_required
def updateequipmentpost():
    if request.method == 'POST' and request.form['updateequipment']:
        wia = request.form.get("wia")
        category = request.form.get("category")
        cost = request.form.get("cost")
        aquired = request.form.get("aquired")
        description_field = request.form.get("description_field")
        serial_field = request.form.get("serial_field")
        owner_field = request.form.get("owner_field")
        use_field = request.form.get("use_field")
        location_field = request.form.get("location_field")
        condition_field = request.form.get("condition_field")
        inspection = request.form.get("inspection")
        disposition = request.form.get("disposition")
        grant_data = request.form.getlist("grant[]")
        notes = request.form.get("notes")
        logging.warning("wia = %s", wia)
        logging.warning("category = %s", category)
        logging.warning("cost = %s", cost)
        logging.warning("aquired = %s", aquired)
        logging.warning("description_field = %s", description_field)
        logging.warning("serial_field = %s", serial_field)
        logging.warning("owner_field = %s", owner_field)
        logging.warning("use_field = %s", use_field)
        logging.warning("location_field = %s", location_field)
        logging.warning("condition_field = %s", condition_field)
        logging.warning("inspection = %s", inspection)
        logging.warning("disposition = %s", disposition)
        logging.warning("grant_data = %s", grant_data)
        logging.warning("notes = %s", notes)
        logging.warning("id = %s", session['updateequipment'])
        if db.update_equipment(wia = wia,category = category,cost = cost,aquired = aquired,description_field = description_field,serial_field = serial_field,owner_field = owner_field,use_field = use_field,location_field = location_field,condition_field = condition_field,inspection = inspection,disposition = disposition,grant_data = grant_data,notes = notes, id =  session['updateequipment']):
            flash('A equipment has been updated')

        else:
            flash('A equipment can not be updated')

        session.pop('updateequipment', None)

        return redirect(url_for('equip.equipment'))
    else:
        return redirect(url_for('equip.equipment'))

@equip.route('/viewequipment/<int:id>/')
@login_required
def viewequipment(id):
    data,funding = db.read_equipment(id)
    logging.warning(data)
    logging.warning(funding)
    if len(data) == 0:
        return redirect(url_for('equip.equipment'))
    else:
        session['deleteequipment'] = id
    length_funding = len(funding)
    return render_template('equipment/viewequipment.html', data=data, funding=funding, length_funding=length_funding)
@equip.route('/deleteequipment/<int:id>/')
@login_required
def deleteequipment(id):
    data,funding = db.read_equipment(id)
    logging.warning(data)
    logging.warning(funding)
    if len(data) == 0:
        return redirect(url_for('equip.equipment'))
    else:
        session['deleteequipment'] = id
    length_funding = len(funding)
    return render_template('equipment/deleteequipment.html', data=data, funding=funding, length_funding=length_funding)
@equip.route('/deleteequipment', methods = ['POST'])
@login_required
def deleteequipmentpost():
    if request.method == 'POST' and request.form['deleteequipment']:

        if db.delete_equipment(session['deleteequipment']):
            flash('A equipment has been deleted')

        else:
            flash('A equipment can not be deleted')

        session.pop('deleteequipment', None)

        return redirect(url_for('equip.equipment'))
    else:
        return redirect(url_for('equip.equipment'))