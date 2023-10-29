from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1028)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.URLField(blank=True)
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    
    def __str__(self): 
        return f"{self.title} {self.description} {self.category} {self.price} {self.image} {self.created} {self.is_active}" 


class Watchitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watching_users")
    
    def __str__(self): 
        return f"{self.user} {self.listing}"
    
    
class Bid(models.Model):
    bid = models.IntegerField()
    placed = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.bid} {self.placed} {self.user} {self.listing}"
    
    
class Comments(models.Model):
    comment = models.CharField(max_length=1028)
    created = models.DateField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.comment} {self.created} {self.user} {self.listing}"