import pandas as pd
import numpy as np

base_sim_path = ""
base_csv_path = ""

user_folded_df = pd.DataFrame()
product_folded_df = pd.DataFrame()
review_folded_df = pd.DataFrame()

def clean_reviews(review_df):
    review_df.sort_values(by = ['iduser','idproduct','date'], ascending = [True, True, False], inplace = True)
    review_df.drop_duplicates(subset = ['iduser', 'idproduct'], keep = "first", inplace = True)
    return review_df

def init_utility(fold = 5):
    global idfold
    global review_folded_df
    global product_folded_df
    global user_folded_df

    idfold = fold

    review_folded_df = pd.read_csv(base_csv_path+"reviewfolded.csv")
    review_folded_df = review_folded_df[review_folded_df['idfold']!=idfold]
    review_folded_df = clean_reviews(review_folded_df)
    
    product_folded_df = pd.read_csv(base_csv_path+"product_folded.csv")
    product_folded_df = product_folded_df.astype({'idproduct':int})
    product_folded_df = product_folded_df.set_index('idproduct')

    user_folded_df = pd.read_csv(base_csv_path+"userfolded.csv")
    user_folded_df = user_folded_df.set_index('iduser')

def get_actual_rating(iduser,idproduct):
    filtered_df = review_folded_df[(review_folded_df['iduser']==iduser) & (review_folded_df['idproduct']==idproduct)]['rating']
    print(filtered_df)
    if(filtered_df.empty == False):
        return int(filtered_df['rating'])
    return np.nan

def get_average_user_rating(iduser):
    return float(user_folded_df['f'+str(idfold)+'_train_avg'][iduser])


def get_average_product_rating(idproduct):
    return float(product_folded_df['fold'+str(idfold)+'_average_rating'][idproduct])
