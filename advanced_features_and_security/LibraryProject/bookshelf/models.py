from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(blank=False, null=False)
    profile_photo = models.ImageField(
        upload_to='profile_photos/', blank=False, null=False)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, profile_photo,  password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, date_of_birth=date_of_birth, profile_photo=profile_photo)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, profile_photo, password=None):
        user = self.create_user(email, date_of_birth, profile_photo, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
