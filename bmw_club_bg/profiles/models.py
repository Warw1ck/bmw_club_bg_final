from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models
from PIL import Image

# Create your models here.

User = get_user_model()


def validate_image_size(image):
    # 2 MB = 2 * 1024 * 1024 bytes
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('The image size should not exceed 2 MB.')

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Do not show'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                  validate_image_size,
                              ]
                            )
    first_name = models.CharField(max_length=12, validators=[MinLengthValidator(2)], null=True, blank=True)
    last_name = models.CharField(max_length=12, validators=[MinLengthValidator(2)], null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, null=True, blank=True)

