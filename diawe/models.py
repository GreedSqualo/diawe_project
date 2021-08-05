from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Teams(models.Model):
    idT = models.IntegerField(unique=True,default=0)
    nameTeam = models.CharField(max_length=100)
    users = models.ManyToManyField(UserProfile)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.idT)
        super(Teams,self).save(*args, **kwargs)

    def __str__(self):
        return self.nameTeam

class LogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('diawe:detail', args=[self.id])


class Comment(models.Model):
    log = models.ForeignKey(LogPost,on_delete=models.CASCADE,related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment2')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
