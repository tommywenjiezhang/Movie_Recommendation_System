import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def similarty(train_df):
    similarty = pairwise_distances(train_df, metric='cosine')
    return similarty

def pivot(df):
    train_df = pd.pivot_table(df,index="user_id", columns="movie_id", values="rating", fill_value=0)
    return train_df

class CfRec():
    def __init__(self, M, items, X=None, k=20, top_n=10):
        # similarty
        self.X = X
        # pivot table
        self.M = M
        self.k = k
        self.top_n = top_n
        # movie table
        self.items = items
        print("inside class of CFrec")
    
    def recommend_pearson(self,user_id):
        target = self.M.T[user_id]
        similar_to_target = self.M.T.corrwith(target)
        corr_target = pd.DataFrame(similar_to_target, columns = ['PearsonR'])
        corr_target.dropna(inplace = True)
        corr_target = corr_target.sort_values('PearsonR', ascending = False)
        corr_target.index = corr_target.index.map(int)
        corr_target = corr_target.join(self.items)
        return corr_target.reset_index(drop=True).merge(self.items)
        
    def recommend_user_based(self, user):
        print("inside recommend user")
        ix = self.M.index.get_loc(user)
        # Use it to index the User similarity matrix
        u_sim = self.X[ix]
        # obtain the indices of the top k most similar users
        most_similar = self.M.index[u_sim.argpartition(-(self.k+1))[-(self.k+1):]]
        # Obtain the mean ratings of those users for all movies
        rec_items = self.M.loc[most_similar].mean(0).sort_values(ascending=False)
        # Discard already seen movies
        # already seen movies
        seen_mask = self.M.loc[user].gt(0)
        seen = seen_mask.index[seen_mask].tolist()
        rec_items = rec_items.drop(seen).head(self.top_n)
        # return recommendations - top similar users rated movies
        return (rec_items.index.to_frame()
                                .reset_index(drop=True)
                                .merge(self.items))

    def recommend_item_based(self, item):
        liked = self.items.loc[self.items.movie_id.eq(item), 'title'].item()
        print(f"Because you liked {liked}, we'd recommend you to watch:")
        # get index of movie
        ix = self.M.columns.get_loc(item)
        # Use it to index the Item similarity matrix
        i_sim = self.X[ix]
        # obtain the indices of the top k most similar items
        most_similar = self.M.columns[i_sim.argpartition(-(self.k+1))[-(self.k+1):]]
        return (most_similar.difference([item])
                                 .to_frame()
                                 .reset_index(drop=True)
                                 .merge(self.items)
                                 .head(self.top_n))


def because_user_liked(user_item_m, ratings, user):
    ix_user_seen = user_item_m.loc[user]>0.
    seen_by_user = user_item_m.columns[ix_user_seen]
    return (seen_by_user.to_frame()
                 .reset_index(drop=True)
                 .merge(ratings[ratings.user_id.eq(user)])
                 .sort_values('rating', ascending=False).head(10))