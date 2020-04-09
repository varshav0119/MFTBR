from flask import Flask, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# global set-up
mftbr_db = mysql.connector.connect(host = "localhost", user = "root", database = "mftbr")


@app.route("/health", methods = ["GET"])
def health():
    return "Welcome to Living Hell! (P.S. At the very least, this server is running)"


@app.route("/tables")
def tables():
    cursor = mftbr_db.cursor()
    print(cursor)
    cursor.execute("show tables")
    res = cursor.fetchall()
    return res.__str__()

@app.route("/user", methods = ["GET"])
def user():
    if request.method == "GET":
        # cursor = mftbr_db.cursor()
        # cursor.execute("select iduser from user")
        # res = cursor.fetchall()
        # print(res)
        return "user GET"

@app.route("/model", methods = ["GET"])
def model():
    if request.method == "GET":
        print("called")
        iduser = request.args.get("iduser")
        idproduct = request.args.get("idproduct")
        print(iduser, idproduct)
        return { "pred": 3.8, "actual": 4 }