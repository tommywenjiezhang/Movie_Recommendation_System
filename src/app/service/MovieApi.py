import re
from flask import current_app
import json
from app.service.spider import MovieImagesScraper
from  app.service.MovieRunner import run_process

class Movie_api():
    def __init__(self):
        self.api = MovieImagesScraper()

    def search_movie(self,movies):
        try:
            images_urls = []
            idx = {name: i for i, name in enumerate(list(movies), start=1)} 
            # movies.title = movies.title.apply(lambda x : re.match(r"[A-Za-z\s]+", x).group(0))
            images_urls = list(run_process(self.item,idx,list(movies.itertuples())))
            return images_urls
        except Exception as e:
            print(e)
            return None

    def item(self,idx, movie):
        entry = {}
        entry["title"]= movie[idx["title"]]
        entry["genre"]= movie[idx["genres"]]
        entry["movie_id"] = str(movie[idx["movie_id"]])
        
        if "images_url" not in idx or not movie[idx["images_url"]]:
            res = self.api.start_requests(entry["title"],movie[idx["movie_id"]])
            entry["url"] = res["images"][0]
            entry["description"] = res["desc"]
            entry["site_url"] = res["redirect_url"]
        else:
            entry["url"] = movie[idx["images_url"]]
            entry["description"] = movie[idx["desc"]]
            entry["site_url"] = movie[idx["site_url"]]
            
        return entry