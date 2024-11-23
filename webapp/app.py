import flask
import saml
from flask_login import LoginManager
from flask_login import UserMixin, login_user, login_required, current_user

import pandas as pd

login_manager = LoginManager()

app = flask.Flask(__name__)

app.config.update({
    'SECRET_KEY': 'soverysecret',
    'SAML_METADATA_URL': 'https://shibidp-test.cit.cornell.edu/idp/shibboleth',
})

saml.FlaskSAML(app)
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    # db = pd.read_csv("db.csv")
    user = User(name="unknown", id=user_id)
    return user

@saml.saml_authenticated.connect_via(app)
def on_saml_authenticated(sender, subject, attributes, auth):
    user = User(name=attributes["displayName"], id=attributes["uid"][0])
    login_user(user)

@app.get("/")
def hello_world():
    return flask.render_template('index.html')

@app.route("/get-cards")
@login_required
def get_cards():
    id = current_user.id
    db = pd.read_csv("db.csv", index_col="id")
    cards = db.loc[id].astype(int)
    print(db.loc[id].astype(int))
    year_names = ["Spring 2016", "Spring 2017", "Spring 2018", "Spring 2019", "Spring 2020", "Spring 2021", "Spring 2022", "Spring 2023", "Spring 2024", "Fall 2024"]
    return flask.render_template('index.html', cards=cards, year_names=year_names)