from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL


db = Flask(__name__)

db.config["MYSQL_HOST"]="138.41.20.102"
db.config["MYSQL_PORT"]=53306
db.config["MYSQL_DB"]="venerito_conte"
db.config["MYSQL_USER"]="ospite"
db.config["MYSQL_PASSWORD"]="ospite"

mysql=MySQL(db)








db.run(debug=True)
