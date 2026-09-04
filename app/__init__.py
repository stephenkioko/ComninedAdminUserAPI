from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///james.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize extensions with the app
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

from app import models, routes