
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
from flask_migrate import Migrate
from flask_admin import Admin
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
babel = Babel(app)

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