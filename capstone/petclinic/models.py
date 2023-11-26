from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    identical_number = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.identical_number}, {self.first_name}, {self.last_name}, {self.phone_number}, {self.email}"
    

class Pet(models.Model):
    icon = models.CharField(max_length=8, blank=True)
    nickname = models.CharField(max_length=64)
    birth_date = models.DateField()
    pet_type = models.CharField(max_length=64)
    details = models.CharField(max_length=2056, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    
    def __str__(self): 
        return f"{self.icon} {self.nickname} {self.birth_date} {self.pet_type} {self.details} {self.created} {self.owner}" 

class Insurance(models.Model):
    start_date = models.DateField()
    monthly_price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="insurances")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="insurance")
    
    def __str__(self):
        return f"{self.start_date} {self.monthly_price} {self.owner} {self.pet}"
    
class Visit(models. Model):
    date_visit = models.DateField()
    time_visit = models.CharField(max_length=64)
    type_visit = models.CharField(max_length=128)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="visits")
    
    def __str__(self):
        return f"{self.date_visit} {self.time_visit} {self.type_visit} {self.pet}"
    

    