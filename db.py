from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

db=Flask(__name__)

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
         query = "INSERT INTO Libri (isbn, categoria, titolo, codA, anno, copie) VALUES(%s,%s,%s,%s,%s,%s)"
         cursor.execute(query, (isbn,categoria,titolo,codA,anno,ncopie))
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
    cursor.execute(query2,(copie,))
    cursor.close()
    return 1



        
    
