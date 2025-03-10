# Generated by Django 5.1.4 on 2025-01-26 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_user_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Profile Picture'),
        ),
    ]
