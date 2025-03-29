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
    tmp=cursor.fetchone()
    cursor.close()
    if tmp!=0:
         cursor = mysql.connection.cursor()
         query = "INSERT INTO Libri (isbn, categoria, titolo, codA, anno, copie) VALUES(%s,%s,%s,%s,%s,%s)"
         cursor.execute(query, (isbn,categoria,titolo,codA,anno,ncopie))
         mysql.connection.commit()
         cursor.close()
         return 1

    cursor=mysql.connection.cursor()
    query="SELECT Copie FROM Libri WHERE isbn=%s"
    cursor.execute(query,(isbn,))
    tmp=cursor.fetchone()
    cursor.close()
    copie = tmp[0]

    copie_attuali=copie+ncopie
    cursor=mysql.connection.cursor()
    query2="UPDATE Libri SET copie %d WHERE isbn=%d"
    cursor.execute(query2,(copie_attuali, isbn))
    mysql.connection.commit()
    cursor.close()
    return 1

def ricercaLibro(terminiRicerca):
    cursor=mysql.connection.cursor()
    query="SELECT * FROM Libri WHERE titolo LIKE %s" #SI PUò FARE ANCHE CATEGORIA
    cursor.execute(query, ("%" + terminiRicerca + "%",))
    risultati = cursor.fetchall()
    cursor.close()

    autoriR={}
    for libro in risultati:
        codA = libro[3]

        cursor=mysql.connection.cursor()
        query="SELECT Nome, Cognome FROM Autori WHERE codA = %s"
        cursor.execute(query, (codA, ))
        autore=cursor.fetchall()
        cursor.close()

        if len(autore)>0:
            autoriR.update({libro[0] : " ".join(autore[0])}) #il dizionario associa l'isbn all'autore, JOIN unisce tutti gli elementi di una tupla in una stringa usando il carattere specificato come separatore
        else:
            autoriR.update({libro[0] : "Sconosciuto"})
    
    return render_template("risultatiRicerca.html", libri=risultati, titolo= "Risultati ricerca", autori=autoriR)

def lista():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri"
    cursor.execute(query,)
    libri = cursor.fetchall()
    cursor.close()

    autoriR={}
    for libro in libri:
        codA = libro[3]

        cursor=mysql.connection.cursor()
        query="SELECT Nome, Cognome FROM Autori WHERE codA = %s"
        cursor.execute(query, (codA, ))
        autore=cursor.fetchall()
        cursor.close()

        if len(autore)>0:
            autoriR.update({libro[0] : " ".join(autore[0])}) #il dizionario associa l'isbn all'autore, JOIN unisce tutti gli elementi di una tupla in una stringa usando il carattere specificato come separatore
        else:
            autoriR.update({libro[0] : "Sconosciuto"})

    return render_template("listaLibri.html", libri=libri, titolo="Tutti i libri", autori=autoriR)

def ordinaPerAutore():
    cursor = mysql.connection.cursor()
    query = """
            SELECT l.isbn, l.categoria, l.titolo, CONCAT(a.nome, ' ', a.cognome), l.anno, l.copie
            FROM Libri AS l
            INNER JOIN Autori AS a on l.codA = a.codA
            ORDER BY a.Nome, a.Cognome
            """
    cursor.execute(query)
    libriOrdinati = cursor.fetchall()
    cursor.close()
    return render_template("libriPerTitolo.html", titolo="Libri Per Autore", libri=libriOrdinati)

def ordinaPerTitolo():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri ORDER BY Titolo"
    cursor.execute(query)
    libriOrdinati = cursor.fetchall()
    cursor.close()

    autoriR={}
    for libro in libriOrdinati:
        codA = libro[3]

        cursor=mysql.connection.cursor()
        query="SELECT Nome, Cognome FROM Autori WHERE codA = %s"
        cursor.execute(query, (codA, ))
        autore=cursor.fetchall()
        cursor.close()

        if len(autore)>0:
            autoriR.update({libro[0] : " ".join(autore[0])}) #il dizionario associa l'isbn all'autore, JOIN unisce tutti gli elementi di una tupla in una stringa usando il carattere specificato come separatore
        else:
            autoriR.update({libro[0] : "Sconosciuto"})

    return render_template("listaLibri.html", titolo = "Libri per titolo", libri = libriOrdinati, autori = autoriR)

def filtraGenere(genere):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri WHERE Categoria = %s"
    cursor.execute(query, (genere,))
    libri=cursor.fetchall()
    cursor.close()


    cursor = mysql.connection.cursor()
    query = "INSERT INTO RicercheCategoria VALUES (%s, 1) ON DUPLICATE KEY UPDATE nRicerche = nRicerche+1"
    cursor.execute(query, (genere,))
    mysql.connection.cursor()
    mysql.connection.commit()
    cursor.close()
        
def statisticheGenere():
    return

    return render_template("libriPerTitolo.html", libri = libri, titolo = "Libri " + genere)
        
    
