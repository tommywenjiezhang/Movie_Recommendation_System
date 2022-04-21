from flask import render_template, request, redirect, url_for, session, current_app
from app.models import Moviedb, create_rating,get_popular_movie, getMovies
import pandas as pd
from app.service.MovieApi import Movie_api
import re
import os
import json
import random
import pickle
import traceback
from app.service.algo import Pipeline

""" 
Generate the login form (using flask) for the index.html page, where you will 
enter a new user. The form itself is created in forms.py. 
The index() route method is called from app.py
"""


def index():
    if request.method == 'POST':
        current_app.logger.debug("POST Method")
        user_review = process_movie(request.form.to_dict())
        session["user_id"] = random.randint(1000, 2000)
        entries = []
        for entry in user_review.keys():
            entries.append({"user_id": session["user_id"], "movie_id": int(entry), "rating": float(user_review[entry])})
        input_movie = max(user_review.items(), key = lambda k : k[1])
        input_movie_name = input_movie[1]
        mdb = Moviedb()
        rating = mdb.get_rating()
        movies = mdb.get_movies()
        pipe = Pipeline(rating,movies)
        user_liked = pipe.because_user_liked(user_review)
        recommended = pipe.predict_movies(input_movie_name)
        m_api = Movie_api()
        liked = m_api.search_movie(user_liked)
        movie_with_images = m_api.search_movie(recommended)

        print(user_liked)
        print("===============================")
        print(recommended)

        return render_template("movies.html", messages=liked, movies = movie_with_images)
    m = get_popular_movie(getMovies())
    return render_template('index.html',  movies=m.to_dict('records'))

def process_movie(movies):
    entries = {}
    if movies:
        for movie in movies.keys():
            key = re.sub(re.escape("movie_"),"",movie)
            entries[key] = movies[movie]
        return entries



    

""" 
Retrieve all the rows from the database and return them.
All the data will be displayed on entire_database.html file.
The view_database() route method is called from app.py
"""
