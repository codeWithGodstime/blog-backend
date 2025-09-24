from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import CustomUserManager

class CustomUser(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

