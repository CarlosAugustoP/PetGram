from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
import uuid


# Create your models here.

class User(AbstractUser):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('turtle', 'Turtle'),
        ('horse', 'Horse'),
        ('snake', 'Snake'),
        ('lizard', 'Lizard'),
        ('pig', 'Pig'),
        ('monkey', 'Monkey'),
        ('other', 'Other'),
    ]

    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    amount_of_followers = models.IntegerField(default=0)
    amount_of_following = models.IntegerField(default=0)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='following_user')
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', default='images/defaultuser.png')
    bio = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, upload_to='images/')
    description = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    who_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.description
    
    def increment_likes(self):
        self.likes += 1
        self.save()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_posts_reverse')

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
class FollowersCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username