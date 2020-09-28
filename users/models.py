from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    socialToken = models.CharField(max_length=255, blank=True)
    isFirstUser = models.BooleanField(default=True)
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
