# Generated by Django 4.1.3 on 2023-08-09 05:53

import bmw_club_bg.profiles.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), bmw_club_bg.profiles.models.validate_image_size]),
        ),
    ]
