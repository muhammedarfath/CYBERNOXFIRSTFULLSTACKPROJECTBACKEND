# Generated by Django 5.1.4 on 2025-01-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_bodytype_alter_profile_body_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unique_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
