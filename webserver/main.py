__author__ = 'kai'

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def hello():
    token = request.form['token']
    f = open("token.txt", "w")
    f.write(token)
    f.close
    return token
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000)
