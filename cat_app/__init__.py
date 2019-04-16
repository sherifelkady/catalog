from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = "A!@#EDls0_lA6790"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cat_app.db"
create_engine("postgresql://grader:T@@r%&9)Ek@localhost/grader")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manger = LoginManager(app)
login_manger.login_view = "login"


from cat_app import route  # nopep8
