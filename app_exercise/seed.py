from models import User, Post, db
from app import app


class Seed():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    sam = User(first_name='Sam', last_name="Hatcliff", image_url="/photos/2.jpeg")
    stephany = User(first_name='Stephany', last_name="Garcia", image_url="/photos/1.png")
    steve = User(first_name='Steve', last_name="Johnson", image_url="/photos/2.jpeg")
    dustin = User(first_name='Dustin', last_name="Hayes", image_url="/photos/3.jpeg")
    tim = User(first_name='Tim', last_name="Smith", image_url="/photos/4.png")
    mason = User(first_name='Mason', last_name="Torabi", image_url="/photos/5.jpeg")
    gabby = User(first_name='Gabby', last_name="Smith", image_url="/photos/6.jpeg")

    db.session.add(sam)
    db.session.add(stephany)
    db.session.add(steve)
    db.session.add(dustin)
    db.session.add(tim)
    db.session.add(mason)
    db.session.add(gabby)

    db.session.commit()
