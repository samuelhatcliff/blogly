# from models import User, Post, Tag, PostTag, db



# class Seed():
#     db.drop_all()
#     db.create_all()

#     sam = User(first_name='Sam', last_name="Hatcliff", image_url="/photos/2.jpeg")
#     stephany = User(first_name='Stephany', last_name="Garcia", image_url="/photos/1.png")
#     steve = User(first_name='Steve', last_name="Johnson", image_url="/photos/2.jpeg")
#     dustin = User(first_name='Dustin', last_name="Hayes", image_url="/photos/3.jpeg")
#     tim = User(first_name='Tim', last_name="Smith", image_url="/photos/4.png")
#     mason = User(first_name='Mason', last_name="Torabi", image_url="/photos/5.jpeg")
#     gabby = User(first_name='Gabby', last_name="Smith", image_url="/photos/6.jpeg")
    
#     funny = Tag(name="funny")
#     sad = Tag(name="sad")
#     whoa = Tag(name="whoa")

#     post = Post(title="My First Post", content="This is my content", author=1)
#     post2 = Post(title="My Second Post", content="This is more content", author=1)
#     post3 = Post(title="My third Post", content="This is even more content", author=2)
    
    
#     db.session.add(sam)
#     db.session.add(stephany)
#     db.session.add(steve)
#     db.session.add(dustin)
#     db.session.add(tim)
#     db.session.add(mason)
#     db.session.add(gabby)
#     db.session.add(post)
#     db.session.add(post2)
#     db.session.add(post3)
#     db.session.add(funny)
#     db.session.add(sad)
#     db.session.add(whoa)

#     db.session.commit()
