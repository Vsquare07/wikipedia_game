from bs4 import BeautifulSoup
import requests

def get_correct_wiki_url(search_term):
    """Get corrected wikipedia url for a search, crtitical because wikipedia.org/wiki/search_term may not always generate a valid URL
        \nexample : https://en.wikipedia.org/wiki/cloth -> https://en.wikipedia.org/wiki/textile
        \nthis is because cloth is a topic in the wiki page of textile

    """
    api_url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "titles": search_term,
        "redirects": 1,
        "format": "json",
        "prop": "info",
        "inprop": "url"
    }
    
    headers = {'User-Agent': 'MyBot/1.0 (vatsalvarenya@gmail.com)'}
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        first_page = list(pages.values())[0]
        
        if "missing" in first_page:
            return None
            
        return first_page.get("fullurl")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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