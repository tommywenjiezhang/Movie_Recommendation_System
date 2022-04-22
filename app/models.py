from tkinter import image_names
import pandas as pd
import numpy as np
from app import db
import os


class Moviedb():
    def __init__(self):
        self._movies = pd.read_sql("Select * from movies",db.engine)
        self._rating = pd.read_sql("Select * from rating", db.engine)
        self._movies_links = pd.read_sql("Select * from Meta", db.engine)

    def get_movies(self):
        return self._movies
    def get_rating(self):
        return self._rating
    def get_movies_links(self):
        return self._movies_links
    def get_random_five(self):
        return self._movies


class Movie(db.Model):
    __tablename__ = "movies"
    index = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    title = db.Column(db.String)
    genres = db.Column(db.String)

    def __init__(self, index, movie_id ,title,genres):
        self.index = index
        self.movie_id = movie_id
        self.title = title
        self.genres = genres

    


class MovieMeta(db.Model):
    __tablename__ = "Meta"
    movie_id = db.Column(db.Integer, primary_key=True)
    images_url = db.Column(db.String)
    site_url = db.Column(db.String)
    desc = db.Column(db.String)

    def __init__(self, movie_id, images_url, site_url, desc):
        self.movie_id = movie_id
        self.images_url = images_url
        self.site_url = site_url
        self.desc = desc




    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'movie_id'         : self.movie_id,
           'images_url': self.images_url,
           'site_url'  : self.site_url,
           "desc" : self.desc
       }

    @staticmethod
    def create_meta(movie_id, images_url, site_url,desc):
        meta = MovieMeta(movie_id, images_url, site_url, desc)
        db.session.add(meta)
        db.session.commit()
        return meta
            




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
    links = m.get_movies_links()
    moives_rating = pd.merge(rating,movies,left_on='movie_id', right_on='movie_id')
    movies_link = pd.merge(moives_rating, links, how="left" ,left_on='movie_id', right_on='movie_id')
    return movies_link

def get_popular_movie(df):
    highest_rating = pd.DataFrame(df.groupby('movie_id')['rating'].count())
    high_index = highest_rating.sort_values(by="rating",ascending=False).index.unique()
    df =  df.set_index("movie_id").loc[high_index,["title","genres","rating"]]
    df.loc[high_index,"number of vote"]  = highest_rating.loc[high_index,"rating"]
    df = df[df["number of vote"] > df["number of vote"].median()]
    return df.drop_duplicates(subset="title").sample(5).reset_index()


def clean():
    if os.path.exists("model_pkl"):
        os.remove("model_pkl")
        return True
    else:
        return False
    