# Generated by Django 5.1.4 on 2025-01-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrinkingPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmokingPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
