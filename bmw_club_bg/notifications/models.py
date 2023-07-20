from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received', null=True)
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_liked', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)