from django.db import models


class User(models.Model):
    name = models.CharField (max_length=200)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200,unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name