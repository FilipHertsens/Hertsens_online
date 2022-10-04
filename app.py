from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babelex import Babel
from flask_migrate import Migrate
from flask_admin import Admin
from forms import LoginForm
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import UserMixin, UserManager
from flask import abort, redirect, url_for
from flask_user import UserMixin, UserManager
from flask_login import current_user
from buttons import navbuttons
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
babel = Babel(app)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'filip@hertsens.eu'
app.config['MAIL_PASSWORD'] = 'GE022022!'
app.config['MAIL_DEFAULT_SENDER'] = ('Hertsens Online','garage@hertsens.eu')

app.config['USER_APP_NAME'] = "Hertsens Online"
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_EMAIL_SENDER_NAME'] = "Hertsens Online"
app.config['USER_EMAIL_SENDER_EMAIL'] = 'garage@hertsens.eu'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                      db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')))

role_navbarbuttons = db.Table('role_navbarbuttons',
                              db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')),
                              db.Column('button_id', db.Integer(), db.ForeignKey('navbarbutton.id')))

person_type_person = db.Table('person_type_person',
                              db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
                              db.Column('person_type_id', db.Integer(), db.ForeignKey('person_type.id')))

def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_active:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_func


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    navbarbutton = db.relationship('Navbarbutton', secondary='role_navbarbuttons', backref='premissions')

    def __repr__(self):
        return '{}'.format(self.name)


class Navbarbutton(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    new_tab = db.Column(db.Boolean, default=False, nullable=True)
    href = db.Column(db.String(50), )
    navbarcat_id = db.Column(db.Integer, db.ForeignKey('navbarcat.id'))

    def __repr__(self):
        return '{}'.format(self.name)


class Navbarcat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    buttons = db.relationship('Navbarbutton', backref='navbarcat')

    def __repr__(self):
        return '{}'.format(self.name)

class Projects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    robaws_id = db.Column(db.Integer(), unique=True)
    robaws_logicid = db.Column(db.String(50), unique=True)
    planningName = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True, nullable=True)
    street = db.Column(db.String(150))
    city = db.Column(db.String(50))
    postalCode = db.Column(db.String(20))
    country = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '{}'.format(self.name)


    def tableKeys(self):
        keydict = {}
        keydict['id'] = {'text': 'id', 'type': 'text'}
        keydict['wacs_id'] = {'text': 'wacs_id', 'type': 'text'}
        keydict['name'] = {'text': 'name', 'type': 'text'}
        keydict['licenseplate'] = {'text': 'licenseplate', 'type': 'text'}
        keydict['vin'] = {'text': 'vin', 'type': 'text'}
        keydict['brand'] = {'text': 'asset_brands', 'type': 'text'}
        keydict['model'] = {'text': 'asset_model', 'type': 'text'}
        keydict['status'] = {'text': 'asset_status', 'type': 'text'}
        keydict['FirstRegistration'] = {'text': 'FirstRegistration', 'type': 'text'}
        keydict['kindWacs'] = {'text': 'kindWacs', 'type': 'text'}
        return keydict


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(50, collation='NOCASE'), unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(200))
    roles = db.relationship('Role', secondary='user_roles', backref='premissions')
    confirmedRegistrations = db.relationship('Hour_registrations', backref='confirmed_by')

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_navbarbuttons(self):
        return navbuttons(self)



class Timetables(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100, collation='NOCASE'), unique=True)
    startWeekday = db.Column(db.Float)
    stopWeekday = db.Column(db.Float)
    breakWeekday = db.Column(db.Float)
    startSaturday = db.Column(db.Float)
    stopSaturday = db.Column(db.Float)
    breakSaturday = db.Column(db.Float)
    startSunday = db.Column(db.Float)
    stopSunday = db.Column(db.Float)
    breakSunday = db.Column(db.Float)
    startHoliday = db.Column(db.Float)
    stopHoliday = db.Column(db.Float)
    breakHoliday = db.Column(db.Float)
    persons = db.relationship('Person', backref='timetable')

    def __repr__(self):
        return '{}'.format(self.name)


