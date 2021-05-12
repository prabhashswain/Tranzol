from enum import unique
from .extensions import db
import re
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern,'-',s)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(255))
    author = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    blog_author = db.relationship('Blog',
                    foreign_keys='Blog.author',
                    backref='writer',
                    lazy=True)
    
    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self,unhashed_password):
        self.password = generate_password_hash(unhashed_password)
    
    def __str__(self):
        return self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(140),unique=True)
    body = db.Column(db.Text)
    author = db.Column(db.Integer,db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime,default=datetime.now())

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.generate_slug()
    
    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return self.title
