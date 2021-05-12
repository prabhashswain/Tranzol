from flask import Flask
from .Admin.views import admin
from .Home.views import home
from .extensions import db,login_manager
from .commands import create_table
from .models import *

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    #config sqlalchemy
    db.init_app(app)
    #flask-login config
    login_manager.init_app(app)
    login_manager.login_view = 'home.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    #register admin blueprint
    app.register_blueprint(admin)
    app.register_blueprint(home)
    app.cli.add_command(create_table)

    return app