from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from bmw_club_bg.common.models import Post

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=12, validators=[MinLengthValidator(2)])
    description = models.TextField()
    image = models.ImageField(upload_to='group_images')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(Post, related_name='groups')
    users = models.ManyToManyField(User, related_name='user')

    def __str__(self):
        # Customize the name of the group as needed
        return self.name

