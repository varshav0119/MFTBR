import pandas as pd
import numpy as np

base_sim_path = ""
base_csv_path = ""

review_folded_df = pd.DataFrame()
product_df = pd.DataFrame()
product_folded_df = pd.DataFrame()
category_df = pd.DataFrame()
category_expertise_df = pd.DataFrame()
user_df = pd.DataFrame()
user_folded_df = pd.DataFrame()
idfold = 5

def init_CT_module(fold = 5):

    global idfold
    global review_folded_df
    global product_df
    global product_folded_df
    global category_df
    global category_expertise_df
    global user_df
    global user_folded_df

    idfold = fold
    
    review_folded_df = pd.read_csv(base_csv_path+"reviewfolded.csv")
    review_folded_df = review_folded_df[review_folded_df['idfold']!=idfold]
    
    product_df = pd.read_csv(base_csv_path+"product.csv")
    product_df = product_df.set_index('idproduct')
    
    product_folded_df = pd.read_csv(base_csv_path+"product_folded.csv")
    product_folded_df = product_folded_df.astype({'idproduct':int})
    product_folded_df = product_folded_df.set_index('idproduct')

    category_df = pd.read_csv(base_csv_path+"category.csv")
    category_df = category_df.set_index('idcategory')

    category_expertise_df = pd.read_csv(base_csv_path+"category_expertise.csv")
    category_expertise_df = category_expertise_df.set_index('idcategory')

    user_df = pd.read_csv(base_csv_path+"user.csv")

    user_folded_df = pd.read_csv(base_csv_path+"userfolded.csv")
    user_folded_df = user_folded_df.set_index('iduser')

