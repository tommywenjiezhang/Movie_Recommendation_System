import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class MovieImagesScraper():
    def __init__(self):
        self._url = "https://www.imdb.com/find"
        self._baseurl = "https://www.imdb.com"
    
    def start_requests(self,keywords):
        query = "+".join(keywords.split(" ")) if " " in keywords else keywords
        # go to the best buy website
        headers = {'User-agent': 'Mozilla/5.0',"Accept-Encoding": "*",
            "Connection": "keep-alive"}
        payload = {"q":query}
        r = requests.get(self._url, params=payload, headers= headers)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")
        finded_url = soup.find("td",class_= "result_text")
        next_pages =  finded_url.findChildren("a" , recursive=False)
        next_page = urljoin(self._baseurl, next_pages[0]["href"])
        r = requests.get(urljoin(self._baseurl, next_page),headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        images = []
        descriptions = []
        try:
            image_urls = soup.find_all('img')
            descriptions = soup.find("span",class_= "sc-16ede01-2").text
            for i in image_urls:
                if "https" in i["src"]:
                    images.append(i["src"])
        except Exception as err:
            return None
        return {"images":images, "desc":descriptions, "redirect_url": r.url}






if __name__ == "__main__":
    print("Program started... ")
    m = MovieImagesScraper()
    url = m.start_requests("Super Man")
    print(url["desc"])
    # Use excel to open gpu.csv (the file we just output it )