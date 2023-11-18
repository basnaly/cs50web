from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    identical_number = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.identical_number} {self.phone_number}"
    
