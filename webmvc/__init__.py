from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from urllib.parse import quote_plus
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "comptedb.db"

password=quote_plus('p@u!in')
conn='postgresql://postgres:{}@localhost:5432/comptedb'.format(password)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rezerty'
    app.config['SQLALCHEMY_DATABASE_URI']=conn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_views = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
