import numpy as np
import pandas as pd
import keras
import keras.backend as kb
import tensorflow as tf
from keras.backend import set_session
from keras.models import load_model
# from sklearn.preprocessing import StandardScaler
from pickle import load

saved_model = None
scaler = None

def init_network(weights_file = 'model4.h5', scaler_file = 'scaler.pkl'):
    global saved_model, scaler, graph
    # kb.clear_session()
    # kb.get_session().run(tf.local_variables_initializer())
    saved_model = tf.keras.models.load_model(weights_file)
    # graph = tf.get_default_graph()
    # print(saved_model.summary())
    # saved_model._make_predict_function()
    scaler = load(open(scaler_file, 'rb'))

class neural_network:
    def __init__(self,average_user_rating, average_product_rating,similar_user_rating, local_trust_rating, category_trust_rating, review_feedback_rating):
        
        self.average_user_rating = average_user_rating
        self.average_product_rating = average_product_rating
        self.similar_user_rating = similar_user_rating + average_user_rating
        self.local_trust_rating = local_trust_rating + average_user_rating
        self.category_trust_rating = category_trust_rating + average_user_rating
        self.review_feedback_rating = review_feedback_rating + average_user_rating
        
        self.fill_na_if_some_empty(0)
        
        if np.isnan(self.similar_user_rating):
            self.similar_user_rating = self.average_product_rating
        if np.isnan(self.local_trust_rating):
            self.local_trust_rating = self.average_product_rating
        if np.isnan(self.category_trust_rating):
            self.category_trust_rating = self.average_product_rating
        if np.isnan(self.review_feedback_rating):
            self.review_feedback_rating = self.average_product_rating
        
        query = np.asarray([self.average_user_rating, self.average_product_rating, self.similar_user_rating, self.local_trust_rating, self.category_trust_rating, self.review_feedback_rating])
        print(query)
        query = query.reshape(1,-1)
        self.query = scaler.transform(query)

    def fill_na_if_some_empty(self, value):
        similar_is_null = np.isnan(self.similar_user_rating)
        local_is_null = np.isnan(self.local_trust_rating)
        global_is_null = np.isnan(self.category_trust_rating)
        popular_is_null = np.isnan(self.review_feedback_rating)
        if (similar_is_null and local_is_null and global_is_null) == False:
            if (similar_is_null):
                self.similar_user_rating = value
            if (local_is_null):
                self.local_trust_rating = value
            if (global_is_null):
                self.category_trust_rating = value
            if (popular_is_null):
                self.review_feedback_rating = value

    def predict(self):
        # global graph
        # graph = tf.get_default_graph()
        # with graph.as_default():
        predicted_rating = saved_model.predict(self.query)
        return predicted_rating
    