class category_trust_ratings:
    def __init__(self):
        self.review_df = review_folded_df
        self.idcategory_list = list(category_df.index)
        self.idcategory_dict = {}
        for idc in self.idcategory_list:
            self.idcategory_dict[idc] = self.get_direct_global_trusted_users(idc)
            
    def get_average_rating(self, row):
        #Assuming iduser is valid
        row['average_user_rating'] = float(user_folded_df['f'+str(idfold)+'_train_avg'][row['iduser']])
        return row
    
    def get_direct_global_trusted_users(self,idcategory):
        if(idcategory not in category_expertise_df.index):
            return ([],[],[])
        trusted_users = category_expertise_df.loc[idcategory]
        
        category_leads = trusted_users['category_leads']
        cl = []
        if(type(category_leads) == str):
            cl = category_leads.replace(" ","")
            cl = str(cl[1:-1]).split(",")
            for c in range(len(cl)):
                cl[c] = int(cl[c])

        top_reviewers = trusted_users['top_reviewers']
        tr = []
        if(type(top_reviewers) == str):
            tr = top_reviewers.replace(" ","")
            tr = str(tr[1:-1]).split(",")
            for t in range(len(tr)):
                tr[t] = int(tr[t])

        advisors = trusted_users['advisors']
        ad = []
        if(type(advisors) == str):
            ad = advisors.replace(" ","")
            ad = str(ad[1:-1]).split(",")
            for a in range(len(ad)):
                ad[a] = int(ad[a])
                
        return (cl,tr,ad)
    
    def clean_reviews(self, review_df):
        review_df.sort_values(by = ['iduser','date'], ascending = [True, False], inplace = True)
        review_df.drop_duplicates(subset = ["iduser"], keep = "first", inplace = True)
        return review_df
    
    def get_product_ratings(self, idproduct, is_direct):
        if(idproduct not in product_df.index):
            return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
        idcategory = int(product_df['idcategory'][idproduct])
        if(is_direct == False):
            idcategory = category_df['parent'][idcategory]
            if(np.isnan(idcategory)):
                return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
            else:
                idcategory = int(idcategory)

        cl, tr, ad = self.idcategory_dict[idcategory]

        cl_df = self.review_df[(self.review_df['idproduct'] == idproduct) & (self.review_df['iduser'].isin(cl))][['iduser','rating','review_rating','date']]
        tr_df = self.review_df[(self.review_df['idproduct'] == idproduct) & (self.review_df['iduser'].isin(tr))][['iduser','rating','review_rating','date']]
        ad_df = self.review_df[(self.review_df['idproduct'] == idproduct) & (self.review_df['iduser'].isin(ad))][['iduser','rating','review_rating','date']]

        if(cl_df.empty == False):
            cl_df = cl_df.apply(self.get_average_rating, axis = 1)
        if(tr_df.empty == False):
            tr_df = tr_df.apply(self.get_average_rating, axis = 1)
        if(ad_df.empty == False):
            ad_df = ad_df.apply(self.get_average_rating, axis = 1)

        return (cl_df,tr_df,ad_df)
    
    def get_rating_prediction(self, iduser, idproduct, direct_weight = 0.66, parent_weight = 0.34):
        #Assumes equal weightage for category leads, top reviewers, advisors
        
        self.direct_ratings = self.get_product_ratings(idproduct, True)
        self.parent_ratings = self.get_product_ratings(idproduct, False)
        
        direct_ratings = list(self.direct_ratings)
        parent_ratings = list(self.parent_ratings)
        
        denominator = 0
        direct_sum_all = 0
        parent_sum_all = 0
        mean_direct_rating = 0
        mean_parent_rating = 0
        
        total_direct_ratings = len(direct_ratings[0]) + len(direct_ratings[1]) + len(direct_ratings[2])
        if(total_direct_ratings):
            if(direct_ratings[0].empty == False):
                direct_ratings[0] = self.clean_reviews(direct_ratings[0])
                direct_sum_all = (direct_ratings[0]['rating'] - direct_ratings[0]['average_user_rating']).sum()
            if(direct_ratings[1].empty == False):
                direct_ratings[1] = self.clean_reviews(direct_ratings[1])
                direct_sum_all += (direct_ratings[1]['rating'] - direct_ratings[1]['average_user_rating']).sum()
            if(direct_ratings[2].empty == False):
                direct_ratings[2] = self.clean_reviews(direct_ratings[2])
                direct_sum_all += (direct_ratings[2]['rating'] - direct_ratings[2]['average_user_rating']).sum()

            mean_direct_rating = direct_sum_all/total_direct_ratings
            denominator += direct_weight

        total_parent_ratings = len(parent_ratings[0]) + len(parent_ratings[1]) + len(parent_ratings[2])
        if(total_parent_ratings):
            if(parent_ratings[0].empty == False):
                parent_sum_all = (parent_ratings[0]['rating'] - parent_ratings[0]['average_user_rating']).sum()
            if(parent_ratings[1].empty == False):
                parent_sum_all += (parent_ratings[1]['rating'] - parent_ratings[1]['average_user_rating']).sum()
            if(parent_ratings[2].empty == False):
                parent_sum_all += (parent_ratings[2]['rating'] - parent_ratings[2]['average_user_rating']).sum()
        
            mean_parent_rating = parent_sum_all/total_parent_ratings
            denominator += parent_weight
        
        if(denominator):
            # target_user_average_rating = float(user_folded_df['f'+str(idfold)+'_train_avg'][iduser])
            # return target_user_average_rating + (direct_weight*mean_direct_rating + parent_weight*mean_parent_rating)/denominator
            return (direct_weight*mean_direct_rating + parent_weight*mean_parent_rating)/denominator
        else:
            return np.nan

    def get_expert_rating_df(self):
        expert_df = pd.DataFrame()
        expert_df = expert_df.append(list(self.direct_ratings))
        expert_df = expert_df.append(list(self.parent_ratings))
        return expert_df

# global_trust_instance = global_trust_ratings(train_review_df)

# global_trust_instance.get_rating_prediction(57377)

# global_trust_instance.get_expert_rating_df()

# global_trust_instance.get_rating_prediction(666)

# global_trust_instance.get_expert_rating_df()

