from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    content = models.TextField()
    image_url = models.URLField()
    location = models.CharField(max_length=20, validators=[MinLengthValidator(2)])
    comments = models.ManyToManyField(User, through='Comment', related_name='commented_posts')
    likes = models.ManyToManyField(User, related_name='liked_posts')
    date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
