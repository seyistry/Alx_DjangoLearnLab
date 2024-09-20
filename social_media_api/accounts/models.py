from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework.authtoken.models import Token

# Create your models here.


class CustomUser(AbstractUser):
    # Add additional fields
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # ManyToMany field to represent followers (symmetrical=False for directed relationship)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username