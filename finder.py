import time
from scraper import LinkGenerator, get_correct_wiki_url
from model import BERT

class Explorer():
    def __init__(self, endWord:str):
        self.visited = set()
        self.generator = LinkGenerator()
        self.BERT = BERT(path="model_weights")
        self.end_wordVector = self.BERT.wordVector(endWord)

    def nextClosestWord(self, url:str) -> tuple[str, str]:
        nextLinks = self.generator.connections(url)
        time.sleep(1)

        cos_sim = -2
        for name, link in nextLinks.items():
            name = name.lower()
            if name in self.visited:
                continue
            self.visited.add(name)

            next_wordVector = self.BERT.wordVector(name)
            new_cos_sim = self.BERT.cos_sim(next_wordVector ,self.end_wordVector)

            if new_cos_sim > cos_sim:
                cos_sim = new_cos_sim
                closestWord = name
                closestLink = link

        return (closestWord, closestLink)
    

if __name__ == "__main__":
    LIMIT = 20
    startWord = input("Enter start word : ").lower()
    endWord = input("Enter end word : ").lower()
    explorer = Explorer(endWord)

    startURL = get_correct_wiki_url(startWord)
    endURL = get_correct_wiki_url(endWord)

    currWord = startWord
    currURL = startURL

    status = False
    for i in range(LIMIT):
        print(f"{i} || {currWord} ----> {currURL}")

        if currWord == endWord or currURL == endURL:
            status = True
            break
        
        currWord, currURL = explorer.nextClosestWord(currURL)
    
    if not status:
        print("The end word wasn't reached in the 20 steps limit")