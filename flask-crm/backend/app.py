from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np

from custom_modules.similar_user import init_SU_module, similar_user_ratings
from custom_modules.local_trust import init_LT_module, local_trust_ratings
from custom_modules.category_trust import init_CT_module, category_trust_ratings
from custom_modules.review_feedback import init_RF_module, review_feedback_ratings
from custom_modules.utility import init_utility, get_actual_rating, get_average_user_rating, get_average_product_rating
from custom_modules.utility import iduser_is_valid, idproduct_is_valid, get_reviewed_combinations, get_product_list, get_user_list
from custom_modules.neural_network import init_network, neural_network


app = Flask(__name__)
CORS(app)

init_LT_module()
init_CT_module()
init_SU_module()
init_RF_module()
init_utility()
init_network()

category_trust_instance = category_trust_ratings()
similar_user_instance = similar_user_ratings()
review_feedback_instance = review_feedback_ratings()

############ Helper Functions ############

def run_facets(iduser, idproduct):
    actual_rating = float(get_actual_rating(iduser, idproduct))
    average_user_rating = get_average_user_rating(iduser)
    average_product_rating = get_average_product_rating(idproduct)
    print("\n\nFrom dataset:", actual_rating, average_user_rating, average_product_rating)

    if(np.isnan(average_user_rating)):
        average_user_rating = 3.95
    if(np.isnan(average_product_rating)):
        average_product_rating = 3.95

    print("\n\nFrom dataset, after imputing:", actual_rating, average_user_rating, average_product_rating)

    similar_predicted_rating = similar_user_instance.get_rating_prediction(iduser,idproduct)
    print("\n\nSimilar:", similar_predicted_rating, average_user_rating + similar_predicted_rating )
    similar_user_ratings_df = similar_user_instance.get_similar_user_ratings_df()
    print(similar_user_ratings_df)

    local_trust_instance = local_trust_ratings(iduser)
    local_predicted_rating = local_trust_instance.get_rating_prediction(idproduct)
    print("\n\nLocal:", local_predicted_rating, average_user_rating + local_predicted_rating )
    local_trust_ratings_df = local_trust_instance.get_local_trust_rating_df()
    print(local_trust_ratings_df)

    category_predicted_rating = category_trust_instance.get_rating_prediction(iduser,idproduct)
    print("\n\nCategory:", category_predicted_rating, average_user_rating + category_predicted_rating )
    global_category_ratings_df = category_trust_instance.get_expert_rating_df()
    print(global_category_ratings_df)

    review_predicted_rating = review_feedback_instance.get_product_rating(idproduct)
    print("\n\nReview Feedback:", review_predicted_rating, average_user_rating + review_predicted_rating)

    neural_network_instance = neural_network(average_user_rating, average_product_rating, similar_predicted_rating, local_predicted_rating, category_predicted_rating, review_predicted_rating)
    final_predicted_rating = float(neural_network_instance.predict()[0][0])
    print("\n\nFinal:", final_predicted_rating)

    return pack_response(iduser, idproduct, actual_rating, average_user_rating, average_product_rating,
            similar_predicted_rating + average_user_rating, similar_user_ratings_df,
            local_predicted_rating + average_user_rating, local_trust_ratings_df,
            category_predicted_rating + average_user_rating, global_category_ratings_df,
            review_predicted_rating + average_user_rating, final_predicted_rating)

def pack_response(iduser, idproduct, actual_rating, average_user_rating, average_product_rating,
                    similar_predicted_rating, similar_user_ratings_df,
                    local_predicted_rating, local_trust_ratings_df,
                    category_predicted_rating, expert_ratings_df,
                    review_predicted_rating, final_predicted_rating):
    # convert pandas dataframes to dictionaries
    similar_user_ratings_dict = similar_user_ratings_df.to_dict('records')
    local_trust_ratings_dict = local_trust_ratings_df.to_dict('records')
    expert_ratings_dict = expert_ratings_df.to_dict('records')

    res = dict()
    res['iduser'] = str(iduser)
    res['idproduct'] = str(idproduct)
    res['actual'] = str(round(actual_rating, ndigits=2))
    res['average_user_rating'] = str(round(average_user_rating, ndigits=2))
    res['average_product_rating'] = str(round(average_product_rating, ndigits=2))
    res['similar_user_pred'] = str(round(similar_predicted_rating, ndigits=2))
    res['similar_user_ratings'] = similar_user_ratings_dict
    res['local_trust_pred'] = str(round(local_predicted_rating, ndigits=2))
    res['local_trust_ratings'] = local_trust_ratings_dict
    res['global_category_pred'] = str(round(category_predicted_rating, ndigits=2))
    res['global_category_ratings'] = expert_ratings_dict
    res['review_pred'] = str(round(review_predicted_rating, ndigits=2))
    res['pred'] = str(round(final_predicted_rating, ndigits=2))

    print(res)
    return res

    
############ API routes ############

@app.route("/health", methods = ["GET"])
def health():
    return "Welcome to MFTBR! (P.S. This server is running)"

@app.route("/reviewed_combinations", methods = ["GET"])
def reviewed_combinations():
    if request.method == "GET":
        print("\n\nGET for review combinations")
        rc = get_reviewed_combinations()
        rc_transform = []
        for combination in rc:
            rc_transform.append({'iduser': combination[0], 'idproduct': combination[1]})
        return jsonify(rc_transform)

@app.route("/reviewed_combinations/safe", methods = ["GET"])
def reviewed_combinations_safe():
    if request.method == "GET":
        print("\n\nGET for safe review combinations")
        rc = [(467, 834), (277, 50280), (276, 65903), (1265, 1501), (650, 41796), (312, 64230), (2449, 130712)]
        rc_transform = []
        for combination in rc:
            rc_transform.append({'iduser': combination[0], 'idproduct': combination[1]})
        # !!!!!! to replace with the combinations that we want
        rc_transform = rc_transform[:30]
        return jsonify(rc_transform)

@app.route("/users", methods = ["GET"])
def users():
    if request.method == "GET":
        print("\n\nGET for users")
        user_list = get_user_list()
        users_transform = []
        for u in user_list:
            users_transform.append({'iduser': u})
        return jsonify(users_transform)

@app.route("/users_simple_list", methods = ["GET"])
def users_simple_list():
    if request.method == "GET":
        print("\n\nGET for users")
        user_list = get_user_list()
        return {'list': user_list}

@app.route("/products", methods = ["GET"])
def products():
    if request.method == "GET":
        print("\n\nGET for products")
        prod_list = get_product_list()
        prod_transform = []
        for p in prod_list:
            prod_transform.append({'idproduct': p})
        return jsonify(prod_transform)

@app.route("/products_simple_list", methods = ["GET"])
def products_simple_list():
    if request.method == "GET":
        print("\n\nGET for products")
        prod_list = get_product_list()
        return {'list': prod_list}

@app.route("/model/predict", methods = ["GET"])
def predict():
    if request.method == "GET":
        print("\n\n\n\nPredict Called\n")
        iduser = int(request.args.get("iduser"))
        idproduct = int(request.args.get("idproduct"))
        print(iduser, idproduct)

        if(iduser_is_valid(iduser) == False):
            # change to sending error response with appropriate error code
            return Response("Invalid User ID", status = 404)

        if(idproduct_is_valid(idproduct) == False):
            # change to sending error response with appropriate error code
            return Response("Invalid Product ID", status = 404)

        res = run_facets(iduser, idproduct)

        return jsonify(res)