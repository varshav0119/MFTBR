from flask import Flask
import mysql.connector

app = Flask(__name__)

# global set-up
mftbr_db = mysql.connector.connect(host = "localhost", user = "root", database = "mftbr")


@app.route("/")
def index():
    return "Welcome to Living Hell :)"


@app.route("/tables")
def tables():
    cursor = mftbr_db.cursor()
    print(cursor)
    cursor.execute("show tables")
    res = cursor.fetchall()
    return res.__str__()