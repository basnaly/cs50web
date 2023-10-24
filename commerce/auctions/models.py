from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1028)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.ImageField()
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.price} {self.image} {self.created}" 
