import pandas as pd
import numpy as np

base_sim_path = ""
base_csv_path = ""

review_folded_df = pd.DataFrame()
user_df = pd.DataFrame()
user_folded_df = pd.DataFrame()
similarity_df = pd.DataFrame()
idfold = 5

def init_SU_module(fold = 5):

    global idfold
    global review_folded_df
    global user_df
    global user_folded_df
    global similarity_df

    idfold = fold

    review_folded_df = pd.read_csv(base_csv_path+"reviewfolded.csv")
    review_folded_df = review_folded_df[review_folded_df['idfold']!=idfold]
    
    user_df = pd.read_csv(base_csv_path+"user.csv")

    user_folded_df = pd.read_csv(base_csv_path+"userfolded.csv")
    user_folded_df = user_folded_df.set_index('iduser')

    similarity_df = pd.read_csv(base_sim_path+"fold"+str(idfold)+"_similarity_matrices.csv")

class similar_user_ratings:
    def __init__(self):
        self.user_df = user_folded_df
        self.similarity_df = similarity_df
        self.review_df = review_folded_df
        self.review_df_to_dict()

    def review_df_to_dict(self):
        self.review_df.sort_values(by = ['iduser','idproduct','date'], ascending = [True, True, False], inplace = True)
        self.review_df.drop_duplicates(subset = ["iduser",'idproduct'], keep = "first", inplace = True)
        #self.ratings.set_index(['iduser','idproduct'], inplace = True)
        self.review_dict = self.review_df.set_index(['iduser','idproduct']).T.to_dict('list')
        #self.ratings.set_index(['idreview'],inplace = True)
        
    def print_ratings_dict(self):
        return self.review_dict
        
    def get_rating_prediction(self, iduser, idproduct):
        # Assuming iduser is valid
        meanRatingUser = float(self.user_df['f'+str(idfold)+'_train_avg'][iduser])
        # obtain the similar users for this particular user
        filteredSimilarity = self.similarity_df[self.similarity_df["iduser"] == iduser]
        runningRatingSigma = 0
        # ratingsIncludedCounter = 0
        self.similar_ratings_df = pd.DataFrame()
        denom = 0
        for i in filteredSimilarity.index:
            similarUser = filteredSimilarity.loc[i]["idsimilar"]
            #similarUserRating = self.ratings[(self.ratings["idproduct"]==product) & (self.ratings["iduser"]==similarUser)].reset_index(drop = True)
            if (similarUser, idproduct) in self.review_dict:
                similarUserRating = self.review_dict[(similarUser, idproduct)]
                self.similar_ratings_df = self.similar_ratings_df.append(pd.DataFrame([[int(similarUser)] + similarUserRating]))
            else:
                continue
            # Assuming similarUser is valid            
            meanRatingSimilarUser = float(self.user_df['f'+str(idfold)+'_train_avg'][similarUser])
            s = filteredSimilarity.loc[i]["similarity"]
            denom+=abs(s)
            toAdd = s*(similarUserRating[1] - meanRatingSimilarUser)
            runningRatingSigma+=toAdd
            #print("Similar user: ",similarUser, s, similarUserRating[1], toAdd, runningRatingSigma)
            
        if denom:
            #print(meanRatingUser, runningRatingSigma, ratingsIncludedCounter)
            return runningRatingSigma/denom
            # return meanRatingUser + runningRatingSigma/denom
        else:
#             ratings = self.ratings[(self.ratings["idproduct"] == idproduct)]['rating']
#             if(ratings.empty == False):
#                 return ratings.mean()
#             else:
#                 return np.nan
            return np.nan
    
    def get_similar_user_ratings_df(self):
        if self.similar_ratings_df.empty == True:
            return pd.DataFrame()
        self.similar_ratings_df.columns = ['iduser','idreview','rating','review_rating','date','idfold']
        del self.similar_ratings_df['idfold']
        self.similar_ratings_df = self.similar_ratings_df.set_index(['idreview'])
        return self.similar_ratings_df

# similarity_instance = similar_user_ratings(user_folded_df, review_folded_df, similarity_df)
# #2-3 minutes on local runtime

# similarity_instance.get_rating_prediction(1980,4297)

# similarity_instance.get_similar_user_ratings_df()

# similarity_instance.similar_ratings_df.set_index()

# similarity_instance.review_df

