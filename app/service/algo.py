
from tkinter import E
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
from functools import lru_cache
from flask import current_app
from scipy.sparse import csr_matrix
from fuzzywuzzy import fuzz
import os
import pickle






class Pipeline():
    def __init__(self,rating,movies):
        self.rating = rating
        self.movies = movies
        self.PT = rating.pivot(index='movie_id', columns='user_id', values='rating').fillna(0)
    
    def apply_knn(self,input):
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        movie_user_mat_sparse = csr_matrix(self.PT.values)
        knn = Knn_Recommender(model_knn, movie_user_mat_sparse,self.movies)
        movie_to_idx = {
                movie: i for i, movie in 
                enumerate(list(self.movies.set_index('movie_id').loc[self.PT.index].title))
            }
        results = knn.make_recommendation(input,movie_to_idx,10)
        return results

    def because_user_liked(self, user):
        movie_idx = [int(k) for k in user.keys()]
        seen_by_user = self.movies.set_index("movie_id").loc[movie_idx]
        return (seen_by_user.reset_index(drop=True))

    def predict_movies(self,input):
        return self.apply_knn(input)

    
        
def fuzzy_matching(mapper, fav_movie, verbose=True):
    """
    return the closest match via fuzzy ratio. If no match found, return None
    
    Parameters
    ----------    
    mapper: dict, map movie title name to index of the movie in data

    fav_movie: str, name of user input movie
    
    verbose: bool, print log if True

    Return
    ------
    index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_movie.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        return
    if verbose:
        return match_tuple[0][1]


class Knn_Recommender():
    def __init__(self,model,data,movies):
        if not os.path.exists("model_pkl"):
            self.model = model
            self.model.fit(data)
            pickle.dump(self.model, open("model_pkl", "wb")) 
        else:
            self.model = pickle.load(open('model_pkl','rb'))
        self.data = data
        self.movies = movies

    def make_recommendation(self,fav_movie, mapper, n_recommendations):
        self.model.fit(self.data)
        title = self.movies.set_index("movie_id").loc[int(fav_movie)].title
        idx = fuzzy_matching(mapper, title, verbose=True)
        distances, indices = self.model.kneighbors(self.data[idx], n_neighbors=n_recommendations+1)
        raw_recommends = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        reverse_mapper = {v: k for k, v in mapper.items()}
        movie_idx = [reverse_mapper[idx] for (idx,distance) in raw_recommends]
        return self.movies.set_index("title").loc[movie_idx,:].reset_index()



