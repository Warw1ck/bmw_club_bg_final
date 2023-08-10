from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models

# Create your models here.
from bmw_club_bg.common.models import Post

User = get_user_model()


def validate_image_size(image):
    # 2 MB = 2 * 1024 * 1024 bytes
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('The image size should not exceed 2 MB.')


class Group(models.Model):
    name = models.CharField(max_length=12, validators=[MinLengthValidator(2)])
    description = models.TextField()
    image = models.ImageField(upload_to='group_images',
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                  validate_image_size,
                              ]
                              )
    date_of_creation = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(Post, related_name='groups')
    users = models.ManyToManyField(User, related_name='user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups', null=True)

    def __str__(self):
        return self.name

