from flask import Flask, request, render_template, redirect, flash, session
import psycopg2
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Post, Tag, PostTag





app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "topsecret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():

    
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

@app.route('/users/<int:user_id>/remove', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ("/users") 
    
@app.route('/users/<int:user_id>/posts/new')
def get_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)
    
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    getlist= request.form.getlist("tag")
    tag_ids = [int(num) for num in getlist]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    print(getlist, "<----GET LIST")
    print(tag_ids, "<----TAG IDS")
    print(tags, "<----TAGs")
    post = Post(title=request.form["title"], content=request.form["content"], author=user.id, tags=tags)
    db.session.add(post)
    db.session.commit()
    return redirect (f"/{user_id}") 

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags= post.tags
    return render_template("show_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    post_tags = post.tags
    all_tags = Tag.query.all()
    print(post_tags, "<--- tags already on post")
    return render_template("edit_post.html", post=post, post_tags=post_tags, all_tags=all_tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    getlist= request.form.getlist("tag")
    tag_ids = [int(num) for num in getlist]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
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


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template ('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

# @app.route('/tags/<int:tag_id>', methods=["POST"])
# def post_edit_tag(tag_id):
#     tag = Tag.query.get_or_404(tag_id)
#     tag.name = request.form['new_tag_name']
#     return render_template('show_tag.html', tag=tag)

@app.route('/tags/new')
def gen_new_tag_form():
    return render_template('create_tags.html')
    
@app.route('/tags/new', methods=["POST"])
def post_new_tag():
    tag = Tag(name= request.form['name'])
    db.session.add(tag)
    db.session.commit()
    return redirect ('/tags')

@app.route('/tags/<int:tag_id>/edit')
def gen_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def post_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    new_name = request.form['new_tag_name']
    tag.name = new_name
    db.session.add(tag)
    db.session.commit()
    return redirect ('/tags')

@app.route('/tags/<int:tag_id>/remove', methods=["POST"])
def remove_post(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect ('/tags')
    
    

    


    

    
    

    
    
    
    
    
    
    
        
        
    
 

    
    