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
        return render_template('url.html')
    
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/protected_area')
@login_is_required
def protected_area():
    return "Protected!"

@app.route('/login')
def login():
    return redirect("/protected_area")

@app.route('/callback')
def callback():
    pass

@login_is_required
@app.route('/logout')
def logout():
    pass

if __name__ == '__main__':
    app.run(port=2222, debug=True)
