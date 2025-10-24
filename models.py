from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    details = db.Column(db.Text)
    benefits = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    application = db.Column(db.Text)
    documents = db.Column(db.Text)
    level = db.Column(db.String(50))
    schemeCategory = db.Column(db.String(100))
    tags = db.Column(db.String(150))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def like_count(self):
        return Like.query.filter_by(scheme_id=self.id).count()

    @property
    def comments(self):
        return Comment.query.filter_by(scheme_id=self.id).order_by(Comment.timestamp.desc()).all()

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    scheme_id = db.Column(db.Integer, db.ForeignKey('scheme.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    scheme_id = db.Column(db.Integer, db.ForeignKey('scheme.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
