from flask import Flask, render_template, url_for
from db import DB

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')

app.run(debug=True)
