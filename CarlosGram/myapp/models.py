from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='myapp_users')
    user_permissions = models.ManyToManyField(Permission, related_name='myapp_users')
    phone = models.CharField(max_length=20, null = True, blank=True)
    address = models.CharField(max_length=50 , null=True, blank=True)
# Create your models here.
