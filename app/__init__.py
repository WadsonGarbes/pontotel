from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from apifairy import APIFairy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_message = "Você deve fazer login para acessar esta página!"
login.login_view = "auth.login"
apifairy = APIFairy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    apifairy.init_app(app)
    ma.init_app(app)

    from app.api.tokens import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from app.api.usuarios import usuarios
    app.register_blueprint(usuarios, url_prefix='/api')
    from app.api.cotacoes import cotacoes
    app.register_blueprint(cotacoes, url_prefix='/api')

    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from app import views, models

    return app