from bs4 import BeautifulSoup
import requests

class LinkGenerator():
    def __init__(self):
        self.headers = {'User-Agent': 'MyBot/1.0 (vatsalvarenya@gmail.com)'}
    def connections(self, url: str)->dict:
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        anchor_tags = soup.find_all('a')
        req = {}
        for a in anchor_tags:
            link = a.get('href')
            name = a.text

            if link!=None and link.startswith("/wiki/"):
                if a.find('span'):
                    continue
                if ':' in link:
                    continue
                req[name] = "https://en.wikipedia.org"+link
        return req