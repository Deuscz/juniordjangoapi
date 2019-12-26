from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Account(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    join_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
