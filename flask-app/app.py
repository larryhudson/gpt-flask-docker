from flask import Flask, render_template, request, url_for, redirect
from gpt_index import GPTSimpleVectorIndex, Document
from gpt_index.readers import SimpleWebPageReader
from gpt_index.langchain_helpers.text_splitter import TokenTextSplitter
import os
from datetime import datetime

app = Flask(__name__)

def get_latest_index_file():
    index_files = [filename for filename in os.listdir('.') if filename.startswith("index_")]

    if index_files:
        print(index_files)

        index_filename = sorted(index_files)[-1]
        print(index_filename)
        return index_filename
    else:
        return None

def get_index_timestamp_filename():
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    return f'index_{int(ts)}.json'

@app.route('/')
def home():
    # initial_urls = ["https://www.informationaccessgroup.com/our_services.html"]
    # documents = SimpleWebPageReader(html_to_text=True).load_data(initial_urls)

    # index = GPTSimpleVectorIndex(documents)
    
    # index.save_to_disk('index.json')

    return render_template('index.html')

@app.route('/query')
def query():
    query_string = request.args.get('q')

    index_filename = get_latest_index_file()
    index = GPTSimpleVectorIndex.load_from_disk(index_filename)

    response = index.query(query_string)
    print(response)

    return render_template('query.html', query=query_string, response=response)

@app.route('/add-url')
def add_url():
    # Example URL: http://localhost:8000/add-url?url=https%3A%2F%2Fwebaim.org%2Fintro%2F
    # Get the URL to add from the 'url' search param
    url = request.args.get('url')

    print("Adding webpage", url)

    index_filename = get_latest_index_file()

    if index_filename:
        index = GPTSimpleVectorIndex.load_from_disk(index_filename)
    else:
        index = GPTSimpleVectorIndex([])

    # Fetch the webpage URL
    document = SimpleWebPageReader(html_to_text=True).load_data([url])[0]

    # Split up the document into chunks. Followed these docs: https://github.com/jerryjliu/gpt_index/blob/main/examples/paul_graham_essay/InsertDemo.ipynb
    text_splitter = TokenTextSplitter(separator=" ", chunk_size=2048, chunk_overlap=20)
    text_chunks = text_splitter.split_text(document.text)
    doc_chunks = [Document(t) for t in text_chunks]

    for doc_chunk in doc_chunks:
        index.insert(doc_chunk)

    # Save the updated index
    new_index_filename = get_index_timestamp_filename()
    index.save_to_disk(new_index_filename)

    return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
