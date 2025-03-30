from flask import Flask, render_template, url_for, flash, redirect, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

db=Flask(__name__)
db.secret_key = "MY_SECRET_KEY"

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

def addLibro(titolo,isbn,codA,categoria,anno,ncopie, riassunto):
    cursor=mysql.connection.cursor()
    query="SELECT * FROM Libri WHERE isbn=%s"
    cursor.execute(query,(isbn,))
    tmp=cursor.fetchone()
    cursor.close()
    
    cursor = mysql.connection.cursor()
    query = "INSERT INTO Libri (isbn, categoria, titolo, codA, anno, copie, riassunto) VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE copie = copie+%s" #inserisce il libro se questo non esiste altrimenti aggiorna le copie
    cursor.execute(query, (isbn,categoria,titolo,codA,anno,ncopie,riassunto, ncopie))
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
    mysql.connection.commit()
    cursor.close()

    return render_template("libriPerTitolo.html", libri = libri, titolo = "Libri " + genere)

        
def statisticheGenere():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM RicercheCategoria"
    cursor.execute(query)
    risultati = cursor.fetchall()
    cursor.close()
    return render_template("statistiche.html", titolo = "Statistiche sulle ricerche", statistiche = risultati)

def register(nome, cognome, username, password, confermapassword, email):
    if (nome=="" or cognome=="" or username=="" or password=="" or confermapassword==""):
        flash("Compila tutti i campi prima di continuare")
        return redirect(url_for('register'))
    
    if confermapassword != password:
        flash("le password non corrispondono")
        return redirect(url_for('register'))
    
    cursor=mysql.connection.cursor()
    query_select="SELECT * FROM Utenti WHERE username=%s"
    cursor.execute(query_select,(username,))
    tmp=cursor.fetchall()
    if len(tmp)>0:
        flash("utente già esistente")
        return redirect(url_for('register'))

    query="INSERT INTO Utenti VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,nome,cognome,email,generate_password_hash(password)))
    mysql.connection.commit()
    cursor.close()
    flash("utente registrato correttamente")
    return redirect(url_for('register'))
    
def login(username, password):
    cursor=mysql.connection.cursor()
    query="SELECT password FROM Utenti WHERE username=%s"
    cursor.execute(query,(username,))
    tmp=cursor.fetchall()
    cursor.close()

    if len(tmp)==0:
        flash("utente o password errata")
        return redirect(url_for('login'))
    
    passwordconfronta=tmp[0][0]
    if check_password_hash(passwordconfronta,password)==True:
        session['user_id'] = username
        session['greet'] = f"Login effettuato con successo - {session['user_id']}."
        if username == "admin":
            return redirect(url_for("sessionAdmin"))
        return redirect(url_for("session"))

    flash("errore")
    return redirect(url_for('login'))
    
def logout():
    session.pop('user_id')
    session['notify'] = "Logout effettuato con successo"
    return redirect(url_for("home"))

def prestito(titolo, dataFine):
    if dataFine < datetime.now():
        flash("Inserisci una data valida")
        return redirect(url_for('prestito'))
    
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri WHERE titolo = %s"
    cursor.execute(query, (titolo,))
    libro = cursor.fetchone()
    cursor.close

    username = session.get('user_id')
    if 'user_id' not in session:
        flash("Devi effettuare il login per richiedere un prestito")
        return redirect(url_for('login'))
    
    if len(libro) > 0:
        data_inizio = datetime.now().strftime('%Y-%m-%d ')
        data_fine = dataFine.strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor()
        query = "INSERT INTO Prestiti VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (username, libro[0], data_inizio, data_fine))
        mysql.connection.commit()
        cursor.close()

        flash("Prestito inserito correttamente")
        return redirect(url_for('session'))
    
    flash("Libro non disponibile")
    return redirect(url_for('session'))
    
