from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25), 
                    nullable=False)
    #still accepts no first name even though nullable is set to false. why?
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(), default= "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    
class Post(db.Model):
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(75), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default= datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = db.relationship('User', backref="posts", single_parent=True, cascade="all, delete-orphan")
    
    tags = db.relationship('Tag', secondary = 'post_tags', backref="posts")
    
    
    
class Tag(db.Model):
    
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    
    
class PostTag(db.Model):
    
    __tablename__ = 'post_tags'
    
    post_id= db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id= db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    