class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robaws_id = db.Column(db.String(5), unique=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(50, collation='NOCASE'), unique=True)
    distanceToWork = db.Column(db.Integer)
    telegram_id = db.Column(db.String(50))
    street = db.Column(db.String(150))
    city = db.Column(db.String(50))
    postalCode = db.Column(db.String(20))
    country = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    driverLicense = db.Column(db.String(20))
    pay_type = db.Column(db.String(20))
    statute = db.Column(db.String(20))
    gsm = db.Column(db.String(20))
    dateOfBirth = db.Column(db.DateTime())
    civilStatus = db.Column(db.String(50))
    email_confirmed_at = db.Column(db.DateTime())
    type = db.relationship('Person_type', secondary='person_type_person', backref='persons')
    rfid_tag = db.relationship('Tags', backref='person', uselist=False)
    rfid_registrations = db.relationship('Hour_registrations', backref='person')
    status = db.Column(db.Boolean, default=True, nullable=True)
    timeTable_id = db.Column(db.Integer, db.ForeignKey('timetables.id'))



    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Person_type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '{}'.format(self.name)


class POI(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    traccar_id = db.Column(db.Integer(), unique=True)
    description = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Float)

    def __repr__(self):
        return '{}'.format(self.name)


class Tags(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nr = db.Column(db.String(50), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    registraties = db.relationship('Hour_registrations', backref='tag')

    def __repr__(self):
        return '{}'.format(self.nr)


class Action_registrations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    working = db.Column(db.Boolean, default=False, nullable=True)
    icon = db.Column(db.String(100))
    hourregistrations = db.relationship('Hour_registrations', backref='action')

    def __repr__(self):
        return '{}'.format(self.name)


class Iot_devices(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    serial_nr = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))
    hourregistrations = db.relationship('Hour_registrations', backref='device')

    def __repr__(self):
        return '{}'.format(self.name)


class Hour_registrations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    time = db.Column(db.DateTime())
    action_id = db.Column(db.Integer, db.ForeignKey('action_registrations.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('iot_devices.id'))
    lat = db.Column(db.String(50))
    long = db.Column(db.String(50))
    photoUrl = db.Column(db.String(50))
    remark = db.Column(db.String(200))
    valid = db.Column(db.Boolean, default=True, nullable=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=True)
    confirmed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '{}'.format(self.id)


user_manager = UserManager(app, db, User)


""" 
to update db
open terminal
    1   flask db stamp head
    2   flask db migrate
    3   flask db upgrade
"""


class MyModelView(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

    def is_accessible(self):
        if current_user.is_active:
            roless = current_user.roles
            for x in roless:
                if x.name == 'Admin':
                    return current_user.is_authenticated
                else:
                    return False
            return False
        else:
            return False

    def get_edit_userForm(self):
        form_user = ModelView(User, db.session).get_edit_form()
        del form_user.password
        return form_user


admin.add_sub_category(name="users", parent_name="Users")
admin.add_view(MyModelView(User, db.session, category="Users"))
admin.add_view(MyModelView(Role, db.session, category="Users"))
admin.add_view(MyModelView(Navbarcat, db.session, category="Users"))
admin.add_view(MyModelView(Navbarbutton, db.session, category="Users"))

admin.add_sub_category(name="persons", parent_name="Persons")
admin.add_view(MyModelView(Person, db.session, category="Persons"))
admin.add_view(MyModelView(Person_type, db.session, category="Persons"))
admin.add_view(MyModelView(Tags, db.session, category="Persons"))
admin.add_view(MyModelView(Hour_registrations, db.session, category="Persons"))
admin.add_view(MyModelView(Action_registrations, db.session, category="Persons"))
admin.add_view(MyModelView(Timetables, db.session, category="Persons"))

admin.add_sub_category(name="iot devices", parent_name="iot_devices")
admin.add_view(MyModelView(Iot_devices, db.session, category="iot_devices"))

admin.add_sub_category(name="Projects", parent_name="Projects")
admin.add_view(MyModelView(Projects, db.session, category="Projects"))
admin.add_view(MyModelView(POI, db.session, category="Projects"))


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',user=current_user, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        print(user)
        next_url = request.form.get("next")
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if next_url:
                    return redirect(next_url)
                return redirect(url_for('index'))
            else:
                error = 'Invalid password for this user'
        else:
            error = f'No user with {form.email.data} as email'
    return render_template('login.html', form=form, error=error,user=current_user)

@app.route('/logout')
@logged_in
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/mobile/time_registration')
def timereg():
    return render_template('time_registration.html')


@app.route('/data/getUser', methods=['POST'])
def getUser():
    return {'valid':True,'name':'Filip Hertsens'}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)