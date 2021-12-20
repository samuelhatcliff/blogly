from flask import Flask, request, render_template, redirect, flash, session
import psycopg2
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Post





app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "topsecret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():
    
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    sam = User(first_name='Sam', last_name="Hatcliff", image_url="/photos/sam_photo.jpg")
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
    return redirect ("users")

@app.route('/users')
def list_users():
    """shows list of all users in db"""
    users = User.query.all()

    return render_template('listing.html', users=users) 

@app.route('/users/new')
def create_new_user():
    users = User.query.all()
    return render_template("new_user.html", users=users)

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if not request.form["image_url"]:
        img = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
    else: 
        img = request.form["image_url"]
        
    new_user = User(first_name=first_name, last_name=last_name, image_url=img)
    db.session.add(new_user)
    db.session.commit()
    return redirect ("/users") 

@app.route('/<int:user_id>')
def show_user_profile(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    """get404 method comes from flask sqlalchemy, which replaces "None" with a 404 error"""
    return render_template('profiles.html', user=user)
    
@app.route('/users/<int:user_id>/edit')
def get_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)
    
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.form["first_name"]:
        user.first_name = request.form["first_name"]
    if request.form["last_name"]:
        user.last_name = request.form["last_name"]
    if request.form["image_url"]:
            user.img = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect ("/users") 

@app.route('/users/<int:user_id>/remove')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect ("/users") 
    
@app.route('/users/<int:user_id>/posts/new')
def get_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)
    
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    post = Post(title=request.form["title"], content=request.form["content"], author=user.id)
    db.session.add(post)
    db.session.commit()
    return redirect ("/users") 

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("show_post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    return redirect (f'/posts/{post_id}')
    
@app.route('/posts/<int:post_id>/remove')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect (f"/{user_id}") 
    

    
    
    
    
    
    
    
        
        
    
 

    
    