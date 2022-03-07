import random
import string
import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

from utility.decorators import *

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

if __name__ == '__main__':
    app.run(port=2222, debug=True)
