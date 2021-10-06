import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

USER_TYPES = [
    ('patient', 'Patient'),
    ('pharmacist', 'Pharmacist'),
    ('doctor', 'Doctor'),
    ('admin', 'Admin'),
]

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='patient')
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
