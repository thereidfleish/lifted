import saml
from flask import Flask, redirect, send_file, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

import pandas as pd
import requests
import io

login_manager = LoginManager()

app = Flask(__name__)

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
def home():
    if current_user.is_authenticated:
        id = current_user.id
        db = pd.read_csv("db.csv", index_col="id")
        cards = db.loc[id].astype(int)
        print(db.loc[id].astype(int))
        print(cards.index)
        sem_names = ["Spring 2016", "Spring 2017", "Spring 2018", "Spring 2019", "Spring 2020", "Spring 2021", "Spring 2022", "Spring 2023", "Spring 2024", "Fall 2024"]
        return render_template('index.html', sem_shortname=cards.index, num_cards=cards.values, sem_names=sem_names)
    else:
        return render_template('index.html')

# @app.route("/get-cards")
# @login_required
# def get_cards():
#     id = current_user.id
#     db = pd.read_csv("db.csv", index_col="id")
#     cards = db.loc[id].astype(int)
#     print(db.loc[id].astype(int))
#     print(cards.index)
#     sem_names = ["Spring 2016", "Spring 2017", "Spring 2018", "Spring 2019", "Spring 2020", "Spring 2021", "Spring 2022", "Spring 2023", "Spring 2024", "Fall 2024"]
#     return render_template('index.html', sem_shortname=cards.index, num_cards=cards.values, sem_names=sem_names)

@app.route("/get-pdf/<sem>/<message_num>")
@login_required
def get_pdf(sem, message_num):
    # if id == current_user.id:
        url = f'https://cards.cornelllifted.com/pdfs/{sem}/{current_user.id}/{message_num}_2638.pdf'
        return redirect(url)
        # req = requests.get(url)
        # return send_file(
        #              io.BytesIO(req.content),
        #             #  attachment_filename='report.pdf',
        #              mimetype='application/pdf'
        #        )
    # else:
        # return "You are not authorized to view this Lifted message.  If you think this in error, please email lifted@cornell.edu"