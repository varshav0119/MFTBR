from flask import Flask, request
from flask_cors import CORS

import mysql.connector

import numpy as np

from custom_modules.similar_user import init_SU_module, similar_user_ratings
from custom_modules.local_trust import init_LT_module, local_trust_ratings
from custom_modules.category_trust import init_CT_module, category_trust_ratings
from custom_modules.review_feedback import init_RF_module, review_feedback_ratings

from custom_modules.utility import init_utility, get_actual_rating, get_average_user_rating, get_average_product_rating, iduser_is_valid, idproduct_is_valid
from custom_modules.neural_network import init_network, neural_network


app = Flask(__name__)
CORS(app)

# global set-up
# mftbr_db = mysql.connector.connect(host = "localhost", user = "root", database = "mftbr")

init_LT_module()
init_CT_module()
init_SU_module()
init_RF_module()
init_utility()
init_network()

category_trust_instance = category_trust_ratings()
similar_user_instance = similar_user_ratings()
review_feedback_instance = review_feedback_ratings()


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
        print("\n\n\n\ncalled\n")
        iduser = int(request.args.get("iduser"))
        idproduct = int(request.args.get("idproduct"))
        print(iduser, idproduct)

        if(iduser_is_valid(iduser) == False):
            # change to sending error response with appropriate error code
            return { "Error: Invalid User ID" }

        if(idproduct_is_valid(idproduct) == False):
            # change to sending error response with appropriate error code
            return { "Error: Invalid Product ID" }

        actual_rating = get_actual_rating(iduser, idproduct)
        average_user_rating = get_average_user_rating(iduser)
        average_product_rating = get_average_product_rating(idproduct)
        print("\n\n", actual_rating, average_user_rating, average_product_rating)

        if(average_user_rating == np.nan):
            average_user_rating = 3.95
        if(average_product_rating == np.nan):
            average_product_rating = 3.95

        similar_predicted_rating = similar_user_instance.get_rating_prediction(iduser,idproduct)
        print("\n\nSimilar:", similar_predicted_rating, average_user_rating + similar_predicted_rating )
        print(similar_user_instance.get_similar_user_ratings_df())

        local_trust_instance = local_trust_ratings(iduser)
        local_predicted_rating = local_trust_instance.get_rating_prediction(idproduct)
        print("\n\nLocal:", local_predicted_rating, average_user_rating + local_predicted_rating )
        print(local_trust_instance.get_local_trust_rating_df())

        category_predicted_rating = category_trust_instance.get_rating_prediction(iduser,idproduct)
        print("\n\nCategory:", category_predicted_rating, average_user_rating + category_predicted_rating )
        print(category_trust_instance.get_expert_rating_df())

        review_predicted_rating = review_feedback_instance.get_product_rating(idproduct)
        print("\n\nReview Feedback:", review_predicted_rating, average_user_rating + review_predicted_rating)
        # review_predicted_rating = -0.0777799133333333

        neural_network_instance = neural_network(average_user_rating, average_product_rating, similar_predicted_rating, local_predicted_rating, category_predicted_rating, review_predicted_rating)
        # neural_network_instance = neural_network(3.5910625, 4, 0.4145682102077913, 0.008330130000000047, 0.8109773000000002, -0.0777799133333333)
        final_predicted_rating = float(neural_network_instance.predict()[0][0])
        print("\n\nFinal:", final_predicted_rating)

        return { "pred": final_predicted_rating , "actual": 4 }
        # return { "pred": 0 , "actual": 0 }