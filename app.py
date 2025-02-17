from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
import db

app = Flask(__name__)
app.config["MYSQL_HOST"]="138.41.20.102"
app.config["MYSQL_PORT"]=53306
app.config["MYSQL_DB"]="venerito_conte"
app.config["MYSQL_USER"]="ospite"
app.config["MYSQL_PASSWORD"]="ospite"
mysql = MySQL(app)


@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')

@app.route("/user")
def user():
    return

app.run(debug=True)
