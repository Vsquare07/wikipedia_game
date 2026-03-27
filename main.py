import time
import requests
import torch
from transformers import BertTokenizer, BertModel

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model = model.to(DEVICE)

def get_correct_wiki_url(search_term):
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # We are asking the API to query the title, follow any redirects, 
    # and give us the 'info' which includes the full URL.
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

from bs import LinkGenerator
generator = LinkGenerator()

start_word = input("Enter the start word : ").lower()
end_word = input("Enter the end word : ").lower()

start = get_correct_wiki_url(start_word)
end = get_correct_wiki_url(end_word)

LIMIT = 30

end_inputs = tokenizer(end_word, return_tensors="pt").to(DEVICE)
with torch.no_grad():
    outputs = model(**end_inputs)
end_vector = outputs.last_hidden_state[0, 1, :]

print(f"Starting point {start_word}:{start}")
currLink = start
currName = start_word

status = True

visited = set()
for i in range(LIMIT):
    if currName == end_word or currLink == end:
        print(f"Found the end point {end_word}:{end}")
        status = False
        break
    nextLinks = generator.connections(currLink)
    time.sleep(1)

    curr_inputs = tokenizer(currName, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model(**curr_inputs)
    currVector = outputs.last_hidden_state[0, 1, :]
    norm = 2*1e9

    smallest_name = None
    correspoding_link = None

    for name, link in nextLinks.items():
        name = name.lower()
        if name in visited:
            continue
        visited.add(name)
        next_inputs = tokenizer(name, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = model(**next_inputs)
        nextVec = outputs.last_hidden_state[0, 1, :]

        new_norm = torch.linalg.norm(nextVec - end_vector)
        new_norm = new_norm.item()
        if new_norm < norm:
            norm = new_norm
            smallest_name = name
            corresponding_link = link
    currLink = corresponding_link
    currName = smallest_name

    print(f"{i+1} => {currName}:{currLink}")

if status:
    print("Target word not found within 30 steps")