# Generated by Django 4.1.3 on 2023-07-20 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user_like',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to=settings.AUTH_USER_MODEL),
        ),
    ]
