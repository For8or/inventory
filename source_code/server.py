from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint
from controller.database import Database
from server.category import cat
from server.condition import con
from server.grant import gran
from server.location import loc
from server.owner import own
from server.equipment import equip
app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

app.register_blueprint(cat)
app.register_blueprint(con)
app.register_blueprint(gran)
app.register_blueprint(loc)
app.register_blueprint(own)
app.register_blueprint(equip)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001, host="0.0.0.0")