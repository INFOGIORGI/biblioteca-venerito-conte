from flask import Flask, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
import db

app = Flask(__name__)

mysql = MySQL(app)

app.secret_key = "secret key"

@app.route("/")
def home():
    return render_template("index.html", titolo="HOME")

#@app.route("/ricerca/", method = "POST")
#def ricerca():
#    stringa = request.form.get("stringa", "Stringa vuota")
#    return db.ricerca(stringa)

@app.route("/addLibro/", methods = ['GET', 'POST'])
def addLibro():
    if request.method == 'GET':
        return render_template('addLibro.html', titolo = "Aggiungi un Libro")
    
    titolo = request.form.get("titolo", "Stringa vuota")
    isbn = request.form.get("isbn", "Stringa vuota")
    codA = request.form.get("autore", "Stringa vuota")
    categoria = request.form.get("categoria", "Stringa vuota")
    anno = request.form.get("anno", "Stringa vuota")
    nCopie = request.form.get("nCopie", "Stringa vuota")

    autoreConfronta = db.getAutore(codA)
    
    if autoreConfronta == True and (titolo != "Stringa vuota" or isbn != "Stringa vuota" or codA != "Stringa vuota" or categoria != "Stringa vuota" or anno != "Stringa vuota" or nCopie != "Stringa vuota"):
        ritorno=db.addLibro(titolo,isbn,codA,categoria,anno,nCopie)
    else:
        flash('Autore inesistente o campi non compilati')
        return redirect(url_for('addLibro'))
    if ritorno==1:
        flash('libro inserito')
        return redirect(url_for('home'))
    


app.run(debug=True)