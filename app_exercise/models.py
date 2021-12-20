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
    user = db.relationship('User', backref="posts")
    
    

    