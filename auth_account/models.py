# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django_countries.fields import CountryField
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male')
    city = models.CharField(max_length=30, default='New York')
    country = CountryField(default='US')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom name for reverse accessor
        blank=True,
        help_text='The groups this user belongs to. A user may belong to multiple groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom name for reverse accessor
        blank=True,
        help_text='Specific permissions for this user.'
    )

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
