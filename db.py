from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

db=Flask(__name__)
db.config["MYSQL_HOST"]="138.41.20.102"
db.config["MYSQL_PORT"]=53306
db.config["MYSQL_DB"]="venerito_conte"
db.config["MYSQL_USER"]="5di"
db.config["MYSQL_PASSWORD"]="colazzo"
mysql=MySQL(db)

def getAutore(codA):
    cursor=mysql.connection.cursor()
    query="SELECT * FROM Autori WHERE codA=%s"
    cursor.execute(query,(codA,))
    tmp=cursor.fetchall()
    cursor.close()
    if len(tmp)>0:
        return True
    else:
        return False

def addLibro(titolo,isbn,codA,categoria,anno,ncopie):
    cursor=mysql.connection.cursor()
    query="SELECT * FROM Libri WHERE isbn=%s"
    cursor.execute(query,(isbn,))
    tmp=cursor.fetchall()
    cursor.close()
    if len(tmp)==0:
         cursor = mysql.connection.cursor()
         query = "INSERT INTO Libri VALUES(%s,%s,%s,%s,%s,%s)"
         cursor.execute(query, (titolo,isbn, codA,categoria,anno,ncopie))
         mysql.connection.commit()
         cursor.close()
         return 1

    cursor=mysql.connection.cursor()
    query="SELECT Copie FROM Libri WHERE isbn=%s"
    cursor.execute(query,(isbn,))
    copie=cursor.fetchall()
    cursor.close()
    copie=copie+ncopie
    cursor=mysql.connection.cursor()
    query2="ALTER TABLE Libri ALTER COLUMN copie %d"
    cursor.execute(query,(copie,))
    cursor.close()
    return 1



        
    
