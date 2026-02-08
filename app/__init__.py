from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from flask_login import LoginManager
import time
from sqlalchemy.exc import OperationalError


# instance created at module level 
db = SQLAlchemy()
migrate = Migrate()

# login manager defined
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        db.init_app(app)
        migrate.init_app(app, db)

        # initializing login manager for login sessions 
        login_manager.init_app(app)

        # AUTO-CREATE TABLES FOR FRESH DB (DOCKER / AWS SAFE)
        from app import models
        with app.app_context():
            for _ in range(10):  # wait for DB to be ready
                try:
                    db.create_all()
                    break
                except OperationalError:
                    time.sleep(1)

    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

    from app.controllers.auth import auth
    app.register_blueprint(auth)

    from app.controllers.routes import bp
    app.register_blueprint(bp)

    from app.controllers.admin import admin
    app.register_blueprint(admin)

    return app


# User Loader for Flask-Login  
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))