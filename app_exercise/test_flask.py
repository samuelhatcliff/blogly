from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_flask_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        user2 = User(first_name="Thisistoolongforafirstname", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)
            self.assertIn('User', html)
            self.assertNotIn("Thisistoolongforafirstname", html)

    def test_show_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Test</h1>", html)
            self.assertIn("<h1>User</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirst", "last_name": "TestLast"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst", html)
            self.assertIn("TestLast", html)
            
    def test_404r(self):
        with app.test_client() as client:
            resp = client.get(f"/10")
            self.assertEqual(resp.status_code, 404)
            
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirst", "last_name": "TestLast"}
            resp = client.post("/users/<int:user_id>/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst", html)
            self.assertIn("TestLast", html)
    

    def test_publish_post(self):
        with app.test_client() as client:
            d = {"title": "TestTitle", "content": "TestContent"}
            resp = client.post('/posts/<int:post_id>/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst", html)
            self.assertIn("TestLast", html)




        
            
            
       
