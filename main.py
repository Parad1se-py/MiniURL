import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

from utility.database import *

app = Flask("Mini URL")
load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/url', methods=['POST', 'GET'])
def url():
    if request.method == 'POST':
        return request.form['url']
    else:
        return render_template('url_page.html')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = get_long_url(short_url)
    if long_url is False:
        return render_template('error.html')
    else:
        return redirect(str(long_url))
    
@app.route('/allurls')
def all_urls():
    # grab all urls from the database and display them (FOR TEST PURPOSES)
    docs = get_all_docs()
    return render_template('all_urls.html', docs=docs)

if __name__ == '__main__':
    app.run(port=2222, debug=True)
