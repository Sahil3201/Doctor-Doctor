from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class account(AbstractUser):
    id          = models.CharField(primary_key=True)
    username    = models.CharField(max_length=255)
    name        = models.CharField(max_length=255, null=True, blank=True)
    surname     = models.CharField(max_length=255, null=True, blank=True)

    password    = models.CharField(max_length=255)
    email       = models.CharField(max_length=255, blank=True)
    phone_number= models.CharField(blank=True, null=True, unique=True)
    date_joined = models.DateField(auto_now=True, editable=False)

    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password',]