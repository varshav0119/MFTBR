import pandas as pd
import numpy as np

base_sim_path = ""
base_csv_path = ""

review_feedback_df = pd.DataFrame()

def init_RF_module():
    global review_feedback_df
    review_feedback_df = pd.read_csv(base_csv_path+"review_feedback_df.csv")
    review_feedback_df = review_feedback_df.set_index('idproduct')
    
class review_feedback_ratings:
    def get_product_rating(self, idproduct):
        if(idproduct not in review_feedback_df.index):
            return np.nan
        else:
            return review_feedback_df.loc[idproduct]['review_feedback_rating']
