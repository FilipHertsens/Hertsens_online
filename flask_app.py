
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template, request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/mobile/time_registration')
def timereg():
    return render_template('time_registration.html')

@app.route('/data/getUser', methods=['POST'])
def getUser():
    return {'valid':True,'name':'Filip Hertsens'}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)