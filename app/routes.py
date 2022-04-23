from flask import render_template, request, redirect, url_for, session, current_app, send_from_directory
from app.models import Moviedb, create_rating,get_popular_movie, getMovies, clean, MovieMeta
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
        # user_review = process_movie(request.form.to_dict())
        # session["user_id"] = random.randint(1000, 2000)
        # entries = []
        # for entry in user_review.keys():
        #     entries.append({"user_id": session["user_id"], "movie_id": int(entry), "rating": float(user_review[entry])})
        # input_movie = max(user_review.items(), key = lambda k : k[1])

        input_movie_name = request.form.get('movie_id')
        mdb = Moviedb()
        rating = mdb.get_rating()
        movies = mdb.get_movies()
        pipe = Pipeline(rating,movies)
        # user_liked = pipe.because_user_liked(user_review)
        print("Import movie {}".format(request.form))
        recommended = pipe.predict_movies(input_movie_name)
        m_api = Movie_api()
        # liked = m_api.search_movie(user_liked)
        movie_with_images = m_api.search_movie(recommended)
        return json.dumps({ "recommended": movie_with_images})

        # return render_template("movies.html", messages=liked, movies = movie_with_images)
    m = get_popular_movie(getMovies())
    m_api = Movie_api()
    popular_m = m_api.search_movie(m)
    print(popular_m)
    # return render_template('index.html',  movies=m.to_dict('records'))
    return json.dumps({"movies":popular_m})

def serve():
    print(url_for("static", filename="images/not_found.webp"))
    return send_from_directory(current_app.static_folder, 'index.html')

def movie_links():
    links = [i.serialize for i in MovieMeta.query.limit(10).all()]
    return json.dumps(links)
    



def process_movie(movies):
    entries = {}
    if movies:
        for movie in movies.keys():
            key = re.sub(re.escape("movie_"),"",movie)
            entries[key] = movies[movie]
        return entries

def clean_model():
    flag = clean()
    if flag:
        return "Remove Model"


    

""" 
Retrieve all the rows from the database and return them.
All the data will be displayed on entire_database.html file.
The view_database() route method is called from app.py
"""
