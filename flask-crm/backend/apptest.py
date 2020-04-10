import requests
import random
import numpy as np

from custom_modules.utility import init_utility, get_user_list, get_product_list, get_reviewed_combinations

class UnexpectedResponseException(Exception):
    pass

# Test the 'predict' API with various randomly chosen combinations of users and products and check for validity of response
class AppPredictAPITest:

    def __init__(self):
        self.predict_url = "http://localhost:5000/model"
        init_utility()
        self.user_list = get_user_list()
        self.product_list = get_product_list()
        self.reviewed_combinations = get_reviewed_combinations()

    def test_predict_random(self, times):
        for i in range(times):

            iduser = random.choice(self.user_list)
            idproduct = random.choice(self.product_list)
            print("iteration = %s, iduser = %s, idproduct = %s"%(i, iduser, idproduct))

            res = requests.get(self.predict_url, params = {'iduser':str(iduser), 'idproduct':str(idproduct)})
            if res.status_code == 404:
                print(res.text)
            elif res.status_code == 200:
                res_json = res.json()
                if not isinstance(res_json["pred"], float):
                    raise UnexpectedResponseException("pred might have gotten messed up")
                elif res_json["pred"]>5 or res_json["pred"]<0:
                    raise UnexpectedResponseException("pred is in wrong range")
                else:
                    print(res_json)
                    print("All is Well (?)\n")
            else:
                raise UnexpectedResponseException("bad response code")
    
    def test_predict_reviewed_combinations(self, times):
        for i in range(times):
            
            iduser, idproduct = random.choice(self.reviewed_combinations)

            res = requests.get(self.predict_url, params = {'iduser':str(iduser), 'idproduct':str(idproduct)})
            if res.status_code == 404:
                print(res.text)
            elif res.status_code == 200:
                res_json = res.json()
                if not isinstance(res_json["pred"], float):
                    raise UnexpectedResponseException("pred might have gotten messed up")
                elif res_json["pred"]>5 or res_json["pred"]<0:
                    raise UnexpectedResponseException("pred is in wrong range")
                else:
                    print(res_json)
                    print("All is Well (?)\n")
            else:
                raise UnexpectedResponseException("bad response code")



test_client = AppPredictIT()
# test_client.test_predict(1000)
test_client.test_predict_reviewed_combinations(300)
            

