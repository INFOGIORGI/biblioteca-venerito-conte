from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
import db

app = Flask(__name__)
app.config["MYSQL_HOST"]="138.41.20.102"
app.config["MYSQL_PORT"]=53306
app.config["MYSQL_DB"]="venerito_conte"
app.config["MYSQL_USER"]="5di"
app.config["MYSQL_PASSWORD"]="colazzo"
mysql = MySQL(app)


@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')

<<<<<<< HEAD
@app.route("/user")
def user():
    return

@app.route("/ricerca/", method = "POST")
def ricerca():
    stringa = request.form.get("stringa", "Stringa vuota")
    return db.ricerca(stringa)
=======
@app.route("/user/")
def user():
    return 

@app.route("/ricerca/" methods="POST")
def ricerca():
    return db.ricerca()

>>>>>>> 6173b5e (7)

app.run(debug=True)
