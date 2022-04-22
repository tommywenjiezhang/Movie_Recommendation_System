from flask import Flask
import sqlalchemy
from flask_session import Session
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


def testdb():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>It works.</h1>'
    except Exception as e:
        
        return '<h1>Something is broken.</h1> <p>{}</p>'.format(e)


def create_app():
    app = Flask(__name__, static_folder='build',static_url_path='')
    app.config.from_pyfile("config.py")
    db.init_app(app)
    logging.basicConfig(filename='error.log',level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    CORS(app)
    import app.routes as routes
    # Home page (where you will add a new user)
    all_methods = ['GET', 'POST']
    app.add_url_rule("/", view_func=routes.serve)
    app.add_url_rule('/api', methods=all_methods, view_func=routes.index)
    app.add_url_rule("/movies_links", view_func=routes.movie_links)
    app.add_url_rule("/db",view_func=testdb)
    # "Thank you for submitting your form" page
    return app