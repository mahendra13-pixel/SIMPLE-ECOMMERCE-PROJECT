from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

'''pip install phonenumbers django-phonenumber-field'''
# Create your models here.
class CustomUser(AbstractUser):
    phone=PhoneNumberField(region='NP',blank=True)
    street_address=models.CharField(max_length=200)

class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    profile_picture=models.ImageField(upload_to='images')
    bio=models.TextField()
    dob=models.DateTimeField(null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


    
