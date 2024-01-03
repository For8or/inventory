from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint, Response
from controller.database import Database
from io import StringIO
import csv
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
    grant = request.form.getlist("grant[]")
    notes = request.form.get("notes")
    save = request.form.get("save")
    percent = request.form.getlist("percent[]")

    # Debugging: Print or log the percentages
    logging.warning("Percentages: %s", percent)
    if request.method == 'POST' and save:
        if db.insert_equipment(wia=wia,category=category,cost=cost,aquired=aquired,description_field=description_field,serial_field=serial_field,owner_field=owner_field,use_field=use_field,location_field=location_field,condition_field=condition_field,inspection=inspection,disposition=disposition,grant=grant,percent=percent,notes=notes):
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
        grant = request.form.getlist("grant[]")
        notes = request.form.get("notes")
        percent = request.form.getlist("percent[]")

        # Debugging: Print or log the percentages
        logging.warning("Percentages: %s", percent)
        
        
        if db.update_equipment(wia = wia,category = category,cost = cost,aquired = aquired,description_field = description_field,serial_field = serial_field,owner_field = owner_field,use_field = use_field,location_field = location_field,condition_field = condition_field,inspection = inspection,disposition = disposition,grant = grant,percent=percent,notes = notes, id =  session['updateequipment']):
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

@equip.route('/download-equipment-csv')
@login_required
def download_equipment_csv():
    # Assuming db.get_equipment_data_with_funding() returns a list of equipment items
    # Each item should be a dictionary or object with the fields mentioned in the headers
    def generate():
        data = StringIO()
        writer = csv.writer(data)

        # Write the headers
        writer.writerow(['ID', 'WIA', 'Category', 'Cost', 'Acquired', 'Description', 'Serial', 'Owner', 'Use', 'Location', 'Condition', 'Inspection', 'Disposition', 'Notes', 'Funding Names'])

        # Fetch the equipment data
        equipment_data = db.get_equipment_data_with_funding()

        # Iterate over each equipment item and write it to the CSV
        for item in equipment_data:
            writer.writerow([
                item[0],  # ID
                item[1],  # WIA
                item[2],  # Category
                item[3],  # Cost
                item[4],  # Acquired
                item[5],  # Description
                item[6],  # Serial
                item[7],  # Owner
                item[8],  # Use
                item[9],  # Location
                item[10], # Condition
                item[11], # Inspection
                item[12], # Disposition
                item[13], # Notes
                item[14]  # Funding Names
            ])

        data.seek(0)
        yield data.read()
    response = Response(generate(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='equipment.csv')
    return response
