from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Posts(models.Model):
    body = models.CharField(max_length=1028)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    
    def __str__(self):
        return f"{self.body} {self.created} {self.owner}"
    
    def is_valid_post(self):
        return self.body != ""
    

class Likes(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")
    
    def __str__(self):
        return f"{self.owner} {self.post}"
    
    def is_valid_like(self):
        return self.owner != self.post.owner
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")   
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    def is_valid_follow(self):
        return self.follower != self.following