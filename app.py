from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/url', methods=['POST', 'GET'])
def url():
    if request.method == 'POST':
        # url_recieved = request.form['url']
        return request.form['url']
    else:
        return render_template('url.html')
    
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=2222, debug=True)