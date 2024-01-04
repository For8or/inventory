from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
from server.category import cat
from server.condition import con
from server.grant import gran
from server.location import loc
from server.owner import own
from server.equipment import equip
from server.user import usr
app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()
from functools import wraps
from flask import session, redirect, url_for

app.register_blueprint(cat)
app.register_blueprint(con)
app.register_blueprint(gran)
app.register_blueprint(loc)
app.register_blueprint(own)
app.register_blueprint(equip)
app.register_blueprint(usr)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
    #Add print list option(csv)(ROUTE IS MISSING)
    
