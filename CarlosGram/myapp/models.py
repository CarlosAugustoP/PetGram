from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError


class User(AbstractUser):
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    phone = models.CharField(max_length=20, null = True, blank=True)
    address = models.CharField(max_length=50 , null=True, blank=True)
    amount_of_followers = models.IntegerField(default=0)
    amount_of_following = models.IntegerField(default=0)
    followers = models.ManyToManyField('self', blank=True)
# Create your models here.

class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, upload_to='images/')
    description = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comment = models.CharField(max_length=100, null=True, blank=True)
    who_liked = models.ManyToManyField(User, related_name='who_liked', blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', default='images/defaultuser.png')

    def __str__(self):
        return self.user.username
    
