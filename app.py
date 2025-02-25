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
    autore = request.form.get("autore", "Stringa vuota")
    categoria = request.form.get("categoria", "Stringa vuota")
    anno = request.form.get("anno", "Stringa vuota")
    nCopie = request.form.get("nCopie", "Stringa vuota")
    
    if len(autore) > 0 and (titolo != "Stringa vuota" or isbn != "Stringa vuota" or autore != "Stringa vuota" or categoria != "Stringa vuota" or anno != "Stringa vuota" or nCopie != "Stringa vuota"):
        return db.addLibro(titolo, isbn, autore, categoria, anno, nCopie)
    else:
        flash('Autore inesistente o campi non compilati')
        return redirect(url_for(home))


app.run(debug=True)