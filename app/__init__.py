import cloudinary
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/quanlyphongmach?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='dxajszqyt',
    api_key='459639577438341',
    api_secret='Yz2n3Ya3RK3Q15utZktXz1yOnZs'
)

login = LoginManager(app=app)

from twilio.rest import Client

account_sid = 'AC6a7e42ccb9fd068e4ac602e161118172'
auth_token = '0299ed1f759f807fbd5d45d50a1777ab'
client = Client(account_sid, auth_token)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
