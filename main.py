import time
from scraper import LinkGenerator, get_correct_wiki_url
from model import BERT

generator = LinkGenerator()
BERT = BERT()

start_word = input("Enter the start word : ").lower()
end_word = input("Enter the end word : ").lower()

start_url = get_correct_wiki_url(start_word)
end_url = get_correct_wiki_url(end_word)

target_wordVector = BERT.wordVector(end_word)

print(f"Starting point {start_word}:{start_url}")
currLink = start_url
currWord = start_word

status = True
visited = set()

LIMIT = 30
for i in range(LIMIT):
    if currWord == end_word or currLink == end_url:
        print(f"Found the end point {end_word}:{end_url}")
        status = False
        break

    nextLinks = generator.connections(currLink)
    time.sleep(1)

    curr_wordVector = BERT.wordVector(currWord)
    norm = 2*1e9

    smallest_name = None
    correspoding_link = None

    for name, link in nextLinks.items():
        name = name.lower()
        if name in visited:
            continue
        visited.add(name)

        next_wordVector = BERT.wordVector(name)

        new_norm = BERT.norm(next_wordVector ,target_wordVector)
        if new_norm < norm:
            norm = new_norm
            smallest_name = name
            corresponding_link = link
    currLink = corresponding_link
    currWord = smallest_name

    print(f"{i+1} => {currWord} ------> {currLink}")

if status:
    print("Target word not found within 30 steps")