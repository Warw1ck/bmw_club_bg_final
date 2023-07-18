from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Do not show'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    first_name = models.CharField(max_length=12, validators=[MinLengthValidator(2)], null=True, blank=True)
    last_name = models.CharField(max_length=12, validators=[MinLengthValidator(2)], null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, null=True, blank=True)

