import random
import string
import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

from utility.database import *

app = Flask("Mini URL")
load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route('/url', methods=['POST', 'GET'])
def url():
    if request.method == 'POST':
        # url_recieved = request.form['url']
        return request.form['url']
    else:
        return render_template('url_page.html')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = get_long_url(short_url)
    if long_url == False:
        return render_template('error.html')
    else:
        return redirect(str(long_url))

if __name__ == '__main__':
    app.run(port=2222, debug=True)
