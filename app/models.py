from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import CheckConstraint

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)
    
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    username = db.Column(db.String(50), unique=True, nullable=False)
    total_links = db.Column(db.Integer, default=0)
    created_by_agency = db.Column(db.String(120), nullable=True)
    
    #additional fields for profile page
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True) # Can be skipped
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age > 0'), nullable=False)
    profession = db.Column(db.String(100), nullable=False)     
    bio = db.Column(db.String(250), nullable=True)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'

    # Link Model based on datetime

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='links')

    def __repr__(self):
        return f'<Link {self.short_code}>'