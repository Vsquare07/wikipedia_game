from flask import Flask, render_template, request, redirect, Response
from finder import Explorer
from scraper import get_correct_wiki_url
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == "POST":
        global startWord
        startWord = request.form.get('start_word_input')
        global endWord
        endWord = request.form.get('end_word_input')
        global startURL
        startURL = get_correct_wiki_url(startWord)
        global endURL
        endURL = get_correct_wiki_url(endWord)
        global explorer
        explorer = Explorer(endWord)

        return render_template('result.html', start_word=startWord, end_word=endWord)

def generate():
    LIMIT = 20
    word = startWord
    url = startURL
    for i in range(LIMIT+1):
        if i == LIMIT:
            data = {
                "word": "__NOTfound__",
                "url": "__NOTfound__"
            }
            yield f"data: {json.dumps(data)}\n\n"
        elif word == endWord or url == endURL:
            data = {
                "word": "__found__",
                "url": "__found__"
            }
            yield f"data: {json.dumps(data)}\n\n"
        else:
            word, url = explorer.nextClosestWord(url)
            data = {
                "word": f"{word}",
                "url": f"{url}"
            }
            yield f"data: {json.dumps(data)}\n\n"

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='text/event-stream')

@app.route('/restart', methods=['POST'])
def restart(): 
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)