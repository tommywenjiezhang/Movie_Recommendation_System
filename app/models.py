import pandas as pd
import numpy as np
from app import db
import os


class Moviedb():
    def __init__(self):
        self._movies = pd.read_sql("Select * from movies",db.engine)
        self._rating = pd.read_sql("Select * from rating", db.engine)

    def get_movies(self):
        return self._movies
    def get_rating(self):
        return self._rating
    def get_random_five(self):
        return self._movies



class Rating(db.Model):
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    index = db.Column(db.Integer, primary_key=True)

    # A Rating has a name, a price and some calories:
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    rating = db.Column(db.Float)

    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

def create_rating(user_id, movie_id, rating):
    # Create a dessert with the provided input.
    # At first, we will trust the user.

    # This line maps to line 16 above (the Dessert.__init__ method)
    rating = Rating(user_id, movie_id, rating)

    # Actually add this rating to the database
    db.session.add(rating)

    # Save all pending changes to the database
    db.session.commit()

    return rating


def getMovies():
    m = Moviedb()
    movies = m.get_movies()
    rating = m.get_rating()
    moives_rating = pd.merge(rating,movies,left_on='movie_id', right_on='movie_id')
    return moives_rating

def get_popular_movie(df):
    highest_rating = pd.DataFrame(df.groupby('movie_id')['rating'].count())
    high_index = highest_rating.sort_values(by="rating",ascending=False).index.unique()
    df =  df.set_index("movie_id").loc[high_index,["title","genres","rating"]]
    df.loc[high_index,"number of vote"]  = highest_rating.loc[high_index,"rating"]
    df = df[df["number of vote"] > df["number of vote"].median()]
    return df.drop_duplicates(subset="title").sample(5).reset_index()

def clean_db(movies_file_path, rating_file_path, connection):
    new_movie_df = pd.read_csv(movies_file_path)
    new_rating_df = pd.read_csv(rating_file_path)
    new_rating_df.to_sql(name='rating', con=connection,if_exists= 'replace')
    new_movie_df.to_sql(name="movies", con=connection,if_exists= 'replace')
    