import requests
from flask import current_app, url_for
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class MovieImagesScraper():
    def __init__(self):
        self._url = "https://www.imdb.com/find"
        self._baseurl = "https://www.imdb.com"
    
    def start_requests(self,keywords,movie_id):
        if keywords is None:
            return {"images":["/static/images/not_found.webp"], "desc":"not available", "redirect_url": ""}
        query = "+".join(keywords.split(" ")) if " " in keywords else keywords
        query = clean_movie_title(query)
        # go to the best buy website
        headers = {'User-agent': 'Mozilla/5.0',"Accept-Encoding": "*",
            "Connection": "keep-alive"}
        payload = {"q":query}
        r = requests.get(self._url, params=payload, headers= headers)
        try:
            content = r.content
            soup = BeautifulSoup(content, "html.parser")
            finded_url = soup.find("td",class_= "result_text")
            next_pages =  finded_url.findChildren("a" , recursive=False)
            next_page = urljoin(self._baseurl, next_pages[0]["href"])
            r = requests.get(urljoin(self._baseurl, next_page),headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
            images = []
            descriptions = []
            image_urls = soup.find_all('img')
            descriptions = soup.find("span",class_= "sc-16ede01-2").text
            for i in image_urls:
                if "https" in i["src"]:
                    images.append(i["src"])
            return {"images":images, "desc":descriptions, "redirect_url": r.url}
        except Exception as err:
            return {"images":[ "/static/images/not_found.webp"], "desc":"not available", "redirect_url": r.url }
        







def clean_movie_title(title):
    return re.sub(r'\([0-9]+\)', '', title)



# def create_link(conn, movie):

#     sql = ''' INSERT INTO Meta (movie_id,images_url,site_url,desc)
#               VALUES(?,?,?,?); '''

#     cur = conn.cursor()
#     cur.execute(sql, movie)
#     conn.commit()

#     return cur.lastrowid



# def insertdb(conn, row):
#     m = MovieImagesScraper()
#     url = m.start_requests(row[2])
#     movie = (row[1], url["images"][0],url["redirect_url"],url["desc"])
#     print("inserting movie {} title {} url {}".format(*movie))
#     create_link(conn, movie)

# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except Error as e:
#         print(e)

#     return conn

if __name__ == "__main__":
    print("Program started... ")

    # import pandas as pd
    # import pickle
    # from MovieRunner import run_process
    # conn = create_connection('./app/info.db')
    # df = pd.read_sql("SELECT * FROM movies",conn,index_col="index")
    # # with open("movie_url.csv", mode= "a" ) as csv_file:
    # #     csv_writer = csv.writer(csv_file)
    # for row in df.iloc[955].itertuples():
    #     insertdb(conn, row)








    # df.loc["url"] = df.title.apply(lambda x : m.start_requests(x)["images"][0])
    # pickle.dump(df[["title", "movie_id", "url"]], open("movie.obj","wb"))
    # df.to_sql("MovieLinks",conn, if_exists="replace")
    # Use excel to open gpu.csv (the file we just output it )