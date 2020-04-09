from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from custom_modules.local_trust import init_LT_module, local_trust_ratings
from custom_modules.category_trust import init_CT_module, category_trust_ratings
from custom_modules.similar_user import init_SU_module, similar_user_ratings
from custom_modules.utility import init_utility, get_actual_rating, get_average_user_rating, get_average_product_rating
import numpy as np

app = Flask(__name__)
CORS(app)

# global set-up
mftbr_db = mysql.connector.connect(host = "localhost", user = "root", database = "mftbr")

init_LT_module()
init_CT_module()
init_SU_module()
init_utility()

category_trust_instance = category_trust_ratings()
similar_user_instance = similar_user_ratings()

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
        iduser = int(request.args.get("iduser"))
        idproduct = int(request.args.get("idproduct"))
        print(iduser, idproduct)

        actual_rating = get_actual_rating(iduser, idproduct)
        average_user_rating = get_average_user_rating(iduser)
        average_product_rating = get_average_product_rating(idproduct)
        print(actual_rating, average_user_rating, average_product_rating)

        if(average_user_rating == np.nan or average_product_rating == np.nan):
            average_user_rating = 3.95
            average_product_rating = 3.95

        local_trust_instance = local_trust_ratings(iduser)
        local_predicted_rating = local_trust_instance.get_rating_prediction(idproduct)
        print("Local:", local_predicted_rating )

        category_predicted_rating = category_trust_instance.get_rating_prediction(iduser,idproduct)
        print("Category:", category_predicted_rating )

        similar_predicted_rating = similar_user_instance.get_rating_prediction(iduser,idproduct)
        print("Similar:", similar_predicted_rating )

        return { "pred": 3.8, "actual": 4 }