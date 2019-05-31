from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'Admin({self.name})'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_type = title = db.Column(db.String(10), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(60), unique=True, nullable=False)
    category = db.Column(db.String(60), unique=False, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(240), nullable=False)
    documentation = db.Column(db.Text, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id), nullable=False)
