from app import db
from datetime import datetime

class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(db.Integer, primary_key=True)
    
    #short_code is our 1 char out of 62
    short_code = db.Column(db.String(3), unique=True, nullable=False)
    original_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Link {self.short_code}>'