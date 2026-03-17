import gensim
import numpy as np
import time
import gensim.downloader as api
import requests

def get_correct_wiki_url(search_term):
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # We are asking the API to query the title, follow any redirects, 
    # and give us the 'info' which includes the full URL.
    params = {
        "action": "query",
        "titles": search_term,
        "redirects": 1,         # <--- This is the magic key that follows redirects
        "format": "json",
        "prop": "info",
        "inprop": "url"
    }
    
    headers = {'User-Agent': 'MyBot/1.0 (vatsalvarenya@gmail.com)'}
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        
        # The API returns data inside a 'pages' dictionary. 
        # The keys are random page IDs, so we just grab the first page it returns.
        pages = data.get("query", {}).get("pages", {})
        first_page = list(pages.values())[0]
        
        # If the page doesn't exist at all, Wikipedia returns a "missing" flag
        if "missing" in first_page:
            return None
            
        return first_page.get("fullurl")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

model = gensim.models.KeyedVectors.load("google_w2v.model")
from bs import LinkGenerator
generator = LinkGenerator()
word2index = model.key_to_index

while True:
    start_word = input("Enter the start word : ").lower()
    if start_word in word2index:
        break
    print("That word doesnt exist in the vocabulary, please try again")

while True:
    end_word = input("Enter the end word : ").lower()
    if end_word in word2index:
        break
    print("That word doesnt exist in the vocabulary, please try again")

start = get_correct_wiki_url(start_word)
end = get_correct_wiki_url(end_word)

LIMIT = 10

print(f"Starting point {start_word}:{start}")
currLink = start
currName = start_word

end_vector = model[end_word]

status = True
for i in range(LIMIT):
    if currName == end_word or currLink == end:
        print(f"Found the end point {end_word}:{end}")
        status = False
        break
    nextLinks = generator.connections(currLink)
    time.sleep(1)
    currVector = model[currName]
    norm = 2*1e9
    smallest_name = None
    correspoding_link = None
    for name, link in nextLinks.items():
        name = name.lower()
        if name in word2index:
            nextVec = model[name]
        else:
            continue

        new_norm = np.linalg.norm(nextVec - end_vector)
        if new_norm < norm:
            norm = new_norm
            smallest_name = name
            corresponding_link = link
    currLink = corresponding_link
    currName = smallest_name

    print(f"{i+1} => {currName}:{currLink}")

if status:
    print("Target word not found within 10 steps")