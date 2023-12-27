from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser): # look into AbstractBaseUser
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return self.username
