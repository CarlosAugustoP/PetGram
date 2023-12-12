from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class User(AbstractUser):
    phone = models.CharField(max_length=20, null = True, blank=True)
    address = models.CharField(max_length=50 , null=True, blank=True)
# Create your models here.

class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comment = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.user) + ' ' + str(self.date)