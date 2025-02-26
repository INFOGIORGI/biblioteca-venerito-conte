from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

db=Flask(__name__)
db.config["MYSQL_HOST"]="138.41.20.102"
db.config["MYSQL_PORT"]=53306
db.config["MYSQL_DB"]="venerito_conte"
db.config["MYSQL_USER"]="5di"
db.config["MYSQL_PASSWORD"]="colazzo"
mysql=MySQL(db)

def addLibro(titolo,isbn,autore,categoria,anno,ncopie):
    
    cursor=mysql.connection.cursor()
    query="SELECT * FROM Libri WHERE isbn=%s"
    cursor.execute(query,(isbn,))
    tmp=cursor.fetchall()
    cursor.close()
    

    return 0