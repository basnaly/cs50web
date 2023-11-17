from django.test import TestCase, Client
from django.db.models import Max

from .models import User, Posts, Likes, Follow

# Create your tests here.

class PostsTestCase(TestCase):
    
    def setUp(self):
        
        # Create users.
        a1 = User.objects.create(id=1, username="User A")
        a2 = User.objects.create(id=2, username="User B")
        
        # Create posts.
        p1 = Posts.objects.create(id=1, body = "Hello", owner = a1)
        p2 = Posts.objects.create(id=2, body = "", owner = a2)
        
        # Create likes.
        l1 = Likes.objects.create(id=1, owner=a2, post=p1)
        l2 = Likes.objects.create(id=2, owner=a1, post=p1)
        
        # Create follow.
        f1 = Follow.objects.create(id=1, follower=a1, following=a2)
        f2 = Follow.objects.create(id=2, follower=a1, following=a1)
        
    def test_valid_post(self):
        a1 = User.objects.get(id=1)
        p = Posts.objects.get(body = "Hello", owner = a1)
        self.assertTrue(p.is_valid_post())
        
    def test_invalid_post(self):
        a2 = User.objects.get(id=2)
        p = Posts.objects.get(body = "", owner = a2)
        self.assertFalse(p.is_valid_post())
        
    def test_valid_like(self):
        l = Likes.objects.get(id=1)
        self.assertTrue(l.is_valid_like())
        
    def test_invalid_like(self):
        l = Likes.objects.get(id=2)
        self.assertFalse(l.is_valid_like())
        
    def test_valid_follow(self):
        f = Follow.objects.get(id=1)
        self.assertTrue(f.is_valid_follow())
        
    def test_invalid_follow(self):
        f = Follow.objects.get(id=2)
        self.assertFalse(f.is_valid_follow())
        
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 2)
        
    # user's profile exists in the database
    def test_valid_user(self):
        a1 = User.objects.get(id=1)
        c = Client()
        response = c.get(f"/profile/{a1.id}")
        self.assertEqual(response.status_code, 200)
        
    # user's profile doesn't exist in database
    def test_invalid_user(self):
        max_id = User.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"/profile/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
        
    # test pagination of posts
    def test_valid_pagination(self):
        a1 = User.objects.get(id=1)
        for i in range(3, 12):
            Posts.objects.create(id=i, body = f"Hello{i}", owner = a1)
        c = Client()
        
        # check 1-st page
        response = c.get(f"/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[ "has_next"],True)
        self.assertEqual(response.context["posts"].count(), 10)
        
        # check 2-st page
        response = c.get(f"/?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[ "has_previous"],True)
        self.assertEqual(response.context[ "has_next"],False)
        self.assertEqual(response.context["posts"].count(), 1)
   
    # test new post form  
    def test_unauthenticated_user_not_allowed_to_create_post(self):
        c = Client()
        response = c.get(f"/new_post")
        self.assertEqual(response.status_code, 302)
        
    # test following
    def test_unauthenticated_user_not_allowed_to_see_following(self):
        c = Client()
        response = c.get(f"/following")
        self.assertEqual(response.status_code, 302)