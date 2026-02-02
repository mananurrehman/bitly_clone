from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        db.init_app(app)
        migrate.init_app(app, db)
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

    try:
        from app.routes import bp
        app.register_blueprint(bp)

        from app import models
    except ImportError as e:
        logging.error(f"Module import filed: {e}")
    
    return app