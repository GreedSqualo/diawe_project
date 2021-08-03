from django.db import models
from django.contrib.auth.models import User

class aUser(models.Model):
    name = models.CharField (max_length=200)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200,unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    reemail = models.EmailField(max_length=200,unique=True)
    def __str__(self):
        return self.user.username