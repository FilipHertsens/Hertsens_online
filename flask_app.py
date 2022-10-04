
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template, request
import json


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/timereg')
def timereg():
    return render_template('test.html')

@app.route('/data/getUser', methods=['POST'])
def getUser():
    data = json.loads(request.data)
    # response = requests.get(
    #     f'https://app.robaws.be/api/v2/projects/{nr}',
    #     headers={'Authorization': 'Basic %s' % userAndPass},
    # )
    return {'valid':True,'name':'Filip Hertsens'}