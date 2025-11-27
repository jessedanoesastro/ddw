from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models



