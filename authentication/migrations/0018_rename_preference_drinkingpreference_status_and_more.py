# Generated by Django 5.1.4 on 2025-01-29 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_drinkingpreference_ethnicgroup_physicalstatus_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drinkingpreference',
            old_name='preference',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='ethnicgroup',
            old_name='group_name',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='smokingpreference',
            old_name='preference',
            new_name='status',
        ),
    ]
