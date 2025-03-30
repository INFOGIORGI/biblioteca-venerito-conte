from flask import Flask, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
import db

app = Flask(__name__)
app.config["MYSQL_HOST"]="138.41.20.102"
app.config["MYSQL_PORT"]=53306
app.config["MYSQL_DB"]="venerito_conte"
app.config["MYSQL_USER"]="5di"
app.config["MYSQL_PASSWORD"]="colazzo"
mysql = MySQL(app)

app.secret_key = "secret key"

@app.route("/")
def home():
    return render_template("index.html", titolo="HOME")

@app.route("/addLibro/", methods = ['GET', 'POST'])
def addLibro():
    if request.method == 'GET':
        return render_template('addLibro.html', titolo = "Aggiungi un Libro")
    
    titolo = request.form.get("titolo", "Stringa vuota")
    isbn = request.form.get("isbn", "Stringa vuota")
    codA = request.form.get("autore", "Stringa vuota")
    categoria = request.form.get("categoria", "Stringa vuota")
    anno = request.form.get("anno", "Stringa vuota")
    nCopie = request.form.get("nCopie", "1")
    riassunto = request.form.get("riassunto", "Riassunto inesistente")

    autoreConfronta = db.getAutore(codA)
    
    if autoreConfronta == True and (isbn != "Stringa vuota" or codA != "Stringa vuota" or categoria != "Stringa vuota" or anno != "Stringa vuota" or nCopie != "Stringa vuota"):
        ritorno=db.addLibro(titolo,isbn,codA,categoria,anno,nCopie, riassunto)
    else:
        flash('Autore inesistente o campi non compilati')
        return redirect(url_for('addLibro'))
    if ritorno==1:
        flash('libro inserito')
        return redirect(url_for('home'))

@app.route("/ricercaLibro/", methods = ['GET', 'POST'])
def ricerca():
    if request.method == 'GET':
        return render_template("ricercaLibro.html", titolo = "Cerca un Libro")
    
    terminiRicerca = request.form.get("terminiRicerca")

    if len(terminiRicerca) != None:
        return db.ricercaLibro(terminiRicerca)

    flash('Inserisci almeno un carattere per la ricerca')
    return redirect(url_for('ricerca'))
    
@app.route('/listaLibri/')
def lista():
    return db.lista()

@app.route('/ordinaPerAutore/')
def ordinaAutore():
    return db.ordinaPerAutore()

@app.route('/ordinaPerTitolo/')
def ordinaTitolo():
    return db.ordinaPerTitolo()

@app.route('/filtraPerGenere/', methods = ["POST"])
def filtraGenere():
    genere = request.form.get("genere")
    return db.filtraGenere(genere)

@app.route('/statisticheGenere/', methods = ["POST"])
def statisticheGenere():
    return db.statisticheGenere()

@app.route("/register/",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html",titolo='registrazione')
    
    nome=request.form.get("nome","")
    cognome=request.form.get("cognome","")
    username=request.form.get("username","")
    password=request.form.get("password","")
    confermapassword=request.form.get("confermapassword","")

    return db.register(nome, cognome, username, password, confermapassword)
    
@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html",titolo='login')
    
    username=request.form.get("username")
    password=request.form.get("password")

    return db.login(username, password)
    

app.run(debug=True)