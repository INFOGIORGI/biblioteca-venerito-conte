from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

db=Flask(__name__)
db=MySQL(db)

def addLibro():
    return 0