from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from flask_login import LoginManager
from app.auth import auth

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
        # initializing login manager for login sessions 
        login_manager.init_app(app)

        migrate.init_app(app, db)
        app.register_blueprint(auth)
        
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

    try:
        from app.routes import bp
        app.register_blueprint(bp)

        from app import models
    except ImportError as e:
        logging.error(f"Module import filed: {e}")
    
    return app

# store only user-id 
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
