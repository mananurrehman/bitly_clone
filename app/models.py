from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(225), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, passowrd):
        return check_password_hash(self.password_hash, passowrd)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
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